import os
import argparse
import requests
import yfinance as yf
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_monthly_data(ticker):
    print(f"Scraping monthly data for ticker: {ticker}")
    folder_path = '../data/raw'
    try:
        start_date = int(datetime(2019, 1, 1).timestamp())
        end_date = int(datetime(2024, 4, 1).timestamp())
        url = f'https://finance.yahoo.com/quote/{ticker}/history?period1={start_date}&period2={end_date}&interval=1mo&filter=history&frequency=1mo'
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table')
            if table:
                headers = ['Date', 'Open', 'High', 'Low', 'Close*', 'Adj Close**', 'Volume']
                rows = []
                for row in table.find_all('tr'):
                    cols = row.find_all('td')
                    if len(cols) > 0:
                        rows.append([cell.text.strip() for cell in cols])

                df = pd.DataFrame(rows, columns=headers)
                csv_file_name = f'{ticker}_monthly.csv'
                csv_file_path = os.path.join(folder_path, csv_file_name)
                df.to_csv(csv_file_path, index=False)
                print(f"The file '{csv_file_name}' has been created at {csv_file_path}")
                return df
            else:
                raise ValueError("Table not found on Yahoo Finance page")
        else:
            response.raise_for_status()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def fetch_financial_statements(ticker_symbol):
    # Create a Ticker object
    ticker = yf.Ticker(ticker_symbol)

    # Fetch financial statements
    financial_statements = {
        'annual_income_statement': ticker.financials.T,
        #'quarterly_income_statement': ticker.quarterly_financials.T,
        'annual_balance_sheet': ticker.balance_sheet.T,
        #'quarterly_balance_sheet': ticker.quarterly_balance_sheet.T,
        'annual_cash_flow': ticker.cashflow.T,
        #'quarterly_cash_flow': ticker.quarterly_cashflow.T
    }
    ticker = ticker_symbol
    # Save the data to csv files
    folder_path = '../data/raw'
    os.makedirs(folder_path, exist_ok=True)  # Ensure the directory exists
    annual_income_statement_file_name = f'{ticker}_annual_income_statement.csv'
    annual_balance_sheet_file_name = f'{ticker}_annual_balance_sheet.csv'
    annual_cash_flow_file_name = f'{ticker}_annual_cash_flow.csv'
    annual_income_statement_file_path = os.path.join(folder_path, annual_income_statement_file_name)
    annual_balance_sheet_file_path = os.path.join(folder_path, annual_balance_sheet_file_name)
    annual_cash_flow_file_path = os.path.join(folder_path, annual_cash_flow_file_name)
    
    df_annual_income_statement = pd.DataFrame(financial_statements['annual_income_statement'])
    df_annual_balance_sheet = pd.DataFrame(financial_statements['annual_balance_sheet'])
    df_annual_cash_flow = pd.DataFrame(financial_statements['annual_cash_flow'])
    df_annual_income_statement.to_csv(annual_income_statement_file_path, index=True)
    df_annual_balance_sheet.to_csv(annual_balance_sheet_file_path, index=True)
    df_annual_cash_flow.to_csv(annual_cash_flow_file_path, index=True)
    #df.to_csv(csv_file_path, index=False)
    print(f"The financial files has been created.")
    return financial_statements


def main():
    parser = argparse.ArgumentParser(description='scrape monthly data from Yahoo Finance website')
    parser.add_argument('ticker', type=str, help='ticker of stock')
    args = parser.parse_args()

    # Define the folder to save CSV files
    folder_path = '../data/raw'
    os.makedirs(folder_path, exist_ok=True)  # Ensure the directory exists

    # Scrape monthly data and save to CSV
    scrape_monthly_data(args.ticker)

    # Fetch financial statements and save to CSV
    fetch_financial_statements(args.ticker)
    
if __name__ == "__main__":
    main()