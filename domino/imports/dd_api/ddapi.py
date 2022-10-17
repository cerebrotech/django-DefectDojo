from domino.base_helpers import aws_helper
from domino.base_helpers import base_helper
import requests
import json
from pprint import pprint

def basic_auth_headers(region='us-east-1',secret_name='infosec_defectdojo'):
    ss_obj=aws_helper.SecrertsManagerOperations(region=region)
    secrets = ss_obj.get_secret(secret_name)
    token = secrets['dd_token']
    return {"accept":"application/json","Authorization": "Token {}".format(token)}




def get_products(base_api_url_with_slash):
    products_url=base_api_url_with_slash +"products"
    response=requests.get(products_url,headers=basic_auth_headers())
    print("get_products response code: ",response.status_code)
    if response.ok:
        response_json=json.loads(response.text)
        return response_json
    else:
        print("get_products failed: ", response.status_code)
        print(response.text)
        exit(1)


def create_product(product_name,base_api_url_with_slash):
    products_url = base_api_url_with_slash + "products/"
    product_data={"name": product_name,
                  "description": "Project description for: {}".format(product_name),
                  "external_audience": "true",
                  "internet_accessible": "true",
                  "enable_simple_risk_acceptance": "true",
                  "enable_full_risk_acceptance": "true",
                  "prod_type": 1
                  }
    response=requests.post(products_url,headers=basic_auth_headers(),json=product_data)
    print("create_product response code: ", response.status_code)
    if response.ok:
        response_json=json.loads(response.text)
        return response_json
    else:
        print("create_product failed: ", response.status_code)
        print(response.text)
        exit(1)


def get_engagements(product_id,base_api_url_with_slash):
    engagements_url = base_api_url_with_slash + "engagements/"
    querystring = {"product":"{}".format(product_id)}
    response=requests.get(engagements_url,headers=basic_auth_headers(),params=querystring)
    print("get_engagements response code: ", response.status_code)
    if response.ok:
        response_json=json.loads(response.text)
        return response_json
    else:
        print("get_engagements failed: ", response.status_code)
        print(response.text)
        exit(1)

def create_engagaement(product_id,engagement_name,domino_next_release,base_api_url_with_slash,lead=1):
    engagements_url = base_api_url_with_slash + "engagements/"
    payload = {
        "name": engagement_name,
        "description": "engagement description",
        "version": domino_next_release,
        "first_contacted": base_helper.todays_date_dash(),
        "target_start": base_helper.todays_date_dash(),
        "target_end": "2070-12-31",
        "threat_model": True,
        "api_test": True,
        "pen_test": True,
        "check_list": True,
        "status": "In Progress",
        "engagement_type": "CI/CD",
        "product": product_id,
        "lead": lead
    }

    response = requests.post(engagements_url, headers=basic_auth_headers(), json=payload)
    print("create_engagaement response code: ", response.status_code)
    if response.ok:
        response_json = json.loads(response.text)
        return response_json
    else:
        print("create_engagaement failed: ", response.status_code)
        print(response.text)
        exit(1)

def jira_product_config(api_base_url,product_id,project_jira_key,jira_instance=1):
    jira_config_url=api_base_url + "jira_product_configurations/"
    data={
    "project_key": project_jira_key,
    "issue_template_dir": "issue-trackers/jira_full",
    "add_vulnerability_id_to_jira_label": True,
    "push_all_issues": True,
    "enable_engagement_epic_mapping": True,
    "push_notes": True,
    "product_jira_sla_notification": True,
    "risk_acceptance_expiration_notification": True,
    "jira_instance": jira_instance,
    "product": product_id,
    "engagement": None
}
    pprint(data)
    response = requests.post(jira_config_url, headers=basic_auth_headers(), json=data)
    print("create_product response code: ", response.status_code)
    if response.ok:
        response_json = json.loads(response.text)
        return response_json
    else:
        print("create_product failed: ", response.status_code)
        print(response.text)
        exit(1)


def get_tests(engagement_id,base_api_url_with_slash):
    parameters={"engagement":engagement_id}
    get_tests_url=base_api_url_with_slash +'tests'
    response=requests.get(get_tests_url,headers=basic_auth_headers(),params=parameters)

    print("get_tests response code: ", response.status_code)
    if response.ok:
        response_json = json.loads(response.text)
        return response_json
    else:
        print("get_tests failed: ", response.status_code)
        print(response.text)
        exit(1)


def reimport_scan(existing_test_id,scan_json_file_path,base_api_url_with_slash,minimum_severity='High'):
    reimport_url=base_api_url_with_slash +"reimport-scan/"

    files = {
        'minimum_severity': (None, minimum_severity),
        'active': (None, 'true'),
        'verified': (None, 'true'),
        'scan_type': (None, 'Twistlock Domino Image Scan'),
        'file': open(scan_json_file_path, 'rb'),
        'test': (None, existing_test_id),
        'push_to_jira': (None, 'true'),
        'close_old_findings': (None, 'true'),
        'group_by': (None, 'file_path'),
    }

    response = requests.post(reimport_url, headers=basic_auth_headers(),files=files)
    if response.ok:
        print("Results uploaded for existing test id:",existing_test_id,)
        response_json = json.loads(response.text)
        return response_json
    else:
        print("Reupload failed for test id: ",existing_test_id)
        print(response.text)
        exit(1)

def import_scan(engagement_id,scan_json_file_path,base_api_url_with_slash,minimum_severity='High'):
    import_url=base_api_url_with_slash +"import-scan/"

    files = {
        'minimum_severity': (None, minimum_severity),
        'active': (None, 'true'),
        'verified': (None, 'true'),
        'scan_type': (None, 'Twistlock Domino Image Scan'),
        'file': open(scan_json_file_path, 'rb'),
        'engagement': (None, engagement_id),
        'close_old_findings': (None, 'true'),
        'push_to_jira': (None, 'true'),
        'group_by': (None, 'file_path'),
    }

    response = requests.post(import_url, headers=basic_auth_headers(),files=files)
    if response.ok:
        print("New test Results uploaded for engagement id:",engagement_id)
        response_json = json.loads(response.text)
        return response_json
    else:
        print("FAILED: New Test upload failed for engagement id: ",engagement_id)
        print(response.text)
        exit(1)




if __name__ == '__main__':
    base_url_with_slash = 'https://defectdojo.secops-master.domino.tech/'
    api_base_url = base_url_with_slash + "api/v2/"
    # create_product("product_name",api_base_url)
    # jira_product_config(api_base_url, 4, "OSST")
    pprint(get_engagements(4, api_base_url))