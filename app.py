import streamlit as st
import plotly.express as px
import pandas as pd

# 網頁標題
st.title("📊 圖書館讀者提問趨勢分析")

# 1. 自動讀取並處理檔案
# 使用 st.cache_data 可以讓 Streamlit 記住資料，不用每次選單切換都重新讀取 1.3 萬筆資料
@st.cache_data
def load_and_process_data():
    try:
        # 讀取您的 CSV 檔案 (自動處理中文編碼)
        df = pd.read_csv("使用者問題分析結果.csv", encoding="utf-8-sig")
        
        # 確保年度被視為文字，這樣在圖表和下拉選單中才不會變成有小數點的數字 (如 2023.0)
        df['年度'] = df['年度'].astype(str)
        
        # 【核心魔法】：自動計算數量
        # 依照「年度」與「問題類別」進行分組，並計算每一組的筆數 (size)，最後將結果欄位命名為「數量」
        summary_df = df.groupby(['年度', '問題類別']).size().reset_index(name='數量')
        
        return summary_df
    
    except FileNotFoundError:
        st.error("❌ 找不到 '使用者問題分析結果.csv' 檔案。請確認檔案名稱正確，且與程式碼放在同一資料夾！")
        st.stop() # 停止執行

# 載入匯總後的資料
df_summary = load_and_process_data()

# 2. 建立側邊欄或上方的互動下拉式選單
st.markdown("### 🔍 資料篩選")
years = sorted(df_summary["年度"].unique().tolist())
years.insert(0, "所有年度") # 在選單最前面加入「所有年度」
selected_year = st.selectbox("請選擇您想查看的年度：", years)

# 3. 根據選單結果過濾資料
if selected_year == "所有年度":
    filtered_df = df_summary
    chart_title = "歷年各問題類別統計總覽 (分組比較)"
else:
    filtered_df = df_summary[df_summary["年度"] == selected_year]
    chart_title = f"{selected_year} 年度各問題類別統計"

# 4. 繪製互動式圖表 (使用 Plotly)
fig = px.bar(
    filtered_df, 
    x="問題類別", 
    y="數量", 
    color="年度",       # 用顏色區分不同年度
    barmode="group",    # group: 並排顯示；如果您想要疊加起來，可以改為 "relative"
    text="數量",        # 在柱狀圖上直接顯示數字
    title=chart_title,
    height=600          # 設定圖表高度，讓類別文字不擁擠
)

# 優化圖表外觀：讓 X 軸的文字傾斜，避免字太長擠在一起
fig.update_layout(xaxis_tickangle=-45)

# 5. 將圖表渲染到網頁上
st.plotly_chart(fig, use_container_width=True)

# (選用) 在網頁下方顯示具體的數據表格，方便直接查看數字
with st.expander("📄 查看詳細數據表格"):
    st.dataframe(filtered_df, use_container_width=True)