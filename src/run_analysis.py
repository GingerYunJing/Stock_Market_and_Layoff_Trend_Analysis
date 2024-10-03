import argparse
import pandas as pd
import os

def calculate_financial_metrics(company_financial_data):
    df = pd.read_csv(company_financial_data)

    descriptive_stats = df.describe().drop('count')

    output_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'analysis')
    os.makedirs(output_folder, exist_ok=True)
    output_file_name = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(company_financial_data))[0]}_descriptive_stats.csv")

    if os.path.isfile(output_file_name):
        print(f"The file '{output_file_name}' already exists.")
    else:
        descriptive_stats.to_csv(output_file_name, index=True)
        print(f"The file '{output_file_name}' has been created.")

    return descriptive_stats

def main():
    parser = argparse.ArgumentParser(description='run analysis on financial data')
    parser.add_argument('company_financial_data', help='file path to company financial data')

    args = parser.parse_args()
    company_financial_data_metrics = calculate_financial_metrics(args.company_financial_data)
    print("This is a snippet of the statistical analysis\n", company_financial_data_metrics.head())


if __name__ == "__main__":
    main()