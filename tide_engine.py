import numpy as np
import pandas as pd
import math
from datetime import datetime


class LagosTideEngine:

    """
    Hydrographic tide prediction engine for Lagos Harbour.

    Governing equation:

    h(t) = Z0 + Σ f_i H_i cos(ω_i t + V_i + u_i − g_i)

    Where:
        Z0 = Mean sea level
        H  = Constituent amplitude
        ω  = Angular speed
        g  = Phase lag
        V  = Equilibrium astronomical argument
        u  = Nodal phase correction
        f  = Nodal amplitude factor

    Updated using revised harmonic constituent solutions.
    Category D constituents intentionally excluded.
    """

    def __init__(self):

        self.Z0 = 0.961
        self.epoch = datetime(2000, 1, 1)

        # ------------------------------------------------------------------
        # Updated harmonic constituents
        # Category D constituents excluded
        # ------------------------------------------------------------------

        self.constituents = {

            # Principal semidiurnal
            "M2":   {"amp": 0.323358, "phase": 148.461247, "speed": 28.9841042},
            "S2":   {"amp": 0.125703, "phase": 168.496632, "speed": 30.0000000},
            "N2":   {"amp": 0.071262, "phase": 144.282795, "speed": 28.4397295},
            "K2":   {"amp": 0.040561, "phase": 176.083351, "speed": 30.0821373},
            "2N2":  {"amp": 0.027257, "phase": 177.772658, "speed": 27.8953548},
            "MU2":  {"amp": 0.024386, "phase": 162.623000, "speed": 27.9682084},
            "L2":   {"amp": 0.022185, "phase": 176.534567, "speed": 29.5284789},
            "NU2":  {"amp": 0.019882, "phase": 158.210002, "speed": 28.5125831},
            "EPS2": {"amp": 0.017378, "phase": 191.917911, "speed": 29.4556253},
            "OQ2":  {"amp": 0.016957, "phase": 203.333985, "speed": 30.0410667},
            "LDA2": {"amp": 0.013372, "phase": 168.044673, "speed": 29.4556253},
            "ETA2": {"amp": 0.011710, "phase": 195.795480, "speed": 30.6265120},

            # Principal diurnal
            "K1":   {"amp": 0.088065, "phase": 355.294555, "speed": 15.0410686},
            "P1":   {"amp": 0.053137, "phase": 6.331105,   "speed": 14.9589314},
            "J1":   {"amp": 0.037095, "phase": 307.082303, "speed": 15.5854433},
            "THE1": {"amp": 0.026353, "phase": 281.034990, "speed": 15.0000000},
            "PHI1": {"amp": 0.026055, "phase": 2.762098,   "speed": 15.1232059},
            "TAU1": {"amp": 0.018845, "phase": 161.850352, "speed": 14.9178647},
            "NO1":  {"amp": 0.016987, "phase": 282.044074, "speed": 13.3986609},
            "O1":   {"amp": 0.016805, "phase": 309.033965, "speed": 13.9430356},
            "Q1":   {"amp": 0.012287, "phase": 203.083764, "speed": 13.3986609},
            "RHO1": {"amp": 0.011356, "phase": 204.793155, "speed": 13.4715145},
            "BET1": {"amp": 0.011203, "phase": 175.127444, "speed": 13.3986609},
            "SO1":  {"amp": 0.008584, "phase": 354.527043, "speed": 15.0000000},
            "ALP1": {"amp": 0.008164, "phase": 97.367448,  "speed": 14.4966939},
            "2Q1":  {"amp": 0.006886, "phase": 140.192883, "speed": 12.8542862},
            "UPS1": {"amp": 0.006013, "phase": 139.756642, "speed": 14.4966939},
            "CHI1": {"amp": 0.005668, "phase": 275.397339, "speed": 14.5695476},
            "SIG1": {"amp": 0.005046, "phase": 141.579869, "speed": 15.1229960},

            # Long-period constituents
            "SSA":  {"amp": 0.084393, "phase": 93.562157,  "speed": 0.0821373},
            "MSM":  {"amp": 0.038237, "phase": 157.363260, "speed": 0.4715218},
            "MF":   {"amp": 0.016137, "phase": 41.699967,  "speed": 1.0980331},
            "MM":   {"amp": 0.013425, "phase": 130.960591, "speed": 0.5443747},

            # Shallow water / overtides
            "M4":   {"amp": 0.016735, "phase": 55.843908,  "speed": 57.9682084},
            "MN4":  {"amp": 0.006952, "phase": 6.286815,   "speed": 57.4238337},
            "MSN2": {"amp": 0.018764, "phase": 88.994114,  "speed": 58.9841042},
            "MKS2": {"amp": 0.024208, "phase": 66.709432,  "speed": 44.0251729},
            "2MS6": {"amp": 0.009793, "phase": 56.691227,  "speed": 88.9523126},
            "SO3":  {"amp": 0.008572, "phase": 162.064044, "speed": 45.0000000},
            "2MK5": {"amp": 0.005404, "phase": 225.736328, "speed": 87.0092771}
        }

    # ----------------------------------------------------------------------
    # Julian day computation
    # ----------------------------------------------------------------------

    def julian_day(self, dt):

        a = (14 - dt.month) // 12
        y = dt.year + 4800 - a
        m = dt.month + 12 * a - 3

        JDN = (
            dt.day
            + ((153 * m + 2) // 5)
            + 365 * y
            + y // 4
            - y // 100
            + y // 400
            - 32045
        )

        JD = (
            JDN
            + (dt.hour - 12) / 24
            + dt.minute / 1440
            + dt.second / 86400
        )

        return JD

    # ----------------------------------------------------------------------
    # Astronomical arguments
    # ----------------------------------------------------------------------

    def astronomical_arguments(self, dt):

        JD = self.julian_day(dt)
        T = (JD - 2451545.0) / 36525

        s = (218.3164 + 481267.8813 * T) % 360
        h = (280.4661 + 36000.7698 * T) % 360
        p = (83.3535 + 4069.0137 * T) % 360
        N = (125.0445 - 1934.1363 * T) % 360

        return s, h, p, N

    # ----------------------------------------------------------------------
    # Simplified nodal corrections
    # ----------------------------------------------------------------------

    def nodal_corrections(self, dt):

        _, _, _, N = self.astronomical_arguments(dt)

        f = {}
        u = {}

        for constituent in self.constituents:
            f[constituent] = 1.0
            u[constituent] = 0.0

        # Principal constituents
        u["M2"] = -2 * N
        u["N2"] = -3 * N
        u["K1"] = -N
        u["O1"] = -N

        return f, u

    # ----------------------------------------------------------------------
    # Equilibrium arguments
    # ----------------------------------------------------------------------

    def equilibrium_argument(self, dt):

        s, h, p, N = self.astronomical_arguments(dt)

        V = {}

        V["M2"] = (2 * s - 2 * h) % 360
        V["S2"] = (2 * h) % 360
        V["N2"] = (2 * s - 3 * h + p) % 360
        V["K1"] = (h + 90) % 360
        V["O1"] = (s - h) % 360

        return V

    # ----------------------------------------------------------------------
    # Tide prediction
    # ----------------------------------------------------------------------

    def tide_height(self, t):

        hours = (t - self.epoch).total_seconds() / 3600

        height = self.Z0

        V = self.equilibrium_argument(t)
        f, u = self.nodal_corrections(t)

        for name, constituent in self.constituents.items():

            Vu = V.get(name, 0.0) + u.get(name, 0.0)
            f_i = f.get(name, 1.0)

            angle = math.radians(
                constituent["speed"] * hours
                + Vu
                - constituent["phase"]
            )

            height += f_i * constituent["amp"] * math.cos(angle)

        return height

    # ----------------------------------------------------------------------
    # Time series generation
    # ----------------------------------------------------------------------

    def generate_series(self, start, end, interval_minutes=30):

        if interval_minutes <= 0:
            raise ValueError("interval_minutes must be greater than zero")

        if end <= start:
            raise ValueError("end must be after start")

        times = pd.date_range(
            start=start,
            end=end,
            freq=f"{interval_minutes}min"
        )

        heights = [self.tide_height(t) for t in times]

        return pd.DataFrame({
            "Time": times,
            "Height_m": heights
        })


# --------------------------------------------------------------------------
# Example usage
# --------------------------------------------------------------------------

if __name__ == "__main__":

    engine = LagosTideEngine()

    start = datetime(2026, 5, 1)
    end = datetime(2026, 5, 2)

    df = engine.generate_series(start, end, interval_minutes=30)

    print(df.head())
