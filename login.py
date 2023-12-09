import os
import time
import pyotp
from fyers_api import accessToken
from fyers_api import fyersModel
from selenium import webdriver
from selenium.webdriver.common.by import By
from pyotp import TOTP
client_id = '0X7ILODH7P-100'
secret_id = 'ZBR807LNMI'
redirect_uri = 'https://www.google.com/'
username = "XD16634"
totp='333633'
pin1='2'
pin2='0'
pin3='0'
pin4='2'

session=accessToken.SessionModel(client_id=client_id,
secret_key=secret_id,redirect_uri=redirect_uri,
response_type='code', grant_type='authorization_code')
response = session.generate_authcode()
print(response)
#fyers = fyersModel.FyersModel(client_id=client_id, token=access_token,log_path=os.getcwd())

def generate_auth_code( ):
    session = accessToken.SessionModel(client_id=client_id,  secret_key=secret_id, redirect_uri=redirect_uri,
    response_type='code', grant_type='authorization_code')
    response = session.generate_authcode( )
    driver=webdriver.Chrome( )
    driver.get(response)
    time.sleep(2)
    id = driver.find_element(by=By.XPATH,value='//*[@id="fy_client_id"]')
    id.send_keys('XD16634')
    sub = driver.find_element(by=By.XPATH,value='//*[@id="clientIdSubmit"]')
    sub.click()
    time.sleep(2)
    t=pyotp.TOTP('6LR5ECSORHVDDD6ITSQIDN2OJVKOIUF5').now()
    print(t)

    t1 = driver.find_element(by=By.XPATH, value='//*[@id="first"]')
    t1.send_keys(t[0])
    t2 = driver.find_element(by=By.XPATH, value='//*[@id="second"]')
    t2.send_keys(t[1])
    t3 = driver.find_element(by=By.XPATH, value='//*[@id="third"]')
    t3.send_keys(t[2])
    t4 = driver.find_element(by=By.XPATH, value='//*[@id="fourth"]')
    t4.send_keys(t[3])
    t5 = driver.find_element(by=By.XPATH, value='//*[@id="fifth"]')
    t5.send_keys(t[4])
    t6 = driver.find_element(by=By.XPATH, value='//*[@id="sixth"]')
    t6.send_keys(t[5])
    sub_1 = driver.find_element(by=By.XPATH, value='//*[@id="confirmOtpSubmit"]')
    sub_1.click()
    time.sleep(3)
    v1 = driver.find_element(by=By.ID, value="verify-pin-page").find_element(by=By.ID, value='first')
    v1.send_keys(pin1)
    v2 = driver.find_element(by=By.ID, value="verify-pin-page").find_element(by=By.ID, value='second')
    v2.send_keys(pin2)
    v3 = driver.find_element(by=By.ID, value="verify-pin-page").find_element(by=By.ID, value='third')
    v3.send_keys(pin3)
    v4 = driver.find_element(by=By.ID, value="verify-pin-page").find_element(by=By.ID, value='fourth')
    v4.send_keys(pin4)
    sub_2 = driver.find_element(by=By.XPATH, value='//*[@id="verifyPinSubmit"]')
    sub_2.click()
    time.sleep(5)
    newurl = driver.current_url
    auth_code = newurl[newurl.index('auth_code=')+10:newurl.index('&state')]
    driver.quit()
    return auth_code

auth_code=generate_auth_code()
print(auth_code)

session.set_token(auth_code)
response = session.generate_token()
access_token=response["access_token"]
a=open("access_token",'w')
a.write(access_token)
a.close()
