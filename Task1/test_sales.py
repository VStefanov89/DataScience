import pandas as pd


# In this file we will store the test_sales.csv to dataframe object. We will check all columns and make sure they are
# in appropriate type. ALso we will sort the dataframe by order_datetime column and create new column with name quarter


def store_main_df(df_path):
    df = pd.read_csv(df_path)
    df['customer_id'] = df['customer_id'].astype("string")
    df = df[df['customer_id'].notnull()]
    df.customer_id = df.customer_id.replace("-", "", regex=True)
    df['order_number'] = df['order_number'].astype("string")
    df['channel'] = df['channel'].astype("string")
    df["order_datetime"] = pd.to_datetime(df["order_datetime"])
    df = df.sort_values(by="order_datetime")
    df = df.reset_index(drop=True)
    df["quarter"] = df['order_datetime'].dt.to_period('Q')
    return df
