
import pandas as pd
import sqlite_db

# In this file we will create new dataframe object. In it we will store na past 3 months info. When we check the data
# we noticed that the last quarter is 2021Q2, so in that case, we are not able to perform any analysis because now is
# 2022 August. For that reason we will assume that current time is the last quarter of the dataset, when we do that
# we will able to make some analysis for the past 3 months which in our case will be last 4 months.
# We will store the data for the last three months and in the next steps will add the future data which is required
# What we will do here is just filtering the test_sales file by last quarter, after that select each one of the
# customers and for every order he made, count the total orders and total sum of gross value of these orders
# When we find these customers who had made orders in the last quarter we will perform analysis only on these customers,
# because it is not possible to make future projections of the next quarter if we do not know current quarter. We will
# store these customer in our sqlite database to be able to work with them later


def get_last_quarter_data(df):
    last_quarter = df.quarter.iloc[-1]
    last_quarter_data = df[df.quarter == last_quarter]
    last_quarter_data = last_quarter_data.reset_index(drop=True)
    last_quarter_data = last_quarter_data.drop_duplicates(subset="order_number", keep=False)
    return last_quarter_data


def create_new_df(last_quarter_data, main_df):
    new_df = pd.DataFrame()
    order_number_list = []
    number_of_orders_past_3_months = []
    gross_sum_orders_past_3_months = []
    customer_id_list = []
    temp_ids = []
    for customer_id in last_quarter_data.customer_id:
        if customer_id in customer_id_list:
            continue
        customer_id_list.append(customer_id)
        customer_table = last_quarter_data[last_quarter_data.customer_id == str(customer_id)]
        for order_num in customer_table.order_number:
            temp_ids.append(customer_id_list[-1])
            order_number_list.append(order_num)
            number_of_orders_past_3_months.append(len(customer_table.index))
            gross_sum_orders_past_3_months.append(round(sum(customer_table.gross_value), 2))

    new_df["customer_id"] = temp_ids
    new_df["order_numer"] = order_number_list
    new_df["number_of_orders_past_3_months"] = number_of_orders_past_3_months
    new_df["gross_sum_orders_past_3_months"] = gross_sum_orders_past_3_months

    new_df.to_csv("past3months.csv", index=False)
    new_df = pd.read_csv("past3months.csv")
    new_df.customer_id = new_df.customer_id.astype("string")

    for customer_num in new_df.customer_id:
        customer_data = main_df[main_df.customer_id == str(customer_num)]
        customer_data["order_datetime"] = customer_data["order_datetime"].astype("string")
        customer_data["quarter"] = customer_data["quarter"].astype("string")
        sqlite_db.cursor.execute(f"""DROP TABLE IF EXISTS Customer{customer_num}""")
        customer_data.to_sql(name=f"Customer{customer_num}", con=sqlite_db.connection)

    return new_df
