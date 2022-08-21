import pandas as pd
from test_sales import store_main_df
import matplotlib.pyplot as plt


pd.set_option('display.expand_frame_repr', False)

df = store_main_df("test_sales.csv")

df.quarter = df.quarter.astype("string")
df.channel = df.channel.astype("string")

quarters = df.quarter
quarters = quarters.drop_duplicates()
quarters = quarters.tolist()

channels = df.channel
channels = channels.drop_duplicates()
channels = channels.tolist()


def get_info_by_channel(channel_type):

    channel_data = df[df.channel == channel_type]
    print(channel_data)

    over_all_orders = []
    for quarter in quarters:
        quarter_data = channel_data[channel_data.quarter == quarter]
        number_of_orders = len(quarter_data.index)
        over_all_orders.append(number_of_orders)

    print(over_all_orders)
    plt.title("Overall historical orders")
    plt.plot(quarters, over_all_orders, ".-")
    return plt.show()


print(get_info_by_channel("R"))


# As we can see most of the orders are made from channel E, but again nothing significant. Orders are declining and
# business is struggling

