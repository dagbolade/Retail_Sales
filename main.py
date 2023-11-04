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
category_dropdown = st.selectbox("Select Product Category", options=df["Product Category"].unique().tolist(), index=0)

filtered_df = df[(df["Age"] >= age_slider[0]) & (df["Age"] <= age_slider[1]) & (df["Product Category"] == category_dropdown)]

# Display raw data on demand
if st.checkbox('Show Filtered Raw Data'):
    st.subheader('Filtered Raw Data')
    st.write(filtered_df)

# Display total sales
total_sales = filtered_df["Total Amount"].sum()
st.subheader(f'Total Sales for {category_dropdown}: ${total_sales:,.2f}')

# Display sales by all product category using seaborn
st.subheader('Sales by Product Category')
sales_by_category = filtered_df.groupby("Product Category")["Total Amount"].sum()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=sales_by_category.index, y=sales_by_category.values, ax=ax, palette="Blues_d", hue=sales_by_category.index)
ax.set_ylabel('Total Sales Amount')
ax.set_xlabel('Product Category')
st.pyplot(fig)

# Display Gender based sales
# Sales by Gender
st.subheader('Sales by Gender')
gender_sales = df.groupby("Gender")["Total Amount"].sum().reset_index()
fig = px.bar(gender_sales, x='Gender', y='Total Amount', text='Total Amount',
             hover_data={'Total Amount': ':,.2f'}, labels={'Total Amount':'Total Sales'},
             color='Gender', color_discrete_map={'Female': 'pink', 'Male': 'blue'})
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

st.plotly_chart(fig)


