# Phase 2-5: 정렬 & 랭킹

# 개념 및 정의
# 중요 함수
# | 함수 | 설명 | 반환 |
# | ---- | ---- | ----|
# | sort_value() | 값 기준 정렬 | 정렬된 DataFrame | 
# | sort_index() | 인덱스 기준 정렬 | 정렬된 DataFrame |
# | rank() | 순위 분여 | 순위 Series | 
# | nlargest(n) | 상위n개 | DataFrame | 
# | nsmallest(n) | 하위n개 | DataFrame |

# rank() 동점 처리 (method 옵션)
# | method | 동작 | 예: [100, 200, 200, 300] |
# | ------ | ---- | ----------------------- |
# | average | 평균 순위(기본값) | 1, 2.5, 2.5, 4 |
# | min | 최소 순위 | 1, 2, 2, 4 | 
# | max | 최대 순위 | 1, 3, 3, 4 | 
# | first | 등장 순서 | 1, 2, 3, 4 |
# | dense | 건너뛰지 않음 | 1, 2, 2, 3 |


# 2-1. sort_values
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "채널": ["organic", "paid", "social", "email", "referral"],
    "매출": [5200, 8100, 3400, 6800, 4100],
    "CVR": [3.2, 4.5, 1.8, 5.1, 3.8],
    "CPA": [0, 2500, 1800, 800, 500],
})

# 매출 내림차순
print(df.sort_values("매출", ascending=False))

# 복수 열 정렬: CVR 내림차순 → CPA 오름차순
print(df.sort_values(["CVR", "CPA"], ascending=False))

# 원본 수정
# df.sort_values("매출", ascending=False, inplace=True)

# NaN 위치 제어
df.loc[2, "매출"] = np.nan
print(df.sort_values("매출", na_position="first"))  # NaN을 맨 위로


# 2-2. rank
df = pd.DataFrame({
    "팀": ["Alpha", "Beta", "Gamma", "Delta", "Epsilon"],
    "매출": [520, 810, 340, 680, 810],
})

# 기본 랭킹 (ascending=True → 작은 값 = 낮은 순위)
df["매출순위"] = df["매출"].rank(ascending=False)  # 큰 값 = 1등
print(df)
#       팀   매출  매출순위
# 0  Alpha   520      4.0
# 1   Beta   810      1.5  ← 동점 → 평균
# 2  Gamma   340      5.0
# 3  Delta   680      3.0
# 4 Epsilon  810      1.5

# dense: 건너뛰지 않는 순위 (리더보드에 적합)
df["dense순위"] = df["매출"].rank(ascending=False, method="dense").astype(int)
# Beta, Epsilon: 1등, Delta: 2등, Alpha: 3등, Gamma: 4등

# 백분위 순위 (pct=True)
df["상위%"] = (1 - df["매출"].rank(pct=True)) * 100


# 2-3. 실무 패턴
np.random.seed(42)
df = pd.DataFrame({
    "product": [f"P{i:03d}" for i in range(1, 21)],
    "revenue": np.random.randint(100, 5000, size=20),
    "units": np.random.randint(10, 500, size=20),
})

# 상위/하위 추출
print(df.nlargest(5, "revenue"))    # 매출 TOP 5
print(df.nsmallest(5, "revenue"))   # 매출 BOTTOM 5

# 매출 순위 + 누적 비중 (파레토 분석)
df = df.sort_values("revenue", ascending=False).reset_index(drop=True)
df["rank"] = range(1, len(df)+1)
df["cumulative_pct"] = df["revenue"].cumsum() / df["revenue"].sum() * 100
# 상위 20% 제품이 매출의 몇 %를 차지하는지
top20 = df.head(int(len(df) * 0.2))
print(f"상위 20% 제품 누적 매출 비중: {top20['cumulative_pct'].iloc[-1]:.1f}%")


# ================================================================================================
# 연습 문제
# Lv.1 기본

# 문제 1-1) sort_values
df = pd.DataFrame({
    "사원": ["A", "B", "C", "D", "E"],
    "매출": [320, 450, 280, 450, 510],
    "고객수": [15, 22, 12, 20, 25],
})

# 1. 매출 내림차순 정렬
print(df.sort_values("매출", ascending=False))

# 2. 매출 순위 (dense, 내림차순)
df["순위"] = df["매출"].rank(ascending=False, method="dense")
print(df)

# 3. 고객수 기준 상위 3명
top3 = df.nlargest(3, "고객수")
print(top3)

# 4. "객단가" 열 추가 (매출/고객수) 후 객단가 기준 정렬
df["객단가"] = df["매출"] / df["고객수"]
df_avg_sorted = df.sort_values(by="객단가", ascending=False)
print(df)


'''
py 05_pandas_sorting_ranking.py
'''