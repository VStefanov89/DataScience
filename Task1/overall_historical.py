import pandas as pd
from test_sales import store_main_df
import matplotlib.pyplot as plt


pd.set_option('display.expand_frame_repr', False)

df = store_main_df("test_sales.csv")
print(df)

df.quarter = df.quarter.astype("string")
quarters = df.quarter
quarters = quarters.drop_duplicates()
quarters = quarters.tolist()


over_all_orders = []
for quarter in quarters:
    quarter_data = df[df.quarter == quarter]
    number_of_orders = len(quarter_data.index)
    over_all_orders.append(number_of_orders)

print(quarters)
print(over_all_orders)

plt.title("Overall historical orders")
plt.plot(quarters, over_all_orders, ".-")
plt.show()

# It is clearly from the graph that the business is not going very well. Orders per quarter are consistently declining.
# We noticed that as well, when we were looking for customers who are making orders every quarter. We noticed that,
# most of the customers are stopping making orders each quarter, when we filtered out dataset ( a lot of the customers
# has been gone). So when we see the graph me can assume that the business is in downtrend and maybe the company has
# some problems


