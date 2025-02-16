import streamlit as st
import pandas as pd

def calculate_auc_ratio(CR, IR):
    return 1 / (1 - CR * IR)

def calculate_ir(CR, AUCratio):
    return (AUCratio - 1) / (AUCratio * CR)

def calculate_auc_ratio_ic(CR, IC):
    return 1 / (1 + CR * IC)

def calculate_ic(CR, AUCratio):
    return (1 - AUCratio) / (AUCratio * CR)

st.title("薬物相互作用 計算ツール")

# 入力欄
col1, col2 = st.columns(2)
if "CR" not in st.session_state:
    st.session_state.CR = 0.0
if "IR" not in st.session_state:
    st.session_state.IR = 0.0
if "IC" not in st.session_state:
    st.session_state.IC = 0.0
if "AUCratio" not in st.session_state:
    st.session_state.AUCratio = 0.0

CR = col1.number_input("CR (基質寄与率)", min_value=0.0, step=0.01, format="%.2f", key="CR")
IR = col2.number_input("IR (阻害率)", min_value=0.0, step=0.01, format="%.2f", key="IR")
IC = col1.number_input("IC (誘導率)", step=0.01, format="%.2f", key="IC")
AUCratio = col2.number_input("AUCratio", min_value=0.0, step=0.01, format="%.2f", key="AUCratio")

# 計算処理
if st.button("計算"):
    results = {}
    if CR > 0 and IR > 0:
        results["AUCratio"] = calculate_auc_ratio(CR, IR)
    if CR > 0 and AUCratio > 0:
        results["IR"] = calculate_ir(CR, AUCratio)
    if CR > 0 and IC > 0:
        results["AUCratio (誘導)"] = calculate_auc_ratio_ic(CR, IC)
    if CR > 0 and AUCratio > 0:
        results["IC"] = calculate_ic(CR, AUCratio)
    
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
        st.warning("計算に必要な値を入力してください。")

# Reset ボタン
if st.button("Reset"):
    st.session_state["CR"] = 0.0
    st.session_state["IR"] = 0.0
    st.session_state["IC"] = 0.0
    st.session_state["AUCratio"] = 0.0
