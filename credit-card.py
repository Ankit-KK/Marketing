import streamlit as st
import pandas as pd
import plotly.express as px

# Sample Data (Replace this with your actual dataset)
data = pd.read_csv("Marketing_data.csv")

# Create the figures
fig_balance_freq = px.histogram(data, x='BALANCE_FREQUENCY', nbins=14, title='Distribution of Balance Frequencies')
fig_oneoff_vs_installments = px.scatter(data, x='ONEOFF_PURCHASES', y='INSTALLMENTS_PURCHASES', title='One-Off vs Installment Purchases', trendline='ols')
fig_cash_advance_freq = px.histogram(data, x='CASH_ADVANCE_FREQUENCY', nbins=20, title='Distribution of Cash Advance Frequency')
fig_cash_advance_trx = px.histogram(data, x='CASH_ADVANCE_TRX', nbins=20, title='Distribution of Cash Advance Transactions')
fig_purchase_freq = px.density_heatmap(data, x='PURCHASES_FREQUENCY', y='PURCHASES_INSTALLMENTS_FREQUENCY', title='Purchase Frequency vs Installments Frequency', nbinsx=16, nbinsy=16)
correlation_matrix = data.corr(numeric_only=True)
fig_corr_heatmap = px.imshow(correlation_matrix, text_auto=True, title='Correlation Heatmap', width=1000, height=1000)
fig_payments_tenure = px.line(data, x='TENURE', y='PAYMENTS', title='Payments by Tenure').update_layout(height=600, width=800)
fig_min_payments = px.histogram(data, x='MINIMUM_PAYMENTS', nbins=10, title='Distribution of Minimum Payments')

# Distribution of Credit Limit
fig_credit_limit = px.histogram(data, x='CREDIT_LIMIT', nbins=30, title='Distribution of Credit Limit')
fig_credit_limit.update_layout(xaxis_title='Credit Limit', yaxis_title='Count')

# Scatter Plot of Balance vs Purchases
fig_balance_vs_purchases = px.scatter(data, x='BALANCE', y='PURCHASES',
                                      title='Balance vs Purchases',
                                      trendline='ols')
fig_balance_vs_purchases.update_layout(xaxis_title='Balance', yaxis_title='Purchases')

# Box Plot of Payments by Tenure
fig_payments_by_tenure = px.box(data, x='TENURE', y='PAYMENTS',
                                title='Payments by Tenure')
fig_payments_by_tenure.update_layout(xaxis_title='Tenure (months)', yaxis_title='Payments')

# Bar Chart of Total Purchases by Tenure
total_purchases_tenure = data.groupby('TENURE')['PURCHASES'].sum().reset_index()
fig_total_purchases_tenure = px.bar(total_purchases_tenure, x='TENURE', y='PURCHASES',
                                    title='Total Purchases by Tenure')
fig_total_purchases_tenure.update_layout(xaxis_title='Tenure (months)', yaxis_title='Total Purchases')

# Pie Chart of Full Payment Proportion
full_payment_proportion = data['PRC_FULL_PAYMENT'].apply(lambda x: 'Full Payment' if x == 1 else 'Partial Payment').value_counts().reset_index()
full_payment_proportion.columns = ['Payment Type', 'Count']
full_payment_proportion = full_payment_proportion.sort_values(by='Count', ascending=False)  # Sort by count

# Create the pie chart
fig_full_payment_proportion = px.pie(
    full_payment_proportion,
    values='Count',
    names='Payment Type',
    title='Proportion of Full Payments',
    color='Payment Type',
    color_discrete_map={'Full Payment': 'green', 'Partial Payment': 'orange'},
    hole=0.6  # Adjust the hole size
)

# Add labels and percentages
fig_full_payment_proportion.update_traces(
    textinfo='percent+value',
    textfont_size=14,
    hoverinfo='label+percent+value',
    marker=dict(
        line=dict(color='#FFFFFF', width=2)  
    )
)

# Create a sunburst plot as shadow
fig_shadow = px.sunburst(
    full_payment_proportion,
    names='Payment Type',
    values='Count',
    color_discrete_sequence=['gray', 'gray']
)
fig_shadow.update_traces(marker=dict(line=dict(width=0)))
fig_shadow.update_layout(margin=dict(t=0, l=0, r=0, b=0))

# Add the shadow to the pie chart
fig_full_payment_proportion.add_trace(fig_shadow.data[0])

# Customize layout
fig_full_payment_proportion.update_layout(
    showlegend=True,
    legend=dict(
        x=0.8,
        y=1,
        traceorder='normal',
        font=dict(
            family='sans-serif',
            size=14,
            color='black'
        )
    ),
    margin=dict(l=50, r=50, t=80, b=50)
)

# Histogram of Payments
fig_payments_histogram = px.histogram(data, x='PAYMENTS', nbins=30, title='Distribution of Payments')
fig_payments_histogram.update_layout(xaxis_title='Payments', yaxis_title='Count')

# Box Plot of Minimum Payments by Credit Limit
fig_min_payments_credit_limit = px.box(data, x='CREDIT_LIMIT', y='MINIMUM_PAYMENTS',
                                       title='Minimum Payments by Credit Limit')
fig_min_payments_credit_limit.update_layout(xaxis_title='Credit Limit', yaxis_title='Minimum Payments')

import streamlit as st

# Streamlit App
st.title("Credit Card Analysis Dashboard")

# Sidebar with options
option = st.sidebar.radio('Choose a visualization', ['Credit Limits', 'Balance vs Purchases', 'Payments Analysis', 'Purchases by Tenure', 'Balance Frequency', 'One-Off vs Installments', 'Cash Advance', 'Purchase Frequency', 'Correlation Heatmap', 'Payments by Tenure', 'Minimum Payments'])

# Render selected visualization
if option == 'Credit Limits':
    st.plotly_chart(fig_credit_limit)
elif option == 'Balance vs Purchases':
    st.plotly_chart(fig_balance_vs_purchases)
elif option == 'Payments Analysis':
    st.subheader("Payments Analysis")
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_payments_by_tenure)
    col2.plotly_chart(fig_full_payment_proportion)
    col1.plotly_chart(fig_payments_histogram)
    col2.plotly_chart(fig_min_payments_credit_limit)
elif option == 'Purchases by Tenure':
    st.plotly_chart(fig_total_purchases_tenure)
elif option == 'Balance Frequency':
    st.plotly_chart(fig_balance_freq)
elif option == 'One-Off vs Installments':
    st.plotly_chart(fig_oneoff_vs_installments)
elif option == 'Cash Advance':
    st.subheader("Cash Advance Analysis")
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_cash_advance_freq)
    col2.plotly_chart(fig_cash_advance_trx)
elif option == 'Purchase Frequency':
    st.plotly_chart(fig_purchase_freq)
elif option == 'Correlation Heatmap':
    st.plotly_chart(fig_corr_heatmap)
elif option == 'Payments by Tenure':
    st.plotly_chart(fig_payments_tenure)
elif option == 'Minimum Payments':
    st.plotly_chart(fig_min_payments)
