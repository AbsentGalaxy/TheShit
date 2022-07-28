import requests
import pprint
from requests.auth import HTTPDigestAuth
from openpyxl import load_workbook
import pandas as pd
import xlsxwriter
import time

# Opens the file to be read.
df = pd.read_excel(
    #     Put the path to file here
    r'C:\Users\cmill\Desktop\New_Cgminer\Lists\0Test.xlsx')
IP = df["IP"].tolist()
#IP = "10.1.1.1"
#print("Total Miners: ", len(IP))
for i in IP:
        try:
                url = f'http://{i}/cgi-bin/log.cgi'
                response = requests.post(url, auth=HTTPDigestAuth('root', '8Mh*LsL3*P'))
        #print(i)
                KernalLog = (str(response.content))
                #print(KernalLog) 
                if "TEMP_TOO_HIGH" in KernalLog:
                        print(i + ": TEMP TOO HIGH")
                elif "POWER_LOST" in KernalLog:
                        print(i + ": Power Lost")
                if "fan_id = 0, fan_speed = 0" in KernalLog:
                        print(i + ": Fan 1 Bad")
                if "fan_id = 1, fan_speed = 0" in KernalLog:
                        print(i + ": Fan 2 Bad")
                if "fan_id = 2, fan_speed = 0" in KernalLog:
                        print(i + ": Fan 3 Bad")
                if "fan_id = 3, fan_speed = 0" in KernalLog:
                        print(i + ": Fan 4 Bad")
        
        except (requests.exceptions.ConnectionError):
                print("Failed to get data from " + i)
                pass
       
        
