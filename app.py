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


def fetch_dxy_from_stooq(tf_label):
    """
    🔒 CRITICAL FAILOVER MECHANISM: Bypasses Yahoo completely by sourcing 
    the US Dollar Index via Stooq's public financial network.
    """
    # Stooq identifier for the US Dollar Index is USDX
    url = f"https://stooq.com/q/d/l/?s=usdx&i={tf_label.lower()}"
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = r.get(url, headers=headers, timeout=10)
        if response.status_code == 200 and "Date" in response.text:
            lines = response.text.strip().split('\n')
            if len(lines) > 21:
                # Parse the CSV data returned by Stooq
                data = [line.split(',') for line in lines[1:]]
                df = pd.DataFrame(data, columns=lines[0].split(','))
                df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
                df = df.dropna()
                return df['Close'].tolist()
    except Exception:
        pass
    return None


def fetch_dxy_regime_data():
    """
    Part 2 Law: Connects live to Yahoo Finance for DXY. 
    If a data-center ban or block is detected, it deploys the Stooq failover mechanism.
    """
    timeframes_p2 = {"15m": "15m", "1h": "1h", "4h": "1h"}
    results = {}
    
    # Step 1: Attempt standard Yahoo Finance collection with headers
    try:
        session = r.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
        })
        ticker = yf.Ticker("DX-Y.NYB", session=session)
        
        yahoo_failed = False
        for tf_label, yf_interval in timeframes_p2.items():
            period = "5d" if tf_label == "4h" else "2d"
            df = ticker.history(interval=yf_interval, period=period)
            
            if df.empty or len(df) < 20:
                yahoo_failed = True
                break
                
            if tf_label == "4h":
                df = df.resample('4h').agg({'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last'}).dropna()
                
            closes = df['Close'].tolist()
            current_price = closes[-1]
            recent_window = closes[-20:]
            max_boundary = max(recent_window)
            min_boundary = min(recent_window)
            range_width = (max_boundary - min_boundary) / min_boundary
            sma20 = pd.Series(closes).rolling(window=20).mean().iloc[-1]
            
            if range_width <= 0.010:
                if abs(current_price - sma20) / sma20 <= 0.001:
                    results[tf_label] = {"regime": "RANGING", "character": "INTERNAL BOX"}
                else:
                    results[tf_label] = {"regime": "RANGING", "character": "BOX"}
            else:
                results[tf_label] = {"regime": "TRENDING", "character": "CLEAR"}
                
        if not yahoo_failed and len(results) == 3:
            return results
            
    except Exception:
        pass

    # Step 2: FAILOVER TRIGGERED — Sourcing from Stooq Infrastructure
    for tf_label in ["15m", "1h", "4h"]:
        # Map parameters to Stooq data files
        stooq_tf = "d" if tf_label == "4h" else tf_label
        closes = fetch_dxy_from_stooq(stooq_tf)
        
        if closes and len(closes) >= 20:
            current_price = closes[-1]
            recent_window = closes[-20:]
            max_boundary = max(recent_window)
            min_boundary = min(recent_window)
            range_width = (max_boundary - min_boundary) / min_boundary
            sma20 = pd.Series(closes).rolling(window=20).mean().iloc[-1]
            
            source_tag = " (FAILOVER)"
            if range_width <= 0.010:
                if abs(current_price - sma20) / sma20 <= 0.001:
                    results[tf_label] = {"regime": "RANGING", "character": f"INTERNAL BOX{source_tag}"}
                else:
                    results[tf_label] = {"regime": "RANGING", "character": f"BOX{source_tag}"}
            else:
                results[tf_label] = {"regime": "TRENDING", "character": f"CLEAR{source_tag}"}
        else:
            results[tf_label] = {"regime": "OFFLINE", "character": "DATA WALL"}
            
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
                
