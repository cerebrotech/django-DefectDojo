import json
from pprint import pprint
from domino.imports.metadata.scan_json_metadata import  ScanReport
from domino.base_helpers import base_helper
from domino.imports.metadata.vuln_metadata import VulnMetadata


def parse_twistlock_json_for_fixale_severity(scan_json_file_path,acceptable_severity=['critical','high']):
    scan_report_obj = ScanReport(scan_json_file_path)
    vulns_of_interest_list = []
    for vuln_dict in scan_report_obj.vulnerabilities:
        vuln_obj = VulnMetadata(vuln_dict)
        try:
            if vuln_obj.severity in acceptable_severity and vuln_obj.is_fixed:
                vulns_of_interest_list.append(vuln_dict)
        except Exception as e:
            print("Couldn't find severity for: ", vuln_obj.vuln_dict)

    report_json = scan_report_obj.report_json_to_dict
    report_json['results'][0]['vulnerabilities'] = vulns_of_interest_list
    parsed_json_path_to_save=scan_json_file_path.split(".json")[0] +"_parsed.json"
    base_helper.save_json(report_json,parsed_json_path_to_save)

    return parsed_json_path_to_save


if __name__ == '__main__':
    scan_json_file_path = '/Users/mannysingh/Documents/daily-work/defectdojo/NO-CVE-2022-32532-vuln812.json'
    acceptable_severity=['critical','high']
    parse_twistlock_json_for_fixale_severity(scan_json_file_path, acceptable_severity=['critical', 'high'])


