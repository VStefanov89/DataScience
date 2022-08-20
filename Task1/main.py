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

#
# import sqlite3
# from numpy import timedelta64
#
# connection = sqlite3.connect("customers.db")
# cursor = connection.cursor()
#
#
#
# df = pd.read_csv("test_sales.csv")
# df['customer_id'] = df['customer_id'].astype("string")
# df = df[df['customer_id'].notnull()]
# df.customer_id = df.customer_id.replace("-", "", regex = True)
# df['order_number'] = df['order_number'].astype("string")
# df['channel'] = df['channel'].astype("string")
# df["order_datetime"] = pd.to_datetime(df["order_datetime"])
# df = df.sort_values(by="order_datetime")
# df = df.reset_index(drop=True)
# df["quarter"] = df['order_datetime'].dt.to_period('Q')
#
#
# last_quarter = df.quarter.iloc[-1]
# last_quarter_data = df[df.quarter == last_quarter]
# last_quarter_data = last_quarter_data.reset_index(drop=True)
# last_quarter_data = last_quarter_data.drop_duplicates(subset="order_number", keep=False)
#
# new_df = pd.DataFrame()#
# order_number_list = []
# number_of_orders_past_3_months = []
# gross_sum_orders_past_3_months = []
# customer_id_list = []
# temp_ids = []
# for customer_id in last_quarter_data.customer_id:
#     if customer_id in customer_id_list:
#         continue
#     customer_id_list.append(customer_id)
#     customer_table = last_quarter_data[last_quarter_data.customer_id == customer_id]
#     for order_num in customer_table.order_number:
#         temp_ids.append(customer_id_list[-1])
#         order_number_list.append(order_num)
#         number_of_orders_past_3_months.append(len(customer_table.index))
#         gross_sum_orders_past_3_months.append(round(sum(customer_table.gross_value), 2))
#
# new_df["customer_id"] = temp_ids
# new_df["order_numer"] = order_number_list
# new_df["number_of_orders_past_3_months"] = number_of_orders_past_3_months
# new_df["gross_sum_orders_past_3_months"] = gross_sum_orders_past_3_months
#
#
# new_df.to_csv("past3months.csv", index=False)
# new_df = pd.read_csv("past3months.csv")
# new_df.customer_id = new_df.customer_id.astype("string")
# print(new_df)
#
# customer_ids = []
# for customer_num in new_df.customer_id:
#
#     customer_data = df[df.customer_id == str(customer_num)]
#     customer_data.order_datetime = customer_data.order_datetime.astype("string")
#     customer_data.quarter = customer_data.quarter.astype("string")
#     print(customer_data)
#     cursor.execute(f"""DROP TABLE IF EXISTS Customer{customer_num}""")
#     customer_data.to_sql(name=f"Customer{customer_num}", con=connection)
#     print(f"Dataframe {customer_num} is inserted to DB")
#
#
# for customer_id in new_df.customer_id:
#     print(f"Customer{customer_id}")
#     try:
#          query = cursor.execute(f"""SELECT * FROM Customer{customer_id} """)
#     except:
#         continue
#     cols = [column[0] for column in query.description]
#     customer_df = pd.DataFrame.from_records(data = query.fetchall(), columns=cols)
#     print(customer_df)
#     customer_df["order_datetime"] = pd.to_datetime(customer_df["order_datetime"])
#     customer_df["quarter"] = pd.to_datetime(customer_df["quarter"])
#     customer_df["quarter_diff"] = customer_df.quarter.diff()
#     customer_df['quarter_diff'] = customer_df['quarter_diff'].fillna(pd.Timedelta(seconds=0))
#     customer_df.quarter_diff = customer_df.quarter_diff / timedelta64(1, 'D')
#
#     if any(customer_df.quarter_diff > 92):
#         cursor.execute(F"""DROP TABLE IF EXISTS Customer{customer_id}""")
#         print(f"Table name Customer{customer_id} was dropped")
#         connection.commit()
#
#
#
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# temp_tables_names = cursor.fetchall()
# table_names = []
# for table in temp_tables_names:
#     table_names.append(*table)
#
#
# new_df["numer_of_orders_future_3_months"] = "Data has gaps or customer doesn't make order for the last 3 months"
# new_df["gross_sum_orders_future_3_months"] = "Data has gaps or customer doesn't make order for the last 3 months"
#
#
#
#
#
# for table in table_names:
#     query = cursor.execute(f"""SELECT * FROM {table} """)  #
#     cols = [column[0] for column in query.description]
#     customer_df = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
#     print(customer_df)
#     quarters = customer_df.quarter.drop_duplicates()
#     print(quarters)
#
#     if len(quarters) < 4:
#         last_quarter_customer_data = customer_df[customer_df.quarter == str(last_quarter)]
#         future_orders = len(last_quarter_customer_data.index)
#         print(f"furure orders = {future_orders}")
#         future_gross = round(sum(last_quarter_customer_data.gross_value), 2)
#         print(f"future_gross = {future_gross}")
#
#         index_row = new_df.index[new_df['customer_id'] == customer_df.customer_id[0]].tolist()
#
#         new_df.loc[index_row, "numer_of_orders_future_3_months"] = future_orders
#         new_df.loc[index_row, "gross_sum_orders_future_3_months"] = future_gross
#         print(new_df[new_df['customer_id'] == customer_df.customer_id[0]])
#     else:
#         count_of_orders_per_quarter = []
#         count_of_gross_per_quarter = []
#         for quarter in quarters:
#             temp_df = customer_df[customer_df.quarter == str(quarter)]
#             number_of_orders = len(temp_df.index)
#             number_of_gross = round(sum(temp_df.gross_value), 2)
#             count_of_orders_per_quarter.append(number_of_orders)
#             count_of_gross_per_quarter.append(number_of_gross)
#
#         i = 0
#         moving_average_for_orders = []
#         moving_average_for_gross = []
#         window_size = 4
#
#         while i < len(count_of_orders_per_quarter) - window_size + 1:
#             # Calculate the average of current window
#             window_average_orders = round(sum(count_of_orders_per_quarter[
#                                               i:i + window_size]) / window_size, 2)
#
#             window_average_gross = round(sum(count_of_gross_per_quarter[
#                                              i:i + window_size]) / window_size, 2)
#
#             # Store the average of current window in moving average list
#             moving_average_for_orders.append(window_average_orders)
#             moving_average_for_gross.append(window_average_gross)
#             # Shift window to right by one position
#             i += 1
#
#         print(moving_average_for_orders)
#         print(moving_average_for_gross)
#         future_orders = round(moving_average_for_orders[-1])
#         future_gross = moving_average_for_gross[-1]
#
#         index_row = new_df.index[new_df['customer_id'] == customer_df.customer_id[0]].tolist()
#         new_df.loc[index_row, "numer_of_orders_future_3_months"] = future_orders
#         new_df.loc[index_row, "gross_sum_orders_future_3_months"] = future_gross
#         print(new_df[new_df.customer_id == customer_df.customer_id[0]])
#
#
# new_df = new_df.drop(['customer_id'], axis=1)
# new_df.to_csv("past3months.csv", index=False)




