import requests
# from bin.container_report_parsing.nist_cve_metadata import  CveMetadata

class VulnMetadata(object):
    def __init__(self, vuln_dict):
        self.vuln_dict = vuln_dict
        # CveMetadata.__init__(self,self.vuln_dict['id'],self.link)


    @property
    def cve(self):
        return self.vuln_dict['id']

    @property
    def status(self):
        if 'status' in self.vuln_dict.keys():
            if "fixed" in self.vuln_dict['status']:
                return "fixed"
            else:
                return self.vuln_dict['status']
        else:
            return "No status provided"

    @property
    def cvss(self):
        return self.vuln_dict.get('cvss',"None")

    @property
    def vector(self):
        return self.vuln_dict['vector']

    @property
    def description(self):
        if "description" in self.vuln_dict.keys():
            return self.vuln_dict['description']
        else:
            return "no description"

    @property
    def severity(self):
        return self.vuln_dict['severity']

    @property
    def severity_from_cvss(self):
        if self.cvss and self.cvss !="None":
            sev_temp=int(self.cvss)
            if sev_temp >=9:
                return "critical"
            elif sev_temp >=7 and sev_temp <9:
                return "high"
            elif sev_temp >=4 and sev_temp <7 :
                return "medium"
            else:
                return "low"
        else:
            return self.severity


    @property
    def packageName(self):
        return self.vuln_dict['packageName']

    @property
    def packageVersion(self):
        return self.vuln_dict['packageVersion']

    @property
    def link(self):
        if "link" in self.vuln_dict.keys():
            return self.vuln_dict['link']
        else:
            return "no link provided"

    @property
    def riskFactors(self):
        return self.vuln_dict['riskFactors']

    @property
    def impactedVersions(self):
        return self.vuln_dict['impactedVersions'].decode('ascii')

    @property
    def publishedDate(self):
        return self.vuln_dict['publishedDate']

    @property
    def discoveredDate(self):
        return self.vuln_dict['discoveredDate']

    @property
    def fixDate(self):
        if self.is_fixed:
            if "fixDate" in self.vuln_dict.keys():
                return self.vuln_dict['fixDate']
            else:
                return "no fix date provided"
        else:
            return "no fix date provided"

    @property
    def is_fixed(self):
        if self.status.lower() == "open":
            return False
        elif self.status.lower().strip() =="fixed":
            return True
        else:
            return False

    @property
    def fixed_in_pkg(self):
        if self.is_fixed:
            return self.vuln_dict['status'].replace("fixed in", '').strip()
        else:
            return "fix not available yet"

    @property
    def conatainer_vuln_header_row(self):
        return ['container_name', 'tag', 'scan_date',
                'distro', 'cve', 'cvss' "type",
                'severity', 'status', 'pkg_name',
                'pkg_version', 'fixed_in_pkg', 'discovered_date',
                'fix_date', 'first_found_date', 'description',
                'link', 'exception', 'rational'
                ]

    # @property
    # def nist_date_published(self):
    #     return
    #
    # @property
    # def nist_date_modified(self):
    #     return

            # @property
    # def summary_header_row(self):
    #     return ['container_name', 'tag', 'scan_date', 'distro',
    #             'all_vulns', 'all_high', 'all_medium', 'all_low',
    #             'os_vulns', 'os_high', 'os_medium', 'os_low',
    #             'fixable_os_vulns', 'fixable_os_high', 'fixable_os_medium', 'fixable_os_low',
    #             'age_of_oldest_high_os_fixable', 'age_of_oldest_medium_os_fixable', 'age_of_oldest_low_os_fixable'
    #                                                                                 'non_os_vulns', 'non_os_high',
    #             'non_os_medium', 'non_os_low',
    #             'fixable_vulns', 'fixable_high', 'fixable_medium', 'fixable_low',
    #             'no_fix_vulns', 'no_fix_high', 'no_fix_medium', 'no_fix_low',
    #             'no_fix_os_vulns', 'no_fix_os_high', 'no_fix_os_medium', 'no_fix_os_low',
    #             'no_fix_non_os_vulns', 'no_fix_non_os_high', 'no_fix_non_os_medium', 'no_fix_non_os_low',
    #             ]


