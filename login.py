from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from time import sleep
from PIL import Image

from crop import crop
from predict import predict
import json
import os
# 可以在setting.json裡預先輸入帳密，就不用每次都重新輸入
with open('setting.json', 'r', encoding="utf8") as f:
    data=json.load(f)

if data["account"]=="unknown" or data["password"]=="unknown":
    print("please set the password first")
    os._exit(1)
else :
    USER_NAME=data["account"]
    PASSWORD=data["password"]

URL="https://ecsa.ntcu.edu.tw/"

chrome_options = Options()
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument('--disable-notifications')
chrome_options.add_argument("headless")
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

def handleAlert():
    try:
        alert = driver.switch_to.alert
        #print(alert.text)
        if(alert.text=='請確定帳號、密碼是否輸入正確!'):
            print('1')
            driver.quit()
            os._exit(1)
        elif(alert.text=='登入錯誤已達3次，請於15分鐘後再重新登入系統！!'):
            print('2')
            os._exit(1)
        elif(alert.text=='驗證碼錯誤'):
            print('check code error')
        else:
            print('others')
        
        alert.accept()
    except:
        pass

def login():
    
    driver.get(URL)
    
    #get_element
    account_element = driver.find_element(By.ID,"User_Account")
    password_element = driver.find_element(By.ID,"User_Password")
    checkcode_element = driver.find_element(By.ID,"Check_Code")
    client_Login_element = driver.find_element(By.ID,"Client_Login")
    check_code_img = driver.find_element(By.ID,"Check_Code_Img")
    #fill in
    account_element.send_keys(USER_NAME)
    password_element.send_keys(PASSWORD)
    #download checkcode image
    
    with open('code_img.png', 'wb') as img:
        img.write(check_code_img.screenshot_as_png)
        img.close()
    #crop image (use crop.py)
    crop("code_img.png")

    #predict (use crop.py)
    code = predict("code_img.png")
    checkcode_element.send_keys(code)
    client_Login_element.click()
    sleep(3)
    handleAlert()  

    try:
        driver.find_element(By.XPATH,'//*[@id="myform"]/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr/td[3]/a').click()
    except:
        pass
    #抓取系級
    try:
        grade=driver.find_element(By.XPATH,'//*[@id="ClassName"]').text
        name=driver.find_element(By.XPATH,'//*[@id="Name"]').text
        data["grade"]=grade
        data["name"]=name
        with open('setting.json', 'w', encoding="utf8") as f:
                f.write(json.dumps(data,ensure_ascii=False))

        return 0
    except:
        print("login error")
        return -1  

def getData():
    URL2='https://ecsa.ntcu.edu.tw/STDWEB/GRDYearsScore.aspx'
    driver.get(URL2)
    driver.implicitly_wait(5)
    handleAlert()
    courseList={}   
    for i in range(1,100):
        
        course_code='//*[@id="table_std_GRDlist"]/tbody/tr[{}]/td[3]'.format(i)
        course_name='//*[@id="table_std_GRDlist"]/tbody/tr[{}]/td[4]'.format(i)
        course_credit='//*[@id="table_std_GRDlist"]/tbody/tr[{}]/td[6]'.format(i)
        score = '//*[@id="table_std_GRDlist"]/tbody/tr[{}]/td[7]'.format(i)
              
        try:
            driver.implicitly_wait(2)
            
            subject_score = driver.find_element(By.XPATH,score)
            #print(float(subject_score.text))
            if float(subject_score.text) >=60 or subject_score.text=='及格':
                courseList[driver.find_element(By.XPATH,course_code).text]=[driver.find_element(By.XPATH,course_name).text,driver.find_element(By.XPATH,course_credit).text]
            
        except:
            
            with open('myCourse.json', 'w', encoding="utf8") as f:
                f.write(json.dumps(courseList,indent=4,ensure_ascii=False))

            print("getData end")
            break

def main():
    for i in range(2):
        if login()==0:
            getData() 
            break

if __name__ == '__main__':
    main()