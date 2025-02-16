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

# 入力欄
col1, col2 = st.columns(2)

CR = col1.number_input("CR (基質寄与率)", min_value=0.0, step=0.01, format="%.2f", key="CR")
AUCratio = col2.number_input("AUCratio", min_value=0.0, step=0.01, format="%.2f", key="AUCratio")
IR = col1.number_input("IR (阻害率)", min_value=0.0, step=0.01, format="%.2f", key="IR")
IC = col2.number_input("IC (誘導率)", step=0.01, format="%.2f", key="IC")

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
