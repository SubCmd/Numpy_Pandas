# 2-1. Series & DataFrame 기초

# Pandas?
# : Pandas는 표 형태(tabular) 데이터를 다루기 위한 파이썬 핵심 라이브러리
# : NumPy 배열 위에 레이블(인덱스, 컬럼명)을 입힌 것이 핵심 차이

'''
| 특성 | NumPy | Pandas |
| --- | --- | ------|
| 데이터 구조 | ndarray(숫자 배열) | Series / DataFrame(레이블 있는 표) |
| 데이터 타입 | 단일 dtype | 열마다 다른 dtype 가능 |
| 인덱싱 | 정수 위치 기반 | 레이블 + 위치 모두 가능 |
| 결측치 | 직접 관리 | NaN 내장 지원 |
| 활용 | 수치 연산, 선형대수 | 데이터 전처리, EDA, 분석 |
'''

# Series란?
# : 1차원 레이블이 있는 배열. 인덱스(index) + 값(values)으로 구성됨.
'''
인덱스    값
"월"  →  1200
"화"  →  1350
"수"  →  980
'''

# DataFrame이란?
# : 2차원 레이블이 있는 표. 행 인덱스(index) + 열 이름(columns) + 값으로 구성됨.
# : 여러 Series가 열 방향으로 결합된 것이라 이해할 수 있음.
'''
        DAU    매출    전환율
월      3200   1200    3.2
화      3450   1350    3.5
수      3100    980    2.9
'''

# PM/분석가 관점에서의 핵심
# - SQL 테이블 ≈ DataFrame
# - Excel 시트 ≈ DataFrame
# - GA4 내보내기 데이터 ≈ DataFrame
# - 분석의 80%는 DataFrame 조작이다


# 2-1. Series 생성과 기본 조회
from locale import normalize
import numpy as np
import pandas as pd

# ── 리스트로 생성 ──
daily_dau = pd.Series([3200, 3450, 3100, 3800, 3650, 2900, 2700])
print(daily_dau)
# 0    3200
# 1    3450
# ...
# dtype: int64

# ── 인덱스 지정 ──
days = ["월", "화", "수", "목", "금", "토", "일"]
daily_dau = pd.Series([3200, 3450, 3100, 3800, 3650, 2900, 2700], index=days)
print(daily_dau)
# 월    3200
# 화    3450
# 수    3100
# ...

# ── 딕셔너리로 생성 ──
channel_cvr = pd.Series({
    "organic": 3.2,
    "paid": 4.5,
    "social": 1.8,
    "email": 5.1,
    "referral": 3.8,
})

# ── 기본 속성 ──
print(f"shape : {daily_dau.shape}")     # (7,)
print(f"dtype : {daily_dau.dtype}")     # int64
print(f"index : {daily_dau.index.tolist()}")    # ['월', '화', ...]
print(f"values : {daily_dau.values}")     # NumPy 배열 반환
print(f"name : {daily_dau.name}")       # None

daily_dau.name = "DAU"
print(daily_dau.name)   # DAU

# ── 기본 통계 ──
print(daily_dau.describe())
# count       7.0
# mean     3257.1
# std       404.5
# min      2700.0
# 25%      3000.0
# 50%      3200.0
# 75%      3550.0
# max      3800.0


# 2-2. DataFrame 생성
# ── 딕셔너리로 생성 (가장 흔한 방법) ──
df = pd.DataFrame({
        "DAU" : [3200, 3450, 3100, 3800, 3650, 2900, 2700],
        "매출" : [1200, 1350, 980, 1500, 1420, 1100, 1680],
        "전환율" : [3.2, 3.5, 2.9, 3.8, 3.6, 2.5, 2.1],
        "신규가입" : [150, 230, 180, 290, 310, 275, 340],
},index=["월", "화", "수", "목", "금", "토", "일"])

print(df)
#     DAU    매출  전환율  신규가입
# 월  3200  1200   3.2    150
# 화  3450  1350   3.5    230
# ...

# ── NumPy 배열로 생성 ──
np.random.seed(42)
data = np.random.randint(100, 500, size=(5, 3))
df_np = pd.DataFrame(data,
                        columns=["세션수", "페이지뷰", "전환수"],
                        index=[f"Week_{i}" for i in range(1, 6)]
                        )
print(f"NumPy 배열 df : ")
print(f"{df_np}")

# ── 리스트 of 딕셔너리로 생성 (API 응답, JSON 파싱 후) ──
records = [
    {"user_id": 1001, "plan": "pro", "mrr": 49000},
    {"user_id": 1002, "plan": "basic", "mrr": 19000},
    {"user_id": 1003, "plan": "enterprise", "mrr": 199000},
]
df_records = pd.DataFrame(records)
print(f"DF 딕셔너리")
print(f"{df_records}")


# 2-3. DataFrame 기본 속성 & 조회

df = pd.DataFrame({
    "DAU": [3200, 3450, 3100, 3800, 3650, 2900, 2700],
    "매출": [1200, 1350, 980, 1500, 1420, 1100, 1680],
    "전환율": [3.2, 3.5, 2.9, 3.8, 3.6, 2.5, 2.1],
    "신규가입": [150, 230, 180, 290, 310, 275, 340],
    }, index=["월", "화", "수", "목", "금", "토", "일"])

print(df)

# ── 기본 속성 ──
print(f"shape: {df.shape}")           # (7, 4)
print(f"columns: {df.columns.tolist()}")  # ['DAU', '매출', '전환율', '신규가입']
print(f"index: {df.index.tolist()}")      # ['월', '화', ...]
print(f"dtypes:\n{df.dtypes}")
# DAU       int64
# 매출      int64
# 전환율    float64
# 신규가입   int64

# ── 빠른 탐색 5종 세트 ──
print("DF 가장 위에서 3개")
print(df.head(3))       # 처음 3행
print("DF 가장 아래에서 3개")
print(df.tail(2))       # 마지막 2행
print(df.info())        # 전체 구조 요약 (dtype, non-null count)
print(df.describe())    # 수치형 컬럼 통계
print(df.shape)         # (행, 열) 개수

# ── 열 선택 ──
dau_series = df["DAU"]           # Series 반환
print(type(dau_series))          # <class 'pandas.core.series.Series'>
print(dau_series)

dau_df = df[["DAU"]]             # DataFrame 반환 (대괄호 이중)
print(type(dau_df))              # <class 'pandas.core.frame.DataFrame'>
print(dau_df)

multi_cols = df[["DAU", "매출"]]  # 복수 열 선택
print(multi_cols.shape)           # (7, 2)

# ── 열 추가 ──
df["ARPU"] = df["매출"] / df["DAU"] * 1000 # 파생지표
# Average Revenue Per User (사용자당 평균 매출)
df["목표달성"] = df["매출"] >= 1200          # 불리언 열

print(df.head(3))

# ── 열 삭제 ──
df_clean = df.drop(columns=["목표달성"])
# 또는 원본 수정 : df.drop(columns=["목표달성"], inplace=True)


# 2-4. Series 연산 (벡터화)
# Series도 NumPy처럼 벡터화 연산 가능
revenue =df["매출"]

# 스칼라 연산
print(revenue * 1.1)    # 10% 증사
print(revenue / 10000)  # 억원 단윈 변환

# Series 간 연산 (인덱스 자동 정렬!)
arpu = df["매출"] / df["DAU"] * 10000
print(arpu)

# ⚠️ 인덱스 정렬 주의
s1 = pd.Series([10, 20, 30], index=["a", "b", "c"])
s2 = pd.Series([100, 200, 300], index=["b", "c", "d"])
print(s1)
print(s2)
print(s1 + s2)
# a      NaN   ← s2에 "a" 없음
# b    120.0
# c    230.0
# d      NaN   ← s1에 "d" 없음
# → 인덱스가 일치하지 않으면 NaN 발생!


# 2-5. 값 카운트 & 고윳값
plans = pd.Series(["pro", "basic", "pro", "business", "basic",
                   "pro", "basic", "pro", "business", "pro"])

# 빈도 카운트
print(plans.value_counts())     # Series(열)에 각 값이 몇 번 등장하는지? (빈도)
# pro           5
# basic         3
# enterprise    2

# 비율
print(plans.value_counts(normalize=True))       # 전체 대비 비율(확률)로 변환
# pro           0.5
# basic         0.3
# enterprise    0.2

# 고윳값
print(plans.unique())   # ['pro', 'basic', 'business']  # 중복 제거된 실젯값 반환
print(plans.nunique())  # 3     # 갯수만 반환


# ================================================================================================
# 연습 문제
# Lv.1 기본

# 문제 1-1) Series 생성 & 조회
# 데이터 : 5개 마케팅 채널 이번 달 전환 수
# - organic: 1200
# - paid_search: 850
# - social: 620
# - email: 950
# - referral: 430

import pandas as pd

# 1. 딕셔너리로 Series 생성 (name="월간전환")
conv = pd.Series({"organic" : 1200, "paid_search" : 850,
        "social" : 620, "email" : 950, "referral" : 430
        }, name="월간전환")
print(conv)

# 2. shape, dtype, index 속성 출력
print(f"shape : {conv.shape}")  # (5, )
print(f"dtype : {conv.dtype}")  # int64
print(f"index : {conv.index}")  # 

# 3. 전환 수가 가장 많은 채널과 가장 적은 채널 (idxmax, idxmin)
print(f"최대 채널 : {conv.idxmax()} ({conv.max()})")
print(f"최소 채널 : {conv.idxmin()} ({conv.min()})")

# 4. 전환 수 800 이상인 채널만 필터링
print(conv[conv >= 800])
# organic        1200
# paid_search     850
# email           950

# 5. describe() 결과 확인
print(conv.describe())


# 문제 1-2) DataFrame 생성 & 기본 조회
# 데이터: 4개 제품의 분기 성과
product_data = {
    "제품명": ["Dashboard", "Analytics", "Automation", "Reporting"],
    "Q1_매출": [4500, 3200, 2800, 1500],
    "Q2_매출": [5200, 3800, 3100, 1800],
    "Q3_매출": [4800, 4100, 3500, 2100],
    "Q4_매출": [6100, 4500, 3900, 2400],
}

# 1. DataFrame 생성
df = pd.DataFrame(product_data)
print(df)

# 2. shape, columns, index, dtypes 확인
print(f"shape : {df.shape}")
print(f"columns : {df.columns.tolist()}")
print(f"index : {df.index.tolist()}")
print(f"dtypes : {df.dtypes}")

# 3. head(2)와 tail(2)
print(f"가장 앞 2개 값 : {df.head(2)}")
print(f"가장 뒤 2개 값 : {df.tail(2)}")

# 4. "연간매출" 열 추가 (Q1~Q4 합계)
df["연간매출"] = df["Q1_매출"] + df["Q2_매출"] + df["Q3_매출"] + df["Q4_매출"]
print(df)

# 5. "성장률" 열 추가: (Q4 - Q1) / Q1 × 100
df["성장률"] = df["Q4_매출"] - df["Q1_매출"] / df["Q4_매출"] * 100
print(df[["제품명", "연간매출", "성장률"]])

# 6. 연간매출 기준 내림차순 정렬 → sort_values
df_sorted = df.sort_values("연간매출", ascending=False)
print(df_sorted[["제품명", "연간매출"]])

# ================================================
# Lv.2 응용 — 복합 개념 조합

# 문제 2-1) 일별 지표 DataFrame 구축 & 파생 지표
np.random.seed(42)
days = 30

# 일별 데이터를 담은 DataFrame을 생성하세요:
# - 인덱스: pd.date_range("2024-01-01", periods=30, freq="D")
# - DAU: np.random.randint(3000, 5000, size=30)
# - 신규가입: np.random.randint(100, 400, size=30)
# - 전환수: np.random.randint(80, 250, size=30)
# - 매출: np.random.randint(5000, 15000, size=30)




'''
python 01_pandas_series_dataframe.py
'''