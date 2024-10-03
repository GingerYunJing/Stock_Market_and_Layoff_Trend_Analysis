import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from math import sqrt

def plot_correlation_heatmap(stock_data):
    df = pd.read_csv(stock_data)

    # Compute correlation matrix
    df.drop('Date', axis=1, inplace=True)
    correlation_matrix = df.corr()

    # Create a heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title(f'Correlation Heatmap for {os.path.basename(stock_data)}')

    output_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'visualizations')
    os.makedirs(output_folder, exist_ok=True)
    output_file_path = os.path.join(output_folder, f'Correlation Heatmap for {os.path.basename(stock_data)}.png')
    plt.savefig(output_file_path)

    plt.show()

def plot_machine_learning_results(stock_data):
    df = pd.read_csv(stock_data)
    data = df.drop(['Date', 'Close*', 'Adj Close**'], axis=1)
    training_x, testing_x , training_y, testing_y = train_test_split(
        data, df['Adj Close**'], test_size=0.20,shuffle = False
    )
    print("This is the head of the training features: \n", training_x.head())
    print("This is the head of the testing features: \n",testing_x.head())
    model = LinearRegression()
    model.fit(training_x, training_y)
    predictions = model.predict(testing_x)
    rmse = sqrt(mean_squared_error(testing_y, predictions))
    mae = mean_absolute_error(testing_y, predictions)
    r_squared = r2_score(testing_y, predictions)
    RMSE = []
    MAE = []
    R_SQUARED = []
    RMSE.append(rmse)
    MAE.append(mae)
    R_SQUARED.append(r_squared)
    print(f"Test RMSE for {os.path.basename(stock_data)}: {rmse}")
    print(f"Test MAE for {os.path.basename(stock_data)}: {mae}")
    print(f"Test R-SQUARED for {os.path.basename(stock_data)}: {r_squared}")

    plt.figure(figsize=(12,7))
    plt.plot(testing_y.index, testing_y, label='Actual Prices')
    plt.plot(testing_y.index, predictions, label='Predicted Prices')
    plt.title(f'Predicted VS Actual Prices for {os.path.basename(stock_data)}')
    plt.legend()

    output_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'visualizations')
    os.makedirs(output_folder, exist_ok=True)
    output_file_path = os.path.join(output_folder, f'Predicted VS Actual Prices for {os.path.basename(stock_data)}.png')
    plt.savefig(output_file_path)

    plt.show()

def plot_layoff(stock_data, layoff_data):
    stock = pd.read_csv(stock_data)
    layoff = pd.read_csv(layoff_data)

    # Convert 'Date' to datetime in both dataframes
    stock['Date'] = pd.to_datetime(stock['Date'])
    layoff['Date'] = pd.to_datetime(layoff['Date'])

    # Drop unnecessary columns from the stock data
    stock = stock.drop(['Open', 'High', 'Low', 'Close*', 'Volume'], axis=1)

    # Initialize the plot
    fig, ax1 = plt.subplots(figsize=(12,7))

    # Plot the layoff data as a bar chart on the first axis
    bars = ax1.bar(layoff['Date'], layoff['Laid Off'], label='Layoff', color='red', width=15)
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Layoff Count', color='red')
    ax1.tick_params(axis='y', labelcolor='red')
    ax1.set_title(f'Impact of layoff on stock performance of {os.path.basename(stock_data)}')
    ax1.xaxis_date()  # Ensure the x-axis is treated as dates

    # Annotate the top of each bar with its value
    for bar in bars:
        height = bar.get_height()
        ax1.annotate('{}'.format(height),
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 3),  # 3 points vertical offset
                     textcoords="offset points",
                     ha='center', va='bottom')

    # Create the second axis for the stock data
    ax2 = ax1.twinx()

    # Plot the stock data as a line chart on the second axis
    ax2.plot(stock['Date'], stock['Adj Close**'], label='Actual Prices', color='blue', linestyle='-', marker='o')
    ax2.set_ylabel('Adjusted Close Price', color='blue')
    ax2.tick_params(axis='y', labelcolor='blue')

    # Set up the legend to show both labels
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc='upper left')

    # Adjust the layout to prevent overlap
    plt.tight_layout()

    # Here we assume that __file__ is defined. In Jupyter or interactive environments, you might not have this variable.
    # In such cases, you need to provide the path directly or use another way to specify the output folder.
    output_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'visualizations')
    os.makedirs(output_folder, exist_ok=True)
    output_file_path = os.path.join(output_folder, f'Impact of layoff on stock performance of {os.path.basename(stock_data)}.png')
    plt.savefig(output_file_path)

    # Show the plot
    plt.show()
    

def main():
    parser = argparse.ArgumentParser(description='output correlation heatmap for stock data and machine learning results')
    parser.add_argument('stock_data', help='file path to stock data')
    parser.add_argument('layoff_data', help='file path to layoff data')

    args = parser.parse_args()
    plot_correlation_heatmap(args.stock_data)
    plot_machine_learning_results(args.stock_data)
    plot_layoff(args.stock_data, args.layoff_data)


if __name__ == "__main__":
    main()