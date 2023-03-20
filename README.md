# Apr/Inflation Calculator

This is a pretty simple python script used to query the estimated Inflation
and staking APR(without comissions included) for the Unification Mainchain.

Due to the way inflation works with Unification, being variable depending on
eFUND usage, this script is just an estimation.

## Notes
The script becomes more accurate with time, since the inflation calculation 
is based on the average difference in supply over a period of time. 

With the way the script is set up, best results come from running the script
for atleast 24 hours. 

Current community tax is already deducted from results, but not comissions.

Preferably used with a local node with API enabled, and changing the `url` variable
to reflect this.

Any outliers in eFUND usage may throw off the calculation(Such as a new BEACON being registered)

## Usage
To use, simply install the needed requirements using:
```bash
pip install -r /path/to/requirements.txt
```
and run using
```bash
python /path/to/main.py
```


