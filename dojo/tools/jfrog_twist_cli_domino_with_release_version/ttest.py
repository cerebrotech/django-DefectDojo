import csv
import hashlib
import io
import json
import logging
import textwrap

def convert_severity(severity):
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

        if cvssv3_score and cvssv3_score.strip().lower() != 'none':
            cvssv3_score_bool = True
        else:
            cvssv3_score_bool = False

        # if cve and 'prisma-' in cve.lower():
        #     out_of_scope_bool = True
        #     active_bool = False

        out_of_scope_bool = True
        active_bool = False
        if severity and cve and 'prisma-' not in cve.lower():
            if status.strip().lower()=='fixed' and severity.strip().lower() in ['high','critical']:
                print("ingest",cve,severity,status)
            else:
                print("nested else",cve,severity,status)
        else:
            print("main else",cve,severity)

    def parse(self, filename, test):
        if filename is None:
            return
        # content = filename.read()
        dupes = dict()
        # if type(content) is bytes:
        #     content = content.decode('utf-8')

        with open(filename) as fp:
            reader = csv.DictReader(fp, delimiter=',', quotechar='"')
            for i,row in enumerate(reader):
                finding = self.parse_issue(row, test)
                if finding is not None:
                    # key = hashlib.md5((finding.severity + '|' + finding.title + '|' + finding.description).encode('utf-8')).hexdigest()
                    # if key not in dupes:
                    if True:
                        dupes[i] = finding
        return list(dupes.values())

if __name__ == '__main__':
    filename='/Users/mannysingh/temp/jfrog-cli-scans-local/reports/csv/buildkit:v0.12.5-rootless__combined_with_twistlock.csv'
    # filename='/Users/mannysingh/Downloads/all_vulns env parser.csv'
    filename='/tmp/s3/all/buildkit:v0.12.5.csv'
    test=''
    CombinedCSVParser().parse(filename, test)