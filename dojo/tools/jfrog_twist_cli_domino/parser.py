import csv
import hashlib
import io
import json
import logging
import textwrap

from dojo.models import Finding

logger = logging.getLogger(__name__)


class CombinedCSVParser(object):

    def parse_issue(self, row, test):
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

        if cve and pkg_name:
            title = cve + ": " + pkg_name + " - " + pkg_version
        elif pkg_name and pkg_version:
            title = pkg_name + " - " + pkg_version
        else:
            title = description

        if cvssv3_score:
            finding = Finding(
                cve=cve,
                title=textwrap.shorten(title, width=255, placeholder="..."),
                test=test,
                severity=severity,
                cvssv3_score =cvssv3_score,
                description=description,
                mitigation=fixed_in_pkg,
                component_name=textwrap.shorten(pkg_name, width=200, placeholder="..."),
                component_version=pkg_version,
                file_path=cve,
                service=pkg_path,
                unique_id_from_tool=tool,
                vuln_id_from_tool=type,
                false_p=False,
                duplicate=False,
                out_of_scope=False,
                mitigated=None,
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
                false_p=False,
                duplicate=False,
                out_of_scope=False,
                mitigated=None,
                # severity_justification="(CVSS v3 base score: {})".format(data_cvss),
                impact=status)
        finding.description = finding.description.strip()
        if cve:
            finding.unsaved_vulnerability_ids = [cve]
        return finding

    def parse(self, filename, test):
        if filename is None:
            return
        content = filename.read()
        dupes = dict()
        if type(content) is bytes:
            content = content.decode('utf-8')
        reader = csv.DictReader(io.StringIO(content), delimiter=',', quotechar='"')
        for row in reader:
            finding = self.parse_issue(row, test)
            if finding is not None:
                key = hashlib.md5((finding.severity + '|' + finding.title + '|' + finding.description).encode('utf-8')).hexdigest()
                # if key not in dupes:
                if True:
                    dupes[key] = finding
        return list(dupes.values())



def get_item(vulnerability,pkg_typeNameVersion_to_path_dict, test):
    pkg_pk_to_find_pkg_path=vulnerability['packageName']+"#"+vulnerability['packageVersion']
    pkg_path=pkg_typeNameVersion_to_path_dict.get(pkg_pk_to_find_pkg_path,' ')
    severity = convert_severity(vulnerability['severity']) if 'severity' in vulnerability else "Info"
    vector = vulnerability['vector'] if 'vector' in vulnerability else "CVSS vector not provided. "
    status = vulnerability['status'] if 'status' in vulnerability else "There seems to be no fix yet. Please check description field."
    cvss = vulnerability['cvss'] if 'cvss' in vulnerability else "No CVSS score yet."
    riskFactors = vulnerability['riskFactors'] if 'riskFactors' in vulnerability else "No risk factors."

    # create the finding object
    finding = Finding(
        title=vulnerability['id'] + ": " + vulnerability['packageName'] + " - " + vulnerability['packageVersion'],
        test=test,
        severity=severity,
        description=vulnerability['description'] + "<p> Vulnerable Package: " +
        vulnerability['packageName'] + "</p><p> Current Version: " + str(
            vulnerability['packageVersion']) + "</p>",
        mitigation=status.title(),
        references=vulnerability['link'],
        component_name=vulnerability['packageName'],
        component_version=vulnerability['packageVersion'],
        false_p=False,
        duplicate=False,
        out_of_scope=False,
        mitigated=None,
        severity_justification="{} (CVSS v3 base score: {})\n\n{}".format(vector, cvss, riskFactors),
        impact=severity,
        file_path=pkg_path)
    finding.unsaved_vulnerability_ids = [vulnerability['id']]
    finding.description = finding.description.strip()

    return finding


def convert_severity(severity):
    if severity.lower() == 'important':
        return "Info"
    elif severity.lower() == 'moderate':
        return "Medium"
    elif severity.lower() == 'information':
        return "Info"
    elif severity.lower() == 'informational':
        return "Info"
    elif severity == '':
        return "Info"
    elif severity == 'medium':
        return "Medium"
    elif severity == 'low':
        return "Low"
    elif severity == 'high':
        return "High"
    elif severity == 'critical':
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

