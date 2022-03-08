#import packages

import datetime as dt
import pandas as pd


#read excel

df = pd.read_excel("D:\Dekstop\pythonProject\online_retail_II.xlsx", sheet_name= "Year 2010-2011")
df.head()
df = df.copy()

df.head()
df.shape

df.describe().T

df.isnull().sum()
df.dropna(inplace = True)
df.shape
df["StockCode"].nunique()

stockcodeCount = df.groupby("StockCode").agg({ "StockCode":  "count"})
stockcodeCount.sort_values("StockCode", ascending=True)

df["TotalPrice"] = df["Quantity"] * df["Price"]

df = df[~df["Invoice"].str.contains("C", na=False)]
df.head()

df["InvoiceDate"].max()

today_date =dt.datetime(2010,12,11)
rfm = df.groupby("Customer ID").agg({ "InvoiceDate": lambda InvoiceDate:(today_date - InvoiceDate.max()).days,
                                "Invoice": lambda Invoice: Invoice.nunique(),
                                "TotalPrice": lambda TotalPrice: TotalPrice.sum()})

rfm.columns = ["recency", "frequency", "monetary"]
rfm["recency_score"] = pd.qcut(rfm["recency"], 5, labels=[5,4,3,2,1])
rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method = "first"),5 ,labels=[1,2,3,4,5])
rfm["monetary_score"] = pd.qcut(rfm["monetary"], 5, labels=[1,2,3,4,5])
rfm.head()

rfm["RFM_SCORE"] =  (rfm["recency_score"].astype(str) + rfm["frequency_score"].astype(str))


rfm.describe().T
rfm[rfm["RFM_SCORE"] == "55"].head()

seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

rfm["segment"] = rfm["RFM_SCORE"].replace(seg_map,regex = True)
rfm = rfm[["recency", "frequency", "monetary", "segment"]]
rfm.head()

rfm_loyal =  rfm[rfm["segment"] == "loyal_customers"]
