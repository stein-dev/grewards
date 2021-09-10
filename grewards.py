import base64
import sys
import uuid
import requests
import json
import os
import os.path
import time

from requests import api

# CONSTANT. DO NOT CHANGE!!!
url_otp = "https://api.sugar.digitalventures.ph/api/v1/user/otp"
url_verify = "https://api.sugar.digitalventures.ph/api/v1/user/verify"
url_register = "https://api.sugar.digitalventures.ph/api/v1/user/register"
url_points = "https://api.sugar.digitalventures.ph/api/v1/user/loyalty-points"
url_host = "api.sugar.digitalventures.ph"
api_key = "uMWTroc9Ms9uNIJ6XsMG05gEc7rwGely9ZoL7CrO"
laz100 = "3d4f0e30-c7a9-11eb-abd6-61ed24c80cd5"


def redeemRewards():
    print("""
===========================
   [3] REDEEM REWARDS
===========================

[1] Lazada Voucher 100
[2] Shoppee Voucher 100
[3] Go back to menu
""")
    global vchoice
    global nchoice
    
    vchoice = input("Select voucher: ")
    nchoice = input("Number of voucher: ")

    if vchoice == "" or nchoice == "":
        print("Please input something. Pleassseeee.")
        alertMsg()
    else:
        global shchoice
        shchoice = input("Share reward to other number [y/n]: ")
        if shchoice == "y":
            global shnum
            shnum = input("Enter mobile number: ")
            if shnum == "":
                print("Mobile number must not be empty!")
                alertMsg()
            else:
                if vchoice == "1":
                    redeem(nchoice, laz100, shchoice)
                elif vchoice == "2":
                    print("Not yet implemented!")
                    alertMsg()    
        elif shchoice == "n":          
            if vchoice == "1":
                redeem(nchoice, laz100, shchoice)
            elif vchoice == "2":
                print("Not yet implemented!")
                alertMsg()
        else:
            print("Invalid input. Please learn to read!")
            alertMsg()   

def redeem(str1, str2, str3):
    payload = {
            "X-GlobeRewards-Mobile": readFile('info.json', 'mobile'),
            "X-GlobeRewards-Device": readFile('info.json', 'devid'),
            "X-GlobeRewards-Device-Type": "android",
            "X-GlobeRewards-UUID": readFile('info.json', 'uuid'),
            "X-GlobeRewards-Token": readFile('info.json', 'token'),
            "X-Api-Key": api_key,
            "Content-Type": "application/json; charset=UTF-8",
            "Host": url_host,
            "Connection": "close",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.1"
        }
    if str3 == "n":    
        body = {
            "recipient": "null", "rewards": [{"message": "null", "name": "null", "quantity": int(str1), "uuid": str2}]
        }
        url = "https://api.sugar.digitalventures.ph/api/v1/reward/redeem"
    elif str3 == "y":
        body = {
            "recipient": shnum, "rewards": [{"message": "null", "name": "null", "quantity": int(str1), "uuid": str2}]
        }
        url= "https://api.sugar.digitalventures.ph/api/v1/rewards/share"
                
    print("Sending redeem request. Please wait...")
    r = requests.post(url, data=json.dumps(body), headers=payload)
    if r.status_code == 200:
        data = json.loads(r.content)
        if data['status'] == True:
            s = data['redemption_status']['success']
            f = data['redemption_status']['failed']
            if len(s) == 0:
                print("===========")
                print("FAILED")
                print("===========")
                print("Uuid: " + data['redemption_status']['failed'][0]['uuid'])
                print("Name: " + data['redemption_status']['failed'][0]['name'])
                print("Message: " + data['redemption_status']['failed'][0]['message'])
                pressAnyKey()
            elif len(f) == 0:
                print("===========")
                print("SUCCESS")
                print("===========")
                print("Uuid: " + data['redemption_status']['success'][0]['uuid'])
                print("Name: " + data['redemption_status']['success'][0]['name'])
                print("Message: " + data['redemption_status']['success'][0]['message'])
                pressAnyKey()  
            else:
                print("Try sending otp first to generate token.")
                alertMsg()        


def viewPoints():
    print("""
=======================
     [2] DASHBOARD
======================= 
""")
    
    payload = {
        "X-GlobeRewards-Mobile": readFile('info.json','mobile'),
        "X-GlobeRewards-Device": readFile('info.json','devid'),
        "X-GlobeRewards-Device-Type": "android",
        "X-GlobeRewards-UUID": readFile('info.json','uuid'),
        "X-GlobeRewards-Token": readFile('info.json','token'),
        "X-Api-Key": api_key,
        "Host": url_host,
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "okhttp/3.12.1"
    }

    r = requests.get(url_points, headers=payload)
    if r.status_code == 200:
        data = json.loads(r.content)
        if data['status'] == True:
            tpoints = data['data']['totalPoints']
            exp = data['data']['loyaltyPoints'][0]['expired_at']
            print("Total Points: " + str(tpoints))
            print("Expiration: " + str(exp))
            pressAnyKey()
        else:
            print("Try sending otp first to generate token.")
            alertMsg()   
    else:
        print("Something's wrong. I can feel it.")
        alertMsg()

def register():
    payload = {
        "X-GlobeRewards-Mobile": readFile('info.json','mobile'),
        "X-GlobeRewards-Device": readFile('info.json','devid'),
        "X-GlobeRewards-Device-Type": "android",
        "X-Api-Key": api_key,
        "X-GlobeRewards-App-Version": "3.2.35",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": url_host,
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "okhttp/3.12.1"
    }

    body = "first_name=Test&last_name=Ting&gender=Male&email=testing@byom.de&birthdate=1900-09-01&province=MilkyWay&municipality=Mars&pin=" + pinmsg + "&agree=true"

    print("Sending register request with dubious data...")
    r = requests.post(url_register, data=body, headers=payload)
    if r.status_code == 200:
        data = json.loads(r.content)
        if data['status'] == True:
            uuid_data = data['user']['uuid']
            updateFile("info.json", "uuid", uuid_data)
            token_data = data['user']['token']
            updateFile("info.json", "token", token_data)
            print("Successfully registered. Your account info has been saved.")
            print("=========================================================")
            print("UUID: " + uuid_data)
            print("Token: " + token_data)
            print("Mobile: " + data['user']['mobile'])
            print("========================================================")
            pressAnyKey()
        else:
            print("Try sending otp first to generate token.")
            alertMsg() 

    else:    
        print("Something's wrong. I can feel it.")  
        alertMsg()


def verifyOTP():
    global pinmsg
    pinmsg = input("Enter 6 digits pin code: ")

    payload = {
        "X-GlobeRewards-Mobile": number,
        "X-GlobeRewards-Device": readFile('info.json','devid'),
        "X-GlobeRewards-Device-Type": "android",
        "X-Api-Key": api_key,
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": url_host,
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "okhttp/3.12.1"
    }

    body = 'pin=' + pinmsg

    print("Verifying pin code. Please wait...")
    r = requests.post(url_verify, data=body, headers=payload)
    if r.status_code == 200:
        data = json.loads(r.content)
        if data['status'] == True:
            print("Pin is correct.")
            register()
        else:
            print("Pin is incorrect maybeeeee.")
            alertMsg()  
    else:
        print("Something's wrong. I can feel it.")  
        alertMsg()


def getOTP():
    print("""
=======================
    [1] SEND OTP
======================= 
""")
   
    global number
    number = input("Input mobile #: ")
    updateFile("info.json", "mobile", number)
    
    payload = {
        "X-GlobeRewards-Mobile": number,
        "X-GlobeRewards-Device": readFile('info.json','devid'),
        "X-GlobeRewards-Device-Type": "android",
        "X-Api-Key": api_key,
        "Host": url_host,
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "okhttp/3.12.1"
    }

    print("Sending otp to you number. Please wait...")
    r = requests.get(url_otp, headers=payload)
    if r.status_code == 200:
        data = json.loads(r.content)
        if data['status'] == True:
            tmp = data['message']
            print(tmp.replace("\n", "").replace("  ", "\n"))
            verifyOTP()
        else:
            tmp = data['message']
            print(tmp.replace("\n", "").replace("  ", "\n"))
            alertMsg() 
    else:
        print("Something's wrong. I can feel it.")
        alertMsg()

def encodeG(str1):
    try:
        return base64.b64encode(str1).decode('UTF-8')
    except:
        print("Something's wrong. I can feel it.")

def generateDeviceID():
    a = str(uuid.uuid1())
    aa = a.encode('UTF-8')
    b = "bq1v1e14aqwmui1er"
    bb = b.encode('UTF-8')
    c = encodeG(bb + aa)
    return c

def createFile(str):
    if not os.path.exists(str):
        info = {
            "devid" : generateDeviceID(),
            "token" : "pigscanfly",
            "uuid": "pigscanfly",
            "mobile": "pigscanfly"
        }
        json_object = json.dumps(info, indent = 4)
        with open(str, "w") as file:
            file.write(json_object)
            file.close()

def updateFile(str1, str2, str3):
     with open(str1, "r+") as file:
            data = json.load(file)
            data[str2] = str3
            json_object = json.dumps(data, indent = 4)
            file.seek(0)
            file.write(json_object)
            file.truncate()
            file.close()

def readFile(str1, str2):
    with open(str1, 'r') as openfile:
        json_object = json.load(openfile)
        return json_object[str2]

def alertMsg():
    print("\nGoing back to menu. Please wait...")
    time.sleep(5)
    clearConsole()

def pressAnyKey():
    input("\nPress any key to go back to menu")  
    clearConsole()  

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    else:
        command  = 'clear' 
    os.system(command)    

def main():
    print("""
=========================
GRewards by @pigscanfly
=========================

[1] Login/verify OTP
[2] Dashboard
[3] Redeem rewards
[4] Exit
    """)

    choice = input("Select number: ")

    if choice == "1":
        clearConsole()
        getOTP()
    elif choice == "2":
        clearConsole()
        viewPoints()
    elif choice == "3":
        clearConsole()
        redeemRewards()
    elif choice == "4":
        sys.exit("Bye bye! GRewards by @pigscanfly")        
    else:
        print("Something's wrong i can feel it.")        

clearConsole()
createFile("info.json")   
while True:
    main()

   
