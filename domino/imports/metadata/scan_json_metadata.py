import json

class ScanReport():
    def __init__(self,report_path):
        self.report_path=report_path
        self.vulnerabilities=self._vulnerabilities

    @property
    def report_json_to_dict(self):
        with open(self.report_path) as fp:
            return json.load(fp)

    @property
    def results(self):
        return self.report_json_to_dict['results'][0]

    @property
    def container_name_with_tag(self):
        return self.results['name']

    @property
    def container_name(self):
        return self.container_name_with_tag.split(":")[0]

    @property
    def container_tag(self):
        return self.container_name_with_tag.split(":")[1]

    @property
    def distro(self):
        return self.results['distro']

    @property
    def distro_release(self):
        return self.results['distroRelease']

    @property
    def digest(self):
        return self.results['digest']

    @property
    def packages(self):
        if 'packages' in self.results.keys():
            return self.results['packages']
        else:
            return []

    @property
    def applications(self):
        return self.results['applications']

    @property
    def compliances(self):
        return self.results['compliances']

    @property
    def compliance_distribution(self):
        return self.results['complianceDistribution']

    @property
    def compliance_scan_passed(self):
        return self.results['complianceScanPassed']

    @property
    def _vulnerabilities(self):
        try:
            return self.results['vulnerabilities']
        except:
            #no vulns
            return []

    @property
    def vulnerability_distribution(self):
        return self.results['vulnerabilityDistribution']

    @property
    def vulnerability_scan_passed(self):
        return self.results['vulnerabilityScanPassed']

    @property
    def applications(self):
        if "applications" in self.results.keys():
            return self.results['applications']
        else:
            return []

    @property
    def pkg_to_type_dict(self):
        _pkg_to_type_dict={}
        for pkg_dict in self.packages:
            pkg_name=pkg_dict['name']
            pkg_type=pkg_dict['type']
            _pkg_to_type_dict[pkg_name]=pkg_type
        for application in self.applications:
            pkg_name = application['name']
            if pkg_name =='busybox':
                pkg_type = 'os'
            else:
                pkg_type = 'application'
            _pkg_to_type_dict[pkg_name] = pkg_type
        return _pkg_to_type_dict