import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st

# Load the dataset
file_path = 'harshit.data.csv'  # Replace with your file path
data = pd.read_csv(file_path)

# Strip whitespace from column names (if any)
data.columns = data.columns.str.strip()

# Streamlit page configuration
st.set_page_config(
    page_title="Sales Data Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set custom theme colors
st.markdown(
    """
    <style>
    .main { background-color: #F9F9F9; }
    .sidebar .sidebar-content { background-color: #2C3E50; color: white; }
    h1, h2, h3 { color: #2E86C1; }
    </style>
    """,
    unsafe_allow_html=True
)

# 1. Most popular product categories
def most_popular_categories():
    product_counts = data['Category'].value_counts().reset_index()
    product_counts.columns = ['Category', 'Count']

    fig = px.bar(
        product_counts,
        x='Category',
        y='Count',
        title="Most Popular Product Categories",
        labels={"Count": "Number of Purchases", "Category": "Product Category"},
        color='Count',
        text='Count',
    )
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

# 2. Most common payment method across product categories
def common_payment_method():
    payment_method = data.groupby('Category')['Payment_Method'].agg(lambda x: x.mode()[0]).reset_index()
    payment_method.columns = ['Category', 'Most Common Payment Method']

    st.subheader('Most Common Payment Method Across Categories')
    st.dataframe(payment_method, use_container_width=True)

# 3. Product categories generating the highest revenue
def highest_revenue_categories():
    revenue_by_category = data.groupby('Category')['Final_Price(Rs.)'].sum().reset_index()
    revenue_by_category = revenue_by_category.sort_values('Final_Price(Rs.)', ascending=False)
    revenue_by_category.columns = ['Category', 'Total Revenue (₹)']

    fig = px.bar(
        revenue_by_category,
        x='Category',
        y='Total Revenue (₹)',
        title="Categories Generating the Highest Revenue",
        labels={"Total Revenue (₹)": "Revenue (₹)", "Category": "Product Category"},
        color='Total Revenue (₹)',
        text='Total Revenue (₹)',
    )
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)



# 5. Products consistently having the highest discounts
def highest_discounted_products():
    product_discounts = data.groupby('Product_ID')['Discount (%)'].mean().sort_values(ascending=False).head(10).reset_index()
    product_discounts.columns = ['Product ID', 'Average Discount (%)']

    fig = px.bar(
        product_discounts,
        x='Product ID',
        y='Average Discount (%)',
        title="Products with the Highest Discounts",
        labels={"Average Discount (%)": "Discount (%)", "Product Name": "Product Name"},
        color='Average Discount (%)',
        text='Average Discount (%)',
    )
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

# 6. Average price before and after discounts for each product category
def avg_price_before_after_discount():
    data['Price_Before_Discount'] = data['Final_Price(Rs.)'] / (1 - data['Discount (%)'] / 100)
    avg_prices = data.groupby('Category')[['Price_Before_Discount', 'Final_Price(Rs.)']].mean().reset_index()
    avg_prices.columns = ['Category', 'Average Price Before Discount (₹)', 'Average Final Price (₹)']

    fig = px.bar(
        avg_prices.melt(id_vars='Category', var_name='Price Type', value_name='Average Price (₹)'),
        x='Category',
        y='Average Price (₹)',
        color='Price Type',
        barmode='group',
        title="Average Prices Before and After Discounts by Category",
        text='Average Price (₹)',
    )
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

# 7. Users who purchase more frequently or spend more on average
def user_purchase_spending():
    user_spending = data.groupby('User_ID')['Final_Price(Rs.)'].sum().sort_values(ascending=False).head(10).reset_index()
    user_purchases = data.groupby('User_ID')['Product_ID'].count().sort_values(ascending=False).head(10).reset_index()

    user_spending.columns = ['User ID', 'Total Spending (₹)']
    user_purchases.columns = ['User ID', 'Total Purchases']

    st.subheader('Top 10 Users by Total Spending')
    fig1 = px.bar(
        user_spending,
        x='User ID',
        y='Total Spending (₹)',
        title="Top 10 Users by Spending",
        text='Total Spending (₹)',
        color='Total Spending (₹)'
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader('Top 10 Users by Total Purchases')
    fig2 = px.bar(
        user_purchases,
        x='User ID',
        y='Total Purchases',
        title="Top 10 Users by Purchases",
        text='Total Purchases',
        color='Total Purchases'
    )
    st.plotly_chart(fig2, use_container_width=True)

# 8. Average basket value per transaction
def avg_basket_value():
    average_basket_value = data['Final_Price(Rs.)'].mean()
    st.metric("Average Basket Value per Transaction", f"₹{average_basket_value:,.2f}")

# Streamlit UI layout
def main():
    st.title("Sales Data Analysis Dashboard")
    st.sidebar.title("Analysis Options")

    # Sidebar options to select different analyses
    options = [
        "Most Popular Categories",
        "Most Common Payment Method Across Categories",
        "Categories Generating the Highest Revenue",
        
        "Products Consistently Having the Highest Discounts",
        "Average Price Before and After Discounts by Product Category",
        "Users Who Purchase More Frequently or Spend More",
        "Average Basket Value per Transaction"
    ]
    
    selection = st.sidebar.selectbox("Choose Analysis", options)

    if selection == "Most Popular Categories":
        most_popular_categories()
    elif selection == "Most Common Payment Method Across Categories":
        common_payment_method()
    elif selection == "Categories Generating the Highest Revenue":
        highest_revenue_categories()
    elif selection == "Products Consistently Having the Highest Discounts":
        highest_discounted_products()
    elif selection == "Average Price Before and After Discounts by Product Category":
        avg_price_before_after_discount()
    elif selection == "Users Who Purchase More Frequently or Spend More":
        user_purchase_spending()
    elif selection == "Average Basket Value per Transaction":
        avg_basket_value()

if __name__ == "__main__":
    main()
