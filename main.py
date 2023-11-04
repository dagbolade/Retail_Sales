import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
# Load data
@st.cache_data
def load_data():
    data = pd.read_excel("retail_sales_dataset.xlsx")
    return data

df = load_data()

# Title of the dashboard
st.title('Retail Sales Dashboard')

# Interactive Filters
age_slider = st.slider("Select Age Range", int(df["Age"].min()), int(df["Age"].max()), (18, 64))

# Multiselect for product category
selected_categories = st.multiselect('Select Product Category', options=df['Product Category'].unique())

# Filter the dataframe based on selected categories and age range
if selected_categories:
    # If categories are selected, filter by both age and category
    filtered_df = df[(df["Age"] >= age_slider[0]) & (df["Age"] <= age_slider[1])]
    filtered_df = filtered_df[filtered_df['Product Category'].isin(selected_categories)]
else:
    # If no categories are selected, filter by age only
    filtered_df = df[(df["Age"] >= age_slider[0]) & (df["Age"] <= age_slider[1])]



# Display raw data on demand
if st.checkbox('Show Filtered Raw Data'):
    st.subheader('Filtered Raw Data')
    st.write(filtered_df)

# Display total sales
total_sales = filtered_df["Total Amount"].sum()
st.subheader(f'Total Sales for {selected_categories}: ${total_sales:,.2f}')

# Display total quantity of products sold
total_quantity = filtered_df["Quantity"].sum()
st.subheader(f'Total Quantity of Products Sold for {selected_categories}: {total_quantity:,.2f}')

# Display total number of customers
total_customers = filtered_df["Customer ID"].nunique()
st.subheader(f'Total Number of Customers for {selected_categories}: {total_customers:,.2f}')



# Display sales by all product category using seaborn
st.subheader('Sales by Product Category')
sales_by_category = filtered_df.groupby("Product Category")["Total Amount"].sum()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=sales_by_category.index, y=sales_by_category.values, ax=ax, palette="Blues_d", hue=sales_by_category.index)
ax.set_ylabel('Total Sales Amount')
ax.set_xlabel('Product Category')
st.pyplot(fig)

# Display Gender based sales

st.subheader('Sales by Gender')
gender_sales = df.groupby("Gender")["Total Amount"].sum().reset_index()
fig = px.bar(gender_sales, x='Gender', y='Total Amount', text='Total Amount',
             hover_data={'Total Amount': ':,.2f'}, labels={'Total Amount':'Total Sales'},
             color='Gender', color_discrete_map={'Female': 'pink', 'Male': 'blue'})
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

st.plotly_chart(fig)

# display sales trends over time
st.subheader("Sales Trends Over Time")
time_series = df.groupby('Date')['Total Amount'].sum().reset_index()
fig = px.line(time_series, x='Date', y='Total Amount', labels={'Total Amount': 'Total Sales'})
st.plotly_chart(fig)


#display the purchase by age group
st.subheader('Purchase by Age Group')
age_group_sales = df.groupby("Age")["Total Amount"].sum().reset_index()
fig = px.bar(age_group_sales, x='Age', y='Total Amount', text='Total Amount',
             hover_data={'Total Amount': ':,.2f'}, labels={'Total Amount':'Total Sales'},
             color='Age', color_discrete_map={'18-24': 'pink', '25-34': 'blue', '35-44': 'green', '45-54': 'red', '55-64': 'yellow'})
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

st.plotly_chart(fig)

# display the quantity of products sold by product category

st.subheader('Quantity of Products Sold by Product Category')
quantity_by_category = df.groupby("Product Category")["Quantity"].sum().reset_index()
fig = px.bar(quantity_by_category, x='Product Category', y='Quantity', text='Quantity',
             hover_data={'Quantity': ':,.2f'}, labels={'Quantity':'Quantity of Products Sold'},
             color='Product Category', color_discrete_map={'Furniture': 'pink', 'Office Supplies': 'blue', 'Technology': 'green'})
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

st.plotly_chart(fig)

# display what products category generated the highest revenue
st.subheader('Product Category that Generated the Highest Revenue')
category_revenue = df.groupby("Product Category")["Total Amount"].sum().reset_index()
fig = px.pie(category_revenue, values='Total Amount', names='Product Category', title='Product Category that Generated the Highest Revenue')
st.plotly_chart(fig)


