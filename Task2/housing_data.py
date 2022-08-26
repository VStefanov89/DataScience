import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


#First we need to check the data and get familiar with it. I will compare the sale prices with several columns to
#check is there anything interesting in these charts, I will do checking on prices with LotArea, which is the size in square feet,
#and with overall quality.


pd.set_option('display.expand_frame_repr', False)


def plotting(column):
    housing_data = pd.read_csv("housing_price_data.csv")
    print(housing_data)
    housing_data = housing_data[housing_data[column].notna()]

    plt.plot(housing_data[column], housing_data.SalePrice, ".")
    plt.title(f"{column} vs Prices")
    plt.savefig(f"Plot of {column} vs Prices")
    return plt.show()


print(plotting("LotArea"))
print(plotting("OverallQual"))


#From the plots that are generate, clearly we can see that there are some dependencies in these charts.
#Bigger home --> Bigger price, More quality of the home --> Bigger price.
#So for that reason i will make a multiple regression using all of these columns as
#an independent variables.

