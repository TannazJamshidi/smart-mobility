#!/usr/bin/env python
# coding: utf-8

# # Lab 1

# Professor:

#     PRONELLO Cristina


# # Exercise 1 - Data setup and preliminary analysis

# In[1]:


# The path of input files


# In[2]:


input_micro_mobility = "Divvy_Trips_20240103.csv"


# In[3]:


input_public_transport = "CTA_-_List_of_CTA_Datasets_20240103.csv"


# In[4]:


input_boundaries = "Boundaries_-_Wards__2023-__20240103.csv"


# In[5]:


import pandas as pd


# In[6]:


# Reading csv file


# In[7]:


df_micro_mobility = pd.read_csv(input_micro_mobility, on_bad_lines = 'warn', sep=',')


# In[8]:


df_public_transport = pd.read_csv(input_public_transport, on_bad_lines = 'warn', sep=',')


# In[9]:


df_boundaries = pd.read_csv(input_boundaries, on_bad_lines = 'warn', sep=',')


# In[12]:


# Showing a few rows of the tables


# In[13]:


# Micro Mobolity
df_micro_mobility.head()


# In[14]:


# Public Transport
df_public_transport.head()


# In[15]:


# Boundaries
df_boundaries.head()


# Before answering any questions, some initial data cleaning might be required - Removing empty rows or rows missing essential data.
# Answer the following questions based on the data setup and using python:
# - The number of records before and after data cleaning. What were the types of “bad data” that needed to be cleaned ?
# - When did collection of data start(start-date and time) for micro-mobility dataset and what is the most recent date and time available.
# - Number of records per year and month in micro-mobility dataset – Use bar plots to display patterns using the plot() function of pandas. 
# - Number of unique vehicles by year and vehicle type – identify patterns e.g.,:
# - Are there more vehicles as years go  on ?
# - Is there some change in usage patterns among different days of the week , months is there a trend – seasonal or weekly ?
# - Are there any trends based on the gender and age of the user ?

# In[16]:


# Using count() method to see the missing values in schema of the dataframe.


# In[17]:


df_micro_mobility.count()


# ...........................................................................................

# - The number of records before and after data cleaning. What were the types of “bad data” that needed to be cleaned ?

# As observed, prior to data cleaning, there are 21,242,740 rows (TRIP ID). However, it is evident that certain columns contain missing values (LATITUDE, LONGITUDE, GENDER, BIRTH YEAR), requiring attention. The most important column for us to calculate OD matrix in further sections are LATITUDE and LONGITUDE, so in this level we clean data based on these columns, however we will clean data based on GENDER and BIRTH YEAR separately. Various approaches exist for handling missing data, and for this exercise, we have decided to address it by removing the rows with missing values.

# In[18]:


# Removing null values


# In[10]:


df_MM_clean = df_micro_mobility.dropna(subset=["FROM LATITUDE", "TO LATITUDE"])


# In[20]:


df_MM_clean.count()


# Following the data cleaning process, the dataset now consists of 21,241,850 rows for each column, and all necessary columns are non-null. The data types include integers, objects and floats, with the previous missing values categorized as "bad data" successfully addressed across most columns.

# ...........................................................................................

# - When did collection of data start(start-date and time) for micro-mobility dataset and what is the most recent date and time available.

# In[21]:


# Turning "Start Time" column to datetime object


# In[11]:


df_MM_clean_time = pd.to_datetime(df_MM_clean['START TIME'], format="%m/%d/%Y %I:%M:%S %p")


# In[23]:


# Find the minimum value in the "Start Time" column


# In[24]:


print("Minimum Start Time:", df_MM_clean_time.min())


# Collection of data start(start-date and time) for micro-mobility dataset starts from 01:06:00 of 27th of June 2013.

# In[25]:


print("Most Recent Start Time:", df_MM_clean_time.max())


# The most recent date and time available in dataset is 23:57:17 of 31st December 2019.

# ...........................................................................................

# - Number of records per year and month in micro-mobility dataset – Use bar plots to display patterns using the plot() function of pandas

# In[26]:


# Create columns that we need


# In[12]:


import datetime as dt


# In[13]:


df_MM_clean["YEAR"] = df_MM_clean_time.dt.strftime("%Y")


# In[13]:


df_MM_clean["MONTH"] = df_MM_clean_time.dt.strftime("%m")


# In[14]:


# Function for seasons
def get_season(month):
    if 3 <= month <= 5:
        return 'Spring'
    elif 6 <= month <= 8:
        return 'Summer'
    elif 9 <= month <= 11:
        return 'Autumn'
    else:
        return 'Winter'


# In[15]:


df_MM_clean["SEASON"] = df_MM_clean_time.dt.month.apply(get_season)


# In[16]:


df_MM_clean["DAY OF WEEK"] = df_MM_clean_time.dt.strftime("%A")


# In[20]:


# See the final result


# In[21]:


df_MM_clean.head()


# In[35]:


# Number of per year


# In[28]:


year_groups = df_MM_clean.groupby(["YEAR"]).size()


# In[37]:


print(year_groups)


# In[38]:


bp_year_groups = year_groups.plot(kind="bar")


# It is shown that there is an increasing trend for years and this growth was dramatic from 2013 to 2014 and one of the reasons is that our data start from the June 2013. Also, there was a litle decrease from 2017 to 2018.

# In[39]:


# Number of per month


# In[29]:


month_groups = df_MM_clean.groupby(["MONTH"]).size()


# In[41]:


print(month_groups)


# In[42]:


bp_month_groups = month_groups.plot(kind="bar")


# It shows that the majority of trips occur from June to October and it is less in cold months.

# In[43]:


# Number of per year and month


# In[30]:


month_year_groups = df_MM_clean.groupby(["YEAR", "MONTH"]).size()


# In[45]:


print(month_year_groups)


# In[46]:


# Bar plot to show the year-month pattern of data


# In[47]:


bp_month_year_groups = month_year_groups.plot(kind="bar")


# Number of records per year and month in micro-mobility dataset is shown above. It can be seen that majority of data belong to the middle of each year (from June to October) and generaly every year the trend was increasing.

# ...........................................................................................

# - Number of unique vehicles by year – identify patterns e.g.,:
# - Are there more vehicles as years go  on ?
# - Is there some change in usage patterns among different days of the week , months is there a trend – seasonal or weekly ?
# - Are there any trends based on the gender and age of the user ?

# In[48]:


df_MM_clean.info()


# In[49]:


# Comparing used vehicles in different years


# In[50]:


vehicle_groups = df_MM_clean.groupby(["YEAR", "BIKE ID"]).size()


# In[51]:


print(vehicle_groups)


# In[52]:


# Analyzing seasonal trends


# In[18]:


season_groups = df_MM_clean.groupby(["SEASON"]).size()


# In[19]:


print(season_groups)


# In[20]:


bp_season_groups = season_groups.plot(kind="bar")


# It shows that most of the trips happened on Summer and after that on Autumn

# In[53]:


vehicle_season_groups = df_MM_clean.groupby(["SEASON", "BIKE ID"]).size()


# In[54]:


print(vehicle_season_groups)


# In[56]:


vehicle_month_groups = df_MM_clean.groupby(["YEAR", "MONTH", "BIKE ID"]).size()


# In[57]:


print(vehicle_month_groups)


# In[59]:


# Analyzing weekly trends


# In[24]:


week_groups = df_MM_clean.groupby(["DAY OF WEEK"]).size()


# In[25]:


print(week_groups)


# In[26]:


bp_week_groups = week_groups.plot(kind="bar")


# It shows that most of the trips happened on weekdays but the difference is not too much

# In[60]:


vehicle_week_groups = df_MM_clean.groupby(["DAY OF WEEK", "BIKE ID"]).size()


# In[61]:


print(vehicle_week_groups)


# ...........................................................................................

# In[64]:


# Now we need to clean the data again based on GENDER and BIRTH YEAR
df_MM_clean_GB = df_MM_clean.dropna(axis=0)


# In[65]:


df_MM_clean_GB.count()


# Now we have 16,346,709 rows for all the columns.

# In[66]:


df_MM_clean_GB['GENDER'].value_counts()


# In[67]:


gender_year_groups = df_MM_clean_GB.groupby(["YEAR", "GENDER"]).size()


# In[68]:


print(gender_year_groups)


# In[69]:


bp_gender_year_groups = gender_year_groups.plot(kind="bar")


# It is shown that in general through these years the number of trips increased but the share of males have been always way more than females

# In[70]:


# Evaluating the gender trends within months


# In[71]:


gender_month_groups = df_MM_clean_GB.groupby(["MONTH", "GENDER"]).size()


# In[72]:


print(gender_month_groups)


# In[73]:


bp_gender_month_groups = gender_month_groups.plot(kind="bar")


# The same pattern is here for both males and females, warmer months are more delightful to use these modes of transport.

# ...........................................................................................

# In[74]:


# Calculating the minimum and maximum of "BIRTH YEAR" in order to find out the data


# In[75]:


df_MM_clean_GB['BIRTH YEAR'].min()


# In[76]:


df_MM_clean_GB['BIRTH YEAR'].max()


# In[77]:


# Check the "birth year" column to find out "bad data"


# In[78]:


df_MM_clean_GB['BIRTH YEAR'].value_counts()


# It is shown that there are some data which are obviously incorrect such as 1790. so we need to get rid of these data. 

# In[79]:


# Drop incorrect rows
df_MM_clean_B = df_MM_clean_GB[df_MM_clean_GB['BIRTH YEAR'] >= 1925]


# In[80]:


df_MM_clean_B.count()


# In[81]:


df_MM_clean_B['BIRTH YEAR'].min()


# Now we can say that the minimum of BIRTH YEAR is 1925 and the maximum of it is 2017.

# In[82]:


# Categorizing "BIRTH YEAR" in order to better evaluation.
bins = [1925, 1936, 1947, 1957, 1967, 1977, 1987, 1997, 2007, 2017]


# In[83]:


labels = ['1925-1936', '1936-1947', '1947-1957', '1957-1967', '1967-1977', '1977-1987', '1987-1997', '1997-2007', '2007-2017']


# In[84]:


# Creating a new column "BIRTH YEAR RANGE" based on the range we have defined.


# In[85]:


df_MM_clean_B['BIRTH YEAR RANGE'] = pd.cut(df_MM_clean_B['BIRTH YEAR'], bins=bins, labels=labels, right=False)


# In[86]:


age_groups = df_MM_clean_B.groupby("BIRTH YEAR RANGE").size()


# In[87]:


print(age_groups)


# In[88]:


bp_age_groups = age_groups.plot(kind="bar")


# It can be seen that the majority of users are born between 1977-1997.

# In[89]:


# Evaluating the age trend within years


# In[90]:


age_year_groups = df_MM_clean_B.groupby(["YEAR", "BIRTH YEAR RANGE"]).size()


# In[91]:


print(age_year_groups)


# In[92]:


bp_age_year_groups = age_year_groups.plot(kind="bar")


# It is observed that the same pattern exists for each year.

# -------------------------------------------------------------------------------------------

# # Exercise 2 - Data setup and preliminary analysis

# - Associate each trip in the dataset to an origin and destination ward by combining the trip information with the information about the wards. Check which wards the FROM_LOCATION and TO_LOCATION fields belong to.
# - Compute then the O-D matrix, i.e., the number of bookings starting in ward i and ending in ward j.  Try to visualize the results in a meaningful way. 
# - Prepare OD matrices for different years and different age groups(3 OD matrices for each age-group of 3 consecutive years). Are there any periodicity or trends noticed? Is there a difference between the OD matrices for different age groups?
# - Based on your observation, visualise selected OD matrices that show some trends/periodicity on a map. 
# - If a challenge is needed, students can also attempt to create a flowmap for the OD matrices.

# In[14]:


pip install geopandas


# In[11]:


pip install rtree


# In[15]:


pip install pygeos


# In[ ]:


# For this exercise, because the size of the file is too much large and we encountered memory issues for spatial joining, we decided to select only 3 years to work on.


# In[92]:


df_MM_clean_2016 = df_MM_clean[df_MM_clean['YEAR'] == '2016']


# In[14]:


import geopandas as gpd
from shapely import wkt


# In[93]:


# Convert 'the_geom' in wards_chicago from WKT(Well Known text) to shapely objects
# 'the_geom' column contains MULTIPOLYGON data in text format
df_boundaries['the_geom'] = df_boundaries['the_geom'].apply(wkt.loads)
wards_gdf = gpd.GeoDataFrame(df_boundaries, geometry='the_geom')


# In[94]:


# Convert 'FROM LOCATION' and 'TO LOCATION' in df_chicago from WKT to shapely Point objects
# These columns contain POINT data in text format
df_MM_clean_2016['from_point'] = df_MM_clean_2016['FROM LOCATION'].apply(wkt.loads)
df_from_gdf_2016 = gpd.GeoDataFrame(df_MM_clean_2016, geometry='from_point')


# In[95]:


df_MM_clean_2016['to_point'] = df_MM_clean_2016['TO LOCATION'].apply(wkt.loads)
df_to_gdf_2016 = gpd.GeoDataFrame(df_MM_clean_2016, geometry='to_point')


# In[96]:


# Ensure the CRS for both GeoDataFrames are the same
# This can be done by setting the CRS(Co-ordinate Reference System) of df_from_gdf and df_to_gdf to match that of wards_gdf
# The CRS depends on the data; for example, it can be set to 'EPSG:4326' for WGS84

df_from_gdf_2016 = df_from_gdf_2016.set_crs('EPSG:4326', inplace=True,allow_override = True)
df_to_gdf_2016 = df_to_gdf_2016.set_crs('EPSG:4326', inplace=True,allow_override = True)
wards_gdf = wards_gdf.set_crs('EPSG:4326', inplace=True,allow_override = True)


# In[ ]:


# Perform spatial joins
# Join df_from_gdf and df_to_gdf with wards_gdf to find the corresponding wards
from_joined_2016 = gpd.sjoin(df_from_gdf_2016, wards_gdf, how="left", op='within')


# In[34]:


to_joined_2016 = gpd.sjoin(df_to_gdf_2016, wards_gdf, how="left", op='within')


# In[35]:


# Add the ward information back to the original df_chicago DataFrame
df_MM_clean_2016['FROM WARD'] = from_joined_2016['Ward']  # Replace 'Ward' with the actual column name in wards_gdf
df_MM_clean_2016['TO WARD'] = to_joined_2016['Ward']      # Replace 'Ward' with the actual column name in wards_gdf


# In[36]:


df_MM_clean_2016.to_csv("df_MM_clean_2016", index=False)


# In[30]:


# Display the first few rows of the updated df_chicago to check the results
df_MM_clean_2016.head()


# In[14]:


df_MM_clean_2017 = df_MM_clean[df_MM_clean['YEAR'] == '2017']


# In[18]:


# Convert 'FROM LOCATION' and 'TO LOCATION' in df_chicago from WKT to shapely Point objects
# These columns contain POINT data in text format
df_MM_clean_2017['from_point'] = df_MM_clean_2017['FROM LOCATION'].apply(wkt.loads)
df_from_gdf_2017 = gpd.GeoDataFrame(df_MM_clean_2017, geometry='from_point')
df_MM_clean_2017['to_point'] = df_MM_clean_2017['TO LOCATION'].apply(wkt.loads)
df_to_gdf_2017 = gpd.GeoDataFrame(df_MM_clean_2017, geometry='to_point')


# In[19]:


# Ensure the CRS for both GeoDataFrames are the same
# This can be done by setting the CRS(Co-ordinate Reference System) of df_from_gdf and df_to_gdf to match that of wards_gdf
# The CRS depends on the data; for example, it can be set to 'EPSG:4326' for WGS84
df_from_gdf_2017 = df_from_gdf_2017.set_crs('EPSG:4326', inplace=True,allow_override = True)
df_to_gdf_2017 = df_to_gdf_2017.set_crs('EPSG:4326', inplace=True,allow_override = True)
wards_gdf = wards_gdf.set_crs('EPSG:4326', inplace=True,allow_override = True)


# In[20]:


# Perform spatial joins
# Join df_from_gdf and df_to_gdf with wards_gdf to find the corresponding wards
from_joined_2017 = gpd.sjoin(df_from_gdf_2017, wards_gdf, how="left", op='within')
to_joined_2017 = gpd.sjoin(df_to_gdf_2017, wards_gdf, how="left", op='within')


# In[21]:


# Add the ward information back to the original df_chicago DataFrame
df_MM_clean_2017['FROM WARD'] = from_joined_2017['Ward']  # Replace 'Ward' with the actual column name in wards_gdf
df_MM_clean_2017['TO WARD'] = to_joined_2017['Ward']      # Replace 'Ward' with the actual column name in wards_gdf


# In[22]:


df_MM_clean_2017.to_csv("df_MM_clean_2017", index=False)


# In[24]:


# Display the first few rows of the updated df_chicago to check the results
df_MM_clean_2017.head()


# In[23]:


df_MM_clean_2018 = df_MM_clean[df_MM_clean['YEAR'] == '2018']


# In[24]:


# Convert 'FROM LOCATION' and 'TO LOCATION' in df_chicago from WKT to shapely Point objects
# These columns contain POINT data in text format
df_MM_clean_2018['from_point'] = df_MM_clean_2018['FROM LOCATION'].apply(wkt.loads)
df_from_gdf_2018 = gpd.GeoDataFrame(df_MM_clean_2018, geometry='from_point')
df_MM_clean_2018['to_point'] = df_MM_clean_2018['TO LOCATION'].apply(wkt.loads)
df_to_gdf_2018 = gpd.GeoDataFrame(df_MM_clean_2018, geometry='to_point')


# In[25]:


# Ensure the CRS for both GeoDataFrames are the same
# This can be done by setting the CRS(Co-ordinate Reference System) of df_from_gdf and df_to_gdf to match that of wards_gdf
# The CRS depends on the data; for example, it can be set to 'EPSG:4326' for WGS84
df_from_gdf_2018 = df_from_gdf_2018.set_crs('EPSG:4326', inplace=True,allow_override = True)
df_to_gdf_2018 = df_to_gdf_2018.set_crs('EPSG:4326', inplace=True,allow_override = True)
wards_gdf = wards_gdf.set_crs('EPSG:4326', inplace=True,allow_override = True)


# In[26]:


# Perform spatial joins
# Join df_from_gdf and df_to_gdf with wards_gdf to find the corresponding wards
from_joined_2018 = gpd.sjoin(df_from_gdf_2018, wards_gdf, how="left", op='within')
to_joined_2018 = gpd.sjoin(df_to_gdf_2018, wards_gdf, how="left", op='within')


# In[27]:


# Add the ward information back to the original df_chicago DataFrame
df_MM_clean_2018['FROM WARD'] = from_joined_2018['Ward']  # Replace 'Ward' with the actual column name in wards_gdf
df_MM_clean_2018['TO WARD'] = to_joined_2018['Ward']      # Replace 'Ward' with the actual column name in wards_gdf


# In[28]:


df_MM_clean_2018.to_csv("df_MM_clean_2018", index=False)


# In[30]:


# Display the first few rows of the updated df_chicago to check the results
df_MM_clean_2018.head()


# ...........................................................................................

# - Compute then the O-D matrix, i.e., the number of bookings starting in ward i and ending in ward j.  Try to visualize the results in a meaningful way.

# In[16]:


# OD Matrix 2016 calculation using pivot table
matrix_2016 = (
    df_MM_clean_2016.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_2016


# In[17]:


# OD Matrix 2017 calculation using pivot table
matrix_2017 = (
    df_MM_clean_2017.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_2017


# In[18]:


# OD Matrix 2018 calculation using pivot table
matrix_2018 = (
    df_MM_clean_2018.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_2018


# In[19]:


# Saving OD Matrices
matrix_2016.to_csv("matrix_2016", index=False)
matrix_2017.to_csv("matrix_2017", index=False)
matrix_2018.to_csv("matrix_2018", index=False)


# ...........................................................................................

# - Prepare OD matrices for different years and different age groups(3 OD matrices for each age-group of 3 consecutive years). Are there any periodicity or trends noticed? Is there a difference between the OD matrices for different age groups?

# In[15]:


# Using saved dataframes with "from wards" and "to wards" to avoid kernel disconnecting.
df_MM_clean_2016 = pd.read_csv("df_MM_clean_2016", on_bad_lines = 'warn', sep=',')
df_MM_clean_2017 = pd.read_csv("df_MM_clean_2017", on_bad_lines = 'warn', sep=',')
df_MM_clean_2018 = pd.read_csv("df_MM_clean_2018", on_bad_lines = 'warn', sep=',')


# In[20]:


# Drop null values
df_MM_clean_2016 = df_MM_clean_2016.dropna(subset=['BIRTH YEAR'])


# In[21]:


# Convert BIRTH YEAR to integer
df_MM_clean_2016['BIRTH YEAR'] = df_MM_clean_2016['BIRTH YEAR'].astype('int')


# In[22]:


# Create age groups based on the agr distribution of users
df_MM_clean_2016['age'] = 2024 - df_MM_clean_2016['BIRTH YEAR']


# In[23]:


# Define age groups
age_bins = [0, 18, 30, 40, 50, 60, float('inf')]  # Define age bins/ranges
age_labels = ['0-18', '19-30', '31-40', '41-50', '51-60', '61+']  # Define corresponding labels


# In[24]:


# Create 'age group' column using pd.cut
df_MM_clean_2016['age group'] = pd.cut(df_MM_clean_2016['age'], bins=age_bins, labels=age_labels, right=False)


# In[25]:


age_group_under_18_2016 = df_MM_clean_2016[df_MM_clean_2016['age group'] == '0-18']
# OD Matrix
matrix_age_under_18_2016 = (
    age_group_under_18_2016.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_age_under_18_2016


# It shows that there was no under 18 user in 2016

# In[26]:


age_group_19_30_2016 = df_MM_clean_2016[df_MM_clean_2016['age group'] == '19-30']
# OD Matrix
matrix_age_19_30_2016 = (
    age_group_19_30_2016.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_age_19_30_2016


# Because the OD matrix is too large we postpone the analysis for the next section.

# In[27]:


age_group_31_40_2016 = df_MM_clean_2016[df_MM_clean_2016['age group'] == '31-40']
# OD Matrix
matrix_age_31_40_2016 = (
    age_group_31_40_2016.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_age_31_40_2016


# In[28]:


age_group_41_50_2016 = df_MM_clean_2016[df_MM_clean_2016['age group'] == '41-50']
# OD Matrix
matrix_age_41_50_2016 = (
    age_group_41_50_2016.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_age_41_50_2016


# In[29]:


age_group_51_60_2016 = df_MM_clean_2016[df_MM_clean_2016['age group'] == '51-60']
# OD Matrix
matrix_age_51_60_2016 = (
    age_group_51_60_2016.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_age_51_60_2016


# In[30]:


age_group_above_61_2016 = df_MM_clean_2016[df_MM_clean_2016['age group'] == '61+']
# OD Matrix
matrix_age_above_61_2016 = (
    age_group_above_61_2016.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_age_above_61_2016


# ...........................................................................................

# In[37]:


# Drop null values
df_MM_clean_2017 = df_MM_clean_2017.dropna(subset=['BIRTH YEAR'])


# In[38]:


# Convert BIRTH YEAR to integer
df_MM_clean_2017['BIRTH YEAR'] = df_MM_clean_2017['BIRTH YEAR'].astype('int')


# In[39]:


# Create age groups based on the agr distribution of users
df_MM_clean_2017['age'] = 2024 - df_MM_clean_2017['BIRTH YEAR']


# In[42]:


# Define age groups
age_bins = [0, 18, 30, 40, 50, 60, float('inf')]  # Define age bins/ranges
age_labels = ['0-18', '19-30', '31-40', '41-50', '51-60', '61+']  # Define corresponding labels


# In[41]:


# Create 'age group' column using pd.cut
df_MM_clean_2017['age group'] = pd.cut(df_MM_clean_2017['age'], bins=age_bins, labels=age_labels, right=False)


# In[47]:


age_group_under_18_2017 = df_MM_clean_2017[df_MM_clean_2017['age group'] == '0-18']
# OD Matrix
matrix_age_under_18_2017 = (
    age_group_under_18_2017.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_age_under_18_2017


# As it is shown, the number of under 18 years old users are low and the most trips happened inside ward 28.

# In[48]:


age_group_19_30_2017 = df_MM_clean_2017[df_MM_clean_2017['age group'] == '19-30']
# OD Matrix 2018 calculation using pivot table
matrix_age_19_30_2017 = (
    age_group_19_30_2017.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_age_19_30_2017


# Because the siz of the matrix is too large, it is hard to conclude here, so we will wait untile the next part for further analysis.

# In[49]:


age_group_31_40_2017 = df_MM_clean_2017[df_MM_clean_2017['age group'] == '31-40']
# OD Matrix 2018 calculation using pivot table
matrix_age_31_40_2017 = (
    age_group_31_40_2017.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_age_31_40_2017


# In[50]:


age_group_41_50_2017 = df_MM_clean_2017[df_MM_clean_2017['age group'] == '41-50']
# OD Matrix 2018 calculation using pivot table
matrix_age_41_50_2017 = (
    age_group_41_50_2017.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_age_41_50_2017


# In[52]:


age_group_51_60_2017 = df_MM_clean_2017[df_MM_clean_2017['age group'] == '51-60']
# OD Matrix 2018 calculation using pivot table
matrix_age_51_60_2017 = (
    age_group_51_60_2017.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_age_51_60_2017


# In[51]:


age_group_above_61_2017 = df_MM_clean_2017[df_MM_clean_2017['age group'] == '61+']
# OD Matrix 2018 calculation using pivot table
matrix_age_above_61_2017 = (
    age_group_above_61_2017.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_age_above_61_2017


# Because the siz of the matrix is too large, it is hard to conclude here, so we will wait untile the next part for further analysis.

# ...........................................................................................

# In[55]:


# Drop null values
df_MM_clean_2018 = df_MM_clean_2018.dropna(subset=['BIRTH YEAR'])


# In[56]:


# Convert BIRTH YEAR to integer
df_MM_clean_2018['BIRTH YEAR'] = df_MM_clean_2018['BIRTH YEAR'].astype('int')


# In[57]:


# Create age groups based on the agr distribution of users
df_MM_clean_2018['age'] = 2024 - df_MM_clean_2018['BIRTH YEAR']


# In[58]:


# Define age groups
age_bins = [0, 18, 30, 40, 50, 60, float('inf')]  # Define age bins/ranges
age_labels = ['0-18', '19-30', '31-40', '41-50', '51-60', '61+']  # Define corresponding labels


# In[59]:


# Create 'age group' column using pd.cut
df_MM_clean_2018['age group'] = pd.cut(df_MM_clean_2018['age'], bins=age_bins, labels=age_labels, right=False)


# In[60]:


age_group_under_18_2018 = df_MM_clean_2018[df_MM_clean_2018['age group'] == '0-18']
# OD Matrix 2018 calculation using pivot table
matrix_age_under_18_2018 = (
    age_group_under_18_2018.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_age_under_18_2018


# There is no record for under 18 users in 2018

# In[61]:


age_group_19_30_2018 = df_MM_clean_2018[df_MM_clean_2018['age group'] == '19-30']
# OD Matrix 2018 calculation using pivot table
matrix_age_19_30_2018 = (
    age_group_19_30_2018.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_age_19_30_2018


# In[62]:


age_group_31_40_2018 = df_MM_clean_2018[df_MM_clean_2018['age group'] == '31-40']
# OD Matrix 2018 calculation using pivot table
matrix_age_31_40_2018 = (
    age_group_31_40_2018.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_age_31_40_2018


# In[63]:


age_group_41_50_2018 = df_MM_clean_2018[df_MM_clean_2018['age group'] == '41-50']
# OD Matrix 2018 calculation using pivot table
matrix_age_41_50_2018 = (
    age_group_41_50_2018.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_age_41_50_2018


# In[64]:


age_group_51_60_2018 = df_MM_clean_2018[df_MM_clean_2018['age group'] == '51-60']
# OD Matrix 2018 calculation using pivot table
matrix_age_51_60_2018 = (
    age_group_51_60_2018.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_age_51_60_2018


# In[65]:


age_group_above_61_2018 = df_MM_clean_2018[df_MM_clean_2018['age group'] == '61+']
# OD Matrix 2018 calculation using pivot table
matrix_age_above_61_2018 = (
    age_group_above_61_2018.assign(count=1)
    .pivot_table(index='FROM WARD', columns='TO WARD',
                 values="count", aggfunc="count")
    .fillna(0)
    .astype(int)
).sort_values('FROM WARD')

matrix_age_above_61_2018


# ...........................................................................................

# - Based on your observation, visualise selected OD matrices that show some trends/periodicity on a map. 

# In[31]:


import seaborn as sns


# In[32]:


# Heatmap general 2016
sns.heatmap(matrix_2016,cmap='crest')


# It shows that in general in 2016, most of the trips happened in ward 42. After that there are wards 34 and 43 and also the trips among these three wards.

# In[34]:


# Heatmap 19-30 in 2016
sns.heatmap(matrix_age_19_30_2016,cmap='crest')


# It shows that most of the young people's trips (19-30) in 2016 happened in ward 5. after that there are wards 34, 43, and 42 and trips among these wards.

# In[35]:


# Heatmap 31-40 in 2016
sns.heatmap(matrix_age_31_40_2016,cmap='crest')


# It shows that most of 31-40 people's trips in 2016 happened in ward 42. After that there are wards 43, 34 and 27 and also the trips among these wards.

# In[36]:


# Heatmap 41-50 in 2016
sns.heatmap(matrix_age_41_50_2016,cmap='crest')


# Almost the same pattern exists for 41-50 travelers.

# In[37]:


# Heatmap 51-60 in 2016
sns.heatmap(matrix_age_51_60_2016,cmap='crest')


# Almost the same pattern exists for 51-60 travelers.

# In[39]:


# Heatmap above 61 in 2016
sns.heatmap(matrix_age_above_61_2016,cmap='crest')


# Almost the same pattern exists for above 61 years old travelers.

# In conclusion, we can say that wards 42, 34, and 27 are the most important wards for most of the age groups but ward 5 is only attractive for young people and most of their trips happened there.

# ...........................................................................................

# In[78]:


# Heatmap general 2017
sns.heatmap(matrix_2017,cmap='crest')


# In general, for whole 2017, the most trips happened inside ward 42 and after that from ward 42 to ward 34. insode ward 34 and from ward 34 to 42 are comming after them.

# In[80]:


# Heatmap 0-18 in 2017
sns.heatmap(matrix_age_under_18_2017,cmap='crest')


# It shows that in 2017, although there were a little under 18 users, but most of their trips happened in ward 28.

# In[81]:


# Heatmap 19-30 in 2017
sns.heatmap(matrix_age_19_30_2017,cmap='crest')


# It shows that most of the yung people's trips (19-30) in 2017 happened in ward 5 and after that there are ward 42, 43, and 34.

# In[82]:


# Heatmap 31-40 in 2017
sns.heatmap(matrix_age_31_40_2017,cmap='crest')


# It shows that most of the 31-40 people trips in 2017 happened in ward 42. After that there are 43, 34 and also among these wards.

# In[83]:


# Heatmap 41-50 in 2017
sns.heatmap(matrix_age_41_50_2017,cmap='crest')


# It shows that most of 42-50 people's trips in 2017 happened in wards 42 and 34 and among these two wards.

# In[84]:


# Heatmap 51-60 in 2017
sns.heatmap(matrix_age_51_60_2017,cmap='crest')


# The same pattern exists for 51-60 people.

# In[86]:


# Heatmap above 61 in 2017
sns.heatmap(matrix_age_above_61_2017,cmap='crest')


# The same pattern exists for old people (above 61).

# ...........................................................................................

# In[37]:


# Heatmap general 2018
sns.heatmap(matrix_2018,cmap='crest')


# In[ ]:





# In[73]:


# Heatmap 19-30 in 2018
sns.heatmap(matrix_age_19_30_2018,cmap='crest')


# It shows that the most of the young people's trips (19-30) in 2018 happened inside ward 5. The rest of places respectively belong to ward 42, 34, and 44.

# In[72]:


# Heatmap 31-40 in 2018
sns.heatmap(matrix_age_31_40_2018,cmap='crest')


# It shows that most of 31-40 travelers' trips in 2018 happened in ward 42. The second place belongs to ward 44. Thus, we can see that ward 5 is not very attractive for this group however it was attractive for young people.

# In[71]:


# Heatmap 41-50 in 2018
sns.heatmap(matrix_age_41_50_2018,cmap='crest')


# It shows that 41-50 people's trips in 2018 happened in ward 42 and after that inside the ward 34. Additionally, the trips among these two wards (both ways) are also high. 

# In[70]:


# Heatmap 51-60 in 2018
sns.heatmap(matrix_age_51_60_2018,cmap='crest')


# It shows that the same pattern exists for people between 51-60.

# In[69]:


# Heatmap above 61 in 2018
sns.heatmap(matrix_age_above_61_2018,cmap='crest')


# It shows that, traveler above 61 years old, mostly travel inside ward 42 and after that from ward 42 to ward 34.

# In conclusion, We can say that ward 42 is one of the most important zones in micromobility and ward 34 comes after that. Also, most of the young people's mobility happened in ward 5  but this ward is not very bold for other age groups.

# ...........................................................................................

# - If a challenge is needed, students can also attempt to create a flowmap for the OD matrices.

# In[43]:


import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns

matrix_2016.index = matrix_2016.index.astype(int)
matrix_2016.columns = matrix_2016.columns.astype(int)

# Create a directed graph from the OD matrix
G = nx.DiGraph()

# Add nodes
for node in matrix_2016.index:
    G.add_node(node)

# Add edges
for from_node in matrix_2016.index:
    for to_node in matrix_2016.columns:
        weight = matrix_2016.loc[from_node, to_node]
        if weight > 0:
            G.add_edge(from_node, to_node, weight=weight)

# Draw the graph with a circular layout
pos = nx.circular_layout(G)

# Set node colors based on degree (number of connections)
node_colors = [G.degree(node) for node in G.nodes]

# Set edge colors based on weights
edge_colors = [G[from_node][to_node]['weight'] for from_node, to_node in G.edges]

# Draw nodes
nx.draw_networkx_nodes(G, pos, node_size=700, node_color=node_colors, cmap=plt.cm.Blues)

# Draw edges with weights
nx.draw_networkx_edges(G, pos, width=1, edge_color=edge_colors, edge_cmap=plt.cm.Greens, arrowsize=10)

# Add labels
nx.draw_networkx_labels(G, pos, font_size=8, font_color='black', font_weight='bold')

# Add colorbar for edge weights
edge_weights = nx.get_edge_attributes(G, 'weight')
cbar = plt.colorbar()
cbar.set_label('Flow Counts')

plt.title("Flowmap for OD Matrix 2017")
plt.show()


# In[44]:


import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns

matrix_2017.index = matrix_2017.index.astype(int)
matrix_2017.columns = matrix_2017.columns.astype(int)

# Create a directed graph from the OD matrix
G = nx.DiGraph()

# Add nodes
for node in matrix_2017.index:
    G.add_node(node)

# Add edges
for from_node in matrix_2017.index:
    for to_node in matrix_2017.columns:
        weight = matrix_2017.loc[from_node, to_node]
        if weight > 0:
            G.add_edge(from_node, to_node, weight=weight)

# Draw the graph with a circular layout
pos = nx.circular_layout(G)

# Set node colors based on degree (number of connections)
node_colors = [G.degree(node) for node in G.nodes]

# Set edge colors based on weights
edge_colors = [G[from_node][to_node]['weight'] for from_node, to_node in G.edges]

# Draw nodes
nx.draw_networkx_nodes(G, pos, node_size=700, node_color=node_colors, cmap=plt.cm.Blues)

# Draw edges with weights
nx.draw_networkx_edges(G, pos, width=1, edge_color=edge_colors, edge_cmap=plt.cm.Greens, arrowsize=10)

# Add labels
nx.draw_networkx_labels(G, pos, font_size=8, font_color='black', font_weight='bold')

# Add colorbar for edge weights
edge_weights = nx.get_edge_attributes(G, 'weight')
cbar = plt.colorbar()
cbar.set_label('Flow Counts')

plt.title("Flowmap for OD Matrix 2017")
plt.show()


# In[46]:


import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns

matrix_2018.index = matrix_2018.index.astype(int)
matrix_2018.columns = matrix_2018.columns.astype(int)

# Create a directed graph from the OD matrix
G = nx.DiGraph()

# Add nodes
for node in matrix_2018.index:
    G.add_node(node)

# Add edges
for from_node in matrix_2018.index:
    for to_node in matrix_2018.columns:
        weight = matrix_2018.loc[from_node, to_node]
        if weight > 0:
            G.add_edge(from_node, to_node, weight=weight)

# Draw the graph with a circular layout
pos = nx.circular_layout(G)

# Set node colors based on degree (number of connections)
node_colors = [G.degree(node) for node in G.nodes]

# Set edge colors based on weights
edge_colors = [G[from_node][to_node]['weight'] for from_node, to_node in G.edges]

# Draw nodes
nx.draw_networkx_nodes(G, pos, node_size=700, node_color=node_colors, cmap=plt.cm.Blues)

# Draw edges with weights
nx.draw_networkx_edges(G, pos, width=1, edge_color=edge_colors, edge_cmap=plt.cm.Greens, arrowsize=10)

# Add labels
nx.draw_networkx_labels(G, pos, font_size=8, font_color='black', font_weight='bold')

# Add colorbar for edge weights
edge_weights = nx.get_edge_attributes(G, 'weight')
cbar = plt.colorbar()
cbar.set_label('Flow Counts')

plt.title("Flowmap for OD Matrix 2017")
plt.show()


# In[ ]:




