import json
import requests
import time
import os
from termcolor import colored as c

url = "https://rest.unification.io/"
#url = "http://localhost:1317/"

starttime = time.time()
amount = []

jsonpath = os.environ.get('JSON_PATH')

if jsonpath is None:
    jsonpath = "./apr.json"
elif jsonpath[-1] == "/":
    jsonpath = f"{jsonpath}/apr.json"



# timeframe(seconds) times store is equal to the length
# of time(in seconds) the script will retain information for 
# the average calculation. 

# 86,400 seconds in a day(24hrs) 
# I.E. 6(timeframe) x 14400(store) = 86,400

timeframe = 6
store = 14400
community_tax = 0.02

def start():
    while True:
        res = requests.get(f'{url}/mainchain/enterprise/v1/supply/nund').json()
        if len(amount) == store:
            del amount[0]
        amount.append(float(res['amount']['amount'])) 
        main()
        time.sleep(timeframe)

def main():
    diff = 0
    for i, a in enumerate(amount):
        try:
            diff += amount[i+1] - a
        except IndexError:
            break
    if len(amount) > 1:
        res = requests.get(f'{url}/cosmos/staking/v1beta1/pool',timeout=30).json()
        staked_supply = float(res['pool']['bonded_tokens'])
        current_amount = amount[len(amount)-1]

        average_diff = diff/len(amount)
        inflation = (average_diff*(31536000/timeframe)) #31536000 seconds in a year
        inflation_percentage = inflation/current_amount
        apr = (inflation_percentage/(staked_supply/current_amount))
        apr = apr-(community_tax*apr)

        print(c(f'Store number {len(amount)} every {timeframe} seconds','blue'))
        print(c(f'Calculation based on the last {round((timeframe*len(amount))/60/60,2)} hours','green'))
        print(c('Current Supply: ', 'magenta'),c(f'{round(current_amount/1000000000,3):,} FUND','cyan'))
        print(c('Calculated yearly inflation: ','magenta'),c(f'{round(inflation/1000000000,3):,} FUND','cyan'))
        print(c('Calculated inflation percentage: ','magenta'),c(f'{round(inflation_percentage*100,3)}%','cyan'))
        print(c('Calculated APR percentage: ','magenta'),c(f'{round(apr*100,3)}%\n','cyan'))

        info = {
                "timeframe_hours" : round((timeframe*len(amount))/60/60,2),
                "current_supply" : round(current_amount/1000000000,3),
                "inflation_yearly_amount" : round(inflation/1000000000,3),
                "inflation_yearly_percentage" : round(inflation_percentage*100,3),
                "apr_percentage" : round(apr*100,3)
        }
        with open(jsonpath, 'w',encoding='utf8') as u:
            json.dump(info,u,indent=4,ensure_ascii=False)

start()
