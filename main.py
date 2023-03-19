import os
import json
import requests
import time

url = "https://rest.unification.io/"
#url = "http://localhost:1317/"

starttime = time.time()
timeframe = 6
store = 100000

amount = []
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
#             print(f"""
# Amount: {round(a/1000000000,3):,} FUND
# Diff: {round((amount[i+1]-a)/1000000000,3):,} FUND
# Diff Total: {round(diff/1000000000,3):,} FUND
#
#                   """)
        except IndexError:
            break
    # if len(amount) == store:
    if len(amount) > 1:
        res = requests.get(f'{url}/cosmos/staking/v1beta1/pool',timeout=30).json()
        staked_supply = float(res['pool']['bonded_tokens'])
        average = diff/len(amount)
        inflation = (average*(31536000 / timeframe))
        inflation_percentage = inflation/amount[len(amount)-1]
        apr = inflation_percentage/((staked_supply/1000000000)/(amount[len(amount)-1]/1000000000))
        print(f'Store number {len(amount)} every {timeframe} seconds')
        print(f'Calculated yearly inflation {round(inflation/1000000000,3):,} FUND')
        print(f'Calculated inflation percentage {round(inflation_percentage*100,3)}%')
        print(f'Calculated APR percentage {round(apr*100,3)}%\n')
start()
