# Sell Sheetcoins Script

This project includes a Python script to automatically sell the farmed sheetcoins at the specified date and time of the listing. This README provides instructions on how to set up and run the script on a Linux Ubuntu server.

## Setup

### 1. Clone the Repository
If you don't already have the code, clone the repository with:

```sh
git clone https://github.com/webcuser/bbot.git
cd bbot

```

### 2. Install Dependencies
Install the required libraries using pip. Make sure you have a Python environment set up (you might consider using a virtual environment to avoid conflicts with other libraries):

```sh
pip install -r requirements.txt
```

### 3. Configure Variables
Edit the config.py file with your credentials and settings. Open config.py and update the following values:

```sh
API_KEY = 'la_tua_api_key'
API_SECRET = 'la_tua_api_secret'
ACCOUNT = 'UNIFIED'  # EX: UNIFIED, SPOT, CONTRACT
SYMBOL = 'DOGSUSDT'  
```
### 4. Schedule the Script Execution
Option 1: Use cron To run the script automatically on September 26 at 12:00 PM, you can add a cron job. Run:

```sh
crontab -e
```
Add the following line to the crontab file to execute the script at the specified date and time:

```sh
0 12 20 9 * /usr/bin/python3 /absolute/path/to/connector.py
```
Make sure to replace /absolute/path/to/connector.py with the actual path to your Python script.

