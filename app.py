import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(page_title="Ola Rides Dashboard", layout="wide")
@st.cache_data
def get_data():
df = pd.read_csv("OLA_DataSet.csv")
numeric_cols = ['Booking_Value', 'Ride_Distance', 'Driver_Ratings', 'Customer_Rating', 'V_TAT', 'C_TAT']
for col in numeric_cols:
if col in df.columns:
df[col] = pd.to_numeric(df[col], errors='coerce')
if 'Date' in df.columns:
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
return df
st.title("Ola Rides Analysis 🚗")
# Load data
df = get_data()
   
# ========== EDA SECTION ==========
   st.divider()
   st.header("Exploratory Data Analysis")
   
   # 1. SHAPE + MISSING VALUES
   st.subheader("1. Data Overview")
   col1, col2, col3 = st.columns(3)
   col1.metric("Total Rows", f"{len(df):,}")
   col2.metric("Total Columns", f"{len(df.columns)}")
   col3.metric("Missing Values", f"{df.isnull().sum().sum():,}")
   
   st.write("Missing values per column:")
   st.dataframe(df.isnull().sum().to_frame("Missing Count"))
   
   # 2. DATA TYPES + BASIC STATS
   st.subheader("2. Summary Stats")
   st.write("For numbers like Booking_Value, Ride_Distance:")
   st.dataframe(df.describe())
   
   st.write("For text columns like Status, Vehicle:")
   st.dataframe(df.describe(include='object'))
   
   # 3. DISTRIBUTIONS - 
   st.subheader("3. Distributions")
   num_cols = st.selectbox("Pick a numeric column to plot:", 
                           ['Booking_Value', 'Ride_Distance', 'Driver_Ratings', 'Customer_Rating', 'V_TAT', 'C_TAT'])
   fig = px.histogram(df, x=num_cols, nbins=50, title=f'Distribution of {num_cols}')
   st.plotly_chart(fig, use_container_width=True)
   
   # 4. RELATIONSHIPS - 
   st.subheader("4. Relationships")
   st.write("Does higher distance mean higher booking value?")
   fig = px.scatter(df.sample(min(2000, len(df))), x='Ride_Distance', y='Booking_Value', 
                    color='Vehicle_Type', title='Distance vs Price')
   st.plotly_chart(fig, use_container_width=True)
   
   # 5. GROUPED INSIGHTS -
   st.subheader("5. Grouped Insights")
   group_by = st.selectbox("Group data by:", ['Vehicle_Type', 'Booking_Status', 'Payment_Method'])
   grouped = df.groupby(group_by).agg({
       'Booking_Value': ['mean', 'sum', 'count'],
       'Ride_Distance': 'mean',
       'Driver_Ratings': 'mean'
   }).round(2)
   st.dataframe(grouped)
   
   # 6. TIME TRENDS - if Date column exists
   if 'Date' in df.columns:
       st.subheader("6. Trends Over Time")
       daily_rides = df.groupby(df['Date'].dt.date).size()
       st.line_chart(daily_rides)
