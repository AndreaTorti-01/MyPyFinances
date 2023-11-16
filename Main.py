# import the libraries needed to get finance data from yahoo and plot the data
import yfinance as yf
import matplotlib.pyplot as plt
from typing import List, Tuple

# define stocks as a list of tuples containing the stock ticker and the quantity of shares owned
stocks: List[Tuple[yf.Ticker, int]] = []

# try to load the stocks from a file called stocks.txt
try:
    with open("stocks.txt", "r") as f:
        # check if the file begins with "percentage"
        if f.readline().strip() == "percentage":
            # if it does, read the percentage of the portfolio each stock makes up
            total_percentage = 0
            for line in f:
                try:
                    stock_ticker, percentage = line.split()
                    total_percentage += int(percentage)
                    if total_percentage > 100:
                        raise ValueError("Total percentage exceeds 100")
                    stock = yf.Ticker(stock_ticker)
                    # determine quantity of shares owned based on percentage of portfolio
                    quantity = int(percentage) / 100 * 10000 / stock.history(period="5d", interval="1d")["Close"].iloc[0]
                    stocks.append((stock, int(quantity)))
                except ValueError as e:
                    print(e)
                    exit()
                except:
                    print("Invalid stock ticker or percentage of portfolio")
                    exit()
        for line in f:
            try:
                stock_ticker, quantity = line.split()
                stock = yf.Ticker(stock_ticker)
                stocks.append((stock, int(quantity)))
            except:
                print("Invalid stock ticker or quantity of shares")
                exit()
                
except FileNotFoundError:
    while True:
        try:
            stock_ticker = input(
                "Enter the stock ticker you want to look at (q to stop): "
            )
            if stock_ticker == "q":
                break

            # check if the stock ticker is valid
            stock: yf.Ticker = yf.Ticker(stock_ticker)

            try:
                stock_info = yf.Ticker(stock_ticker)
                _ = stock_info.info
            except:
                print("Invalid stock ticker")
                continue

            quantity = int(input("Enter the quantity of shares you own: "))

            stocks.append((stock_info, quantity))

        except ValueError:
            print("Please enter a valid stock ticker and quantity of shares")

# get the closing prices for each stock over the last 6 months
closings: List = []
for stock_ticker, _ in stocks:
    closings.append(stock_ticker.history(period="6mo")["Close"])

# calculate the sum of the closing prices for each day multiplied by the quantity of shares owned
capital: List[float] = []
for i in range(len(closings[0])):
    total = 0
    for j in range(len(closings)):
        total += closings[j].iloc[i] * stocks[j][1]
    capital.append(total)

# add the 7 day moving average of the capital to the plot
moving_average: List[float] = []
for i in range(len(capital)):
    if i < 7:
        moving_average.append(capital[i])
    else:
        moving_average.append(sum(capital[i - 7 : i]) / 7)
        
# plot the capital and smoothed moving average over time
plt.plot(closings[0].index, capital, label="Capital", linewidth=0.5)
plt.plot(closings[0].index, moving_average, label="7 Day Moving Average")

# add vertical lines where months start
for i in range(1, len(closings[0].index)):
    if closings[0].index[i].month != closings[0].index[i - 1].month:
        plt.axvline(x=closings[0].index[i], color="grey")

# show the plot
plt.title("MyPyFinances")

plt.legend()
plt.show()
