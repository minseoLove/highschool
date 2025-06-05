
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="TOP10 주식 분석", page_icon="📈", layout="wide")

st.title("📈 글로벌 시가총액 TOP10 - 최근 1년 주식 변화")

# TOP10 주식 심볼
stocks = {
    'AAPL': 'Apple',
    'MSFT': 'Microsoft', 
    'GOOGL': 'Google',
    'AMZN': 'Amazon',
    'NVDA': 'NVIDIA',
    'TSLA': 'Tesla',
    'META': 'Meta',
    'BRK-B': 'Berkshire',
    'TSM': 'TSMC',
    'V': 'Visa'
}

# 데이터 로딩
@st.cache_data
def get_stock_data():
    data = {}
    for symbol in stocks.keys():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1y")
            if not hist.empty:
                data[symbol] = hist
        except:
            continue
    return data

# 데이터 로드
with st.spinner("데이터 로딩 중..."):
    stock_data = get_stock_data()

# 차트 1: 주가 변화
st.subheader("💰 주가 변화 (1년)")
fig1 = go.Figure()

for symbol, data in stock_data.items():
    fig1.add_trace(go.Scatter(
        x=data.index,
        y=data['Close'],
        name=f"{symbol} ({stocks[symbol]})",
        line=dict(width=2)
    ))

fig1.update_layout(
    height=500,
    xaxis_title="날짜",
    yaxis_title="주가 ($)",
    hovermode='x unified'
)
st.plotly_chart(fig1, use_container_width=True)

# 차트 2: 수익률 비교
st.subheader("📊 누적 수익률 비교")
fig2 = go.Figure()

for symbol, data in stock_data.items():
    returns = data['Close'].pct_change().fillna(0)
    cum_returns = (1 + returns).cumprod() - 1
    
    fig2.add_trace(go.Scatter(
        x=data.index,
        y=cum_returns * 100,
        name=symbol,
        line=dict(width=2)
    ))

fig2.update_layout(
    height=500,
    xaxis_title="날짜",
    yaxis_title="누적 수익률 (%)",
    hovermode='x unified'
)
st.plotly_chart(fig2, use_container_width=True)

# 수익률 순위
st.subheader("🏆 1년 수익률 순위")
performance = {}
for symbol, data in stock_data.items():
    start_price = data['Close'].iloc[0]
    end_price = data['Close'].iloc[-1]
    return_pct = ((end_price - start_price) / start_price) * 100
    performance[symbol] = return_pct

perf_df = pd.DataFrame(list(performance.items()), columns=['주식', '수익률(%)'])
perf_df = perf_df.sort_values('수익률(%)', ascending=False)
perf_df['회사명'] = perf_df['주식'].map(stocks)
perf_df = perf_df[['주식', '회사명', '수익률(%)']]
perf_df['수익률(%)'] = perf_df['수익률(%)'].round(2)

st.dataframe(perf_df, use_container_width=True, hide_index=True)

# 차트 3: 수익률 바차트
fig3 = go.Figure(data=[
    go.Bar(
        x=perf_df['주식'],
        y=perf_df['수익률(%)'],
        text=perf_df['수익률(%)'].round(1),
        textposition='auto',
        marker_color=['green' if x > 0 else 'red' for x in perf_df['수익률(%)']]
    )
])

fig3.update_layout(
    title="1년 수익률 비교",
    xaxis_title="주식",
    yaxis_title="수익률 (%)",
    height=400
)
st.plotly_chart(fig3, use_container_width=True)
