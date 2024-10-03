import get_data, clean_data, run_analysis, visualize_results

def main():
    company_ticker = ['META', 'AMZN', 'AAPL', 'NFLX', 'GOOGL']
    try:
        for ticker in company_ticker:
            monthly_data = get_data.scrape_monthly_data(ticker)
            financial_data = get_data.fetch_financial_statements(ticker)
            print("This is the first 5 rows of data we scraped:\n", monthly_data[:5])
            print(f"This is the annual income statement data of {ticker}\n", financial_data['annual_income_statement'])

            clean_stock_data = clean_data.clean_stock_data(f'../data/raw/{ticker}_monthly.csv')
            clean_annual_income_statement = clean_data.clean_financial_data(f'../data/raw/{ticker}_annual_income_statement.csv')
            clean_annual_balance_sheet = clean_data.clean_financial_data(f'../data/raw/{ticker}_annual_balance_sheet.csv')
            clean_annual_cash_flow = clean_data.clean_financial_data(f'../data/raw/{ticker}_annual_cash_flow.csv')
            print("This is the first 5 rows of the clean stock data:\n", clean_stock_data[:5])
            print("This is the first 5 rows of the clean annual income statement data:\n", clean_annual_income_statement[:5])

            company_annual_income_statement_metrics = run_analysis.calculate_financial_metrics(f'../data/processed/clean_{ticker}_annual_income_statement.csv')
            company_annual_balance_sheet_metrics = run_analysis.calculate_financial_metrics(f'../data/processed/clean_{ticker}_annual_balance_sheet.csv')
            company_annual_cash_flow_metrics = run_analysis.calculate_financial_metrics(f'../data/processed/clean_{ticker}_annual_cash_flow.csv')
            print("This is a snippet of the statistical analysis\n", company_annual_income_statement_metrics.head())

            visualize_results.plot_correlation_heatmap(f'../data/processed/clean_{ticker}_monthly.csv')
            visualize_results.plot_machine_learning_results(f'../data/processed/clean_{ticker}_monthly.csv')
            visualize_results.plot_layoff(f'../data/processed/clean_{ticker}_monthly.csv', f'../data/processed/{ticker.lower()}_laidoff.csv')
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
if __name__ == '__main__':
    main()