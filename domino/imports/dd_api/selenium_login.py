from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains
import time

def dd_login(driver,usernam,password,login_url):
    driver.get(login_url)
    username = driver.find_element("xpath", "/html/body/div/div[1]/div/div[3]/div/form/fieldset/div[1]/div/input")
    username.send_keys(usernam)
    password_ = driver.find_element("xpath", "/html/body/div/div[1]/div/div[3]/div/form/fieldset/div[2]/div/input")
    password_.send_keys(password)
    submit_button = driver.find_element("xpath",
                                        '/html/body/div/div[1]/div/div[3]/div/form/fieldset/div[3]/div[2]/button')
    submit_button.click()


def create_epic_and_custom_labels_page(driver,engagement_id,base_url_with_slash,custom_labels):

    engagement_url=base_url_with_slash + "engagement/{}/edit".format(engagement_id)
    driver.get(engagement_url)


    #Disable inherit jira settings
    inherit_jira_button=driver.find_element("xpath", '//*[@id="id_jira-project-form-inherit_from_product"]')
    inherit_jira_button.click()

    #add custom labels
    # custom_labels='{"customfield_13459":"selenium"}'
    # labels_field_locator=driver.find_element(By.CSS_SELECTOR, "div[class='CodeMirror cm-s-easymde CodeMirror-wrap']")
    labels_field_locator=driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div[3]/div/form/div[24]/div/div/div[2]")
    action_chains=ActionChains(driver)
    action_chains.click(labels_field_locator).perform()
    #clear existing text
    action_chains.double_click()
    action_chains.send_keys(custom_labels).perform()
    # labels_field_locator.send_keys(custom_labels)


    # enable epic creation
    create_epic_button = driver.find_element("xpath","/html/body/div[1]/div[1]/div/div[3]/div/form/div[33]/div/div/label/input")
    action_chains.click(create_epic_button).perform()
    action_chains.click()
    # create_epic_button.click()

    #Click Done
    done_button = driver.find_element("xpath", "/html/body/div[1]/div[1]/div/div[3]/div/form/div[34]/div/input[3]")
    done_button.click()




def login_main(engagement_id,chromedriver_path,s_user,s_pass,base_url_with_slash,headless,custom_labels):

    # CHROMEDRIVER_PATH = '/Users/mannysingh/Downloads/chromedriver'
    chrome_options = Options()
    chrome_options.add_argument("start-maximized")
    if headless:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=chrome_options)
    # 1
    dd_login(driver, s_user, s_pass, base_url_with_slash)

    # 2 operations at enagement level
    create_epic_and_custom_labels_page(driver, engagement_id, base_url_with_slash,custom_labels)


if __name__ == '__main__':
    base_url_with_slash='https://defectdojo.secops-master.domino.tech/'
    from domino.imports import imports_main
    s_user, s_pass = imports_main.get_s_user_pass()

    ACCOUNT = s_user
    PASSWORD = s_pass
    api_base_url=base_url_with_slash + "api/v2"
    engagement_id=13
    CHROMEDRIVER_PATH = '/Users/mannysingh/Downloads/chromedriver'
    chrome_options = Options()
    chrome_options.add_argument("start-maximized")
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
    #1
    dd_login(driver, ACCOUNT, PASSWORD,base_url_with_slash)

    #2 operations at enagement level
    create_epic_and_custom_labels_page(driver, engagement_id, base_url_with_slash)



