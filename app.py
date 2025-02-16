import streamlit as st
import pandas as pd

def calculate_value(known_values):
    CR = known_values.get("CR")
    IR = known_values.get("IR")
    IC = known_values.get("IC")
    AUCratio = known_values.get("AUCratio")

    if CR is not None and IR is not None:
        return {"AUCratio": 1 / (1 - CR * IR)}
    elif CR is not None and AUCratio is not None:
        return {"IR": (AUCratio - 1) / (AUCratio * CR)}
    elif CR is not None and IC is not None:
        return {"AUCratio": 1 / (1 + CR * IC)}
    elif CR is not None and AUCratio is not None:
        return {"IC": (1 - AUCratio) / (AUCratio * CR)}
    else:
        return {}

st.title("IR, CR, IC, AUCratio 計算アプリ")

col1, col2 = st.columns(2)
CR = col1.number_input("CR (基質寄与率)", min_value=0.0, max_value=1.0, step=0.01, format="%.2f")
IR = col2.number_input("IR (阻害率)", min_value=0.0, max_value=1.0, step=0.01, format="%.2f")
IC = col1.number_input("IC (誘導率)", min_value=0.0, max_value=1.0, step=0.01, format="%.2f")
AUCratio = col2.number_input("AUCratio", min_value=0.0, step=0.01, format="%.2f")

input_values = {"CR": CR, "IR": IR, "IC": IC, "AUCratio": AUCratio}
known_values = {k: v for k, v in input_values.items() if v > 0}

if len(known_values) == 2:
    result = calculate_value(known_values)
    st.write("### 計算結果")
    for key, value in result.items():
        st.write(f"{key}: {value:.4f}")

    if "history" not in st.session_state:
        st.session_state.history = []
    history_entry = {**known_values, **result}
    st.session_state.history.append(history_entry)

    st.write("### 過去の計算結果")
    history_df = pd.DataFrame(st.session_state.history)
    st.dataframe(history_df)
else:
    st.warning("2つの値を入力してください。")
