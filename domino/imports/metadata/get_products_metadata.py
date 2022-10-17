
class GetProductsMetadata():
    def __init__(self,products_json):
        self.products_json=products_json

    @property
    def count(self):
        return self.products_json['count']

    @property
    def next(self):
        return self.products_json['next']

    @property
    def previous(self):
        return self.products_json['previous']

    @property
    def results(self):
        return self.products_json['results']

    @property
    def prefetch(self):
        return self.products_json['prefetch']



class ResultJson():
    def __init__(self,result_json):
        self.result_json=result_json

    @property
    def result_json_id(self):
        return self.result_json['id']

    @property
    def result_json_findings_count(self):
        return self.result_json['findings_count']

    @property
    def result_json_findings_list(self):
        return self.result_json['findings_list']

    @property
    def result_json_tags(self):
        return self.result_json['tags']

    @property
    def result_json_product_meta(self):
        return self.result_json['product_meta']

    @property
    def result_json_name(self):
        return self.result_json['name']

    @property
    def result_json_description(self):
        return self.result_json['description']

    @property
    def result_json_created(self):
        return self.result_json['created']

    @property
    def result_json_prod_numeric_grade(self):
        return self.result_json['prod_numeric_grade']

    @property
    def result_json_business_criticality(self):
        return self.result_json['business_criticality']

    @property
    def result_json_platform(self):
        return self.result_json['platform']

    @property
    def result_json_lifecycle(self):
        return self.result_json['lifecycle']

    @property
    def result_json_origin(self):
        return self.result_json['origin']

    @property
    def result_json_user_records(self):
        return self.result_json['user_records']

    @property
    def result_json_revenue(self):
        return self.result_json['revenue']

    @property
    def result_json_external_audience(self):
        return self.result_json['external_audience']

    @property
    def result_json_internet_accessible(self):
        return self.result_json['internet_accessible']

    @property
    def result_json_enable_simple_risk_acceptance(self):
        return self.result_json['enable_simple_risk_acceptance']

    @property
    def result_json_enable_full_risk_acceptance(self):
        return self.result_json['enable_full_risk_acceptance']

    @property
    def result_json_product_manager(self):
        return self.result_json['product_manager']

    @property
    def result_json_technical_contact(self):
        return self.result_json['technical_contact']

    @property
    def result_json_team_manager(self):
        return self.result_json['team_manager']

    @property
    def result_json_prod_type(self):
        return self.result_json['prod_type']

    @property
    def result_json_sla_configuration(self):
        return self.result_json['sla_configuration']

    @property
    def result_json_members(self):
        return self.result_json['members']

    @property
    def result_json_authorization_groups(self):
        return self.result_json['authorization_groups']

    @property
    def result_json_regulations(self):
        return self.result_json['regulations']


if __name__ == '__main__':
    j={'count': 3, 'next': None, 'previous': None, 'results': [
        {'id': 3, 'findings_count': 0, 'findings_list': [], 'tags': [], 'product_meta': [],
         'name': 'insomania', 'description': 'product description', 'created': '2022-10-12T15:41:52.293798Z', 'prod_numeric_grade': None,
         'business_criticality': None, 'platform': None, 'lifecycle': None, 'origin': None, 'user_records': None, 'revenue': None,
         'external_audience': True, 'internet_accessible': True, 'enable_simple_risk_acceptance': True, 'enable_full_risk_acceptance': True,
         'product_manager': None, 'technical_contact': None, 'team_manager': None, 'prod_type': 1, 'sla_configuration': 1, 'members': [],
         'authorization_groups': [], 'regulations': []},
        {'id': 1, 'findings_count': 20, 'findings_list': [222, 217, 212, 207, 221, 206, 216, 211, 205, 215, 210, 220, 219, 214, 204, 209, 203, 208, 213, 218],
         'tags': [], 'product_meta': [], 'name': 'test-product', 'description': 'test description', 'created': '2022-10-04T17:41:14.171188Z',
         'prod_numeric_grade': None, 'business_criticality': None, 'platform': None, 'lifecycle': None, 'origin': None, 'user_records': None,
         'revenue': None, 'external_audience': False, 'internet_accessible': False, 'enable_simple_risk_acceptance': True,
         'enable_full_risk_acceptance': True, 'product_manager': None, 'technical_contact': None, 'team_manager': None,
         'prod_type': 1, 'sla_configuration': 1, 'members': [], 'authorization_groups': [], 'regulations': []},
        {'id': 2, 'findings_count': 0, 'findings_list': [], 'tags': [], 'product_meta': [], 'name': 'test product name', 'description':
            'test product description', 'created': '2022-10-12T15:31:40.604149Z', 'prod_numeric_grade': None, 'business_criticality': None,
         'platform': None, 'lifecycle': None, 'origin': None, 'user_records': None, 'revenue': None, 'external_audience': False,
         'internet_accessible': False, 'enable_simple_risk_acceptance': True, 'enable_full_risk_acceptance': True, 'product_manager': None,
         'technical_contact': None, 'team_manager': None, 'prod_type': 1, 'sla_configuration': 1, 'members': [], 'authorization_groups': [],
         'regulations': []}
    ], 'prefetch': {}}

    r={'id': 3, 'findings_count': 0, 'findings_list': [], 'tags': [], 'product_meta': [],
         'name': 'insomania', 'description': 'product description', 'created': '2022-10-12T15:41:52.293798Z', 'prod_numeric_grade': None,
         'business_criticality': None, 'platform': None, 'lifecycle': None, 'origin': None, 'user_records': None, 'revenue': None,
         'external_audience': True, 'internet_accessible': True, 'enable_simple_risk_acceptance': True, 'enable_full_risk_acceptance': True,
         'product_manager': None, 'technical_contact': None, 'team_manager': None, 'prod_type': 1, 'sla_configuration': 1, 'members': [],
         'authorization_groups': [], 'regulations': []}
    def iter_dict_into_properties(j,initial='result_json'):
        for k, v in j.items():
            if initial !='get_issue_response':
                function_name= initial + '_' + k
            else:
                function_name=k
            function = '''
        @property
        def {}(self):
            return self.{}['{}']'''.format(function_name,initial, k)

            print(function)

            if isinstance(v,dict):
                iter_dict_into_properties(v,initial=function_name)

    iter_dict_into_properties(r)
