import streamlit as st
import pandas as pd

def calculate_auc_ratio(CR, IR):
    if CR * IR >= 1:
        return None
    return 1 / (1 - CR * IR)

def calculate_ir(CR, AUCratio):
    if AUCratio * CR == 0:
        return None
    return (AUCratio - 1) / (AUCratio * CR)

def calculate_cr_from_ir(AUCratio, IR):
    if AUCratio * IR == 0:
        return None
    return (AUCratio - 1) / (AUCratio * IR)

def calculate_auc_ratio_ic(CR, IC):
    return 1 / (1 + CR * IC)

def calculate_ic(CR, AUCratio):
    if AUCratio * CR == 0:
        return None
    return (1 - AUCratio) / (AUCratio * CR)

def calculate_cr_from_ic(AUCratio, IC):
    if AUCratio * IC == 0:
        return None
    return (1 - AUCratio) / (AUCratio * IC)

st.title("薬物相互作用 計算ツール")

# レイアウト調整
col1, col2, col3 = st.columns([2, 2, 1])

# 入力欄
CR = col1.number_input("CR (基質寄与率)", min_value=0.0, step=0.01, format="%.2f", key="CR")
AUCratio = col2.number_input("AUCratio", min_value=0.0, step=0.01, format="%.2f", key="AUCratio")
IR = col1.number_input("IR (阻害率)", min_value=0.0, step=0.01, format="%.2f", key="IR")
IC = col2.number_input("IC (誘導率)", step=0.01, format="%.2f", key="IC")

# 簡易電卓
with col3:
    st.write("### 電卓")
    calc_value = st.text_input("", "")
    if st.button("7"): calc_value += "7"
    if st.button("8"): calc_value += "8"
    if st.button("9"): calc_value += "9"
    if st.button("4"): calc_value += "4"
    if st.button("5"): calc_value += "5"
    if st.button("6"): calc_value += "6"
    if st.button("1"): calc_value += "1"
    if st.button("2"): calc_value += "2"
    if st.button("3"): calc_value += "3"
    if st.button("0"): calc_value += "0"
    if st.button("."): calc_value += "."
    if st.button("C"): calc_value = ""
    if st.button("Enter"):
        try:
            eval_result = eval(calc_value)
            st.write(f"結果: {eval_result}")
        except:
            st.write("エラー")

# 計算処理
if st.button("計算"):
    results = {}
    
    if IR > 0 and IC == 0:
        if CR > 0 and IR > 0:
            results["AUCratio"] = calculate_auc_ratio(CR, IR)
        if CR > 0 and AUCratio > 0:
            results["IR"] = calculate_ir(CR, AUCratio)
        if AUCratio > 0 and IR > 0:
            results["CR"] = calculate_cr_from_ir(AUCratio, IR)
    
    if IC > 0 and IR == 0:
        if CR > 0 and IC > 0:
            results["AUCratio (誘導)"] = calculate_auc_ratio_ic(CR, IC)
        if CR > 0 and AUCratio > 0:
            results["IC"] = calculate_ic(CR, AUCratio)
        if AUCratio > 0 and IC > 0:
            results["CR"] = calculate_cr_from_ic(AUCratio, IC)
    
    if IR == 0 and IC == 0 and CR > 0 and AUCratio > 0:
        results["IR"] = calculate_ir(CR, AUCratio)
        results["IC"] = calculate_ic(CR, AUCratio)
    
    results = {k: v for k, v in results.items() if v is not None}  # 無効な値を除外
    
    if results:
        st.write("### 計算結果")
        for key, value in results.items():
            st.write(f"{key}: {value:.4f}")
        
        if "history" not in st.session_state:
            st.session_state.history = []
        st.session_state.history.append({**{"CR": CR, "IR": IR, "IC": IC, "AUCratio": AUCratio}, **results})
        
        st.write("### 過去の計算結果")
        history_df = pd.DataFrame(st.session_state.history)
        st.dataframe(history_df)
    else:
        st.warning("計算に必要な値を入力するか、適切な値を設定してください。")
