import csv
import hashlib
import io
import json
import logging
import textwrap

from dojo.models import Finding, System_Settings

logger = logging.getLogger(__name__)


class CombinedCSVParser(object):

    def parse_issue(self, row, test, include_mediums=False):
        if not row:
            return None

        cve = row.get('cve', '')
        pkg_version = row.get('pkg_version', '')
        status = row.get('status', '')
        pkg_name = row.get('pkg_name', '')
        severity = convert_severity(row.get('severity', ''))
        cvssv3_score = row.get('cvss', '')
        type = row.get('type', '')
        fixed_in_pkg = row.get('fixed_in_pkg', '')
        unique_image_identifier = row.get('unique_image_identifier', '')
        description = row.get('description', '')
        pkg_path = row.get('pkg_path', '')
        tool = row.get('tool', '')
        domino_affected_release = row.get('release')
        domino_branch = row.get('Domino_branch')

        if cve and pkg_name:
            title = cve + ": " + pkg_name + " - " + pkg_version
        elif pkg_name and pkg_version:
            title = pkg_name + " - " + pkg_version
        else:
            title = description

        if cvssv3_score and cvssv3_score.strip().lower() != 'none':
            cvssv3_score_bool = True
        else:
            cvssv3_score_bool = False

        # if cve and 'prisma-' in cve.lower():
        #     out_of_scope_bool = True
        #     active_bool = False

        # out_of_scope_bool = False
        active_bool = True
        if severity and cve and 'prisma-' not in cve.lower():
            status_lower = status.strip().lower()
            severity_lower = severity.strip().lower()
            is_high_or_critical_fixed = status_lower == 'fixed' and severity_lower in ['high', 'critical']
            is_medium_fixed_and_allowed = status_lower == 'fixed' and severity_lower == 'medium' and include_mediums
            if is_high_or_critical_fixed or is_medium_fixed_and_allowed:
                # out_of_scope_bool = False
                # active_bool=True

                if cvssv3_score_bool:
                    finding = Finding(
                        cve=cve,
                        title=textwrap.shorten(title, width=255, placeholder="..."),
                        test=test,
                        severity=severity,
                        cvssv3_score=cvssv3_score,
                        description=description,
                        mitigation=fixed_in_pkg,
                        component_name=textwrap.shorten(pkg_name, width=200, placeholder="..."),
                        component_version=pkg_version,
                        file_path=cve,
                        service=pkg_path,
                        unique_id_from_tool=tool,
                        vuln_id_from_tool=type,
                        steps_to_reproduce=domino_affected_release,
                        # false_p=False,
                        # duplicate=False,
                        # out_of_scope=out_of_scope_bool,
                        # active=active_bool,
                        # mitigated=None,
                        # severity_justification="(CVSS v3 base score: {})".format(data_cvss),
                        impact=status)
                else:
                    finding = Finding(
                        cve=cve,
                        title=textwrap.shorten(title, width=255, placeholder="..."),
                        test=test,
                        severity=severity,
                        description=description,
                        mitigation=fixed_in_pkg,
                        component_name=textwrap.shorten(pkg_name, width=200, placeholder="..."),
                        component_version=pkg_version,
                        file_path=cve,
                        service=pkg_path,
                        unique_id_from_tool=tool,
                        vuln_id_from_tool=type,
                        steps_to_reproduce=domino_affected_release,
                        # false_p=False,
                        # duplicate=False,
                        # out_of_scope=out_of_scope_bool,
                        # active=active_bool,
                        # mitigated=None,
                        # severity_justification="(CVSS v3 base score: {})".format(data_cvss),
                        impact=status)
                finding.description = finding.description.strip()
                if cve:
                    finding.unsaved_vulnerability_ids = [cve]
                return finding

        return None







    def parse(self, filename, test):
        if filename is None:
            return
        content = filename.read()
        dupes = dict()
        if type(content) is bytes:
            content = content.decode('utf-8')
        # Materialize the rows so we can pass over them twice: once to decide
        # whether Medium findings should be included at all for this container,
        # and once to actually build the findings with that decision applied.
        rows = list(csv.DictReader(io.StringIO(content), delimiter=',', quotechar='"'))

        include_mediums = self.should_include_mediums(rows)

        for i, row in enumerate(rows):
            finding = self.parse_issue(row, test, include_mediums)
            if finding is not None:
                # key = hashlib.md5((finding.severity + '|' + finding.title + '|' + finding.description).encode('utf-8')).hexdigest()
                # if key not in dupes:
                if True:
                    dupes[i] = finding
        return list(dupes.values())

    def should_include_mediums(self, rows):
        system_settings = System_Settings.objects.get()
        if not system_settings.enable_jfrog_twist_medium_ingestion:
            return False

        medium_fixed_cves = set()
        for row in rows:
            cve = row.get('cve', '')
            status = row.get('status', '')
            severity = convert_severity(row.get('severity', ''))
            if cve and status.strip().lower() == 'fixed' and severity == 'Medium':
                medium_fixed_cves.add(cve)

        threshold = system_settings.jfrog_twist_medium_unique_cve_threshold or 0
        return len(medium_fixed_cves) > threshold



# def get_item(vulnerability,pkg_typeNameVersion_to_path_dict, test):
#     pkg_pk_to_find_pkg_path=vulnerability['packageName']+"#"+vulnerability['packageVersion']
#     pkg_path=pkg_typeNameVersion_to_path_dict.get(pkg_pk_to_find_pkg_path,' ')
#     severity = convert_severity(vulnerability['severity']) if 'severity' in vulnerability else "Info"
#     vector = vulnerability['vector'] if 'vector' in vulnerability else "CVSS vector not provided. "
#     status = vulnerability['status'] if 'status' in vulnerability else "There seems to be no fix yet. Please check description field."
#     cvss = vulnerability['cvss'] if 'cvss' in vulnerability else "No CVSS score yet."
#     riskFactors = vulnerability['riskFactors'] if 'riskFactors' in vulnerability else "No risk factors."
#
#     # create the finding object
#     finding = Finding(
#         title=vulnerability['id'] + ": " + vulnerability['packageName'] + " - " + vulnerability['packageVersion'],
#         test=test,
#         severity=severity,
#         description=vulnerability['description'] + "<p> Vulnerable Package: " +
#         vulnerability['packageName'] + "</p><p> Current Version: " + str(
#             vulnerability['packageVersion']) + "</p>",
#         mitigation=status.title(),
#         references=vulnerability['link'],
#         component_name=vulnerability['packageName'],
#         component_version=vulnerability['packageVersion'],
#         false_p=False,
#         duplicate=False,
#         out_of_scope=False,
#         mitigated=None,
#         severity_justification="{} (CVSS v3 base score: {})\n\n{}".format(vector, cvss, riskFactors),
#         impact=severity,
#         file_path=pkg_path)
#     finding.unsaved_vulnerability_ids = [vulnerability['id']]
#     finding.description = finding.description.strip()
#
#     return finding


def convert_severity(severity):
    # severity=severity.lower()
    if severity.lower() == 'important':
        return "Info"
    elif severity.lower() == 'moderate':
        return "Medium"
    elif severity.lower() == 'information':
        return "Info"
    elif severity.lower() == 'informational':
        return "Info"
    elif severity.lower() == '':
        return "Info"
    elif severity.lower() == 'medium':
        return "Medium"
    elif severity.lower() == 'low':
        return "Low"
    elif severity.lower() == 'high':
        return "High"
    elif severity.lower() == 'critical':
        return "Critical"
    else:
        return "Info"


# class TwistlockDominoParser(object):
# jfrog_twist_cli_domino
class JfrogTwistCliDominoParser(object):

    def get_scan_types(self):
        return ["Jfrog-Twist cli Domino Image Scan"]

    def get_label_for_scan_types(self, scan_type):
        return "Jfrog-Twist cli Domino Image Scan"

    def get_description_for_scan_types(self, scan_type):
        return "Scan output of Jfrog Twistlockv- CSV."

    def get_findings(self, filename, test):

        if filename is None:
            return list()

        if filename.name.lower().endswith('.csv'):
            return CombinedCSVParser().parse(filename, test)
        else:
            raise Exception('Unknown File Format')


# if __name__ == '__main__':
#     from cvss.cvss3 import CVSS3
#     import cvss.parser
#
#     vectors = cvss.parser.parse_cvss_from_text("CVSS:3.0/S:C/C:H/I:H/A:N/AV:P/AC:H/PR:H/UI:R/E:H/RL:O/RC:R/CR:H/IR:X/AR:X/MAC:H/MPR:X/MUI:X/MC:L/MA:X")
#     vectors = cvss.parser.parse_cvss_from_score()

