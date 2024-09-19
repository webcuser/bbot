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
API_KEY = '' #bybit API_KEY
API_SECRET = '' #bybit API_SECRET
ACCOUNT = 'UNIFIED' # only unyfied
SYMBOL = "DOGSUSDT" #add pire like DOGSUSDT or CATSUSDT for spot trade
LISTING_DATE = ""  # everytime like "19/09/2024 14:39" format
```
### 4. Run Script
Run script and wait listing. Run:

```sh
python3 connector.py
```


