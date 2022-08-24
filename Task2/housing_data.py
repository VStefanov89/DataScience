import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

"""
First we need to check the data and get familiar with it. I will compare the sale prices with several columns to 
check is there any interesting in these charts, I will do check for prices with LotArea, which is the size in square feet,
prices with overall quality and with which year is sold the house. 
"""

pd.set_option('display.expand_frame_repr', False)


def plotting(column):
    housing_data = pd.read_csv("housing_price_data.csv")
    print(housing_data)
    housing_data = housing_data[housing_data[column].notna()]

    plt.plot(housing_data[column], housing_data.SalePrice, ".")
    plt.title(f"{column} vs Prices")
    plt.savefig(f"Plot of {column} vs Prices")
    return plt.show()
"""
Clearly we can see that there are some dependencies in these charts. Bigger home --> Bigger price, More quality of
the home --> Bigger price, also we see that all homes are sold between 2006-2010, which is good, because the timeframe
is not so big and sales price should depend more on the LotArea of the home. So for that reason i will
make a multiple regression using all of these three columns as a independent variables. 
"""

print(plotting("LotArea"))
print(plotting("OverallQual"))
print(plotting("YrSold"))

