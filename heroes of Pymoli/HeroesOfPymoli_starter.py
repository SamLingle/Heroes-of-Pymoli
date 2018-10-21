
# coding: utf-8

# ### Heroes Of Pymoli Data Analysis
# * Of the 1163 active players, the vast majority are male (84%). There also exists, a smaller, but notable proportion of female players (14%).
# 
# * Our peak age demographic falls between 20-24 (44.8%) with secondary groups falling between 15-19 (18.60%) and 25-29 (13.4%).  
# -----

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[91]:


# Dependencies and Setup
import pandas as pd
import numpy as np

# File to Load (Remember to Change These)
file_to_load = "Resources/purchase_data.csv"

# Read Purchasing File and store into Pandas data frame
p_data = pd.read_csv(file_to_load)
p_data.head()


# ## Player Count

# * Display the total number of players
# 

# In[92]:


player_count = len(p_data['SN'].unique())
player_count_df = pd.DataFrame([{'Total Players' : player_count}])
player_count_df.set_index('Total Players', inplace = True)
player_count_df


# ## Purchasing Analysis (Total)

# * Run basic calculations to obtain number of unique items, average price, etc.
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame
# 

# In[93]:


drop_duplicates = p_data.drop_duplicates(['Item ID'], keep = 'first')
total_unique = len(drop_duplicates)
total_purchase = p_data['Price'].count()
total_revenue = round(p_data['Price'].sum(),2)
average_price = p_data['Price'].mean()

p_analysis = pd.DataFrame([{
    "Number of Unique Items": total_unique,
    "Average price": average_price,
    "Number of Purchases" : total_purchase,
    "Total Revenue": total_revenue}])

p_analysis.style.format({"Average price": '${:.2f}', "Total Revenue": '${:.2f}'})


# ## Gender Demographics

# * Percentage and Count of Male Players
# 
# 
# * Percentage and Count of Female Players
# 
# 
# * Percentage and Count of Other / Non-Disclosed
# 
# 
# 

# In[94]:


no_dup_players = p_data.drop_duplicates(["Item ID"], keep='first')
gender_counts =  no_dup_players['Gender'].value_counts().reset_index()
gender_counts['Percent of Players'] = round(gender_counts["Gender"]/player_count * 100, 2)
gender_counts.style.format({"Percentage of Players": "%{:.2f}"})


# 
# ## Purchasing Analysis (Gender)

# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. by gender
# 
# 
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[95]:


gender_count_df = p_data.groupby("Gender")["SN"].nunique()
gender_count_df.head()
gender_purchases_df = p_data.groupby("Gender")["Item Name"]
gender_purchases_df = gender_purchases_df.count()
gender_average_df = p_data.groupby("Gender")["Price"].mean()
gender_average_df.round(2)
gender_total_df = p_data.groupby("Gender")["Price"].sum()
gender_total_df
normalized_gender_total_df = gender_total_df/gender_count_df
normalized_gender_total_df.round(2)


gender_analysis_df = pd.DataFrame({"Purchase Count":gender_purchases_df, 
                                   "Average Purchase Price":gender_average_df,
                                   "Total Purchase Value":gender_total_df,
                                   "Average Total Purchase per Person":normalized_gender_total_df})
gender_analysis_df

gender_analysis_df.style.format({'Average Purchase Price': '${:.2f}', 'Total Purchase Value': '${:.2f}', 'Average Total Purchase per Person': '${:.2f}'})


# ## Age Demographics

# * Establish bins for ages
# 
# 
# * Categorize the existing players using the age bins. Hint: use pd.cut()
# 
# 
# * Calculate the numbers and percentages by age group
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: round the percentage column to two decimal points
# 
# 
# * Display Age Demographics Table
# 

# In[96]:



players_df = p_data.groupby(["SN"])
total_players = len(players_df)
player_count_summary = pd.DataFrame({"Total Players":total_players},index=[0])
player_count_summary
bins = [0,10,15,20,25,30,35,40, 45]
age_ranges = ["<10", "10-14","15-19", "20-24", "25-29", "30-34", "35-39", ">=40"]
unique_players_df = p_data.drop_duplicates(subset="SN", keep='first')
unique_players_df["Age Group"] = pd.cut(unique_players_df["Age"], bins, labels=age_ranges)
age_group = unique_players_df.groupby("Age Group").count()
age_group = age_group[["Age"]]
age_group = age_group.rename(columns={"Age": "Total Count"})
age_group["Percentage of Players"] = age_group["Total Count"] / total_players * 100
age_group = age_group[["Total Count", "Percentage of Players"]]
pd.options.display.float_format = '{:,.2f}'.format
print("Age Demographics")
age_group


# ## Purchasing Analysis (Age)

# * Bin the purchase_data data frame by age
# 
# 
# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[97]:


#Create bins
bins = [0,10,15,20,25,30,35,40, 45]
age_ranges = ["<10", "10-14","15-19", "20-24", "25-29", "30-34", "35-39", ">=40"]

pd.cut(p_data["Age"], bins, labels=age_ranges)
p_data["Age Range"] = pd.cut(p_data["Age"], bins, labels= age_ranges)
p_data.head()
age_group_percentage_df = round(p_data["Age Range"].value_counts()/780,2)
age_group_percentage_df
age_group_count_df = p_data.groupby("Age Range")["Item Name"]
age_group_count_df = age_group_count_df.count()
age_group_average_df = p_data.groupby("Age Range")["Price"].mean()
age_group_average_df.round(2)
age_group_total_df = p_data.groupby("Age Range")["Price"].sum()
age_group_total_df
normalized_age_total_df = age_group_total_df/573
normalized_age_total_df.round(2)

age_range_df = pd.DataFrame({"Purchase Count":age_group_count_df,
                            "Average Purchase Price":age_group_average_df,
                            "Total Purchase Value": age_group_total_df,
                            "Normalized Totals": normalized_age_total_df
})
age_range_df


# ## Top Spenders

# * Run basic calculations to obtain the results in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the total purchase value column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[98]:


purchase_amount_by_SN = pd.DataFrame(p_data.groupby('SN')['Price'].sum())
number_purchase_by_SN = pd.DataFrame(p_data.groupby('SN')['Price'].count())
average_purchase_by_SN = pd.DataFrame(p_data.groupby('SN')['Price'].mean())
top_5 = pd.merge(purchase_amount_by_SN, number_purchase_by_SN, left_index = True, right_index = True).merge(average_purchase_by_SN, left_index=True, right_index=True)
top_5.rename(columns = {'Price_x': 'Total Purchase Value', 'Price_y':'Purchase Count', 'Price':'Average Purchase Price'}, inplace = True)
top_5.sort_values('Total Purchase Value', ascending = False, inplace=True)
top_5 = top_5.head()
top_5.style.format({'Total Purchase Value': '${:.2f}', 'Average Purchase Price': '${:.2f}'})


# ## Most Popular Items

# * Retrieve the Item ID, Item Name, and Item Price columns
# 
# 
# * Group by Item ID and Item Name. Perform calculations to obtain purchase count, item price, and total purchase value
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the purchase count column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[99]:


top_5_items_ID = pd.DataFrame(p_data.groupby('Item ID')['Item ID'].count())
top_5_items_ID.sort_values('Item ID', ascending = False, inplace = True)
top5_items_ID = top5_items_ID.iloc[0:5][:]
top5_items_total = pd.DataFrame(p_data.groupby('Item ID')['Price'].sum())
top5_items = pd.merge(top5_items_ID, top5_items_total, left_index = True, right_index = True)
no_dup_items = p_data.drop_duplicates(['Item ID'], keep = 'first')
top5_merge_ID = pd.merge(top5_items, no_dup_items, left_index = True, right_on = 'Item ID')
top5_merge_ID = top5_merge_ID[['Item ID', 'Item Name', 'Item ID_x', 'Price_y', 'Price_x']]
top5_merge_ID.set_index(['Item ID'], inplace = True)
top5_merge_ID.rename(columns =  {'Item ID_x': 'Purchase Count', 'Price_y': 'Item Price', 'Price_x': 'Total Purchase Value'}, inplace=True)
top5_merge_ID.style.format({'Item Price': '${:.2f}', 'Total Purchase Value': '${:.2f}'})


# ## Most Profitable Items

# * Sort the above table by total purchase value in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the data frame
# 
# 

# In[100]:


top5_profit = pd.DataFrame(p_data.groupby('Item ID')['Price'].sum())
top5_profit.sort_values('Price', ascending = False, inplace = True)
top5_profit = top5_profit.iloc[0:5][:]
pur_count_profit = pd.DataFrame(p_data.groupby('Item ID')['Item ID'].count())

#Display data frame preview
top5_profit = pd.merge(top5_profit, pur_count_profit, left_index = True, right_index = True, how = 'left')
top5_merge_profit = pd.merge(top5_profit, no_dup_items, left_index = True, right_on = 'Item ID', how = 'left')
top5_merge_profit = top5_merge_profit[['Item ID', 'Item Name', 'Item ID_x', 'Price_y','Price_x']]
top5_merge_profit.set_index(['Item ID'], inplace=True)
top5_merge_profit.rename(columns = {'Item ID_x': 'Purchase Count', 'Price_y': 'Item Price', 'Price_x': 'Total Purchase Value'}, inplace = True)
top5_merge_profit.style.format({'Item Price': '${:.2f}', 'Total Purchase Value': '${:.2f}'})

