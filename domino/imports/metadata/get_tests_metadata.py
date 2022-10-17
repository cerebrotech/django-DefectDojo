class GetTestsMetadata(object):
    def __init__(self,tests_json):
        self.tests_json=tests_json

    @property
    def count(self):
        return self.tests_json['count']

    @property
    def next(self):
        return self.tests_json['next']

    @property
    def results(self):
        return self.tests_json['results']

    @property
    def latest_results_dict(self):
        if self.count >0:
            if self.count==1:
                return self.results[0]
            else:
                id=0
                final_result_dict={}
                for result_dict in self.results:
                    if id < result_dict['id']:
                        id=result_dict['id']
                        final_result_dict=result_dict
                return final_result_dict
        else:
            return {}

    @property
    def id(self):
        return self.latest_results_dict.get("id",False)

    @property
    def tags(self):
        return self.latest_results_dict.get("tags")

    @property
    def test_type_name(self):
        return self.latest_results_dict.get("test_type_name")

    @property
    def finding_groups(self):
        return self.latest_results_dict.get("finding_groups")

    @property
    def scan_type(self):
        return self.latest_results_dict.get("scan_type")

    @property
    def title(self):
        return self.latest_results_dict.get("title")

    @property
    def description(self):
        return self.latest_results_dict.get("description")

    @property
    def target_start(self):
        return self.latest_results_dict.get("target_start")

    @property
    def target_end(self):
        return self.latest_results_dict.get("target_end")

    @property
    def estimated_time(self):
        return self.latest_results_dict.get("estimated_time")

    @property
    def actual_time(self):
        return self.latest_results_dict.get("actual_time")

    @property
    def percent_complete(self):
        return self.latest_results_dict.get("percent_complete")

    @property
    def updated(self):
        return self.latest_results_dict.get("updated")

    @property
    def created(self):
        return self.latest_results_dict.get("created")

    @property
    def version(self):
        return self.latest_results_dict.get("version")

    @property
    def build_id(self):
        return self.latest_results_dict.get("build_id")

    @property
    def commit_hash(self):
        return self.latest_results_dict.get("commit_hash")

    @property
    def branch_tag(self):
        return self.latest_results_dict.get("branch_tag")

    @property
    def engagement(self):
        return self.latest_results_dict.get("engagement")

    @property
    def lead(self):
        return self.latest_results_dict.get("lead")

    @property
    def test_type(self):
        return self.latest_results_dict.get("test_type")

    @property
    def environment(self):
        return self.latest_results_dict.get("environment")

    @property
    def api_scan_configuration(self):
        return self.latest_results_dict.get("api_scan_configuration")

    @property
    def notes(self):
        return self.latest_results_dict.get("notes")

    @property
    def files(self):
        return self.latest_results_dict.get("files")