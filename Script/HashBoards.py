# Modules
import socket
import json
import sys
import pandas as pd
import xlsxwriter
from openpyxl import load_workbook
from colorama import Fore, Back, Style
from termcolor import colored
import pprint


class CgminerAPI(object):
    def __init__(self, host='localhost', port=4028):
        self.data = {}
        self.host = host
        self.port = port

    def command(self, command, arg=None):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(.5)

        try:
            sock.connect((self.host, self.port))
            payload = {"command": command}
            if arg is not None:
                # Parameter must be converted to basestring (no int)
                payload.update({'parameter': arg})

            if sys.version_info.major == 2:
                sock.send(json.dumps(payload))
            if sys.version_info.major == 3:
                sock.send(bytes(json.dumps(payload), 'utf-8'))
            received = self._receive(sock)
        except Exception as e:
            ({'STATUS': [{'STATUS': 'error', 'description': "{}".format(e)}]})
        else:
            try:
                return json.loads(received[:-1])
            except Exception as e:
                return json({'STATUS': [{'STATUS': 'error', 'description': "{}".format(e)}]})
        finally:
            sock.close()

    def _receive(self, sock, size=4096):
        msg = ''
        while 1:
            chunk = sock.recv(size)
            if chunk:
                if sys.version_info.major == 2:
                    msg += chunk
                if sys.version_info.major == 3:
                    msg += chunk.decode('utf-8')
            else:
                break
        return msg

    def __getattr__(self, attr):

        def out(arg=None):
            return self.command(attr, arg)

        return out


if __name__ == '__main__':
    # Opens the file to be read.
    df = pd.read_excel(
        #     Put the path to file here
        r'C:\Users\cmill\Desktop\New_CGMINER\Lists\0Test.xlsx')

    # Goes through the list of IPs in the "IP" column one at a time
    IP = df["IP"].tolist()
   

    print("Total Miners: ", len(IP))

    for i in IP:
        try:

            # Gets miner info from CGMINER

            Miner = CgminerAPI(host=i)
            data = Miner.stats()

            # Gets Miner Type
            MinerType = str(data['STATS'][0]["Type"])

            # Gets Each ASIC Number Per Board
            asic0 = (data['STATS'][1]["chain_acn1"])
            asic1 = (data['STATS'][1]["chain_acn2"])
            asic2 = (data['STATS'][1]["chain_acn3"])

            # Gets Hashrate
            hashRate = str(data['STATS'][1]['GHS 5s'])

            # Gets Ideal Hashrate
            idealHR = str(data['STATS'][1]['total_rateideal'])

            # Gets Each Boards Hashrate
            chain0HR = (data['STATS'][1]['chain_hw1'])
            chain1HR = (data['STATS'][1]['chain_hw2'])
            chain2HR = (data['STATS'][1]['chain_hw3'])
            chain3HR = (data['STATS'][1]['chain_hw4'])

            # Gets Each Fan Speed
            #fanCount = str(data['STATS'][1]["fan_num"])
            fan1 = str(data['STATS'][1]["fan1"])
            fan2 = str(data['STATS'][1]["fan2"])
            fan3 = str(data['STATS'][1]["fan3"])
            fan4 = str(data['STATS'][1]["fan4"])

            # Prints the IP and Miner Type
            print(print(colored('Miner IP: ' + i,  attrs=['bold'])))
            print("Miner Model Is: " + MinerType)

            # Determines how many ASIC are on each board
            if MinerType == "Antminer S19":
                targetAsic = 76
            elif MinerType == "Antminer S19 Pro":
                targetAsic = 114
            elif MinerType == "Antminer T17":
                targetAsic = 30
            elif MinerType == "Antminer S17":
                targetAsic = 48
            elif MinerType == "Antminer S17 Pro":
                targetAsic = 48
            elif MinerType == "Antminer S17+":
                targetAsic = 65
            elif MinerType == "Antminer T17+":
                targetAsic = 44
            elif MinerType == "Antminer S19+":
                targetAsic = 80
            elif MinerType == "Antminer S19j Pro":
                targetAsic = 126
            elif MinerType == "Antminer L7":
                targetAsic = 120
            elif MinerType == "Antminer L5":
                targetAsic = 120

            # Checks to see if hashboards have all chips
            # if asic0 < targetAsic:
             #   print('Replace Chain 0')
            # if asic1 < targetAsic:
             #  print('Replace Chain 1')
            # if asic2 < targetAsic:
             #   print('Replace Chain 2')

            # Checks to see if a Fan is missing

            # Prints Each Chains ASIC
            print('Chain 0 has: ', asic0, ' ASIC')
            print('Chain 1 has: ', asic1, ' ASIC')
            print('Chain 2 has: ',  asic2, ' ASIC')

            # Prints other info as needed // UNCOMMENT TO SEE RESULTS

            # Fan Speeds

            #print('Fan 1 speed is: ' + fan1)
            #print('Fan 2 speed is: ' + fan2)
            #print('Fan 3 speed is: ' + fan3)
            #print('Fan 4 speed is: ' + fan4)

            # Prints 5 Second Hash Rate
            #print('5 Second Hashrate is: ', hashRate)

            # Prints Ideal Hash Rate
            #print('Ideal Hash Rate is: ' + idealHR)

            # Prints Each Hash Boards Hash Rate
            #print('Chain 0 Hash Rate is: ' + chain0HR)
            #print('Chain 1 Hash Rate is: ' + chain1HR)
            #print('Chain 2 Hash Rate is: ' + chain2HR)

        except:
            print("Failed to get data from " + i)
