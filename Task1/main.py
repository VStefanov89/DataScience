import pandas as pd
from datetime import datetime
from numpy import timedelta64
import matplotlib.pyplot as plt
import sqlite3

#When i check the data i have observed that the data is old and there are no records for the past 3 months, which is
#from from Juno - August 2022, for that reason i will say that the current date is not the real current date, but
#let's say that current date is in the last quarter. In that case we will have records and could make some analysis on them.
# So i will take all records which are in the last quarter start from there.
#When we find records with last quarter info, from them i will take the customer_id and work with them. There is no
#reason to do analysis on records which are to old and on their data there is not info from the past three months.
# It is not possible to make forecast on something that doesn't exists on first plase. So i will take only records that
# have data from the last 3 months and make forecast fpr the next 3 months.

connection = sqlite3.connect("customers.db")
cursor = connection.cursor()
pd.set_option('display.expand_frame_repr', False)

df = pd.read_csv("test_sales.csv")
df['customer_id'] = df['customer_id'].astype("string")
df = df[df['customer_id'].notnull()]
df.customer_id = df.customer_id.replace("-", "", regex = True)
df['order_number'] = df['order_number'].astype("string")
df['channel'] = df['channel'].astype("string")
df["order_datetime"] = pd.to_datetime(df["order_datetime"])
df = df.sort_values(by="order_datetime")
df = df.reset_index(drop=True)
df["quarter"] = df['order_datetime'].dt.to_period('Q')
print(df)

last_quarter = df.quarter.iloc[-1]
last_quarter_data = df[df.quarter == last_quarter]
last_quarter_data = last_quarter_data.reset_index(drop=True)
last_quarter_data = last_quarter_data.drop_duplicates(subset="order_number", keep=False)

new_df = pd.DataFrame()#
order_number_list = []
number_of_orders_past_3_months = []
gross_sum_orders_past_3_months = []
customer_id_list = []
temp_ids = []
for customer_id in last_quarter_data.customer_id:
    if customer_id in customer_id_list:
        continue
    customer_id_list.append(customer_id)
    customer_table = last_quarter_data[last_quarter_data.customer_id == customer_id]
    for order_num in customer_table.order_number:
        temp_ids.append(customer_id_list[-1])
        order_number_list.append(order_num)
        number_of_orders_past_3_months.append(len(customer_table.index))
        gross_sum_orders_past_3_months.append(round(sum(customer_table.gross_value), 2))

new_df["customer_id"] = temp_ids
new_df["order_numer"] = order_number_list
new_df["number_of_orders_past_3_months"] = number_of_orders_past_3_months
new_df["gross_sum_orders_past_3_months"] = gross_sum_orders_past_3_months

print(new_df)
# new_df.to_csv("past3months.csv", index=False)
# new_df = pd.read_csv("past3months.csv")

#
# customer_ids = []
# for customer_num in new_df.customer_id:
#
#     customer_data = df[df.customer_id == customer_num]
#     customer_data.order_datetime = customer_data.order_datetime.astype("string")
#     customer_data.quarter = customer_data.quarter.astype("string")
#     print(customer_data)
#     cursor.execute(f"""DROP TABLE IF EXISTS Customer{customer_num}""")
#     customer_data.to_sql(name=f"Customer{customer_num}", con=connection)
#     print(f"Dataframe {customer_num} is inserted to DB")

# To continue with the analysis i would like to work only with these customers that have constant data. Customers
# that have gaps in their orders are not well-predicted. For that reason i will remove them. Customers only with one
# order will be in my analysis, for them i will perform naive method, which means that the last observation will their
# future observation

# for customer_id in new_df.customer_id:
#     print(f"Customer{customer_id}")
#
#     query = cursor.execute(f"""SELECT * FROM Customer{customer_id} """)#
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

# To prediction about future orders i would say that i need customers with orders > 4. That's mean that i need
# customers with at least one year of orders. All customers below that level i would do naive method for the future
# orders, for the other ones i would do simple moving average

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
temp_tables_names = cursor.fetchall()
table_names = []
for table in temp_tables_names:
    table_names.append(*table)

for table in table_names:
    query = cursor.execute(f"""SELECT * FROM {table} """)  #
    #     cols = [column[0] for column in query.description]
    #     customer_df = pd.DataFrame.from_records(data = query.fetchall(), columns=cols)
print(table_names)



