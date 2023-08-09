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
file_handler = logging.FileHandler('vtextBNPN.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

#############################################################

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
        browser.get(credentials["urlStagingVTEX"])
        logger.info("Setup() successful. Calling LoginScreen()")
        LoginScreen()
    except Exception as e:
        logger.error("ERROR ON FUNCTION setUp()")
        exceptionErrorAndRestart(e)    

def LoginScreen():
    try:
        browser.implicitly_wait(10)

        # Receive access code
        chaveAcesso = browser.find_element(By.XPATH, "//button[@id='loginWithAccessKeyBtn']")
        chaveAcesso.click()

        # input email
        clientEmail = browser.find_element(By.XPATH, "//input[@id='appendedInputButton']")
        clientEmail.click()
        clientEmail.clear()
        clientEmail.send_keys(credentials["testEmail"])

        # Confirm Button
        WebDriverWait(browser, 15).until(
        EC.element_to_be_clickable((By.XPATH, "(//button[@id='sendAccessKeyBtn'])[1]"))).click()

        # Request OTP to user
        otp = input("Enter OTP code: ") # TODO, get OTP code automatically.
        
        # input OTP code
        otpCodeInput = browser.find_element(By.XPATH, "//input[@id='access-code']")
        otpCodeInput.click()
        otpCodeInput.clear()
        otpCodeInput.send_keys(otp) # TODO, get OTP code from email or database

        # Submit Button
        submitButton = browser.find_element(By.XPATH, "//button[@id='confirmLoginAccessKeyBtn']")
        submitButton.click()
        logger.info("LoginScreen() successful. Calling additionalDataScreen()")
        additionalDataScreen()
    except Exception as e:
        logger.error("ERROR ON FUNCTION LoginScreen()")
        exceptionErrorAndRestart(e)

def additionalDataScreen():
    try:
        # Banner
        banner = browser.find_element(By.XPATH, "//img[@id='ihttps://addi.vteximg.com.br/arquivos/ids/155400/nuvemshop addi 2.jpg?v=637490452961730000']")
        banner.click()

        # Buy Button
        buyButton = browser.find_element(By.XPATH, "//div[@class='buy-button-box hidden-xs']//a[@class='buy-button buy-button-ref'][normalize-space()='Comprar']")
        buyButton.click()

        # Checkout button
        checkoutButton = browser.find_element(By.XPATH, "//a[@id='cart-to-orderform']")
        checkoutButton.click()

        # Input email
        finalizePurchaseEmail = browser.find_element(By.XPATH, "//input[@id='client-pre-email']")
        finalizePurchaseEmail.click()
        finalizePurchaseEmail.clear()
        finalizePurchaseEmail.send_keys(credentials["testEmail"])

        # Continue
        continueButton = browser.find_element(By.XPATH, "//span[@data-i18n='global.continue_']")
        continueButton.click()

        # Continue Pop-up
        continueButtonPopUp = browser.find_element(By.XPATH, "//button[@id='btn-identified-user-button']")
        continueButtonPopUp.click()

        # CEP Input
        cepInput = browser.find_element(By.XPATH, "//input[@id='ship-postalCode']")
        cepInput.click()
        cepInput.clear()
        cepInput.send_keys('12345')

        # Proceed to Payment
        cepInput = browser.find_element(By.XPATH, "//button[@id='btn-go-to-payment']")
        cepInput.click()
        
        # Addi Payment Label
        browser.implicitly_wait(10)
        addiPayment = browser.find_element(By.XPATH, "//div[@class='addi-payment-option-item__label']")
        addiPayment.click()

        # Finalize Purchase
        addiPaymentFinalize = browser.find_element(By.XPATH, "//button[3]")
        addiPaymentFinalize.click()
        
        logger.info("additionalDataScreen() successful. Test completed.")
    except Exception as e:
        logger.error("ERROR ON FUNCTION additionalDataScreen()")
        exceptionErrorAndRestart(e)    
    # TODO ADDI payment flow...

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