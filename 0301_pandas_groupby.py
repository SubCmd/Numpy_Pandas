# Phase 3-1: GroupBy 집계

# GroupBy란?
# : Split → Apply → Combine 패턴으로 데이터를 그룹별로 나누고, 각 그룹에 함수를 적용한 뒤, 결과를 합치는 것.
# SQL의 GROUP BY와 동일한 개념이다

'''
원본 데이터                Split           Apply(sum)      Combine
───────────                ─────           ──────────      ───────
채널     매출              organic         1200+980=2180   organic  2180
organic  1200              → [1200, 980]                   paid     2770
paid     1350              paid                            social   1310
organic   980              → [1350, 1420]  1350+1420=2770
social    620              social
paid     1420              → [620, 690]    620+690=1310
social    690
'''

# 핵심메서드
# | 메서드 | 설명 | 반환 |
# |--------|------|------|
# | agg() | 복수 집계 함수 적용 | DataFrame |
# | transform() | 원본과 같은 shape 반환 | Series |
# | filter() | 그룹 조건으로 행 필터링 | DataFrame |
# | apply() | 자유로운 함수 적용 | 유연 |

# agg vs. transform vs. filter - 핵심 구분
# agg       → 그룹당 1개 값 (요약) → shape 줄어듦
# transform → 그룹 값을 원본에 매핑 → shape 유지
# filter    → 조건 만족 그룹만 남김 → 행 필터링


# 2-1. 기본 groupby + 집계
import pandas as pd
import numpy as np

np.random.seed(42)
df = pd.DataFrame({
    "channel": np.random.choice(["organic", "paid", "social", "email"], size=100),
    "device": np.random.choice(["mobile", "desktop", "tablet"], size=100),
    "sessions": np.random.randint(1, 50, size=100),
    "revenue": np.random.randint(0, 200000, size=100),
    "conversions": np.random.randint(0, 10, size=100),
})
print(df.head())

# ── 단일 열 그룹 + 단일 집계 ──
print(df.groupby("channel")["revenue"].sum())
# channel
# email      1234567
# organic    2345678
# paid       3456789
# social     1111111

# ── 단일 열 그룹 + 복수 집계 ──
print(df.groupby("channel")["revenue"].agg(["sum", "mean", "median", "count"]))

# ── 복수 열 그룹 ──
print(df.groupby(["channel", "device"])["revenue"].sum())

# ── 여러 열에 다른 집계 적용 (agg + dict) ──
result = df.groupby("channel").agg({
    "sessions": "mean",
    "revenue": ["sum", "mean"],
    "conversions": "sum",
})
print(result)

# ── Named Aggregation (권장 — 컬럼명 깔끔) ──
result = df.groupby("channel").agg(
    총매출 = ("revenue", "sum"),
    평균매출 = ("revenue", "mean"),
    총전환 = ("conversions", "sum"),
    평균세션 = ("sessions", "mean"),
    건수 = ("revenue","count"),
) # "새로운 컬럼명" = (기존 컬럼, 집계 함수)
print(result)



'''
py 0301_pandas_groupby.py
'''