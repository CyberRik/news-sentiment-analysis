import pandas as pd

def filter_by_date(df, target_date):
    df['datetime'] = pd.to_datetime(df['datetime'])
    return df[df['datetime'].dt.strftime('%m/%d/%Y') == target_date]
