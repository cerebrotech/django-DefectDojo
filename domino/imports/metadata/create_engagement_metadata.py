from domino.base_helpers import base_helper

class CreateEngagementMetadata():
    def __init__(self,input_json):
        self.input_json=input_json

    @property
    def id(self):
        return self.input_json['id']

    @property
    def tags(self):
        return self.input_json['tags']

    @property
    def name(self):
        return self.input_json['name']

    @property
    def description(self):
        return self.input_json['description']

    @property
    def version(self):
        return self.input_json['version']

    @property
    def first_contacted(self):
        return self.input_json['first_contacted']

    @property
    def target_start(self):
        return self.input_json['target_start']

    @property
    def target_end(self):
        return self.input_json['target_end']

    @property
    def reason(self):
        return self.input_json['reason']

    @property
    def updated(self):
        return self.input_json['updated']

    @property
    def created(self):
        return self.input_json['created']

    @property
    def active(self):
        return self.input_json['active']

    @property
    def tracker(self):
        return self.input_json['tracker']

    @property
    def test_strategy(self):
        return self.input_json['test_strategy']

    @property
    def threat_model(self):
        return self.input_json['threat_model']

    @property
    def api_test(self):
        return self.input_json['api_test']

    @property
    def pen_test(self):
        return self.input_json['pen_test']

    @property
    def check_list(self):
        return self.input_json['check_list']

    @property
    def status(self):
        return self.input_json['status']

    @property
    def progress(self):
        return self.input_json['progress']

    @property
    def tmodel_path(self):
        return self.input_json['tmodel_path']

    @property
    def done_testing(self):
        return self.input_json['done_testing']

    @property
    def engagement_type(self):
        return self.input_json['engagement_type']

    @property
    def build_id(self):
        return self.input_json['build_id']

    @property
    def commit_hash(self):
        return self.input_json['commit_hash']

    @property
    def branch_tag(self):
        return self.input_json['branch_tag']

    @property
    def source_code_management_uri(self):
        return self.input_json['source_code_management_uri']

    @property
    def deduplication_on_engagement(self):
        return self.input_json['deduplication_on_engagement']

    @property
    def lead(self):
        return self.input_json['lead']

    @property
    def requester(self):
        return self.input_json['requester']

    @property
    def preset(self):
        return self.input_json['preset']

    @property
    def report_type(self):
        return self.input_json['report_type']

    @property
    def product(self):
        return self.input_json['product']

    @property
    def build_server(self):
        return self.input_json['build_server']

    @property
    def source_code_management_server(self):
        return self.input_json['source_code_management_server']

    @property
    def orchestration_engine(self):
        return self.input_json['orchestration_engine']

    @property
    def notes(self):
        return self.input_json['notes']

    @property
    def files(self):
        return self.input_json['files']

    @property
    def risk_acceptance(self):
        return self.input_json['risk_acceptance']
        
    
    
if __name__ == '__main__':
    j={
	"id": 9,
	"tags": [],
	"name": "quay.io/domino/frontend:5.3.0",
	"description": "engagement description",
	"version": "5.3.0",
	"first_contacted": "2022-10-12",
	"target_start": "2022-10-12",
	"target_end": "2022-12-31",
	"reason": "null",
	"updated": "2022-10-12T18:13:58.472846Z",
	"created": "2022-10-12T18:13:58.405440Z",
	"active": "true",
	"tracker": "null",
	"test_strategy": "null",
	"threat_model": "true",
	"api_test": "true",
	"pen_test": "true",
	"check_list": "true",
	"status": "In Progress",
	"progress": "threat_model",
	"tmodel_path": "none",
	"done_testing": "false",
	"engagement_type": "CI/CD",
	"build_id": "null",
	"commit_hash": "null",
	"branch_tag": "null",
	"source_code_management_uri": "null",
	"deduplication_on_engagement": "false",
	"lead": "null",
	"requester": "null",
	"preset": "null",
	"report_type": "null",
	"product": 3,
	"build_server": "null",
	"source_code_management_server": "null",
	"orchestration_engine": "null",
	"notes": [],
	"files": [],
	"risk_acceptance": []
}
    base_helper.iter_dict_into_properties(j)