#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd 
import datetime as dt
import matplotlib.pyplot as plt #to plot graphs
import squarify #for square chart

data = pd.read_excel("Online Retail.xlsx")


# In[44]:


#Removing irrelevant data
data = data[(data['Quantity']>0)]
data=data[['CustomerID','InvoiceDate','InvoiceNo','Quantity','UnitPrice']]

#Total price is number of quantity * per unit price
data['TotalPrice'] = data['Quantity'] * data['UnitPrice']
#Finding most recent and oldest order date
data['InvoiceDate'].min(),data['InvoiceDate'].max()
#PRESENT = dt.datetime(2020,12,31)
PRESENT = dt.datetime(2011,12,10)
data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])


# In[45]:


#RecentTransaction(Recency) = current date - Last transaction date
#NumOfTransactions(Frequency) = Total No. of Invoice per customer
#MoneySpent(Monetary) = Sum of Money spent for all transactions by single customer
rfm= data.groupby('CustomerID').agg({'InvoiceDate': lambda date: (PRESENT - date.max()).days,
                                        'InvoiceNo': lambda num: len(num),
                                        'TotalPrice': lambda price: price.sum()})
rfm.columns=['RecentTransaction','NumOfTransactions','MoneySpent']
rfm['RecentTransaction'] = rfm['RecentTransaction'].astype(int)
rfm.head()


# In[46]:


#Lesser the value of RecentTransaction, Better Recency
rfm['Recency'] = pd.qcut(rfm['RecentTransaction'], 4, ['1','2','3','4'])
#Greater the value of NumOfTransactions, Better Frequency
rfm['Frequency'] = pd.qcut(rfm['NumOfTransactions'], 4, ['4','3','2','1'])
#Greater the value of MoneySpent, Better Monetary
rfm['Monetary'] = pd.qcut(rfm['MoneySpent'], 4, ['4','3','2','1'])
rfm.head()


# In[47]:


rfm['RFM_Score'] = rfm.Recency.astype(str)+ rfm.Frequency.astype(str) + rfm.Monetary.astype(str)
rfm['RFM_Sum'] = rfm.Recency.astype(int)+ rfm.Frequency.astype(int) + rfm.Monetary.astype(int)
rfm.head()


# In[48]:


#Bifuracting customers into categories based on their RFM_Sum
def RFM_Category(df):
    if df['RFM_Sum'] < 5:
        return 'Champions'
    elif ((df['RFM_Sum'] >= 5) and (df['RFM_Sum'] < 6)):
        return 'Loyal'
    elif ((df['RFM_Sum'] >= 6) and (df['RFM_Sum'] < 7)):
        return 'Potential'
    elif ((df['RFM_Sum'] >= 7) and (df['RFM_Sum'] < 8)):
        return 'Promising'
    elif ((df['RFM_Sum'] >= 8) and (df['RFM_Sum'] < 9)):
        return 'Needs Attention'
    elif ((df['RFM_Sum'] >= 9) and (df['RFM_Sum'] < 11)):
        return 'About to Sleep'
    else:
        return 'Lost'

rfm['RFM_Category'] = rfm.apply(RFM_Category, axis=1)
rfm.head()


# In[59]:


# Calculating mean for each RFM_Category, and returning total count(Using aggregate function)
RFM_Category_agg = rfm.groupby('RFM_Category').agg({'RecentTransaction': 'mean',
                                                'NumOfTransactions': 'mean',
                                                'MoneySpent': ['mean', 'count']}).round(1)
print(RFM_Category_agg)


# In[69]:


#To Visualize the data based on count
RFM_Category_agg.columns = ['RecentTransactionMean','NumOfTransactionsMean','MoneySpentMean', 'Count']

#Creating square plot using squarify and matplot
chart = plt.gcf()
ax = chart.add_subplot()
chart.set_size_inches(17, 8.5)
squarify.plot(sizes=RFM_Category_agg['Count'], 
              label=['About to Sleep',
                     'Champions',
                     'Lost',
                     'Loyal',
                     'Needs Attention',
                     'Potential',
                     'Promising'], alpha=.6 )
plt.title("RFM Segments",fontweight="bold",fontsize=20)
plt.axis('off')
plt.show()


# In[ ]:




