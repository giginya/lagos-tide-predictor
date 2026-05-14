import pandas as pd


def detect_high_low(df):

    h = df["Height_m"].values

    highs = []
    lows = []

    for i in range(1, len(h)-1):

        if h[i] > h[i-1] and h[i] > h[i+1]:
            highs.append(i)

        if h[i] < h[i-1] and h[i] < h[i+1]:
            lows.append(i)

    HW = df.iloc[highs]
    LW = df.iloc[lows]

    return HW, LW


def monthly_tide_table(engine, year, month):

    start = pd.Timestamp(year, month, 1)
    end = start+pd.offsets.MonthEnd()

    df = engine.generate_series(start, end, 10)

    HW, LW = detect_high_low(df)

    return df, HW, LW
