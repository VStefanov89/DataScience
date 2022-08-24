import pandas as pd
from test_sales import store_main_df
from past_three_months import get_last_quarter_data, create_new_df
from check_for_gaps import check_gaps_in_database_tables
from export_new_data import get_tables_name, export_new_data



pd.set_option('display.expand_frame_repr', False)

df = store_main_df("test_sales.csv")
print(df)
last_quarter_data = get_last_quarter_data(df)
print(last_quarter_data)
last_quarter = last_quarter_data.quarter.iloc[0]

new_df = create_new_df(last_quarter_data, main_df=df)
print(new_df)
check_gaps_in_database_tables(new_df)
tables_name = get_tables_name()

new_df["numer_of_orders_future_3_months"] = "Data has gaps or customer doesn't make order for the last 3 months"
new_df["gross_sum_orders_future_3_months"] = "Data has gaps or customer doesn't make order for the last 3 months"

new_df = export_new_data(new_df, last_quarter=last_quarter, tables_names=tables_name)
new_df = new_df.drop(['customer_id'], axis=1)
print(new_df)
new_df.to_csv("past3months.csv", index=False)
