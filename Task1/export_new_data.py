import sqlite_db

import pandas as pd
# We take all customers who has been stored in our database. These are the customers who has not gaps in their data
# and had made orders in the last quarter

def get_tables_name():
    sqlite_db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    temp_tables_names = sqlite_db.cursor.fetchall()
    table_names = []
    for table in temp_tables_names:
        table_names.append(*table)
    return table_names


def export_new_data(new_df, last_quarter, tables_names):
    for table in tables_names:
        query = sqlite_db.cursor.execute(f"""SELECT * FROM {table} """)  #
        cols = [column[0] for column in query.description]
        customer_df = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
        print(customer_df)
        quarters = customer_df.quarter.drop_duplicates()
        print(quarters)

        if len(quarters) < 4:
            last_quarter_customer_data = customer_df[customer_df.quarter == str(last_quarter)]
            future_orders = len(last_quarter_customer_data.index)
            future_gross = round(sum(last_quarter_customer_data.gross_value), 2)
            index_row = new_df.index[new_df['customer_id'] == customer_df.customer_id[0]].tolist()
            new_df.loc[index_row, "numer_of_orders_future_3_months"] = future_orders
            new_df.loc[index_row, "gross_sum_orders_future_3_months"] = future_gross
        else:
            count_of_orders_per_quarter = []
            count_of_gross_per_quarter = []
            for quarter in quarters:
                temp_df = customer_df[customer_df.quarter == str(quarter)]
                number_of_orders = len(temp_df.index)
                number_of_gross = round(sum(temp_df.gross_value), 2)
                count_of_orders_per_quarter.append(number_of_orders)
                count_of_gross_per_quarter.append(number_of_gross)

            i = 0
            moving_average_for_orders = []
            moving_average_for_gross = []
            window_size = 4

            while i < len(count_of_orders_per_quarter) - window_size + 1:
                # Calculate the average of current window
                window_average_orders = round(sum(count_of_orders_per_quarter[
                                                  i:i + window_size]) / window_size, 2)

                window_average_gross = round(sum(count_of_gross_per_quarter[
                                                 i:i + window_size]) / window_size, 2)

                # Store the average of current window in moving average list
                moving_average_for_orders.append(window_average_orders)
                moving_average_for_gross.append(window_average_gross)
                # Shift window to right by one position
                i += 1

            print(moving_average_for_orders)
            print(moving_average_for_gross)
            future_orders = round(moving_average_for_orders[-1])
            future_gross = moving_average_for_gross[-1]

            index_row = new_df.index[new_df['customer_id'] == customer_df.customer_id[0]].tolist()
            new_df.loc[index_row, "numer_of_orders_future_3_months"] = future_orders
            new_df.loc[index_row, "gross_sum_orders_future_3_months"] = future_gross


    return new_df


