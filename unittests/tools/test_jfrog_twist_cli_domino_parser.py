import csv
import io
from types import SimpleNamespace
from unittest.mock import patch

from botocore.exceptions import ClientError

from ..dojo_test_case import DojoTestCase
from dojo.tools.jfrog_twist_cli_domino.parser import CombinedCSVParser


class TestJfrogTwistCliDominoParser(DojoTestCase):
    def make_scan(self):
        rows = [
            ('CVE-1', 'Medium', 'quay.io/domino/seldon-core-operator:v1'),
            ('CVE-2', 'Medium', 'quay.io/domino/seldon-core-operator:v1'),
            ('CVE-3', 'High', 'quay.io/domino/seldon-core-operator:v1'),
            ('CVE-4', 'Medium', 'quay.io/domino/allowed:v1'),
            ('CVE-5', 'Medium', 'quay.io/domino/allowed:v1'),
            ('CVE-6', 'Medium', 'quay.io/domino/low-count:v1'),
            ('CVE-7', 'Medium', 'registry.internal/QUAY.IO/Domino/Train-Mlflow-Docker:V2'),
        ]
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['cve', 'severity', 'status', 'container_name', 'tag',
                         'unique_image_identifier',
                         'pkg_name', 'pkg_version', 'description'])
        for cve, severity, container in rows:
            container_name, tag = container.rsplit(':', 1)
            writer.writerow([cve, severity, 'fixed', container_name, tag,
                             'unrelated-identifier', 'pkg', '1', 'description'])
        output.seek(0)
        return output

    def make_settings(self):
        return SimpleNamespace(
            enable_jfrog_twist_medium_ingestion=True,
            jfrog_twist_medium_unique_cve_threshold=1,
            jfrog_twist_medium_s3_bucket='bucket',
            jfrog_twist_medium_s3_key='excluded.txt',
        )

    def make_medium_scan(self, count):
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['cve', 'severity', 'status', 'container_name', 'tag',
                         'pkg_name', 'pkg_version', 'description'])
        for number in range(count):
            writer.writerow(['CVE-{}'.format(number), 'Medium', 'fixed',
                             'quay.io/domino/allowed', 'v1', 'pkg', '1', 'description'])
        output.seek(0)
        return output

    @patch('dojo.tools.jfrog_twist_cli_domino.parser.System_Settings')
    @patch('dojo.tools.jfrog_twist_cli_domino.parser.boto3.client')
    def test_excludes_matching_containers_after_file_wide_threshold(self, s3_client, settings_model):
        settings_model.objects.get.return_value = self.make_settings()
        s3_client.return_value.get_object.return_value = {
            'Body': io.BytesIO(b'QUAY.IO/DOMINO/SELDON-CORE-OPERATOR\n'
                               b'quay.io/domino/train-mlflow-docker:v2\n'),
        }

        findings = CombinedCSVParser().parse(self.make_scan(), None)

        self.assertEqual({'CVE-3', 'CVE-4', 'CVE-5', 'CVE-6'},
                         {finding.cve for finding in findings})
        s3_client.assert_called_once_with('s3')
        s3_client.return_value.get_object.assert_called_once_with(
            Bucket='bucket', Key='excluded.txt')

    @patch('dojo.tools.jfrog_twist_cli_domino.parser.System_Settings')
    @patch('dojo.tools.jfrog_twist_cli_domino.parser.boto3.client')
    def test_s3_failure_keeps_high_and_skips_all_mediums(self, s3_client, settings_model):
        settings_model.objects.get.return_value = self.make_settings()
        s3_client.side_effect = RuntimeError('S3 unavailable')

        findings = CombinedCSVParser().parse(self.make_scan(), None)

        self.assertEqual({'CVE-3'}, {finding.cve for finding in findings})

    @patch('dojo.tools.jfrog_twist_cli_domino.parser.System_Settings')
    @patch('dojo.tools.jfrog_twist_cli_domino.parser.boto3.client')
    def test_missing_s3_object_keeps_existing_medium_ingestion(self, s3_client, settings_model):
        settings_model.objects.get.return_value = self.make_settings()
        s3_client.return_value.get_object.side_effect = ClientError(
            {'Error': {'Code': 'NoSuchKey', 'Message': 'Object not found'}}, 'GetObject')

        findings = CombinedCSVParser().parse(self.make_scan(), None)

        self.assertEqual({'CVE-1', 'CVE-2', 'CVE-3', 'CVE-4', 'CVE-5', 'CVE-6', 'CVE-7'},
                         {finding.cve for finding in findings})

    @patch('dojo.tools.jfrog_twist_cli_domino.parser.System_Settings')
    @patch('dojo.tools.jfrog_twist_cli_domino.parser.boto3.client')
    def test_unconfigured_s3_location_keeps_existing_medium_ingestion(self, s3_client, settings_model):
        settings = self.make_settings()
        settings.jfrog_twist_medium_s3_bucket = ''
        settings.jfrog_twist_medium_s3_key = ''
        settings_model.objects.get.return_value = settings

        findings = CombinedCSVParser().parse(self.make_scan(), None)

        self.assertEqual(7, len(findings))
        s3_client.assert_not_called()

    @patch('dojo.tools.jfrog_twist_cli_domino.parser.System_Settings')
    @patch('dojo.tools.jfrog_twist_cli_domino.parser.boto3.client')
    def test_missing_s3_keeps_strict_fifteen_cve_threshold(self, s3_client, settings_model):
        settings = self.make_settings()
        settings.jfrog_twist_medium_unique_cve_threshold = 15
        settings.jfrog_twist_medium_s3_key = ''
        settings_model.objects.get.return_value = settings

        parser = CombinedCSVParser()
        self.assertEqual(0, len(parser.parse(self.make_medium_scan(15), None)))
        self.assertEqual(16, len(parser.parse(self.make_medium_scan(16), None)))
        s3_client.assert_not_called()
