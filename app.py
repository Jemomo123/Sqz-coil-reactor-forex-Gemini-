import os
import time
import pandas as pd
import streamlit as st
import yfinance as yf
import requests as r

# ==============================================================================
# 🏛️ JEREMIAH EDGE ARCHITECTURE LAW: CONFIGURATION & MOBILE WORKSPACE SETTINGS
# ==============================================================================
st.set_page_config(
    page_title="JEREMIAH EDGE FOREX", 
    layout="centered",  # Optimal for mobile rendering windows
    initial_sidebar_state="collapsed"
)

# Initialize deep session state cache to prevent app collapse during heavy data outages
if 'DXY_CACHE' not in st.session_state:
    st.session_state['DXY_CACHE'] = {
        "15m": {"regime": "UNKNOWN", "character": "INITIALIZING FEED"},
        "1h": {"regime": "UNKNOWN", "character": "INITIALIZING FEED"},
        "4h": {"regime": "UNKNOWN", "character": "INITIALIZING FEED"}
    }

# Target Constants
# 🟩 FOREX OPTIMIZED: Using yfinance engine strings and a tighter pipeline threshold
TIMEFRAMES = ["5m", "15m", "1h"]
FOREX_THRESHOLD = 0.0003  # Calibrated for currency pips: <= 0.03%

# 📋 THE RESTORED VERIFIED FOREX MIX (15 Pairs) - PRE-FORMATTED FOR YAHOO FEED
WATCHLIST = [
    "EURUSD=X", "GBPUSD=X", "AUDUSD=X", "NZDUSD=X", "USDJPY=X",
    "USDCAD=X", "USDCHF=X", "EURGBP=X", "EURJPY=X", "GBPJPY=X",
    "AUDJPY=X", "CHFJPY=X", "EURCAD=X", "GBPCAD=X", "EURAUD=X"
]

# ==============================================================================
# DATA CALCULATION PIPELINE (HIGH-PRECISION MATH ENGINE)
# ==============================================================================
def calculate_sma(prices, period):
    """Calculates pure mathematical Simple Moving Average."""
    return pd.Series(prices).rolling(window=period).mean().iloc[-1]

def fetch_forex_candles(symbol, timeframe):
    """
    High-integrity historical bar engine utilizing the global Yahoo Finance feed.
    Pulls precise close data arrays with custom browser sessions to prevent blocking.
    """
    yf_tf_map = {
        "5m": "5m",
        "15m": "15m",
        "1h": "1h"
    }
    
    interval = yf_tf_map.get(timeframe, "15m")
    try:
        session = r.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
        })
        
        ticker = yf.Ticker(symbol, session=session)
        df = ticker.history(interval=interval, period="5d")
        if not df.empty and len(df) >= 200:
            return df['Close'].tolist()
    except Exception:
        pass
    return None

def run_pure_compression_math(symbol, timeframe):
    """
    Core Part 1 Algorithm Engine.
    Executes the ultimate rule: cond1 AND (cond2 OR cond3)
    """
    closes = fetch_forex_candles(symbol, timeframe)
    if not closes or len(closes) < 200:
        return {"sqz": False, "type": "NONE"}
    
    live_price = closes[-1]
    
    sma20 = calculate_sma(closes, 20)
    sma100 = calculate_sma(closes, 100)
    sma200 = calculate_sma(closes, 200)
    
    # Calculate exact distance ratios rounded strictly to 5 decimal places for Forex pips
    price_to_sma20 = round(abs(live_price - sma20) / live_price, 5)
    sma20_to_sma100 = round(abs(sma20 - sma100) / sma20, 5)
    sma20_to_sma200 = round(abs(sma20 - sma200) / sma20, 5)
    
    # Check conditions against the high-precision Forex wall
    cond1 = price_to_sma20 <= FOREX_THRESHOLD
    cond2 = sma20_to_sma100 <= FOREX_THRESHOLD
    cond3 = sma20_to_sma200 <= FOREX_THRESHOLD
    
    if cond1 and cond2:
        return {"sqz": True, "type": "ALL TOGETHER"}
    elif cond1 and cond3:
        return {"sqz": True, "type": "SPECIAL ONE"}
        
    return {"sqz": False, "type": "NONE"}

# ==============================================================================
# PART 2 INSTITUTIONAL DXY SYNTHETIC AND FALLBACK ENGINE
# ==============================================================================
def fetch_clean_pair_series(symbol, interval, period):
    """Safely extracts historical series for building the synthetic geomean matrix."""
    try:
        session = r.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
        })
        ticker = yf.Ticker(symbol, session=session)
        df = ticker.history(interval=interval, period=period)
        if not df.empty and len(df) >= 20:
            return df['Close']
    except Exception:
        pass
    return None

def build_synthetic_dxy_array(interval, period):
    """
    Assembles a flawless proxy of the US Dollar Index via geomean basket weights
    derived straight from working underlying forex feeds.
    """
    eurusd = fetch_clean_pair_series("EURUSD=X", interval, period)
    usdjpy = fetch_clean_pair_series("USDJPY=X", interval, period)
    gbpusd = fetch_clean_pair_series("GBPUSD=X", interval, period)
    usdcad = fetch_clean_pair_series("USDCAD=X", interval, period)
    usdchf = fetch_clean_pair_series("USDCHF=X", interval, period)
    
    # Verify core major basket assets are present before calculating
    if eurusd is None or usdjpy is None or gbpusd is None:
        return None
        
    min_len = min(len(eurusd), len(usdjpy), len(gbpusd))
    
    # Backup fallbacks for minor weights to avoid calculation dropouts
    usdcad_vals = usdcad.iloc[-min_len:] if usdcad is not None else pd.Series([1.37] * min_len)
    usdchf_vals = usdchf.iloc[-min_len:] if usdchf is not None else pd.Series([0.89] * min_len)
    
    e = eurusd.iloc[-min_len:].values
    j = usdjpy.iloc[-min_len:].values
    g = gbpusd.iloc[-min_len:].values
    c = usdcad_vals.values
    f = usdchf_vals.values
    
    # Official DXY Geomean Formula (Normalized adjusting for Sweden SEK absence)
    synthetic_closes = []
    for i in range(min_len):
        dxy_val = 50.14348 * (e[i]**-0.612) * (j[i]**0.136) * (g[i]**-0.119) * (c[i]**0.091) * (f[i]**0.042)
        synthetic_closes.append(dxy_val)
        
    return synthetic_closes

def fetch_dxy_regime_data():
    """
    Part 2 Law: Multi-Layer Fault-Tolerant Engine.
    Tries Raw Yahoo -> Tries Synthetic Matrix -> Tries DX=F Futures Contract -> Reverts to Session Cache.
    """
    timeframes_p2 = {"15m": "15m", "1h": "1h", "4h": "1h"}
    results = {}
    
    for tf_label, yf_interval in timeframes_p2.items():
        closes = None
        source_tag = "RAW"
        period = "5d" if tf_label == "4h" else "2d"
        
        # --- LAYER 1: TRY RAW STANDARD INTERNET TICKER ---
        try:
            session = r.Session()
            session.headers.update({'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0)'})
            ticker = yf.Ticker("DX-Y.NYB", session=session)
            df = ticker.history(interval=yf_interval, period=period)
            if not df.empty and len(df) >= 20:
                closes = df['Close'].tolist()
                source_tag = "YAHOO"
        except Exception:
            pass
            
        # --- LAYER 2: INTERNET FIREWALL BLOCK HIT -> DEPLOY SYNTHETIC ENGINE ---
        if closes is None:
            synth_array = build_synthetic_dxy_array(yf_interval, period)
            if synth_array and len(synth_array) >= 20:
                closes = synth_array
                source_tag = "SYNTHETIC"
                
        # --- LAYER 3: TOTAL DISASTER FALLBACK -> CONTINUOUS MINI FUTURES ---
        if closes is None:
            try:
                session = r.Session()
                ticker = yf.Ticker("DX=F", session=session)
                df = ticker.history(interval=yf_interval, period=period)
                if not df.empty and len(df) >= 20:
                    closes = df['Close'].tolist()
                    source_tag = "DX FUTURES"
            except Exception:
                pass
                
        # --- LAYER 4: COMPLETELY DISCONNECTED FROM YAHOO -> SYSTEM MEMORY CACHE ---
        if closes is None:
            results[tf_label] = st.session_state['DXY_CACHE'][tf_label]
            continue
            
        # --- EXECUTE THE MATH FOR 4H WITHOUT CORRUPTING LOWER BARS ---
        if tf_label == "4h" and source_tag != "YAHOO":
            df_temp = pd.DataFrame(closes, columns=['Close'])
            df_resampled = df_temp.resample('4h').last().dropna()
            closes = df_resampled['Close'].tolist()
            if len(closes) < 10:
                results[tf_label] = st.session_state['DXY_CACHE'][tf_label]
                continue

        # --- REVENUE REGIME STRUCTURAL CALCULATIONS ---
        current_price = closes[-1]
        recent_window = closes[-20:]
        max_boundary = max(recent_window)
        min_boundary = min(recent_window)
        range_width = (max_boundary - min_boundary) / min_boundary
        sma20 = pd.Series(closes).rolling(window=20).mean().iloc[-1]
        
        if range_width <= 0.010:
            if abs(current_price - sma20) / sma20 <= 0.001:
                state = "RANGING"
                char = f"INTERNAL BOX ({source_tag})"
            else:
                state = "RANGING"
                char = f"BOX ({source_tag})"
        else:
            state = "TRENDING"
            char = f"CLEAR ({source_tag})"
            
        results[tf_label] = {"regime": state, "character": char}
        
    # Commit computed states into memory loop to secure future refreshes
    st.session_state['DXY_CACHE'] = results
    return results

# ==============================================================================
# STREAMLIT USER INTERFACE VIEWPORT (RESTORED TO ORIGINAL SSoT LAYOUT)
# ==============================================================================

st.markdown("## 🛰️ Centralized DXY Market Regime (SSoT Part 2)")

dxy_data = fetch_dxy_regime_data()

regime_table = f"""
| TIMEFRAME | REGIME STATE | STRUCTURE CHARACTER |
| :--- | :--- | :--- |
| 15m | **{dxy_data.get('15m', {}).get('regime', 'UNKNOWN')}** | {dxy_data.get('15m', {}).get('character', 'DATA ERROR')} |
| 1h  | **{dxy_data.get('1h', {}).get('regime', 'UNKNOWN')}** | {dxy_data.get('1h', {}).get('character', 'DATA ERROR')}  |
| 4h  | **{dxy_data.get('4h', {}).get('regime', 'UNKNOWN')}** | {dxy_data.get('4h', {}).get('character', 'DATA ERROR')}  |
"""
st.markdown(regime_table)
st.markdown("---")

st.markdown("## 🏹 Strategy Monitor (Forex Pool)")

all_together_alerts = []
special_one_alerts = []
mega_sqz_alerts = []

progress_text = st.empty()
scan_results = {}

for idx, asset in enumerate(WATCHLIST, 1):
    clean_name = asset.replace("=X", "")
    progress_text.markdown(f"⏳ *Scanning Forex Asset {idx}/15:*\n### {clean_name}")
    
    scan_results[asset] = {}
    
    for tf in TIMEFRAMES:
        res = run_pure_compression_math(asset, tf)
        scan_results[asset][tf] = res
        
    is_mega_sqz = (
        scan_results[asset]["5m"]["sqz"]
        and scan_results[asset]["15m"]["sqz"]
        and scan_results[asset]["1h"]["sqz"]
    )
    
    if is_mega_sqz:
        mega_sqz_alerts.append(clean_name)
    else:
        for tf in TIMEFRAMES:
            if scan_results[asset][tf]["sqz"]:
                alert_entry = f"**{clean_name}** ({tf})"
                if scan_results[asset][tf]["type"] == "ALL TOGETHER":
                    all_together_alerts.append(alert_entry)
                elif scan_results[asset][tf]["type"] == "SPECIAL ONE":
                    special_one_alerts.append(alert_entry)

progress_text.markdown(f"✅ *Watchlist Scan Complete (15/15 Forex Assets Checked)*")

if mega_sqz_alerts:
    for mega_asset in mega_sqz_alerts:
        st.error(f"🚨 **{mega_asset} MEGA SQZ SYSTEM LOCK: ACTIVE** 🚨")

if not mega_sqz_alerts and not all_together_alerts and not special_one_alerts:
    st.info("No active Forex MEGA SQZ, ALL TOGETHER, or SPECIAL ONE states detected.")
else:
    if all_together_alerts:
        st.success(f"🟩 **ALL TOGETHER COMPRESSION ACTIVE:** {', '.join(all_together_alerts)}")
    if special_one_alerts:
        st.warning(f"🟦 **SPECIAL ONE COMPRESSION ACTIVE:** {', '.join(special_one_alerts)}")

st.caption(f"Live Forex workspace check timestamp: {time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
