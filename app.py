import streamlit as st
from datetime import date, datetime, time, timedelta
from tide_engine import LagosTideEngine
from tide_tables import detect_high_low

MAX_DAYS = 366
MAX_POINTS = 20_000


@st.cache_resource
def get_engine():
    return LagosTideEngine()


@st.cache_data(ttl=3600, max_entries=128)
def build_prediction(start_dt, end_dt, interval_minutes):
    df = get_engine().generate_series(start_dt, end_dt, interval_minutes)
    HW, LW = detect_high_low(df)
    return df, HW, LW


def combine_date_time(day, clock):
    return datetime.combine(day, clock)


def validate_request(start_dt, end_dt, interval_minutes):
    if end_dt <= start_dt:
        return "End date and time must be after the start date and time."

    if end_dt - start_dt > timedelta(days=MAX_DAYS):
        return f"Prediction range is limited to {MAX_DAYS} days."

    points = int(((end_dt - start_dt).total_seconds() // 60) / interval_minutes) + 1
    if points > MAX_POINTS:
        return (
            f"This request would generate about {points:,} rows. "
            f"Increase the interval or shorten the range to stay under {MAX_POINTS:,} rows."
        )

    return None

st.title("🐬 Welcome To Lagos Harbour")
st.title("⚓️ NN @ 70 Tide Predictor")
st.subheader(
    "Thanks for being part of NN's 70th Anniversary celebrations. We wish you a happy stay in Lagos.")

today = date.today()

with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    with col1:
        start_day = st.date_input("Start Date", value=today)
        start_clock = st.time_input("Start Time", value=time(0, 0), step=timedelta(minutes=15))
    with col2:
        end_day = st.date_input("End Date", value=today + timedelta(days=1))
        end_clock = st.time_input("End Time", value=time(0, 0), step=timedelta(minutes=15))

    interval = st.number_input(
        "Interval Minutes",
        min_value=1,
        max_value=1440,
        value=15,
        step=1,
    )

    submitted = st.form_submit_button("Generate Prediction")

if submitted:
    start_dt = combine_date_time(start_day, start_clock)
    end_dt = combine_date_time(end_day, end_clock)
    validation_error = validate_request(start_dt, end_dt, interval)

    if validation_error:
        st.error(validation_error)
        st.stop()

    with st.spinner("Generating tide prediction..."):
        df, HW, LW = build_prediction(start_dt, end_dt, interval)

    st.subheader("Tide Table")
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.subheader("High Waters")
    st.dataframe(HW, use_container_width=True, hide_index=True)

    st.subheader("Low Waters")
    st.dataframe(LW, use_container_width=True, hide_index=True)

    st.subheader("Tidal Curve")
    st.line_chart(df.set_index("Time")["Height_m"])

    csv = df.to_csv(index=False).encode()

    st.download_button(
        "Download CSV",
        csv,
        "lagos_tide_table.csv",
        "text/csv"
    )
