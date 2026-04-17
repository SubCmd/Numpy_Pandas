# 2-2. 데이터 선택 & 필터링

# 1. loc vs. iloc - 가장 중요
# | 접근자 | 기반 | 사용법 | stop 포함 여부 |
# | --- | ------ | ------| -------------|
# | loc | 레이블(이름) | df.loc["mon", "DAU"] | 포함(inclusive) |
# | iloc | 정수 위치 | df.iloc[0, 0] | 미포함(exclusive) |

# 핵심 암기:
# loc  = Label-based  → 이름으로 접근, 끝값 포함
# iloc = Integer-based → 번호로 접근, 끝값 미포함 (파이썬 슬라이싱 규칙)

# 필터링 방법 3가지?
# | 방법 | 사용법 | 장점 | 
# | 불리언 마스크 | df[df["col"] > 100] | 가장 기본, NumPy와 동일| 
# | loc + 조건 | df.loc[조건, 열] | 행 필터 + 열 선택 동시 |
# | query() | df.query("col > 100") | SQL처럼 읽기 쉬움 |


# 2-1. loc - 레이블 기반
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "DAU": [3200, 3450, 3100, 3800, 3650, 2900, 2700],
    "매출": [1200, 1350, 980, 1500, 1420, 1100, 1680],
    "전환율": [3.2, 3.5, 2.9, 3.8, 3.6, 2.5, 2.1],
}, index=["월", "화", "수", "목", "금", "토", "일"])

print(df.shape)

# ── 단일 값 ──
print(df.loc["월", "DAU"])      # 3200

# ── 행 범위 (끝값 포함!) ──
print(df.loc["월":"수"])        # 월, 화, 수 3행 모두 포함

# ── 특정 행 + 특정 열 ──
print(df.loc["월":"수", "DAU":"매출"]) # 3행 x 2열

# ── 특정 행 리스트 ──
print(df.loc[["월", "수", "금"]])

# ── 모든 행, 특정 열 ──
print(df.loc[:, "DAU"])         # DAU 열 전체 (Series)
print(df.loc[:, ["DAU", "전환율"]]) # 2개 열 (DataFrame)

# ── 조건부 행 선택 + 열 선택 ──
print(df.loc[df["DAU"] >= 3200, ["DAU", "매출"]])
# → DAU 3200 이상인 행의 DAU, 매출만 출력


# 2-2. iloc - 정수 위치 기반
# ── 단일 값 ──
print(df.iloc[0, 0])              # 3200 (0행 0열)

# ── 행 범위 (끝값 미포함!) ──
print(df.iloc[0:3])               # 0, 1, 2행 (3개)

# ── 특정 행/열 번호 리스트 ──
print(df.iloc[[0, 2, 4], [0, 2]])  # 0,2,4행의 0,2열

# ── 마지막 행 ──
print(df.iloc[-1])                 # 일요일 행

# ── 마지막 3행 ──
print(df.iloc[-3:])                # 금, 토, 일

# ── 실무 패턴: 정수 인덱스 DataFrame에서 ──
df2 = df.reset_index()  # 인덱스가 0, 1, 2, ...로 변경
# 이 경우 loc[0]과 iloc[0]이 같은 결과 -> 혼동 주의!


# 2-3. 불리언 필터링
# ── 단일 조건 ──
high_dau = df[df["DAU"] >= 3200]
print(high_dau)

# ── 복합 조건: & (and), | (or), ~ (not) ──
# DAU 3000 이상 AND 전환율 3.0 이상
good_days = df[(df["DAU"] >= 3000) & (df["전환율"] >= 3.0)]
print(good_days)

# DAU 3500 이상 OR 매출 1500 이상
strong_days = df[(df["DAU"]>=3500) | (df["매출"] >= 1500)]
print(strong_days)

# 전환율 3.0 미만이 아닌 날 (= 3.0 이상)
not_low = df[~(df["전환율"] < 3.0)]
print(not_low)

# ── isin: 특정 값 목록에 포함 여부 ──
target_days = df[df.index.isin(["월", "수", "금"])]
print(target_days)

# ── between: 범위 필터 ──
mid_dau = df[df["DAU"].between(3000, 3500)] # 3000 이상 3500 이하

# ── 결측치 ──
null = df[df["DAU"].isna()]
print(null)


# 2-4. query() — SQL 스타일 필터링
# ── 기본 사용 ──
print(df.query("DAU >= 3200"))

# ── 복합 조건 ──
print(df.query("DAU >= 3000 and 전환율 >= 3.0"))
print(df.query("DAU >= 3500 or 매출 >= 1500"))

# ── 변수 참조: @ 접두사 ──
threshold = 3200
print(df.query("DAU >= @threshold"))

# ── 문자열 조건 ──
df_plans = pd.DataFrame({
    "user": [1, 2, 3, 4, 5],
    "plan": ["pro", "basic", "pro", "enterprise", "basic"],
    "mrr": [49000, 19000, 49000, 199000, 19000],
})

print(df_plans.query("plan == 'pro'"))
print(df_plans.query("plan in ['pro', 'enterprise']"))

# query vs 불리언 비교
# 불리언:  df[(df["DAU"] >= 3000) & (df["전환율"] >= 3.0)]
# query:   df.query("DAU >= 3000 and 전환율 >= 3.0")
# → query가 더 읽기 쉽고 SQL에 익숙하면 직관적


# 2-5. 값 수정 (loc 활용)
# ── 특정 셀 수정 ──
df.loc["월", "DAU"] = 3250
print(df)

# ── 조건부 수정 ──
df.loc[df["전환율"] < 2.5, "전환율"] = 2.5 # 최솟값 보정
# "loc[조건, 행] = 숫자" : 조건에 맞는 행을 숫자로 변환

# ── 새 열 조건부 생성 ──
df["성과등급"] = "보통"
df.loc[df["매출"] >= 1400, "성과등급"] = "우수"
df.loc[df["매출"] < 1000, "성과등급"] = "미달"
print(df[["매출", "성과등급"]])

# ── np.where 활용 (한 줄) ──
df["주말여부"] = np.where(df.index.isin(["토", "일"]), "주말", "주중")
print(df)
# np.where(조건, "주말", "주중")
# "토", "일"이면 True 


# ================================================================================================
# 연습 문제
# Lv.1 기본 — 문법 확인

# 문제 1-1) loc vs iloc 구분
df = pd.DataFrame({
    "매출": [100, 200, 300, 400, 500],
    "비용": [80, 150, 200, 350, 420],
}, index=["A", "B", "C", "D", "E"])

# 결과 예측하기
# 1. df.loc["B", "매출"]
# 200
print(df.loc["B", "매출"])

# 2. df.iloc[1, 0]
# 200
print(df.iloc[1, 0])

# 3. df.loc["A":"C"]         → 몇 행?
# 3행
print(df.loc["A":"C"])

# 4. df.iloc[0:3]            → 몇 행?
# 3행
print(df.iloc[0:3])

# 5. df.loc["A":"C", "매출"]  → 어떤 타입?
# series
print(df.loc["A":"C", "매출"].dtypes)

# 6. df.iloc[0:3, 0:1]       → 어떤 타입?
# dataframe
print(df.iloc[0:3, 0:1].dtypes)

# ⚠️ 핵심:
# loc["A":"C"] → 3행 (끝 포함)
# iloc[0:3]    → 3행 (끝 미포함)
# 결과 같지만 규칙이 다르다!


# 문제 1-2) 필터링 기초
np.random.seed(42)
df = pd.DataFrame({
    "채널": ["organic"]*5 + ["paid"]*5 + ["social"]*5,
    "DAU": np.random.randint(500, 3000, size=15),
    "CVR": np.round(np.random.uniform(1.0, 6.0, size=15), 1),
})
print(df)

# 1. DAU 1500 이상인 행
print(f"DAU 1500 이상 : {df[df['DAU'] >= 1500]}")

# 2. 채널이 "paid"인 행
print(f"paid : {df[df['채널'] == 'paid']}")

# 3. CVR이 3.0 이상 5.0 이하인 행
print(df[(df['CVR'] >= 3.0) & (df['CVR'] <= 5.0)])
# print(df[df["CVR"].between(3.0, 5.0)])

# 4. organic 채널 중 DAU 1000 이상인 행
print(df[(df["채널"] == 'organic') & (df["DAU"] >= 1000)])

# 5. 위 4번을 query()로 재작성
print(df.query("(채널 == 'organic') & (DAU >= 1000)"))


# ================================================
# Lv.2 응용 — 복합 개념 조합

# 문제 2-1) 다조건 데이터 추출 & 가공
import numpy as np
import pandas as pd

np.random.seed(42)
n = 200
df = pd.DataFrame({
    "order_id": range(1, n+1),
    "user_id": np.random.randint(1000, 1200, size=n),
    "category": np.random.choice(["전자기기", "의류", "식품", "생활용품"], size=n),
    "amount": np.random.randint(5000, 200000, size=n),
    "is_returned": np.random.binomial(1, 0.08, size=n),
})
print(df)

# 1. 반품되지 않은 주문만 필터링
not_returned = df[df["is_returned"] == 0]
print(f"반품 제외 : {len(not_returned)}건")

# 2. 카테고리별 주문 건수와 평균 주문액 (groupby)
print(df.groupby("category")["amount"].agg(["count", "mean"]))

# 3. 주문액 상위 10건 추출 (nlargest)
print(df.nlargest(10, "amount")[["order_id", "category", "amount"]])

# 4. 주문액 5만원 이상 AND 반품 아닌 주문의 카테고리 분포
filtered = df[(df["amount"] >= 50000) & df["is_returned"] == 0]
print(filtered["category"].value_counts())
# 데이터프레임 내 특정 열에서 고유값들 빈도수를 계산해 내림차순으로 정렬된 Sereis 반환

# 5. 유저별 주문 횟수 계산 후, 3회 이상 주문한 유저 ID 추출
user_counts = df["user_id"].value_counts()
repeat_users = user_counts[user_counts >=3].index.tolist()
print(f"3회 이상 주문 유저: {len(repeat_users)}명")

# 6. loc으로 amount 열을 "주문금액"으로 rename 처리
df = df.rename(columns={"amount" : "주문금액"})
print(df)

'''
python 02_pandas_selection_filtering.py
'''