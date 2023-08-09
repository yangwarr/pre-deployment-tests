from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import logging
import random


### Global Logger Settings ##################################

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('payLinkClient.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

######################################################

### Global Settings ##################################

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
browser = webdriver.Chrome(options=chrome_options)
with open("credentials.json", "r") as f:
    credentials = json.load(f)

######################################################

def setUp():
    try:
        browser.maximize_window()
        browser.get(credentials["urlStagingPayLink"])
        logger.info("Setup() successful. Calling LoginScreen()")
        LoginScreen()
    except Exception as e:
        logger.error("ERROR ON FUNCTION setUp()")
        exceptionErrorAndRestart(e)

def LoginScreen():
    try:
        browser.implicitly_wait(10)
        id = browser.find_element(By.ID, '1-email')
        password = browser.find_element(By.NAME, 'password')
        id.send_keys(credentials["username"])
        password.send_keys(credentials["password"])
        submitButton = browser.find_element(By.NAME, 'submit')
        submitButton.click()
        logger.info("LoginScreen() successful. Calling payLinkScreen()")
        payLinkScreen()
    except Exception as e:
        logger.error("ERROR ON FUNCTION LoginSCreen()")
        exceptionErrorAndRestart(e)

def payLinkScreen():
    try:
        browser.implicitly_wait(10)

        primeiroEntendido = browser.find_element(By.XPATH, '//button[text()="Entendido"]')
        primeiroEntendido.click()

        segundoEntendido = browser.find_element(By.XPATH, '//button[text()="Entendido"]')
        segundoEntendido.click()

        # Escolha uma loja
        escolhaLoja = browser.find_element(By.NAME, 'input')
        # //input[@placeholder='Lojas']
        escolhaLoja.send_keys('ADDI BRASIL ADDI BRAZIL ONLINE')

        # CPF do client
        cpfCliente = browser.find_element(By.NAME, 'idNumber')
        # //input[@placeholder='000.000.000-0']
        cpfCliente.click()
        cpfCliente.clear()
        cpfCliente.send_keys(credentials["testCPF"])
        browser.implicitly_wait(5)

        # Valor da compra
        valorCompra = browser.find_element(By.XPATH, '//input[@placeholder="00,00"]')
        valorCompra.send_keys(random.randint(1,999))

        # Descrição da compra
        valorCompra = browser.find_element(By.XPATH, '//input[@placeholder="ex.: sapato masculino em couro preto"]')
        valorCompra.send_keys('RC')

        # Enviar Link
        WebDriverWait(browser, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))).click()
        logger.info("payLinkScreen() successful. Calling getPayLinkFromEmail()")
        getPayLinkFromEmail()
    except Exception as e:
        logger.error("ERROR ON FUNCTION payLinkScreen()")
        exceptionErrorAndRestart(e)

def getPayLinkFromEmail():
    try:
        payLink = input("Enter payLink: ")
        print(payLink)

        browser.execute_script("window.open('');")
        browser.switch_to.new_window('window')
        formatPayLink = "http://" + payLink
        formatPayLink = formatPayLink.strip()

        print(formatPayLink)
        browser.get(formatPayLink)

        WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable((By.XPATH, "(//input[@type='radio'])[2]"))).click()       

        WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable((By.XPATH, "(//button[@class='sc-dFJsGO sc-bsipQr sc-gInsOo EVEGg lbqHaU grsaJH'])[1]"))).click()
        
        #WebDriverWait(browser, 30).until(
        #    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Confirmar']"))).click()

        otpCode = browser.find_element(By.XPATH, "//input[@id='otp-input-0']")
        otpCode.clear()
        otpCode.click()
        otpInput = input("Enter otp code: ")
        
        otpcode1 = browser.find_element(By.XPATH, "//input[@id='otp-input-0']")
        otpcode2 = browser.find_element(By.XPATH, "//input[@id='otp-input-1']")
        otpcode3 = browser.find_element(By.XPATH, "//input[@id='otp-input-2']")
        otpcode4 = browser.find_element(By.XPATH, "//input[@id='otp-input-3']")
        otpcode5 = browser.find_element(By.XPATH, "//input[@id='otp-input-4']")
        otpcode6 = browser.find_element(By.XPATH, "//input[@id='otp-input-5']")
    
        for i, v in enumerate(otpInput):
            if i == 0:
                otpcode1.send_keys(v)
            if i == 1:
                otpcode2.send_keys(v)
            if i == 2:
                otpcode3.send_keys(v)
            if i == 3:
                otpcode4.send_keys(v)
            if i == 4:
                otpcode5.send_keys(v)
            if i == 5:
                otpcode6.send_keys(v)
        logger.info("getPayLinkFromEmail() successful. Calling confirmYourPurchase()")
        confirmYourPurchase()
            # confirmYourPersonalData()
    except Exception as e:
        logger.error("ERROR ON FUNCTION getPayLinkFromEmail()")
        exceptionErrorAndRestart(e)

def confirmYourPersonalData(): # sometimes this is needed in the flow
    browser.implicitly_wait(10)
    fullNameMotherName = browser.find_element(By.XPATH, "//input[@id='fullname']")
    fullNameMotherName.clear()
    fullNameMotherName.send_keys('TEST TEST')

    WebDriverWait(browser, 30).until(
    EC.element_to_be_clickable((By.XPATH, "(//div[@class='Formstyled__ActionContainer-df58vk-11 bsqxZr'])[1]"))).click()
    confirmYourPurchase()

def confirmYourPurchase():
    try:
        browser.implicitly_wait(10)

        WebDriverWait(browser, 30).until(
        EC.element_to_be_clickable((By.XPATH, "(//input[@type='checkbox'])[1]"))).click()

        WebDriverWait(browser, 30).until(
        EC.element_to_be_clickable((By.XPATH, "(//button[normalize-space()='Continuar'])[1]"))).click()
        
        # Confirm pop-up
        WebDriverWait(browser, 30).until(
        EC.element_to_be_clickable((By.XPATH, "(//button[normalize-space()='Ok, entendi'])[1]"))).click()
        logger.info("confirmYourPurchase() successful. Test completed.")
    except Exception as e:
        logger.error("ERROR ON FUNCTION confirmYourPurchase()")
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