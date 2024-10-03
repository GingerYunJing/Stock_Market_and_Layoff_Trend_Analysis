import argparse
import pandas as pd
import os

def clean_stock_data(stock_data):

    df = pd.read_csv(stock_data)

    # Convert the date column to datetime
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Convert price columns to numeric, coerce errors to NaN so they can be handled later
    price_columns = ['Open', 'High', 'Low', 'Close*', 'Adj Close**', 'Volume']
    for col in price_columns:
        # Ensure the column is in string format for replacement
        df[col] = df[col].astype(str)
        # Remove any commas which can interfere with conversion to numeric type
        df[col] = df[col].str.replace(',', '')
        # Convert to numeric, setting errors='coerce' will turn unconvertible data into NaN
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Remove any rows that have NaN values after this conversion
    df.dropna(inplace=True)

    # Sort the DataFrame based on Date to ensure it's in chronological order
    df.sort_values('Date', inplace=True)

    # Reset index after sorting
    df.reset_index(drop=True, inplace=True)
    # df.set_index('Date', inplace=True)

    # Remove any rows where the market was not open
    df = df[df['Volume'] != 0]

    folder_path = '../data/processed'
    csv_file_name = f'clean_{os.path.basename(stock_data)}'
    csv_file_path = os.path.join(folder_path, csv_file_name)
    # Check if the file already exists
    if os.path.isfile(csv_file_path):
        print(f"The file '{csv_file_name}' already exists.")
    else:
        df.to_csv(csv_file_path, index=False)
        print(f"The file '{csv_file_name}' has been created.")
    return df

def clean_financial_data(financial_data):

    df = pd.read_csv(financial_data, index_col=0)
    df.fillna(0, inplace=True)

    folder_path = '../data/processed'
    csv_file_name = f'clean_{os.path.basename(financial_data)}'
    csv_file_path = os.path.join(folder_path, csv_file_name)
    # Check if the file already exists
    if os.path.isfile(csv_file_path):
        print(f"The file '{csv_file_name}' already exists.")
    else:
        df.to_csv(csv_file_path, index=False)
        print(f"The file '{csv_file_name}' has been created.")
    return df


def main():
    parser = argparse.ArgumentParser(description='clean stock prices data and financial data')

    parser.add_argument('--stock_data', help='file path to stock data')
    parser.add_argument('--financial_data', help='file path to financial data')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Determine which function to execute based on the provided arguments
    if args.stock_data is not None:
        clean_data = clean_stock_data(args.stock_data)
        print("This is the first 5 rows of the clean data:\n", clean_data[:5])
    elif args.financial_data is not None:
        clean_data = clean_financial_data(args.financial_data)
        print("This is the first 5 rows of the clean data:\n", clean_data[:5])
    else:
        print("No valid inputs provided. Specify inputs for stock data or financial data.")

if __name__ == "__main__":
    main()
