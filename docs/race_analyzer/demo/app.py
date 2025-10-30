# app.py — Race Analyzer (DEMO-lite)
import os
import base64
import glob
import mimetypes
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Race Analyzer — DEMO", page_icon="🏁", layout="wide")

# ----------------- Ustawienia DEMO -----------------
DEMO_PATH = os.getenv("DEMO_DATA_PATH", "demo_data.csv")

# ----------------- Utility -----------------
def parse_time_to_sec(s: str) -> float:
    if s is None or (isinstance(s, float) and np.isnan(s)): 
        return np.nan
    s = str(s).strip()
    parts = s.split(":")
    try:
        if len(parts) == 3:
            h, m, sec = map(int, parts)
            return h*3600 + m*60 + sec
        if len(parts) == 2:
            m, sec = map(int, parts)
            return m*60 + sec
    except Exception:
        pass
    try:
        f = float(s.replace(",", "."))
        return int(round(f*60))
    except Exception:
        return np.nan

def sec_to_mmss(sec: float) -> str:
    sec = int(round(float(sec)))
    m = sec // 60
    s = sec % 60
    return f"{m:d} min {s:02d} s"

def mmss(sec: float) -> str:
    sec = int(round(float(sec)))
    return f"{sec//60}:{sec%60:02d}"

def detect_sep(sample_text: str) -> str:
    return ";" if sample_text.count(";") >= sample_text.count(",") else ","

def riegel_time(t1_sec: float, d1_km: float, d2_km: float, exponent: float = 1.06) -> float:
    if not t1_sec or t1_sec <= 0: 
        return np.nan
    return float(t1_sec) * (d2_km / d1_km) ** exponent

# ----------------- Tło (opcjonalnie) -----------------
def set_background():
    bg_path = None
    for ext in ("*.jpg", "*.jpeg", "*.png"):
        files = sorted(glob.glob(ext))
        if files:
            bg_path = files[0]
            break
    if not bg_path:
        return
    mime, _ = mimetypes.guess_type(bg_path)
    if mime not in ("image/jpeg", "image/png"):
        mime = "image/jpeg"
    with open(bg_path, "rb") as f:
        bg_b64 = base64.b64encode(f.read()).decode()
    st.markdown(f"""
    <style>
      .stApp {{
        background-image:
          linear-gradient(rgba(0,0,0,.35), rgba(0,0,0,.35)),
          url("data:{mime};base64,{bg_b64}");
        background-size: cover; background-position: center; background-attachment: fixed;
      }}
      .stApp .block-container {{ color: #f2f2f2; }}
      section[data-testid="stSidebar"] * {{ color: #111 !important; }}
    </style>
    """, unsafe_allow_html=True)

set_background()

# ----------------- Dane DEMO (TOP20) -----------------
@st.cache_data(show_spinner=False)
def load_demo_df(path: str) -> pd.DataFrame | None:
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        head = f.read(4096).decode("utf-8", errors="ignore")
    sep = detect_sep(head)
    df = pd.read_csv(path, sep=sep)
    df.columns = [str(c).strip() for c in df.columns]
    return df

def extract_top20(df: pd.DataFrame):
    if df is None or df.empty: 
        return None, None
    lower = {c.lower(): c for c in df.columns}
    # szukamy kolumny czasu
    hits = [nm for nm in lower if any(x in nm for x in ["czas", "time", "netto", "finish"])]
    time_col = lower[hits[0]] if hits else None
    if time_col is None:
        for c in df.columns:
            try:
                s = df[c].astype(str)
                if s.str.contains(r"^\s*\d{1,2}:\d{2}(:\d{2})?\s*$", regex=True, na=False).mean() > 0.3:
                    time_col = c; break
            except Exception:
                pass
    if time_col is None: 
        return None, None
    ser = df[time_col]
    sec = ser.astype(float) if np.issubdtype(ser.dtype, np.number) else ser.map(parse_time_to_sec)
    good = df.loc[sec.notna()].copy()
    good["_sec"] = sec[sec.notna()].astype(int)
    good = good.sort_values("_sec").head(20).reset_index(drop=True)
    return good, time_col

# ----------------- UI -----------------
st.title("🏁 Race Analyzer — DEMO")
st.sidebar.title("⚙️ Ustawienia")

gender = st.sidebar.radio("Płeć", ["M", "K"], horizontal=True)
age = st.sidebar.number_input("Wiek", min_value=12, max_value=100, value=52, step=1)
pace_sec = st.sidebar.slider("Tempo 5 km (sekundy / km)", 180, 420, 330, 5)
m, s = divmod(int(pace_sec), 60)
st.sidebar.caption(f"Tempo ≈ {m}:{s:02d} min/km")

go = st.sidebar.button("Przewiduj 🚀")

left, right = st.columns([2, 1])

with right:
    st.subheader("🎵 Muzyka do biegu (opcjonalnie)")
    mp3s = sorted({Path(p).name.lower(): p for p in glob.glob("*.mp3")}.values())
    if mp3s:
        labels = [Path(p).name for p in mp3s]
        pick = st.selectbox("Wybierz utwór", labels, index=0)
        with open(mp3s[labels.index(pick)], "rb") as f:
            st.audio(f.read(), format="audio/mp3")
    else:
        st.caption("Brak plików .mp3 w katalogu.")

with left:
    if go:
        # Predykcja z tempa (Riegel)
        t5k = float(pace_sec) * 5.0
        hm_sec = riegel_time(t5k, 5.0, 21.0975, exponent=1.06)
        st.success("✅ Przewidywany czas półmaratonu (model DEMO — wzór Riegla)")
        st.metric("Półmaraton (21.1 km)", sec_to_mmss(hm_sec))

        # Podpowiedzi na inne dystanse
        t10 = riegel_time(hm_sec, 21.0975, 10.0)
        t15 = riegel_time(hm_sec, 21.0975, 15.0)
        c10, c15 = st.columns(2)
        c10.metric("Szacunek 10 km", sec_to_mmss(t10))
        c15.metric("Szacunek 15 km", sec_to_mmss(t15))

        # TOP20 z danych DEMO
        st.markdown("### Porównanie z TOP 20 (dane DEMO)")
        df_all = load_demo_df(DEMO_PATH)
        top20, time_col = extract_top20(df_all) if df_all is not None else (None, None)
        if top20 is None:
            st.info("Brak danych DEMO. Upewnij się, że **demo_data.csv** istnieje obok app.py.")
        else:
            show = top20.copy()
            show["czas_s"] = show["_sec"]
            show["czas"] = show["_sec"].map(mmss)
            st.dataframe(show.drop(columns=["_sec"]), use_container_width=True)
