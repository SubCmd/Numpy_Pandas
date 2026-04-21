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


# 2-2. 커스텀 집계 함수
# ── lambda 활용 ──
# 매출 상위 10% 평균 (고가치 유저 지표)
top10_avg = df.groupby("channel")["revenue"].agg(
    lambda x: x.quantile(0.9)
)

# ── 사용자 정의 함수 ──
def revenue_stats(x):
    return pd.Series({
        "총매출": x.sum(),
        "평균": x.mean(),
        "중앙값": x.median(),
        "변동계수": x.std() / x.mean() * 100,  # CV%
        "P90": x.quantile(0.9),
    })

print(df.groupby("channel")["revenue"].apply(revenue_stats).unstack())


# 2-3. transform - 원본 shape 유지
# ── 그룹 평균을 원본 각 행에 매핑 ──
df["channel_avg_rev"] = df.groupby("channel")["revenue"].transform("mean")
# 각 행에 해당 채널의 평균 매출이 들어감

# ── 그룹 내 비중 계산 ──
df["rev_share"] = df["revenue"] / df.groupby("channel")["revenue"].transform("sum") * 100

# ── 그룹 내 정규화 (Z-score) ──
df["rev_zscore"] = df.groupby("channel")["revenue"].transform(
    lambda x: (x - x.mean()) / x.std()
)

# ── 그룹별 결측 채우기 (Phase 2-4 복습) ──
# df["col"] = df.groupby("channel")["col"].transform(lambda x: x.fillna(x.median()))

# ── 그룹 내 순위 ──
df["rank_in_channel"] = df.groupby("channel")["revenue"].rank(
    ascending=False, method="dense"
)


# 2-4. filter - 그룹 단위 필터링
# ── 건수가 20개 이상인 채널만 남기기 ──
filtered = df.groupby("channel").filter(lambda x: len(x) >= 20)
print(f"필터 전: {len(df)}행 → 필터 후: {len(filtered)}행")

# ── 평균 매출이 전체 평균 이상인 채널만 ──
overall_avg = df["revenue"].mean()
high_rev = df.groupby("channel").filter(lambda x: x["revenue"].mean() >= overall_avg)

# ── 전환이 1건 이상 있는 채널만 ──
active = df.groupby("channel").filter(lambda x: x["conversions"].sum() > 0)


# 2-5. 복수 그룹 + 언스택
# 채널 × 디바이스 매출 합계
pivot_like = df.groupby(["channel", "device"])["revenue"].sum().unstack(fill_value=0)
print(pivot_like)
# device      desktop   mobile   tablet
# channel
# email        123456   234567   345678
# organic      ...
# paid         ...
# social       ...

# 비율 계산
total_by_channel = pivot_like.sum(axis=1)
share = pivot_like.div(total_by_channel, axis=0) * 100
print(share.round(1))


# ================================================================================================
# 연습 문제
# Lv.1 기본

# 문제 1-1) GroupBy 기초
import numpy as np
import pandas as pd
np.random.seed(42)

df = pd.DataFrame({
    "부서": np.random.choice(["개발", "마케팅", "영업", "CS"], size=50),
    "직급": np.random.choice(["사원", "대리", "과장", "차장"], size=50),
    "연봉": np.random.randint(3000, 9000, size=50),
    "성과점수": np.random.randint(60, 100, size=50),
})

# 1. 부서별 평균 연봉
print(df.groupby("부서")["연봉"].mean())

# 2. 부서별 인원수, 평균 연봉, 최고 연봉 (Named Agg)
print(df.groupby("부서").agg(
    인원=("연봉", "count"),
    평균연봉=("연봉", "mean"),
    최고연봉=("연봉", "max"),
))

# 3. 부서 × 직급별 평균 성과점수
print(df.groupby(["부서", "직급"])["성과점수"].mean().unstack())

# 4. 각 직원의 부서 내 연봉 순위 (transform + rank)
df["부서내순위"] = df.groupby("부서")["연봉"].rank(ascending=False, method="dense").astype(int)
print(df[["부서", "연봉", "부서내순위"]].sort_values(["부서", "부서내순위"]).head(10))

# 5. 인원이 10명 이상인 부서만 필터링 (filter)
filtered = df.groupby("부서").filter(lambda x: len(x) >= 10)
print(f"필터 후: {filtered['부서'].value_counts()}")



'''
py 0301_pandas_groupby.py
'''