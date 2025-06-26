import yfinance as yf
import streamlit as st
import plotly.express as px
import pandas as pd
from sklearn.linear_model import LinearRegression
st.title("Stock Data and Price Prediction")
tickers = ['SBIN.NS', 'RELIANCE.NS',
'TCS.NS','HDFC.NS','INFY.NS','ICICIBANK.NS','TATAMOTORS.NS','HINDUNILVR.NS','MARUTI.NS','BAJFINANCE.NS']
selected_ticker1 = st.selectbox("Choose the first stock ticker:", tickers)
selected_ticker2 = st.selectbox("Choose the second stock ticker:", tickers)
stock1 = yf.Ticker(selected_ticker1)
stock_info1 = stock1.info
current_price1 = stock_info1.get('currentPrice', 'N/A')
day_high1 = stock_info1.get('dayHigh', 'N/A')
day_low1 = stock_info1.get('dayLow', 'N/A')
previous_close1 = stock_info1.get('previousClose', 'N/A')
volume1=stock_info1.get('volume','N/A')
stock2 = yf.Ticker(selected_ticker2)
stock_info2 = stock2.info
current_price2 = stock_info2.get('currentPrice', 'N/A')
day_high2 = stock_info2.get('dayHigh', 'N/A')
day_low2 = stock_info2.get('dayLow', 'N/A')
previous_close2 = stock_info2.get('previousClose', 'N/A')
volume2=stock_info2.get('volume','N/A')
st.subheader("Current Stock Data")
col1, col2 = st.columns(2)
with col1:
st.write(f"**Current Price of {selected_ticker1}:** {current_price1}")
st.write(f"**Day High:** {day_high1}")
st.write(f"**Day Low:** {day_low1}")
st.write(f"**Previous Close:** {previous_close1}")
st.write(f"**Volume :** {volume1}")
with col2:
st.write(f"**Current Price of {selected_ticker2}:** {current_price2}")
st.write(f"**Day High:** {day_high2}")
st.write(f"**Day Low:** {day_low2}")
st.write(f"**Previous Close:** {previous_close2}")
st.write(f"**Volume :** {volume2}")
stock_hist1 = stock1.history(period="5y")
stock_hist2 = stock2.history(period="5y")
st.subheader("Historical Data for the Last 5 years")
col3, col4 = st.columns(2)
with col3:
st.write(f"**{selected_ticker1} Historical Data**")
st.write(stock_hist1)
with col4:
st.write(f"**{selected_ticker2} Historical Data**")
st.write(stock_hist2)
fig1 = px.line(stock_hist1, x=stock_hist1.index, y='Close', title=f'{selected_ticker1} StockPrice-Last 5 years')
st.plotly_chart(fig1)
fig2 = px.line(stock_hist2, x=stock_hist2.index, y='Close', title=f'{selected_ticker2} StockPrice-Last 5 years')
st.plotly_chart(fig2)
fig_open1 = px.line(stock_hist1, x=stock_hist1.index, y='Open', title=f'{selected_ticker1}OpeningPrices - Last 5 years')
st.plotly_chart(fig_open1)
fig_open2 = px.line(stock_hist2, x=stock_hist2.index, y='Open', title=f'{selected_ticker2}OpeningPrices - Last 5 years')
st.plotly_chart(fig_open2)
fig_high1 = px.line(stock_hist1, x=stock_hist1.index, y='High', title=f'{selected_ticker1}HighPrices - Last 5 years')
st.plotly_chart(fig_high1)
fig_high2 = px.line(stock_hist2, x=stock_hist2.index, y='High', title=f'{selected_ticker2}High
Prices - Last 5 years')
st.plotly_chart(fig_high2)
fig_low1 = px.line(stock_hist1, x=stock_hist1.index, y='Low', title=f'{selected_ticker1} LowPrices- Last 5 years')
st.plotly_chart(fig_low1)
fig_low2 = px.line(stock_hist2, x=stock_hist2.index, y='Low', title=f'{selected_ticker2} LowPrices- Last 5 years')
st.plotly_chart(fig_low2)
stock_hist1 = stock_hist1.dropna()
X1 = stock_hist1[['Open', 'High', 'Low']]
y1 = stock_hist1['Close']
model1 = LinearRegression()
model1.fit(X1, y1)
stock_hist2 = stock_hist2.dropna()
X2 = stock_hist2[['Open', 'High', 'Low']]
y2 = stock_hist2['Close']
model2 = LinearRegression()
model2.fit(X2, y2)
if st.button('Compare and Predict'):
st.subheader("Input Values for Prediction")
open_price1 = st.number_input(f'{selected_ticker1} Open Price', value=float(stock_hist1['Open'].iloc[-1]))
high_price1 = st.number_input(f'{selected_ticker1} High Price', value=float(stock_hist1['High'].iloc[-1]))
low_price1 = st.number_input(f'{selected_ticker1} LowPrice', value=float(stock_hist1['Low'].iloc[-1]))
input_data1 = pd.DataFrame({
'Open': [open_price1],
'High': [high_price1],
'Low': [low_price1]
})
predicted_close1 = model1.predict(input_data1)
st.write(f"**Predicted Close Price for {selected_ticker1}:** {predicted_close1[0]}")
open_price2 = st.number_input(f'{selected_ticker2} Open Price', value=float(stock_hist2['Open'].iloc[-1]))
high_price2 = st.number_input(f'{selected_ticker2} High Price', value=float(stock_hist2['High'].iloc[-1]))
low_price2 = st.number_input(f'{selected_ticker2} LowPrice', value=float(stock_hist2['Low'].iloc[-1]))
input_data2 = pd.DataFrame({
'Open': [open_price2],
'High': [high_price2],
'Low': [low_price2]
})
predicted_close2 = model2.predict(input_data2)
st.write(f"**Predicted Close Price for {selected_ticker2}:** {predicted_close2[0]}")
fig_prediction1 = px.line(
stock_hist1, x=stock_hist1.index, y='Close', title=f'Predicted Close Price for {selected_ticker1}')
fig_prediction1.add_scatter(x=input_data1.index, y=predicted_close1, mode='markers', name='Predicted Close')
st.plotly_chart(fig_prediction1)
fig_prediction2 = px.line(
stock_hist2, x=stock_hist2.index, y='Close', title=f'Predicted Close Price for {selected_ticker2}')
fig_prediction2.add_scatter(x=input_data2.index, y=predicted_close2, mode='markers', name='Predicted Close')
st.plotly_chart(fig_prediction2)
fig_prediction1 = px.line(
stock_hist1, x=stock_hist1.index, y='Volume', title=f'Volume details for {selected_ticker1}')
st.plotly_chart(fig_prediction1)
fig_prediction2 = px.line(
stock_hist2, x=stock_hist2.index, y='Volume', title=f'volume details for {selected_ticker2}')
st.plotly_chart(fig_prediction2)
if predicted_close1[0] > predicted_close2[0]:
st.success(f"**Recommendation:** Based on the predicted close prices, {selected_ticker1}isrecommended.")
else:
st.success(f"**Recommendation:** Based on the predicted close prices, {selected_ticker2}isrecommended.")
