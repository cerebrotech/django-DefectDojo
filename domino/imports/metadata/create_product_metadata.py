from domino.base_helpers import base_helper


class CreateProductMetadata():
	def __init__(self,input_json):
		self.input_json=input_json

	@property
	def id(self):
		return self.input_json['id']

	@property
	def findings_count(self):
		return self.input_json['findings_count']

	@property
	def findings_list(self):
		return self.input_json['findings_list']

	@property
	def tags(self):
		return self.input_json['tags']

	@property
	def product_meta(self):
		return self.input_json['product_meta']

	@property
	def name(self):
		return self.input_json['name']

	@property
	def description(self):
		return self.input_json['description']

	@property
	def created(self):
		return self.input_json['created']

	@property
	def prod_numeric_grade(self):
		return self.input_json['prod_numeric_grade']

	@property
	def business_criticality(self):
		return self.input_json['business_criticality']

	@property
	def platform(self):
		return self.input_json['platform']

	@property
	def lifecycle(self):
		return self.input_json['lifecycle']

	@property
	def origin(self):
		return self.input_json['origin']

	@property
	def user_records(self):
		return self.input_json['user_records']

	@property
	def revenue(self):
		return self.input_json['revenue']

	@property
	def external_audience(self):
		return self.input_json['external_audience']

	@property
	def internet_accessible(self):
		return self.input_json['internet_accessible']

	@property
	def enable_simple_risk_acceptance(self):
		return self.input_json['enable_simple_risk_acceptance']

	@property
	def enable_full_risk_acceptance(self):
		return self.input_json['enable_full_risk_acceptance']

	@property
	def product_manager(self):
		return self.input_json['product_manager']

	@property
	def technical_contact(self):
		return self.input_json['technical_contact']

	@property
	def team_manager(self):
		return self.input_json['team_manager']

	@property
	def prod_type(self):
		return self.input_json['prod_type']

	@property
	def sla_configuration(self):
		return self.input_json['sla_configuration']

	@property
	def members(self):
		return self.input_json['members']

	@property
	def authorization_groups(self):
		return self.input_json['authorization_groups']

	@property
	def regulations(self):
		return self.input_json['regulations']

if __name__ == '__main__':
	j={
	"id": 3,
	"findings_count": 0,
	"findings_list": [],
	"tags": [],
	"product_meta": [],
	"name": "insomania",
	"description": "product description",
	"created": "2022-10-12T15:41:52.293798Z",
	"prod_numeric_grade": "null",
	"business_criticality": "null",
	"platform": "null",
	"lifecycle": "null",
	"origin": "null",
	"user_records": "null",
	"revenue": "null",
	"external_audience": "true",
	"internet_accessible": "true",
	"enable_simple_risk_acceptance": "true",
	"enable_full_risk_acceptance": "true",
	"product_manager": "null",
	"technical_contact": "null",
	"team_manager": "null",
	"prod_type": 1,
	"sla_configuration": 1,
	"members": [],
	"authorization_groups": [],
	"regulations": []
	}
	base_helper.iter_dict_into_properties(j)