import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
from tide_engine import LagosTideEngine
from tide_tables import detect_high_low

engine = LagosTideEngine()

st.title("🐬 Welcome To Lagos Harbour")
st.title("⚓️ NN @ 70 Tide Predictor")
st.subheader(
    "Thanks for being part of NN's 70th Anniversary celebrations. We wish you a happy stay in Lagos.")

start = st.text_input("Start Date (YYYY-MM-DD HH:MM)")
end = st.text_input("End Date (YYYY-MM-DD HH:MM)")
interval = st.number_input("Interval Minutes", value=15)

if st.button("Generate Prediction"):

    start_dt = datetime.strptime(start, "%Y-%m-%d %H:%M")
    end_dt = datetime.strptime(end, "%Y-%m-%d %H:%M")

    df = engine.generate_series(start_dt, end_dt, interval)
    HW, LW = detect_high_low(df)

    st.subheader("Tide Table")
    st.dataframe(df)

    st.subheader("High Waters")
    st.dataframe(HW)

    st.subheader("Low Waters")
    st.dataframe(LW)

    fig, ax = plt.subplots()
    ax.plot(df["Time"], df["Height_m"])
    ax.set_ylabel("Height (m)")
    ax.set_title("Tidal Curve")

    st.pyplot(fig)

    csv = df.to_csv(index=False).encode()

    st.download_button(
        "Download CSV",
        csv,
        "lagos_tide_table.csv",
        "text/csv"
    )
