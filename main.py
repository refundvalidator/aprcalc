import os
import json
import requests
import time

url = "https://rest.unification.io/"
#url = "http://localhost:1317/"

starttime = time.time()
amount = []

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
        current_amount = amount[len(amount)-1]
        staked_supply = float(res['pool']['bonded_tokens'])
        average_diff = diff/len(amount)
        inflation = (average_diff*(31536000/timeframe)) #31536000 seconds in a day
        inflation_percentage = inflation/amount[len(amount)-1]
        apr = (inflation_percentage/(staked_supply/current_amount))
        apr = apr-(community_tax*apr)

        print(f'Store number {len(amount)} every {timeframe} seconds')
        print(f'Current Supply: {round(current_amount/1000000000,3):,} FUND')
        print(f'Calculated yearly inflation: {round(inflation/1000000000,3):,} FUND')
        print(f'Calculated inflation percentage: {round(inflation_percentage*100,3)}%')
        print(f'Calculated APR percentage: {round(apr*100,3)}%\n')
start()
