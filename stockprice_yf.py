#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 10:41:27 2025

@author: aaronkim
"""

import streamlit as st
import yfinance as yf
from datetime import date, timedelta
import pandas as pd

# 앱 레이아웃 설정 (페이지 전체 설정)
st.set_page_config(layout="wide")

# ====================
# 1. 왼쪽 사이드바: 사용자 입력 위젯
# ====================
st.sidebar.header('주식 데이터 설정')

# 종목명 입력
# (예시 종목: AAPL - Apple, MSFT - Microsoft, GOOG - Alphabet)
ticker_symbol = st.sidebar.text_input(
    '종목 티커 입력 (예: AAPL, 005930.KS)',
    'AAPL'
).upper() # 대문자로 변환

# 날짜 설정
today = date.today()
default_start_date = today - timedelta(days=365) # 1년 전을 기본 시작 날짜로 설정

start_date = st.sidebar.date_input(
    '시작 날짜',
    default_start_date
)

end_date = st.sidebar.date_input(
    '끝 날짜',
    today
)

# 데이터 유효성 검사
if start_date >= end_date:
    st.sidebar.error('⚠️ 시작 날짜는 끝 날짜보다 이전이어야 합니다.')
    st.stop() # 오류 발생 시 앱 실행 중지

# ====================
# 2. 메인 화면: 데이터 가져오기 및 시각화
# ====================
st.title(f"{ticker_symbol} 주가 정보 분석")

@st.cache_data # 데이터 캐싱: 동일 입력 시 재다운로드 방지
def get_stock_data(ticker, start, end):
    try:
        kkk = yf.download(ticker, start=start, end=end)
        if kkk.empty:
            return None
        return kkk
    except Exception as e:
        st.error(f"데이터를 가져오는 중 오류가 발생했습니다: {e}")
        return None

# 데이터 가져오기
data = get_stock_data(ticker_symbol, start_date, end_date)

if data is not None:
    # 2-1. 데이터 개요
    st.subheader("Close")
    st.dataframe(data['Close'].tail(), use_container_width=True)

    # 2-2. 종가 그래프
    st.subheader(f"{start_date}부터 {end_date}까지의 주가 변동 (종가)")
    
    # Streamlit의 line_chart를 사용하여 깔끔한 그래프 출력
    st.line_chart(data['Close'])

    # 2-3. 거래량 그래프
    st.subheader("거래량 추이 (Volume)")
    st.bar_chart(data['Volume'])

else:
    st.warning(f"'{ticker_symbol}'에 대한 주식 데이터를 찾을 수 없습니다. 종목 티커를 확인해 주세요.")

# 사이드바 맨 아래에 참고 정보 추가
st.sidebar.markdown('---')
st.sidebar.markdown('**참고:** 미국 주식은 티커만, 한국 주식은 종목 코드 뒤에 `.KS`(코스피) 또는 `.KQ`(코스닥)를 붙여야 합니다. (예: 삼성전자 -> 005930.KS)')