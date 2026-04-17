# Phase 2-4: 결측치 처리

# 결측치(Missing values)란?
# : 데이터에서 값이 없는 상태. Pandas에서는 NaN(Not a Number) 또는 None, pd.NA로 표현됨

# 결측치 처리 전략
# | 전략 | 방법 | 적합한 경우 |
# | ---- | ---- | -----------|
# | 삭제 | dropna() | 결측 비율 낮고, 데이터 충분할 때 |
# | 채우기(상수) | fillna(0) | 결측=0이 논리적일 때(매출, 전환수) | 
# | 채우기(통계) | fillna(mean()) | 평균/중앙값으로 대체 |
# | 앞/뒤 값 | ffill(), bfill() | 시계열에서 이전/다음 값 전파 |
# | 보간 | interpolate() | 시계열 트렌드 유지 |
# | 그룹별 채우기 | groupby + fillna | 세그먼트별 대푯값으로 대체 |

# 핵심 함수
'''
df.isna()           # 결측 여부 (True/False)
df.notna()          # 비결측 여부
df.isna().sum()     # 열별 결측 수
df.dropna()         # 결측 행 삭제
df.fillna(value)    # 결측 채우기
df.interpolate()    # 선형 보간
'''


# 2-1. 결측치 탐지
import numpy as np
import pandas as pd

df = pd.DataFrame({
    "DAU": [3200, np.nan, 3100, 3800, np.nan, 2900, 2700],
    "매출": [1200, 1350, np.nan, 1500, 1420, np.nan, 1680],
    "전환율": [3.2, 3.5, 2.9, np.nan, 3.6, 2.5, 2.1],
    "채널": ["organic", None, "paid", "social", "organic", "paid", None],
}, index=["월", "화", "수", "목", "금", "토", "일"])

# ── 결측 여부 확인 ──
print(df.isna())          # 전체 True/False 테이블
print(df.isna().sum())    # 열별 결측 수
# DAU     2
# 매출    2
# 전환율  1
# 채널    2

print(f"전체 결측 수 : {df.isna().sum().sum()}")    # 전체 결측 수: 7

# ── 결측이 있는 행만 보기 ──
print(df[df.isna().any(axis=1)])    # 하나라도 결측인 행

# ── 결측이 없는 행만 보기 (완전한 행) ──
print(df.dropna())  # 모든 열이 비결측인 행만


# 2-2. dropna — 결측 행/열 삭제
# ── 기본: 하나라도 결측이면 행 삭제 ──
df_clean = df.dropna()
print(f"삭제 전 : {len(df)}행 → 삭제 후: {len(df_clean)}행")

# ── 특정 열 기준으로만 삭제 ──
df_dau_clean = df.dropna(subset=["DAU"])    # DAU가 NaN인 행만 삭제
print(f"DAU 기준 삭제: {len(df_dau_clean)}행")

# ── 모든 값이 결측인 행만 삭제 ──
df.dropna(how="all")  # 모든 열이 NaN인 행만 삭제

# ── 결측이 N개 이상인 행 삭제 ──
df.dropna(thresh=3)   # 비결측 값이 3개 이상인 행만 유지

# ── 열 삭제 (axis=1) ──
df.dropna(axis=1)     # 결측이 있는 열 전체 삭제 (주의: 과도한 삭제)


# 2-3. fillna — 결측 채우기
# ── 상수로 채우기 ──
df["매출"].fillna(0)              # 0으로
df["채널"].fillna("unknown")      # 문자열

# ── 통계값으로 채우기 ──
df["DAU"].fillna(df["DAU"].mean())       # 평균
df["DAU"].fillna(df["DAU"].median())     # 중앙값 (이상치에 강건)

# ── 열별로 다른 값 ──
fill_values = {
    "DAU": df["DAU"].median(),
    "매출": 0,
    "전환율": df["전환율"].mean(),
    "채널": "unknown",
}
df_filled = df.fillna(fill_values)
print(df_filled)

# ── 앞/뒤 값으로 채우기 (시계열) ──
df["DAU"].ffill()    # Forward fill: 이전 값으로 채움
df["DAU"].bfill()    # Backward fill: 다음 값으로 채움

# 시계열 예시
ts = pd.Series([100, np.nan, np.nan, 200, np.nan, 300],
               index=pd.date_range("2024-01-01", periods=6))
print("원본:", ts.values)       # [100. nan nan 200. nan 300.]
print("ffill:", ts.ffill().values)  # [100. 100. 100. 200. 200. 300.]
print("bfill:", ts.bfill().values)  # [100. 200. 200. 200. 300. 300.]

# ── 선형 보간 ──
print("보간:", np.round(ts.interpolate().values))
# [100. 133.3 166.7 200. 250. 300.] — 트렌드 유지


# 2-4. 그룹별 결측 채우기
# 채널별 평균 전환율로 채우기
df2 = pd.DataFrame({
    "채널": ["organic", "organic", "paid", "paid", "organic", "paid"],
    "CVR": [3.2, np.nan, 4.5, np.nan, 3.0, np.nan],
})

# 각 채널의 평균으로 해당 채널의 결측을 채움
df2["CVR"] = df2.groupby("채널")["CVR"].transform(
    lambda x: x.fillna(x.mean())
)
print(df2)
# organic 결측 → organic 평균(3.1)으로
# paid 결측 → paid 평균(4.5)으로


# 2-5. 결측 패턴 시각화 준비
# 결측 요약 함수
def missing_summary(df):
    """결측치 현황 요약 DataFrame 반환"""
    missing = df.isna().sum()
    pct = df.isna().mean() * 100
    summary = pd.DataFrame({
        "결측수": missing,
        "결측률(%)": pct.round(1),
        "dtype": df.dtypes,
    })
    return summary[summary["결측수"] > 0].sort_values("결측수", ascending=False)

# 사용
print(missing_summary(df))


# ================================================================================================
# 연습 문제
# Lv.1 기본

# 문제 1-1) 결측 탐지 & 기본 처리
df = pd.DataFrame({
    "이름": ["김철수", "이영희", None, "박민수", "최지우"],
    "점수": [85, np.nan, 72, 90, np.nan],
    "등급": ["A", "B", np.nan, "A", "C"],
    "출석": [10, 9, 8, np.nan, 10],
})

# 1. 열별 결측 수 확인
print(f"열별 결측 수 : {df.isna().sum()}")

# 2. 결측이 있는 행만 출력
print(f"결측이 있는 행 : {df[df.isna().any(axis=1)]}")

# 3. 점수: 평균으로 채우기
df["점수"] = np.round(df["점수"].fillna(df["점수"].mean()),1)

# 4. 등급: "미분류"로 채우기
df["등급"] = df["등급"].fillna("미분류")

# 5. 이름: 결측인 행 삭제
df = df.dropna(subset=["이름"])

# 6. 출석: 중앙값으로 채우기
df["출석"] = df["출석"].fillna(df["출석"].median())

print(df)



'''
py 04_pandas_missing_values.py
'''