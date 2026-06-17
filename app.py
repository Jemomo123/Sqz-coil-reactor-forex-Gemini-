import os
import time
import pandas as pd
import numpy as np
import streamlit as st
import yfinance as yf
import requests as r

# ==============================================================================
# 🏛️ JEREMIAH EDGE ARCHITECTURE LAW: CONFIGURATION & MOBILE WORKSPACE SETTINGS
# ==============================================================================
st.set_page_config(
    page_title="JEREMIAH EDGE FOREX", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# Persistent Network Connection Pool
@st.cache_resource
def get_global_network_session():
    """Establishes a single, reusable connection pool to prevent rate-limit blocks."""
    session = r.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
    })
    return session

GLOBAL_SESSION = get_global_network_session()

# Initialize Advanced Cache Matrix with Expiry Safeguards
if 'PRO_DXY_CACHE' not in st.session_state:
    st.session_state['PRO_DXY_CACHE'] = {
        "15m": {"regime": "UNKNOWN", "character": "INITIALIZING", "timestamp": 0.0},
        "1h": {"regime": "UNKNOWN", "character": "INITIALIZING", "timestamp": 0.0},
        "4h": {"regime": "UNKNOWN", "character": "INITIALIZING", "timestamp": 0.0}
    }

TIMEFRAMES = ["5m", "15m", "1h"]
FOREX_THRESHOLD = 0.0003

WATCHLIST = [
    "EURUSD=X", "GBPUSD=X", "AUDUSD=X", "NZDUSD=X", "USDJPY=X",
    "USDCAD=X", "USDCHF=X", "EURGBP=X", "EURJPY=X", "GBPJPY=X",
    "AUDJPY=X", "CHFJPY=X", "EURCAD=X", "GBPCAD=X", "EURAUD=X"
]

# ==============================================================================
# DATA CALCULATION PIPELINE
# ==============================================================================
def calculate_sma(prices, period):
    return pd.Series(prices).rolling(window=period).mean().iloc[-1]

def fetch_forex_candles(symbol, timeframe):
    yf_tf_map = {"5m": "5m", "15m": "15m", "1h": "1h"}
    interval = yf_tf_map.get(timeframe, "15m")
    try:
        ticker = yf.Ticker(symbol, session=GLOBAL_SESSION)
        df = ticker.history(interval=interval, period="5d")
        if not df.empty and len(df) >= 200:
            return df['Close'].tolist()
    except Exception:
        pass
    return None

def run_pure_compression_math(symbol, timeframe):
    closes = fetch_forex_candles(symbol, timeframe)
    if not closes or len(closes) < 200:
        return {"sqz": False, "type": "NONE"}
    
    live_price = closes[-1]
    sma20 = calculate_sma(closes, 20)
    sma100 = calculate_sma(closes, 100)
    sma200 = calculate_sma(closes, 200)
    
    price_to_sma20 = round(abs(live_price - sma20) / live_price, 5)
    sma20_to_sma100 = round(abs(sma20 - sma100) / sma20, 5)
    sma20_to_sma200 = round(abs(sma20 - sma200) / sma20, 5)
    
    cond1 = price_to_sma20 <= FOREX_THRESHOLD
    cond2 = sma20_to_sma100 <= FOREX_THRESHOLD
    cond3 = sma20_to_sma200 <= FOREX_THRESHOLD
    
    if cond1 and cond2:
        return {"sqz": True, "type": "ALL TOGETHER"}
    elif cond1 and cond3:
        return {"sqz": True, "type": "SPECIAL ONE"}
        
    return {"sqz": False, "type": "NONE"}

# ==============================================================================
# INSTITUTIONAL GEOMEAN SYNTHETIC DXY MATRIX
# ==============================================================================
def fetch_institutional_component(symbol, interval, period):
    """Fetches clean time-series Series retaining Datetime index structures."""
    try:
        ticker = yf.Ticker(symbol, session=GLOBAL_SESSION)
        df = ticker.history(interval=interval, period=period)
        if not df.empty and len(df) > 0:
            return df['Close']
    except Exception:
        pass
    return None

def calculate_pure_synthetic_dxy(interval, period):
    """Executes true institutional geometric mean across all 6 basket pairs."""
    pairs = {
        "EURUSD": "EURUSD=X", "USDJPY": "USDJPY=X", "GBPUSD": "GBPUSD=X",
        "USDCAD": "USDCAD=X", "USDSEK": "USDSEK=X", "USDCHF": "USDCHF=X"
    }
    
    data = {}
    for key, ticker_symbol in pairs.items():
        series = fetch_institutional_component(ticker_symbol, interval, period)
        if series is not None:
            data[key] = series
            
    # Failover Safety: Check if core index drivers are missing
    if "EURUSD" not in data or "USDJPY" not in data or "GBPUSD" not in data:
        return None
        
    # Align matrix to a single shared unified timestamp tracking grid
    df_matrix = pd.DataFrame(data)
    # Forward-fill gaps to maintain active volatility instead of using broken hardcoded values
    df_matrix = df_matrix.ffill().bfill()
    
    # Mathematical execution of the official DXY geometric weighting
    synthetic_series = (
        50.14348112 *
        (df_matrix["EURUSD"] ** -0.576) *
        (df_matrix["USDJPY"] ** 0.136) *
        (df_matrix["GBPUSD"] ** -0.119) *
        (df_matrix["USDCAD"] ** 0.091) *
        (df_matrix["USDSEK"] ** 0.042) *
        (df_matrix["USDCHF"] ** 0.036)
    )
    return synthetic_series.dropna()

def fetch_dxy_regime_data():
    """
    Executes Priority Redesign Hierarchy: 
    1. Synthetic Calculations -> 2. Continuous Futures (DX=F) -> 3. Protected Cache Line
    """
    # Expanded lookback period ("14d") ensures the 4H resampler has enough bars for a true 20 SMA
    config = {
        "15m": {"interval": "15m", "period": "5d"},
        "1h": {"interval": "1h", "period": "7d"},
        "4h": {"interval": "1h", "period": "14d"} 
    }
    
    results = {}
    current_time_pulse = time.time()
    
    for tf_label, params in config.items():
        dxy_series = None
        source_label = "SYNTHETIC"
        
        # --- LAYER 1: PURE INSTITUTIONAL SYNTHETIC ---
        series_calc = calculate_pure_synthetic_dxy(params["interval"], params["period"])
        if series_calc is not None and len(series_calc) >= 25:
            dxy_series = series_calc
            
        # --- LAYER 2: FUTURES CONTINUOUS CONTRACT BACKUP ---
        if dxy_series is None:
            try:
                ticker = yf.Ticker("DX=F", session=GLOBAL_SESSION)
                df_fut = ticker.history(interval=params["interval"], period=params["period"])
                if not df_fut.empty and len(df_fut) >= 25:
                    dxy_series = df_fut['Close']
                    source_label = "DX FUTURES"
            except Exception:
                pass
                
        # --- LAYER 3: SYSTEM SESSION CACHE WITH TIME DECAY WATCHERS ---
        if dxy_series is None:
            old_cache = st.session_state['PRO_DXY_CACHE'][tf_label]
            # Flag data as STALE if it has been stuck in cache memory for more than 45 minutes
            if old_cache["timestamp"] > 0 and (current_time_pulse - old_cache["timestamp"]) > 2700:
                results[tf_label] = {
                    "regime": old_cache["regime"], 
                    "character": f"{old_cache['character'].split(' (')[0]} (STALE MEMORY)"
                }
            else:
                results[tf_label] = old_cache
            continue
            
        # --- VALID MATHEMATICAL 4H CALENDAR-TIME RESAMPLING ---
        if tf_label == "4h":
            dxy_series = dxy_series.resample('4H').last().dropna()
            
        if len(dxy_series) < 20:
            results[tf_label] = st.session_state['PRO_DXY_CACHE'][tf_label]
            continue
            
        # --- HIGH-PRECISION REGIME CALCULATIONS ---
        closes_list = dxy_series.tolist()
        current_price = closes_list[-1]
        recent_window = closes_list[-20:]
        
        max_boundary = max(recent_window)
        min_boundary = min(recent_window)
        range_width = (max_boundary - min_boundary) / min_boundary
        
        sma20 = dxy_series.rolling(window=20).mean().iloc[-1]
        
        if range_width <= 0.010:
            if abs(current_price - sma20) / sma20 <= 0.001:
                state = "RANGING"
                char = f"INTERNAL BOX ({source_label})"
            else:
                state = "RANGING"
                char = f"BOX ({source_label})"
        else:
            state = "TRENDING"
            char = f"CLEAR ({source_label})"
            
        results[tf_label] = {
            "regime": state, 
            "character": char, 
            "timestamp": current_time_pulse
        }
        st.session_state['PRO_DXY_CACHE'][tf_label] = results[tf_label]
        
    return results

# ==============================================================================
# STREAMLIT USER INTERFACE VIEWPORT
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
