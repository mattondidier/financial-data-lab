"""
US Treasury Yield Curve animation, 1982 to today.
Author: Didier Matton | Financial Engineer | Full Stack Data Scientist

One run produces every video format you need:
    16:9  (1920 x 1080)  -> YouTube, X (Twitter), LinkedIn
    4:5   (1080 x 1350)  -> LinkedIn feed (takes more space on mobile)
    9:16  (1080 x 1920)  -> TikTok, YouTube Shorts, Instagram Reels

BACKGROUND MUSIC (optional)
    Put a royalty-free MP3 next to this script (e.g. from the YouTube Audio Library
    or Pixabay Music, check each track's licence) and set MUSIC_FILE below.
    The 9:16 version stays silent on purpose: on TikTok / Reels / Shorts, add a
    sound from the app's own library instead (licensed, and it helps reach).

INSTALL (once)
    pip install fredapi pandas numpy matplotlib python-dotenv imageio-ffmpeg

API KEY
    Create a file named .env next to this script containing:
        FRED_API_KEY=your_key_here
    Add .env to your .gitignore before publishing on GitHub.

RUN
    python yield_curve_video.py

Comments are hand-written up to the end of 2024. After that, they are generated
from the data itself (short rates, long rates, curve shape), so every month is
commented without claiming events the data does not show.
"""

import os
import textwrap

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter
from matplotlib.patches import FancyBboxPatch


# 1. SETTINGS

DOWNLOAD = True                        # False = reuse the saved CSV
CSV_FILE = "treasury_yields_monthly.csv"
OUTPUT_DIR = "videos"
START = "1982-01-01"

LANGUAGES = ["en","fr"]                     # ["en", "fr"] to also produce French versions
FORMATS = ["16:9", "4:5", "9:16"]      # remove the ones you do not need
PLATFORMS = {                          # platforms written in the file names
    "16:9": "YouTube-X",
    "4:5":  "LinkedIn",
    "9:16": "TikTok-Shorts-Reels",
}
FRAMES_PER_MONTH = 3                   # 2 = shorter video (about 40 s)
FPS = 30

MUSIC_FILE = None                      # e.g. "my_music.mp3"; None = silent videos
MUSIC_FORMATS = ["16:9", "4:5"]        # formats that get the music
MUSIC_VOLUME = 0.8                     # 1.0 = original volume
FADE_IN, FADE_OUT = 1.0, 3.0           # seconds

SERIES = ["DGS3MO", "DGS6MO", "DGS1", "DGS2", "DGS3", "DGS5", "DGS7", "DGS10"]

RECESSIONS = [                         # NBER, peak to trough
    ("1981-07-01", "1982-11-30"), ("1990-07-01", "1991-03-31"),
    ("2001-03-01", "2001-11-30"), ("2007-12-01", "2009-06-30"),
    ("2020-02-01", "2020-04-30"),
]
MANUAL_COMMENTS_END = pd.Timestamp("2024-12-31")


# 2. TEXTS (English and French)

TEXT = {
    "en": {
        "title": "The US Treasury Yield Curve, {a}–{b}",
        "subtitle": "Treasury yields by maturity · monthly averages",
        "shape_label": "Curve shape",
        "spread_label": "10Y – 3M spread",
        "recession": "RECESSION",
        "shapes": {"NORMAL": "NORMAL", "FLAT": "FLAT", "INVERTED": "INVERTED"},
        "caption": "10Y – 3M spread · grey = recessions (NBER) · below zero = inverted curve",
        "axis_y": "Yield (%)", "axis_spread": "Spread (pts)",
        "source": "Source: Federal Reserve (FRED)",
        "signature": "Didier Matton  |  Financial Engineer  |  Full Stack Data Scientist",
        "maturities": ["3M", "6M", "1Y", "2Y", "3Y", "5Y", "7Y", "10Y"],
        "months": ["January", "February", "March", "April", "May", "June", "July",
                   "August", "September", "October", "November", "December"],
        "decimal": ".",
        "comments": [
            ("1982-01", "1982-11", "1982: Paul Volcker's Fed fights inflation, yields near 14%."),
            ("1982-12", "1988-12", "1983–1988: disinflation, yields fall and the curve turns normal again."),
            ("1989-01", "1990-06", "1989: after Fed hikes, the curve flattens, then inverts."),
            ("1990-07", "1992-12", "1990–1992: recession, the Fed cuts rates and the curve steepens."),
            ("1993-01", "1993-12", "1993: low short rates, a very steep curve."),
            ("1994-01", "1995-06", "1994: the Fed doubles its rate in a year, short rates catch up."),
            ("1995-07", "1998-07", "1995–1998: expansion, a normal but fairly flat curve."),
            ("1998-08", "1999-05", "1998: Russian crisis and LTCM collapse, the Fed cuts three times."),
            ("1999-06", "2000-06", "1999–2000: the Fed raises rates up to 6.5%."),
            ("2000-07", "2000-12", "2000: the curve inverts before the dot-com bust."),
            ("2001-01", "2004-05", "2001–2003: the Fed cuts to 1%, the curve steepens."),
            ("2004-06", "2006-07", "2004–2006: 17 straight rate hikes, the curve flattens."),
            ("2006-08", "2007-08", "2006–2007: inversion ahead of the financial crisis."),
            ("2007-09", "2008-12", "2008: financial crisis, the Fed takes rates almost to zero."),
            ("2009-01", "2010-12", "2009–2010: zero short rates and large bond purchases (QE)."),
            ("2011-01", "2012-12", "2011–2012: \"Operation Twist\" pushes long-term yields down."),
            ("2013-01", "2013-12", "2013: the \"taper tantrum\" sends the 10-year toward 3%."),
            ("2014-01", "2015-11", "2014–2015: QE ends, long-term yields ease."),
            ("2015-12", "2018-12", "2015–2018: the Fed hikes step by step, the curve flattens."),
            ("2019-01", "2020-01", "2019: the curve inverts, the Fed cuts rates three times."),
            ("2020-02", "2020-12", "2020: Covid-19, the Fed cuts rates to zero within weeks."),
            ("2021-01", "2022-02", "2021: recovery and rising inflation push long yields up."),
            ("2022-03", "2022-10", "2022: the fastest Fed hiking cycle in 40 years."),
            ("2022-11", "2023-12", "2023: the deepest inversion since the early 1980s."),
            ("2024-01", "2024-08", "2024: the Fed holds rates high, the curve stays inverted."),
            ("2024-09", "2024-12", "Late 2024: first rate cuts, the curve starts to normalize."),
        ],
        "auto": {
            "short_down": "the Fed is cutting, short-term yields fall",
            "short_up": "the Fed is hiking, short-term yields rise",
            "short_flat": "short-term yields are stable",
            "long_up": "long-term yields rise",
            "long_down": "long-term yields fall",
            "long_flat": "long-term yields barely move",
            "uninvert": "The curve is un-inverting.",
            "NORMAL": "Normal curve.", "FLAT": "Flat curve.", "INVERTED": "Inverted curve.",
        },
    },
    "fr": {
        "title": "La courbe des taux américaine, {a}–{b}",
        "subtitle": "Rendement des bons du Trésor selon la maturité · moyennes mensuelles",
        "shape_label": "Forme de la courbe",
        "spread_label": "Écart 10 ans – 3 mois",
        "recession": "RÉCESSION",
        "shapes": {"NORMAL": "NORMALE", "FLAT": "PLATE", "INVERTED": "INVERSÉE"},
        "caption": "Écart 10 ans – 3 mois · gris = récessions (NBER) · sous zéro = courbe inversée",
        "axis_y": "Rendement (%)", "axis_spread": "Écart (pts)",
        "source": "Source : Réserve fédérale (FRED)",
        "signature": "Didier Matton  |  Ingénieur financier  |  Data Scientist Full Stack",
        "maturities": ["3 m", "6 m", "1 an", "2 ans", "3 ans", "5 ans", "7 ans", "10 ans"],
        "months": ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet",
                   "Août", "Septembre", "Octobre", "Novembre", "Décembre"],
        "decimal": ",",
        "comments": [
            ("1982-01", "1982-11", "1982 : la Fed de Paul Volcker combat l'inflation, taux proches de 14 %."),
            ("1982-12", "1988-12", "1983–1988 : désinflation, les taux baissent et la courbe redevient normale."),
            ("1989-01", "1990-06", "1989 : la Fed a monté ses taux, la courbe s'aplatit puis s'inverse."),
            ("1990-07", "1992-12", "1990–1992 : récession, la Fed baisse ses taux et la courbe se pentifie."),
            ("1993-01", "1993-12", "1993 : taux courts bas, courbe très pentue."),
            ("1994-01", "1995-06", "1994 : la Fed double son taux en un an, les taux courts rattrapent les longs."),
            ("1995-07", "1998-07", "1995–1998 : expansion, courbe normale mais peu pentue."),
            ("1998-08", "1999-05", "1998 : crise russe et faillite de LTCM, la Fed baisse trois fois ses taux."),
            ("1999-06", "2000-06", "1999–2000 : la Fed remonte ses taux jusqu'à 6,5 %."),
            ("2000-07", "2000-12", "2000 : inversion avant l'éclatement de la bulle Internet."),
            ("2001-01", "2004-05", "2001–2003 : la Fed coupe ses taux jusqu'à 1 %, la courbe se pentifie."),
            ("2004-06", "2006-07", "2004–2006 : 17 hausses de taux d'affilée, la courbe s'aplatit."),
            ("2006-08", "2007-08", "2006–2007 : inversion avant la crise financière."),
            ("2007-09", "2008-12", "2008 : crise financière, la Fed ramène ses taux quasiment à zéro."),
            ("2009-01", "2010-12", "2009–2010 : taux courts à zéro et rachats massifs d'obligations (QE)."),
            ("2011-01", "2012-12", "2011–2012 : « Operation Twist », la Fed fait baisser les taux longs."),
            ("2013-01", "2013-12", "2013 : « taper tantrum », le 10 ans bondit vers 3 %."),
            ("2014-01", "2015-11", "2014–2015 : fin du QE, les taux longs se détendent."),
            ("2015-12", "2018-12", "2015–2018 : la Fed remonte ses taux pas à pas, la courbe s'aplatit."),
            ("2019-01", "2020-01", "2019 : la courbe s'inverse, la Fed baisse trois fois ses taux."),
            ("2020-02", "2020-12", "2020 : Covid-19, la Fed ramène ses taux à zéro en quelques semaines."),
            ("2021-01", "2022-02", "2021 : reprise et retour de l'inflation, les taux longs remontent."),
            ("2022-03", "2022-10", "2022 : la Fed monte ses taux au rythme le plus rapide depuis 40 ans."),
            ("2022-11", "2023-12", "2023 : inversion la plus profonde depuis le début des années 1980."),
            ("2024-01", "2024-08", "2024 : la Fed maintient ses taux au plus haut, la courbe reste inversée."),
            ("2024-09", "2024-12", "Fin 2024 : premières baisses de taux, la courbe commence à se redresser."),
        ],
        "auto": {
            "short_down": "la Fed baisse ses taux, les taux courts reculent",
            "short_up": "la Fed monte ses taux, les taux courts grimpent",
            "short_flat": "taux courts stables",
            "long_up": "les taux longs montent",
            "long_down": "les taux longs baissent",
            "long_flat": "les taux longs bougent peu",
            "uninvert": "La courbe se désinverse.",
            "NORMAL": "Courbe normale.", "FLAT": "Courbe plate.", "INVERTED": "Courbe inversée.",
        },
    },
}

# 3. LAYOUTS (positions as fractions of the frame)

LAYOUTS = {
    "16:9": dict(
        size=(19.2, 10.8), fs=1.5,
        title=(0.04, 0.935, "left"), subtitle=(0.04, 0.895), date=(0.96, 0.925, "right"),
        ax=[0.07, 0.40, 0.56, 0.45], ax2=[0.07, 0.12, 0.89, 0.19],
        box=(0.675, 0.715, 0.285, 0.135), box_label=(0.69, 0.815), shape=(0.69, 0.738),
        badge=(0.955, 0.745), spread_label=(0.69, 0.655), spread=(0.69, 0.605),
        comment=(0.69, 0.525), wrap=38, comment_fs=12.5,
        rule_y=0.075, signature=(0.5, 0.035), source=(0.04, 0.035, "left"), caption_wrap=None,
    ),
    "4:5": dict(
        size=(10.8, 13.5), fs=1.45,
        title=(0.06, 0.955, "left"), subtitle=(0.06, 0.925), date=(0.06, 0.855, "left"),
        ax=[0.13, 0.48, 0.82, 0.31], ax2=[0.13, 0.135, 0.82, 0.13],
        box=(0.555, 0.838, 0.395, 0.072), box_label=(0.57, 0.89), shape=(0.57, 0.848),
        badge=(0.94, 0.852), spread_label=(0.06, 0.405), spread=(0.06, 0.365),
        comment=(0.44, 0.415), wrap=34, comment_fs=11.5,
        rule_y=0.06, signature=(0.5, 0.032), source=(0.5, 0.012, "center"), caption_wrap=60,
    ),
    "9:16": dict(  # important content kept out of TikTok's bottom and right overlays
        size=(10.8, 19.2), fs=1.55,
        title=(0.06, 0.925, "left"), subtitle=(0.06, 0.905), date=(0.06, 0.855, "left"),
        ax=[0.13, 0.55, 0.80, 0.26], ax2=[0.13, 0.25, 0.72, 0.09],
        box=(0.555, 0.84, 0.395, 0.05), box_label=(0.57, 0.875), shape=(0.57, 0.847),
        badge=(0.94, 0.856), spread_label=(0.06, 0.503), spread=(0.06, 0.476),
        comment=(0.06, 0.443), wrap=44, comment_fs=13,
        rule_y=0.215, signature=(0.5, 0.185), source=(0.5, 0.165, "center"), caption_wrap=48,
    ),
}


# 4. DATA

def download_fred(series, start):
    from dotenv import load_dotenv
    from fredapi import Fred

    load_dotenv()
    api_key = os.getenv("FRED_API_KEY")
    if api_key is None:
        raise ValueError("FRED key not found: create a .env file with FRED_API_KEY=your_key")
    fred = Fred(api_key=api_key)

    data = {}
    for series_id in series:
        try:
            data[series_id] = fred.get_series(series_id, observation_start=start)
            print(f"  {series_id} downloaded")
        except Exception as e:
            print(f"  Failed for {series_id}: {e}")
    if len(data) < len(series):
        raise RuntimeError("Some series could not be downloaded.")

    monthly = pd.DataFrame(data).resample("MS").mean().round(2)
    monthly.index.name = "date"
    return monthly


def load_data():
    if DOWNLOAD:
        print("Downloading FRED data...")
        df = download_fred(SERIES, START)
        df.to_csv(CSV_FILE)
        print(f"Data saved to {CSV_FILE}")
    else:
        df = pd.read_csv(CSV_FILE, index_col="date", parse_dates=True)

    df = df[SERIES].dropna()
    current_month = pd.Timestamp.today().to_period("M").to_timestamp()
    df = df[df.index < current_month]          # keep complete months only
    print(f"Period: {df.index[0]:%Y-%m} to {df.index[-1]:%Y-%m} ({len(df)} months)")
    return df


# 5. COMMENTS

def curve_shape(spread):
    if spread < 0:
        return "INVERTED"
    if spread < 0.5:
        return "FLAT"
    return "NORMAL"


def auto_comment(df, i, t):
    """Comment built from the data for months after the hand-written ones."""
    a = t["auto"]
    j, k = max(0, i - 6), max(0, i - 12)
    d_short = df["DGS3MO"].iloc[i] - df["DGS3MO"].iloc[j]
    d_long = df["DGS10"].iloc[i] - df["DGS10"].iloc[j]
    spread = df["DGS10"].iloc[i] - df["DGS3MO"].iloc[i]
    spread_before = df["DGS10"].iloc[k] - df["DGS3MO"].iloc[k]

    short = a["short_down"] if d_short <= -0.4 else a["short_up"] if d_short >= 0.4 else a["short_flat"]
    long_ = a["long_up"] if d_long >= 0.4 else a["long_down"] if d_long <= -0.4 else a["long_flat"]
    state = a["uninvert"] if spread_before < 0 <= spread else a[curve_shape(spread)]

    if t["decimal"] == ",":                       # French typography
        return f"{df.index[i].year} : {short}, {long_}. {state}"
    return f"{df.index[i].year}: {short[0].upper() + short[1:]}, {long_}. {state}"


def comment(df, i, t):
    date = df.index[i]
    for start, end, text in t["comments"]:
        if pd.Timestamp(start) <= date <= pd.Timestamp(end) + pd.offsets.MonthEnd(0):
            return text
    if date > MANUAL_COMMENTS_END:
        return auto_comment(df, i, t)
    return ""


# 6. VIDEO

BG, PANEL, FG, MUTED, GRID = "#0f172a", "#16213a", "#e5e7eb", "#94a3b8", "#23304d"
COLORS = {"NORMAL": "#38bdf8", "FLAT": "#fbbf24", "INVERTED": "#f87171"}


def ffmpeg_exe():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        return "ffmpeg"                        # assume ffmpeg is installed


def setup_ffmpeg():
    plt.rcParams["animation.ffmpeg_path"] = ffmpeg_exe()


def add_music(video_path, duration):
    """Mix the music into the video: loop if too short, cut at the end, fade in and out."""
    import subprocess

    tmp = video_path.replace(".mp4", "_silent.mp4")
    os.replace(video_path, tmp)
    audio_filter = (f"[1:a]volume={MUSIC_VOLUME},"
                    f"afade=t=in:st=0:d={FADE_IN},"
                    f"afade=t=out:st={max(0, duration - FADE_OUT):.2f}:d={FADE_OUT}[a]")
    cmd = [ffmpeg_exe(), "-y", "-loglevel", "error",
           "-i", tmp, "-stream_loop", "-1", "-i", MUSIC_FILE,
           "-filter_complex", audio_filter,
           "-map", "0:v", "-map", "[a]",
           "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
           "-t", f"{duration:.2f}", video_path]
    try:
        subprocess.run(cmd, check=True)
        os.remove(tmp)
        print("  music added")
    except subprocess.CalledProcessError as e:
        os.replace(tmp, video_path)            # keep the silent video if mixing fails
        print(f"  music could not be added ({e}); silent video kept")


def build_figure(df, fmt, lang):
    """Create the figure for one format and one language; return (fig, draw)."""
    L, t = LAYOUTS[fmt], TEXT[lang]
    s = L["fs"]
    plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": FG,
                         "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED,
                         "xtick.labelsize": 10 * s, "ytick.labelsize": 10 * s,
                         "axes.labelsize": 10.5 * s})

    X = np.arange(len(SERIES))
    Y = df[SERIES].values
    spreads = (df["DGS10"] - df["DGS3MO"]).values
    dates, n = df.index, len(df)
    recessions = [(pd.Timestamp(a), pd.Timestamp(b)) for a, b in RECESSIONS]
    comments = [textwrap.fill(comment(df, i, t), width=L["wrap"]) for i in range(n)]
    dec = t["decimal"]

    fig = plt.figure(figsize=L["size"], dpi=100, facecolor=BG)
    x, y, ha = L["title"]
    title = t["title"].format(a=dates[0].year, b=dates[-1].year)
    fig.text(x, y, title, fontsize=(22 if fmt == "16:9" else 19) * s, weight="bold", ha=ha)
    fig.text(*L["subtitle"], t["subtitle"], fontsize=(11.5 if fmt == "16:9" else 9.5) * s, color=MUTED)
    x, y, ha = L["date"]
    txt_date = fig.text(x, y, "", fontsize=24 * s, weight="bold", ha=ha)

    ax = fig.add_axes(L["ax"], facecolor=PANEL)
    ax.set_xlim(-0.3, len(X) - 0.7)
    ax.set_ylim(0, max(16, np.ceil(Y.max()) + 1))
    ax.set_xticks(X, t["maturities"])
    ax.set_ylabel(t["axis_y"])
    ax.grid(color=GRID, lw=0.8)
    for sp in ax.spines.values():
        sp.set_visible(False)
    TRAIL = 10
    ghosts = [ax.plot([], [], lw=1.5 * s, alpha=0)[0] for _ in range(TRAIL)]
    curve, = ax.plot([], [], lw=3.5 * s, marker="o", ms=7 * s, zorder=5)

    bx, by, bw, bh = L["box"]
    box = FancyBboxPatch((bx, by), bw, bh, boxstyle="round,pad=0.006,rounding_size=0.012",
                         transform=fig.transFigure, fc=PANEL, lw=2 * s)
    fig.add_artist(box)
    fig.text(*L["box_label"], t["shape_label"], fontsize=(11 if fmt == "16:9" else 9) * s, color=MUTED)
    txt_shape = fig.text(*L["shape"], "", fontsize=(26 if fmt == "16:9" else 20) * s, weight="bold")
    bx2, by2 = L["badge"]
    txt_rec = fig.text(bx2, by2, t["recession"], fontsize=(11 if fmt == "16:9" else 8.5) * s,
                       weight="bold", ha="right", color=BG,
                       bbox=dict(boxstyle="round,pad=0.35", fc=COLORS["INVERTED"], ec="none"))
    fig.text(*L["spread_label"], t["spread_label"], fontsize=11 * s, color=MUTED)
    txt_spread = fig.text(*L["spread"], "", fontsize=22 * s, weight="bold")
    txt_comment = fig.text(*L["comment"], "", fontsize=L["comment_fs"] * s, va="top", linespacing=1.4)

    ax2 = fig.add_axes(L["ax2"], facecolor=PANEL)
    ax2.set_xlim(dates[0], dates[-1] + pd.offsets.MonthEnd(0))
    ax2.set_ylim(min(-1.2, spreads.min() - 0.3), max(4.6, spreads.max() + 0.4))
    for a, b in recessions:
        if b >= dates[0] and a <= dates[-1]:
            ax2.axvspan(max(a, dates[0]), b, color="#475569", alpha=0.55, lw=0)
    ax2.axhline(0, color=MUTED, lw=0.9 * s, ls="--")
    ax2.plot(dates, spreads, color="#334155", lw=1.2 * s)
    trace, = ax2.plot([], [], color="#cbd5e1", lw=1.8 * s)
    cursor = ax2.axvline(dates[0], color=FG, lw=1.2 * s)
    ax2.set_ylabel(t["axis_spread"])
    ax2.grid(color=GRID, lw=0.6)
    for sp in ax2.spines.values():
        sp.set_visible(False)
    caption = t["caption"] if L["caption_wrap"] is None else textwrap.fill(t["caption"], L["caption_wrap"])
    ax2.text(0.0, 1.06, caption, transform=ax2.transAxes, fontsize=(10 if fmt == "16:9" else 8.5) * s,
             color=MUTED, va="bottom")

    fig.add_artist(plt.Line2D([0.04, 0.96], [L["rule_y"]] * 2, transform=fig.transFigure, color=GRID, lw=1))
    fig.text(*L["signature"], t["signature"], fontsize=(14 if fmt == "16:9" else 11) * s,
             weight="bold", ha="center")
    x, y, ha = L["source"]
    fig.text(x, y, t["source"], fontsize=8.5 * s, color=MUTED, ha=ha)

    def draw(tt):
        i = int(np.floor(tt)); j = min(i + 1, n - 1); w = tt - i
        yy = Y[i] * (1 - w) + Y[j] * w
        e = spreads[i] * (1 - w) + spreads[j] * w
        shp = curve_shape(e); c = COLORS[shp]
        curve.set_data(X, yy); curve.set_color(c)
        for k, g in enumerate(ghosts):
            idx = i - (k + 1) * 3
            if idx >= 0:
                g.set_data(X, Y[idx]); g.set_alpha(0.28 * (1 - k / TRAIL)); g.set_color(c)
            else:
                g.set_alpha(0)
        d = dates[i]
        txt_date.set_text(f"{t['months'][d.month - 1]} {d.year}")
        txt_shape.set_text(t["shapes"][shp]); txt_shape.set_color(c); box.set_edgecolor(c)
        txt_spread.set_text(f"{e:+.2f} pts".replace(".", dec)); txt_spread.set_color(c)
        txt_rec.set_visible(any(a <= d <= b for a, b in recessions))
        txt_comment.set_text(comments[i])
        trace.set_data(dates[: i + 1], spreads[: i + 1])
        cursor.set_xdata([d, d])

    return fig, draw


def make_video(df, fmt, lang):
    fig, draw = build_figure(df, fmt, lang)
    n = len(df)
    times = (list(np.repeat(0.0, 45))
             + list(np.linspace(0, n - 1, (n - 1) * FRAMES_PER_MONTH + 1))
             + list(np.repeat(float(n - 1), 120)))
    name = f"yield_curve_{lang}_{PLATFORMS[fmt]}_{fmt.replace(':', 'x')}"
    path = os.path.join(OUTPUT_DIR, name + ".mp4")

    writer = FFMpegWriter(fps=FPS, bitrate=8000, codec="libx264", extra_args=["-pix_fmt", "yuv420p"])
    print(f"\n{name}: rendering {len(times)} frames...")
    with writer.saving(fig, path, dpi=100):
        for k, tt in enumerate(times):
            draw(tt)
            writer.grab_frame(facecolor=BG)
            if k % 400 == 0:
                print(f"  {k}/{len(times)}")
    draw(float(n - 1))
    fig.savefig(os.path.join(OUTPUT_DIR, name + "_preview.png"), facecolor=BG)
    plt.close(fig)

    duration = len(times) / FPS
    if MUSIC_FILE and fmt in MUSIC_FORMATS:
        add_music(path, duration)
    print(f"  saved: {path} ({duration:.0f} s)")


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    setup_ffmpeg()
    if MUSIC_FILE and not os.path.exists(MUSIC_FILE):
        raise FileNotFoundError(f"Music file not found: {MUSIC_FILE}")
    data = load_data()
    for lang in LANGUAGES:
        for fmt in FORMATS:
            make_video(data, fmt, lang)
    print("\nDone. 16:9 -> YouTube, X, LinkedIn | 4:5 -> LinkedIn feed | 9:16 -> TikTok, Shorts, Reels")
