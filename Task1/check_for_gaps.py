import pandas as pd
from numpy import timedelta64
import sqlite_db


# Here we just make sure that our data for each customer in our database is correct. We do not want dataset with gaps
# for that reason i will remove these tables. If we have gaps in our data it is not possible to make correct forecast

def check_gaps_in_database_tables(new_df):
    for customer_id in new_df.customer_id:
        print(f"Customer{customer_id}")
        try:
            query = sqlite_db.cursor.execute(f"""SELECT * FROM Customer{customer_id} """)
        except:
            continue
        cols = [column[0] for column in query.description]
        customer_df = pd.DataFrame.from_records(data = query.fetchall(), columns=cols)

        customer_df["order_datetime"] = pd.to_datetime(customer_df["order_datetime"])
        customer_df["quarter"] = pd.to_datetime(customer_df["quarter"])
        customer_df["quarter_diff"] = customer_df.quarter.diff()
        customer_df['quarter_diff'] = customer_df['quarter_diff'].fillna(pd.Timedelta(seconds=0))
        customer_df.quarter_diff = customer_df.quarter_diff / timedelta64(1, 'D')

        if any(customer_df.quarter_diff > 92):
            sqlite_db.cursor.execute(f"""DROP TABLE IF EXISTS Customer{customer_id}""")
            print(f"Table name Customer{customer_id} was dropped")
            sqlite_db.connection.commit()
    return
