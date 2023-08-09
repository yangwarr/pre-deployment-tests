from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import logging

### Global Logger Settings ##################################

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('preApproval.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

#############################################################

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
browser = webdriver.Chrome(options=chrome_options)
with open("credentials.json", "r") as f:
    credentials = json.load(f)

def setUp():
    try:
        browser.maximize_window()
        browser.get(credentials["urlStagingPreApproval"])
        logger.info("Setup() successful. Calling LoginScreen()")
        LoginScreen()
    except Exception as e:
        logging.error("ERROR on function confirmYourPurchase()")
        exceptionErrorAndRestart(e)

def LoginScreen(): 
    try:
        browser.implicitly_wait(10)
        cpfCliente = browser.find_element(By.XPATH, "//input[@placeholder='999.999.999-99']")
        cpfCliente.click()
        cpfCliente.clear()
        cpfCliente.send_keys(credentials["testCPF"])

        WebDriverWait(browser, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Aceitar e Continuar']"))).click()
        logger.info("LoginScreen() successful. Calling additionalDataScreen()")
        additionalDataScreen()
    except Exception as e:
        logging.error("ERROR on function LoginScreen()")
        exceptionErrorAndRestart(e)

def additionalDataScreen():
    # E-mail
    try:
        emailCliente = browser.find_element(By.XPATH, "//input[@id='email']")
        emailCliente.click()
        emailCliente.clear()
        emailCliente.send_keys(credentials["testEmail"])

        # Cellphone
        telefoneCliente = browser.find_element(By.XPATH, "//input[@id='cellphone_number']")
        telefoneCliente.click()
        telefoneCliente.clear()
        telefoneCliente.send_keys(credentials["testPhone"])

        # Birthday
        telefoneCliente = browser.find_element(By.XPATH, "//input[@id='birthdate']")
        telefoneCliente.click()
        telefoneCliente.clear()
        telefoneCliente.send_keys(credentials["testBirthDate"])

        # Submit Button
        WebDriverWait(browser, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Aceitar e continuar']"))).click()
        logger.info("additionalDataScreen() successful. Test completed.")
    except Exception as e:
        logging.error("ERROR on function LoginScreen()")
        exceptionErrorAndRestart(e)

def exceptionErrorAndRestart(e):
    logger.error(e)
    print("Operation failed, attempting to restart")
    browser.execute_script("window.open('');")
    browser.switch_to.new_window('window')
    setUp()

def main():
    setUp()
    while(True):
        pass

if __name__ == "__main__":
    main()