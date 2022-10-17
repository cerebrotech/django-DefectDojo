import json
import requests
from pprint import pprint
from domino.imports.metadata.scan_json_metadata import  ScanReport
from domino.imports.metadata import get_products_metadata
from domino.imports.metadata import create_product_metadata
from domino.imports.metadata import get_engagements_metadata
from domino.imports.metadata import create_engagement_metadata
from domino.imports.metadata import get_tests_metadata
from domino.imports.dd_api import selenium_login
from domino.imports.dd_api import  ddapi
from domino.base_helpers import aws_helper
from domino.imports.twistlock_parser import json_parser

def get_products_list_from_dd(api_base_url):
    products_dict={} #{name:id}
    products_json=ddapi.get_products(api_base_url)
    products_json_obj=get_products_metadata.GetProductsMetadata(products_json)
    for result_dict in products_json_obj.results:
        results_obj=get_products_metadata.ResultJson(result_dict)
        products_dict[results_obj.result_json_name]=results_obj.result_json_id
    return products_dict

def check_if_product_exists(scan_report_obj,products_dict):
    if scan_report_obj.container_name in products_dict.keys():
        return True
    else:
        return False


def set_jira_product_configs(product_id,jira_project_key):
    response_json=ddapi.jira_product_config(api_base_url, product_id, jira_project_key)


def create_new_dd_product(scan_report_obj,api_base_url,jira_project_key):
    product_name=scan_report_obj.container_name
    response_json=ddapi.create_product(product_name,api_base_url)
    response_json_obj=create_product_metadata.CreateProductMetadata(response_json)
    product_id=response_json_obj.id
    set_jira_product_configs(product_id, jira_project_key)
    return product_id

def get_new_or_existing_product_id(scan_report_obj,api_base_url,jira_project_key):
    products_dict = get_products_list_from_dd(api_base_url)
    pprint(products_dict)
    if check_if_product_exists(scan_report_obj, products_dict):
        product_id = products_dict[scan_report_obj.container_name]
    else:
        product_id = create_new_dd_product(scan_report_obj, api_base_url, jira_project_key)
    return product_id





def create_engagement_stub(product_id,expecting_engagement_name,domino_next_release,chromedriver_path,s_user,s_pass,api_base_url,base_url,headless):
    engagement_response_json = ddapi.create_engagaement(product_id, expecting_engagement_name, domino_next_release,
                                                        api_base_url)
    engagement_response_json_obj = create_engagement_metadata.CreateEngagementMetadata(engagement_response_json)
    engagement_id = engagement_response_json_obj.id

    return engagement_id

def get_existing_or_new_engagement_id(product_id,api_base_url,base_url,scan_report_obj,domino_next_release,chromedriver_path,headless):
    s_user,s_pass=get_s_user_pass()
    engagements_dict=ddapi.get_engagements(product_id,api_base_url)
    engagements_dict_obj=get_engagements_metadata.GetEngagementsMetadata(engagements_dict)
    expecting_engagement_name=scan_report_obj.container_name +":" + domino_next_release
    if int(engagements_dict_obj.count) >0:
        engagements_names_dict={}  #{engment_name:id}
        for result_dict in engagements_dict_obj.results:
            result_dict_obj=get_engagements_metadata.GetEngagementsResultsMetadata(result_dict)
            engagements_names_dict[result_dict_obj.name]=result_dict_obj.id
        if expecting_engagement_name in engagements_names_dict.keys():
            #engagement is already there
            engagement_id=engagements_names_dict[expecting_engagement_name]
        else:
            #here we need to create a new engagement
            engagement_id=create_engagement_stub(product_id,expecting_engagement_name,domino_next_release,chromedriver_path,s_user,s_pass,api_base_url,base_url,headless)
    else:
        engagement_id = create_engagement_stub(product_id,expecting_engagement_name,domino_next_release,chromedriver_path,s_user,s_pass,api_base_url,base_url,headless)

    # here we need to enable Create EPIC via selenium headless chrome because it,s not available via API
    selenium_login.login_main(engagement_id, chromedriver_path, s_user, s_pass, base_url, headless)
    return engagement_id


def get_existing_or_new_tests_id(engagement_id,base_api_url_with_slash):
    tests_json=ddapi.get_tests(engagement_id,base_api_url_with_slash)
    tests_json_obj=get_tests_metadata.GetTestsMetadata(tests_json)
    latest_test_id = tests_json_obj.id
    return latest_test_id

def upload_tests(engagement_id,test_id,scan_json_file_path,minimum_severity,base_api_url_with_slash):
    if test_id:
        ddapi.reimport_scan(test_id,scan_json_file_path,base_api_url_with_slash,minimum_severity)
    else:
        ddapi.import_scan(engagement_id,scan_json_file_path,base_api_url_with_slash,minimum_severity)


def get_s_user_pass(region='us-east-1',secret_name='infosec_defectdojo'):
    ss_obj=aws_helper.SecrertsManagerOperations(region=region)
    secrets = ss_obj.get_secret(secret_name)
    s_user = secrets['s_user']
    s_pass = secrets['s_pass']
    return s_user,s_pass


if __name__ == '__main__':
    scan_json_file_path='/Users/mannysingh/Documents/daily-work/defectdojo/NO-CVE-2022-32532-vuln812.json'
    base_url_with_slash = 'https://defectdojo.secops-master.domino.tech/'
    api_base_url = base_url_with_slash + "api/v2/"
    jira_project_key='OSST'
    domino_next_release="5.4.1"
    minimum_severity='High'
    chromedriver_path='/Users/mannysingh/Downloads/chromedriver'
    headless=False
    acceptable_severity_list = ['critical', 'high']
    parsed_json_reprt=json_parser.parse_twistlock_json_for_fixale_severity(scan_json_file_path,acceptable_severity_list)
    scan_report_obj=ScanReport(parsed_json_reprt)

    #1. get existing product and new product id
    product_id=get_new_or_existing_product_id(scan_report_obj, api_base_url,jira_project_key)
    print("Product id: ",product_id)


    #2. get existing or new engagement id
    engagement_id=get_existing_or_new_engagement_id(product_id,api_base_url,base_url_with_slash,scan_report_obj,domino_next_release,chromedriver_path,headless)
    print("engagement id: ", engagement_id)

    #3 get existing or new tests for this engagement
    test_id=get_existing_or_new_tests_id(engagement_id,api_base_url)

    #4 Upload tests to test id
    upload_tests(engagement_id, test_id, scan_json_file_path, minimum_severity, api_base_url)






