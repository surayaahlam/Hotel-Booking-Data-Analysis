#!/usr/bin/env python
# coding: utf-8

# # Importing Libraries

# In[91]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


# # Loading the dataset

# In[92]:


df = pd.read_csv('hotel_bookings 2.csv')


# # Exploratory Data Analysis and Data Cleaning

# In[93]:


df.head()


# In[94]:


df.tail()


# In[95]:


df.shape


# In[96]:


df.columns


# In[97]:


df.info()


# In[98]:


df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'], format='%d/%m/%Y')


# In[99]:


df.describe(include = 'object')


# In[100]:


for col in df.describe(include = 'object').columns:
    print(col)
    print(df[col].unique())
    print('-'*50)


# In[101]:


df.isnull().sum()


# In[102]:


df.drop(['company', 'agent'], axis = 1, inplace = True)    # Droping the column with many null values
df.dropna(inplace = True)   # Droping the null rows


# In[103]:


df.isnull().sum()


# In[104]:


df.describe()


# In[105]:


df['adr'].plot(kind = 'box') # 1 point is greater than other points so this is outlier 


# In[106]:


df = df[df['adr']<5000]


# In[107]:


df.describe()


# # Data Analysis and Visualizations

# In[108]:


canceled_perc = df['is_canceled'].value_counts(normalize = True)    # normalize = True - Returns percentize
print(canceled_perc)


plt.figure(figsize = (5, 4))
plt.title("Reservation Status Count")
plt.bar(('Not Canceled', 'Canceled'), df['is_canceled'].value_counts(), edgecolor = 'k', width = 0.7)


# In[109]:


plt.figure(figsize = (8, 4))
ax1 = sns.countplot(x = 'hotel', hue = 'is_canceled', data = df, palette = 'Blues')
legend_labels,_ = ax1.get_legend_handles_labels()
ax1.legend(('Not Canceled', 'Canceled'), bbox_to_anchor = (1, 1))
plt.title('Reservation status in different hotels', size = 20)
plt.xlabel('Hotel')
plt.ylabel('Number of Reservation')
plt.show()


# In[110]:


resort_hotel = df[df['hotel'] == 'Resort Hotel']
resort_hotel['is_canceled'].value_counts(normalize = True)


# In[111]:


city_hotel = df[df['hotel'] == 'City Hotel']
city_hotel['is_canceled'].value_counts(normalize = True)


# In[112]:


resort_hotel = resort_hotel.groupby('reservation_status_date')[['adr']].mean()
city_hotel = city_hotel.groupby('reservation_status_date')[['adr']].mean()


# In[113]:


plt.figure(figsize = (20, 8))
plt.title('Average Daily Rate in City and Resort Hotel', fontsize = 30)
plt.plot(resort_hotel.index, resort_hotel['adr'], label = 'Resort Hotel')
plt.plot(city_hotel.index, city_hotel['adr'], label = 'City Hotel')
plt.legend(fontsize = 20)
plt.show()


# In[114]:


df['month'] = df['reservation_status_date'].dt.month


# In[115]:


plt.figure(figsize = (16, 8))
ax1 = sns.countplot(x = 'month', hue = 'is_canceled', data = df, palette = 'bright')
legend_labels,_ = ax1.get_legend_handles_labels()
ax1.legend(bbox_to_anchor = (1, 1))
plt.title('Reservation status per month', size = 20)
plt.xlabel('Month')
plt.ylabel('Number of Reservation')
plt.legend(['Not Canceled', 'Canceled'])
plt.show()


# In[116]:


plt.figure(figsize = (15, 8))
plt.title('ADR per month', fontsize = 30)
sns.barplot(x = 'month', y = 'adr', data = df[df['is_canceled'] == 1].groupby('month')[['adr']].sum().reset_index())
plt.show()


# In[117]:


canceled_data = df[df['is_canceled'] == 1]
top_10_country = canceled_data['country'].value_counts()[:10]  # Return country in decending order, [:10] - 1st 10 country
plt.figure(figsize = (8, 8))
plt.title('Top 10 Countries with Reservation Canceled')
plt.pie(top_10_country, autopct = '%.2f', labels = top_10_country.index)
plt.show()


# In[118]:


df['market_segment'].value_counts()


# In[119]:


df['market_segment'].value_counts(normalize = True)


# In[120]:


canceled_data['market_segment'].value_counts(normalize = True)


# In[121]:


not_canceled_data = df[df['is_canceled'] == 0]


# In[122]:


canceled_df_adr = canceled_data.groupby('reservation_status_date')[['adr']].mean()
canceled_df_adr.reset_index(inplace = True)
canceled_df_adr.sort_values('reservation_status_date', inplace = True)

not_canceled_df_adr = not_canceled_data.groupby('reservation_status_date')[['adr']].mean()
not_canceled_df_adr.reset_index(inplace = True)
not_canceled_df_adr.sort_values('reservation_status_date', inplace = True)

plt.figure(figsize = (20, 6))
plt.title('Average Daily Rate')
plt.plot(not_canceled_df_adr['reservation_status_date'], not_canceled_df_adr['adr'], label = 'Not_Canceled')
plt.plot(canceled_df_adr['reservation_status_date'], canceled_df_adr['adr'], label = 'Canceled')
plt.legend()
plt.show()


# In[123]:


canceled_df_adr = canceled_df_adr[(canceled_df_adr['reservation_status_date'] > '2016') & (canceled_df_adr['reservation_status_date'] < '2017-09')]
not_canceled_df_adr = not_canceled_df_adr[(not_canceled_df_adr['reservation_status_date'] > '2016') & (not_canceled_df_adr['reservation_status_date'] < '2017-09')]


# ### Filtered data from 2016 to sep, 2017

# In[124]:


plt.figure(figsize = (20, 6))
plt.title('Average Daily Rate', fontsize = 30)
plt.plot(not_canceled_df_adr['reservation_status_date'], not_canceled_df_adr['adr'], label = 'Not_Canceled')
plt.plot(canceled_df_adr['reservation_status_date'], canceled_df_adr['adr'], label = 'Canceled')
plt.legend(fontsize = 15)
plt.show()

