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
file_handler = logging.FileHandler('vtexBNPL.log')
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
        browser.implicitly_wait(30)
        addiPayment = browser.find_element(By.XPATH, "//div[@class='addi-payment-option-item__label']")
        addiPayment.click()

        shadow_host = browser.find_element(By.CSS_SELECTOR, "addi-payment-description[discount='0']")
        shadow_root = shadow_host.shadow_root

        #shadow_content = shadow_root.find_element(By.CSS_SELECTOR, 'child_iframe_css_selector')
        element = WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.NAME, "addi_subproduct")))
        element.click()

        # Finalize Purchase
        addiPaymentFinalize = browser.find_element(By.XPATH, "//button[3]")
        addiPaymentFinalize.click()
        logger.info("additionalDataScreen() successful. Calling addiFlowBNPL().")
        #addiFlowBNPL()
    except Exception as e:
        logger.error("ERROR ON FUNCTION additionalDataScreen()")
        exceptionErrorAndRestart(e, additionalDataScreen.__name__)    
    # TODO ADDI payment flow...

def addiFlowBNPL():
    try:
        browser.implicitly_wait(30)
        #bnplButton = browser.find_element()
        #bnplButton.click()

        WebDriverWait(browser, 30).until(
        EC.element_to_be_clickable((By.XPATH, "(//input[@type='radio'])[2]"))).click()

        WebDriverWait(browser, 30).until(
        EC.element_to_be_clickable(By.XPATH, "//button[@class='sc-dFJsGO sc-bsipQr sc-gInsOo EVEGg lbqHaU grsaJH']")).click()

       # continueButton = browser.find_element()
        #continueButton.click()
        logger.info("addiFlowBNPL() successful. Calling cellphoneValidation()")
        cellPhoneValidation()
    except Exception as e:
        logger.error("ERROR ON FUNCTION: " + addiFlowBNPL.__name__)
        exceptionErrorAndRestart(e, addiFlowBNPL.__name__)

def cellPhoneValidation():
    try:
        browser.implicitly_wait(30)
        cellPhone = browser.find_element(By.XPATH, "//input[@id='cellphone_number']")
        cellPhone.clear()
        cellPhone.send_keys(credentials["testPhone"])

        continueButton = browser.find_element(By.XPATH, "//button[@type='submit']")
        continueButton.click()

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
                print('otp1: ' + v)
            if i == 1:
                otpcode2.send_keys(v)
                print('otp2: ' + v)
            if i == 2:
                otpcode3.send_keys(v)
                print('otp3: ' + v)
            if i == 3:
                otpcode4.send_keys(v)
                print('otp4: ' + v)
            if i == 4:
                otpcode5.send_keys(v)
                print('otp5: ' + v)
            if i == 5:
                otpcode6.send_keys(v)
                print('otp6: ' + v)
        logger.info("cellPhoneValidation() successful. Calling personalData()")
        personalData()
    except Exception as e:
        logger.error("ERROR ON FUNCTION: " + cellPhoneValidation.__name__)
        exceptionErrorAndRestart(e, cellPhoneValidation.__name__)

def personalData():
    try:
        browser.implicitly_wait(30)
        email = browser.find_element(By.XPATH, "//input[@id='email']")
        email.clear()
        email.send_keys(credentials["testEmail"])

        continueButton = browser.find_element(By.XPATH, "//button[@type='submit']")
        continueButton.click()
        logger.info("personalData() successful. Calling additionalInformation()")
        additionalInformation()
    except Exception as e:
        logger.error("ERROR ON FUNCTION: " + personalData.__name__)
        exceptionErrorAndRestart(e, personalData.__name__)

def additionalInformation():
    try:
        browser.implicitly_wait(30)
        birthDate = browser.find_element(By.XPATH, "//input[@id='birthDate']")
        birthDate.clear()
        birthDate.send_keys(credentials["testBirthDate"])

        WebDriverWait(browser, 30).until(
        EC.element_to_be_clickable((By.XPATH, "(//div[@class='AdditionalInformationFormStyled__ActionContainer-sc-165vu8k-15 goVLHD'])[1]"))).click()
        loanProposal()
        logger.info("additionalInformation() successful. Calling loanProposal()")
    except Exception as e:
        logger.error("ERROR ON FUNCTION: " + additionalInformation.__name__)
        exceptionErrorAndRestart(e, additionalInformation.__name__)

def loanProposal():
    try:
        browser.implicitly_wait(30)
        checkBox = browser.find_element(By.XPATH, "(//input[@type='checkbox'])[1]")
        checkBox.click()

        WebDriverWait(browser, 30).until(
        EC.element_to_be_clickable(browser.find_element(By.XPATH, "(//button[normalize-space()='Continuar'])[1]"))).click()
        logger.info("loanProposal() successful. Calling loanProposal()")
    except Exception as e:
        logger.error("ERROR ON FUNCTION: " + addiFlowBNPL.__name__)
        exceptionErrorAndRestart(e, addiFlowBNPL.__name__)

def exceptionErrorAndRestart(e, functionName):
    logger.error(e)
    print("Operation failed, attempting to restart. Error at: " + functionName)
    browser.execute_script("window.open('');")
    browser.switch_to.new_window('window')
    setUp()

def main():
    setUp()
    while(True):
        pass

if __name__ == "__main__":
    main()