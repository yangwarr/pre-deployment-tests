from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import json
import logging
import random


### Global Logger Settings ##################################

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('nuvemShop.log')
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
        browser.get(credentials["urlStagingNuvemShop"])
        logger.info("Setup() successful. Calling LoginScreen()")
        purchaseLaptopScreen()
    except Exception as e:
        logger.error("ERROR ON FUNCTION setUp()")
        exceptionErrorAndRestart(e, setUp.__name__)

def purchaseLaptopScreen():
    try:
        browser.implicitly_wait(10)

        hoverLaptop = browser.find_element(By.XPATH, "(//img[@alt='Portatil'])[1]")
        hover = ActionChains(browser).move_to_element(hoverLaptop)
        hover.perform()

        buyButton = browser.find_element(By.XPATH, "(//input[@value='Comprar'])[1]")
        buyButton.click()

        basketButton = browser.find_element(By.XPATH, "(//a[@class='js-modal-open js-cart-notification-close js-fullscreen-modal-open btn btn-primary btn-medium w-100 d-inline-block'][normalize-space()='Ver carrinho'])[1]")
        basketButton.click()

        checkOutButton = browser.find_element(By.XPATH, "(//input[@name='go_to_checkout'])[1]")
        checkOutButton.click()
        logger.info("purchaseLaptopScreen() successful. Calling paymentScreen()")
        paymentScreen()
    except Exception as e:
        logger.error("ERROR ON FUNCTION purchaseLaptopScreen()")
        exceptionErrorAndRestart(e, purchaseLaptopScreen.__name__)

def paymentScreen():
    try:
        email = browser.find_element(By.XPATH, "//input[@id='contact.email']")
        email.clear()
        email.send_keys(credentials["testEmail"])

        shippingZipCode = browser.find_element(By.XPATH, "(//input[@id='shippingAddress.zipcode'])[1]")
        shippingZipCode.clear()
        shippingZipCode.send_keys("91360040")

        continueButton = browser.find_element(By.XPATH, "(//span[contains(text(),'Continuar')])[1]")
        continueButton.click()

        pacShippingRadioButton = browser.find_element(By.XPATH, "(//div[@class='selector'])[1]")
        pacShippingRadioButton.click()

        name = browser.find_element(By.XPATH, "(//input[@id='shippingAddress.first_name'])[1]")
        name.send_keys(credentials["testFirstName"])

        lastName = browser.find_element(By.XPATH, "(//input[@id='shippingAddress.last_name'])[1]")
        lastName.send_keys(credentials["testLastName"])

        addressNumber = browser.find_element(By.XPATH, "(//input[@id='shippingAddress.number'])[1]")
        addressNumber.send_keys(credentials["testAddressNumber"])

        complementAddressNumber = browser.find_element(By.XPATH, "(//input[@id='shippingAddress.floor'])[1]")
        complementAddressNumber.send_keys(credentials["testComplementNumber"])
        
        idNumber = browser.find_element(By.XPATH, "(//input[@id='billingAddress.id_number'])[1]")
        idNumber.send_keys(credentials["testCPF"])

        submitButton = browser.find_element(By.XPATH, "(//button[@type='submit'])[1]")
        submitButton.click()

        logger.info("paymentScreen() successful. Calling paymentMethod()")
        paymentMethod()
    except Exception as e:
        logger.error("ERROR ON FUNCTION purchaseLaptopScreen()")
        exceptionErrorAndRestart(e, paymentScreen.__name__)

def paymentMethod():
    try:
        browser.implicitly_wait(90)

        # switch to selected iframe
        browser.switch_to.frame("iFrameResizer0")

        # Now click on button
        browser.find_element(By.XPATH, "//*[contains(text(), 'Paga')]").click()

        browser.switch_to.default_content()

        WebDriverWait(browser, 90).until(
        EC.element_to_be_clickable((By.XPATH, "(//div[@id='btnFinishCheckout'])[1]"))).click()

        WebDriverWait(browser, 90).until(
        EC.element_to_be_clickable((By.XPATH, "(//div[@id='btnFinishCheckout'])[1]"))).click()
        
        logger.info("paymentMethod() successful. Calling addiBNPLFlow")
        addiBNPLFlow()
    except Exception as e:
        logger.error("ERROR ON FUNCTION paymentMethod()")
        exceptionErrorAndRestart(e, paymentMethod.__name__)

def addiBNPLFlow(): 
    try:
        WebDriverWait(browser, 30).until(
        EC.element_to_be_clickable((By.XPATH, "(//input[@type='radio'])[2]"))).click()

        WebDriverWait(browser, 30).until(
        EC.element_to_be_clickable((By.XPATH, "(//button[@class='sc-dFJsGO sc-bsipQr sc-gInsOo EVEGg lbqHaU grsaJH'])[1]"))).click()

        clientCellPhone = browser.find_element(By.XPATH, "//input[@id='cellphone_number']")
        clientCellPhone.click()
        clientCellPhone.send_keys(credentials["testPhone"])

        WebDriverWait(browser, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()
        
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

        WebDriverWait(browser, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()
        logger.info("addiBNPLFlow() successful.")
        personalData()

    except Exception as e:
        logger.error("ERROR ON FUNCTION paymentMethod()")
        exceptionErrorAndRestart(e, addiBNPLFlow.__name__)

def personalData():
    try:
        birthDate = browser.find_element(By.XPATH, "//input[@id='birthDate']")
        birthDate.clear()
        birthDate.click()
        birthDate.send_keys(credentials["testBirthDate"])
        WebDriverWait(browser, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Criar conta Addi']"))).click()
        logger.info("personalData() successful. Calling confirmYourPurchase()")
        confirmYourPurchase()
    except Exception as e:
        logging.error("ERROR on function personalData()")
        exceptionErrorAndRestart(e, personalData.__name__)

def confirmYourPurchase():
    try:
        browser.implicitly_wait(20)
        termsOfServiceCheckBox = browser.find_element(By.XPATH, "(//input[@type='checkbox'])[1]")
        termsOfServiceCheckBox.click()
        WebDriverWait(browser, 30).until(
        EC.element_to_be_clickable((By.XPATH, "(//button[normalize-space()='Continuar'])[1]"))).click()
        
        # Confirm pop-up
        print("confirmYourPurchase() successful. Test ended. Please finish the IDV part manually and press CTRL+C to exit the program.")
        logger.info("confirmYourPurchase() successful. Test ended.")
    except Exception as e:
        logging.error("ERROR on function confirmYourPurchase()")
        exceptionErrorAndRestart(e, confirmYourPurchase.__name__)

def exceptionErrorAndRestart(e, functionName):
    logger.error(e)
    print("Operation failed, attempting to restart. FAILED AT: " + functionName)
    browser.execute_script("window.close('');")
    browser.execute_script("window.open('');")
    browser.switch_to.new_window('window')
    setUp()


def main():
    setUp()
    while(True):
        pass

if __name__ == "__main__":
    main()