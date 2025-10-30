# app.py — Welcome Survey Dashboard
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Welcome Survey Dashboard", page_icon="📋", layout="wide")

# ========= Wczytanie danych =========
@st.cache_data(show_spinner=False)
def load_csv(path: str) -> pd.DataFrame:
    # CSV zwykle ma separator ';' — spróbujmy wykryć/sefguardować
    try:
        return pd.read_csv(path, sep=";", encoding="utf-8")
    except Exception:
        return pd.read_csv(path, sep=",", encoding_errors="ignore")

DATA_PATH = "35__welcome_survey_cleaned.csv"
df = load_csv(DATA_PATH)

if df.empty:
    st.error("Plik CSV został wczytany, ale jest pusty. Sprawdź ścieżkę lub separator.")
    st.stop()

# ========= UI =========
st.title("📋 Welcome Survey – Dashboard ankietowy")
st.caption("Autor: Roman — Aspiring Data Scientist & Python Streamlit Developer")

with st.sidebar:
    st.header("⚙️ Ustawienia")
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()

    sort_col = st.selectbox("Sortuj po kolumnie", df.columns, index=0)
    ascending = st.toggle("Rosnąco", value=True)
    sample_n = st.slider("Losowa próbka (wiersze)", 5, 50, 10, step=5)

    st.divider()
    st.subheader("📝 Notatnik")
    note = st.text_area("Wpisz notatkę")
    if "notes" not in st.session_state:
        st.session_state["notes"] = []
    c1, c2 = st.columns(2)
    if c1.button("➕ Dodaj"):
        if note.strip():
            st.session_state["notes"].append(note.strip())
            st.success("Dodano notatkę.")
        else:
            st.info("Wpisz treść notatki.")
    if c2.button("💾 Zapisz do pliku"):
        with open("notatki.txt", "w", encoding="utf-8") as f:
            f.write("\n\n".join(st.session_state["notes"]))
        st.success("Zapisano do pliku: notatki.txt")

# ========= Podgląd danych =========
st.subheader("🔎 Podgląd danych")
df_sorted = df.sort_values(by=sort_col, ascending=ascending)
st.dataframe(df_sorted.head(200), use_container_width=True)

st.markdown(f"**Losowa próbka ({min(sample_n, len(df))})**")
st.dataframe(df.sample(min(sample_n, len(df))), use_container_width=True)

# ========= Wartości unikatowe =========
with st.expander("🔢 Wartości unikatowe"):
    col = st.selectbox("Kolumna", df.columns, index=0, key="unique_col")
    vc = df[col].value_counts(dropna=False)
    st.write(vc.to_frame("Liczność"))
    st.bar_chart(vc.head(20))

# ========= Wizualizacje =========
st.subheader("📊 Wizualizacje")

# 1) Korelacje
if len(num_cols) >= 2:
    corr = df[num_cols].corr()
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.heatmap(corr, cmap="coolwarm", vmin=-1, vmax=1, annot=False, ax=ax)
    ax.set_title("Macierz korelacji (kolumny numeryczne)")
    st.pyplot(fig)
else:
    st.info("Brak wystarczającej liczby kolumn numerycznych do korelacji.")

# 2) Boxplot (Plotly)
with st.expander("📦 Boxplot (Plotly)"):
    if num_cols and cat_cols:
        y_col = st.selectbox("Kolumna numeryczna (Y)", num_cols, key="y_box")
        x_col = st.selectbox("Kolumna kategoryczna (X)", cat_cols, key="x_box")
        fig_box = px.box(df, x=x_col, y=y_col, points="suspectedoutliers")
        st.plotly_chart(fig_box, use_container_width=True)
    else:
        st.info("Potrzebna co najmniej jedna kolumna numeryczna i jedna kategoryczna.")

# 3) Barplot liczności
with st.expander("📊 Barplot liczności kategorii"):
    if cat_cols:
        cat = st.selectbox("Kolumna kategoryczna", cat_cols, key="bar_cat")
        vc = df[cat].value_counts().reset_index()
        vc.columns = [cat, "count"]
        fig_bar = px.bar(vc.head(30), x=cat, y="count")
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Brak kolumn kategorycznych.")

st.divider()
st.caption("© Roman — Streamlit · Pandas · Seaborn · Plotly")
