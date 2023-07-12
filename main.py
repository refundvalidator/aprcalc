import json
import requests
import time
import os


class APR:
    def __init__(self,url="http://localhost:1317",timeframe=6,store=14400,community_tax=0.02,debug=False):
        self.url = url
        self.timeframe = timeframe
        self.store = store
        self.community_tax = community_tax
        self.amount = []
        self.data = {}
        self.debug = debug

# timeframe(seconds) times store is equal to the length
# of time(in seconds) the script will retain information for 
# the average calculation. 

# 86,400 seconds in a day(24hrs) 
# I.E. 6(timeframe) x 14400(store) = 86,400

    def start(self):
        while True:
            res = requests.get(f'{self.url}/mainchain/enterprise/v1/supply/nund').json()
            if len(self.amount) == self.store:
                del self.amount[0]
            self.amount.append(float(res['amount']['amount'])) 
            self.main()
            time.sleep(self.timeframe)

    def main(self):
        diff = 0
        for i, a in enumerate(self.amount):
            try:
                diff += self.amount[i+1] - a
            except IndexError:
                break
        if len(self.amount) > 1:
            res = requests.get(f'{self.url}/cosmos/staking/v1beta1/pool',timeout=30).json()
            staked_supply = float(res['pool']['bonded_tokens'])
            current_amount = self.amount[len(self.amount)-1]

            average_diff = diff/len(self.amount)
            inflation = (average_diff*(31536000/self.timeframe)) #31536000 seconds in a year
            inflation_percentage = inflation/current_amount
            apr = (inflation_percentage/(staked_supply/current_amount))
            apr = apr-(self.community_tax*apr)

            self.data = {
                    "timeframe_hours" : round((self.timeframe*len(self.amount))/60/60,2),
                    "current_supply" : round(current_amount/1000000000,3),
                    "inflation_yearly_amount" : round(inflation/1000000000,3),
                    "inflation_yearly_percentage" : round(inflation_percentage*100,3),
                    "apr_percentage" : round(apr*100,3)
            }
            t = time.localtime()
            print(f"{[time.strftime('%H:%M:%S', t)]} APR Updated")
            if self.debug:
                print(json.dumps(self.data,indent=4))
if __name__ == "__main__":
    APR().start() 

