import robin_stocks.robinhood as r
import yfinance as yf
import pandas as pd
import csv
import time
import requests

filename = 'data.csv'

email = input("Enter your email: ")
password = input("Enter your password: ")
phone_number = input("Enter your phone_number: ")

last_datetime = pd.Timestamp.now()

while(1):
	#time.sleep()
	while ((pd.Timestamp.now() - pd.DateOffset(seconds=10)) < last_datetime):
		#time.sleep(100)
		print(f'Time since last ran: {pd.Timestamp.now() - last_datetime}\n')
	last_datetime = pd.Timestamp.now()
	print(f'Updating saved time to {last_datetime}\n')
	print('Logging in...\n')
	r.login(email, password)
	print('Login Successful\nRetrieving holdings...\n')
	holdings = r.account.build_holdings()
	print('holdings retrieved successfully.\nLogging out...')
	r.logout()
	print('Logged out successfully.\n')
	yearly_div_expected = 0.00
	equity = 0.00

	for ticker in holdings:
		num_shares = float(holdings[ticker]['quantity'])	#get owned number of stock with given ticker
		dividends = yf.Ticker(ticker).dividends			#get dividend history of ticker from yfinance
		current_date = pd.Timestamp.now(tz=dividends.index.tz)	#get current data in same time format as the divident data
		year_ago = current_date - pd.DateOffset(years=1)	#will see last year of divident payout, so start date is 1 year ago
		ann_dividend = dividends[dividends.index >= year_ago]	#get div data from last year
		ann_dividend = ann_dividend.sum()			#add dividends from last year
		yearly_div_expected += ann_dividend * num_shares	#multiply amount of dividends from last year by number of shares owned and add to total dividends for portfolio.
		equity += float(holdings[ticker]['equity'])
		print (f"{ticker}: ${ann_dividend:.2f} per share: {num_shares:.2f} shares owned. Yearly payout: ${ann_dividend * num_shares:.2f}/{float(holdings[ticker]['equity']):.2f} = {ann_dividend * num_shares * 100.00 / float(holdings[ticker]['equity']):.2f}%\n")
		

	div_percent = 100*yearly_div_expected/equity
	with open(filename, 'a', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow([pd.to_datetime('now').date(), pd.to_datetime('now').time(), yearly_div_expected, div_percent, equity])	
	print(f'${yearly_div_expected:.2f} dividend income /${equity:.2f} = {100* yearly_div_expected/equity:0.2f}%\n')
	resp = requests.post('https://textbelt.com/text', {
		'phone': phone_number,
		'message': f'${yearly_div_expected:.2f} dividend income /${equity:.2f} = {100* yearly_div_expected/equity:0.2f}%',
		'key': 'textbelt',
	})
	print(resp.json())
	print('Not Running\n')

