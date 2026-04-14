# 2-3: 데이터 타입 & 변환

# Q : 왜 데이터 타입이 중요한가?
# 1. 잘못된 dtype → 연산 불가, 정렬 오류, 메모리 낭비
# 2. CSV 읽기 시 숫자가 문자열로 인식되는 문제 빈번
# 3. category 타입으로 전환하면 메모리 대폭 정략 + 정렬 제어


# Pandas 주요 dtype
# | dtype | 설명 | 예시 |
# | ----- | ---- | ------|
# | int64 | 정수 | DAU, 유저수, 건수 |
# | float64 | 실수 | 전환율, ARPU, 금액 | 
# | object | 문자열/혼합 | 채널명, 플랜, 카테고리 |
# | bool | 불리언 | 이탈 여부, 목표 달성 여부 |
# | datetime64 | 날짜/시간 | 가입일, 이벤트 시각 |
# | category | 범주형 | 플랜(free/basic/pro), 등급 |
# | Int64 (nullable) | 결측 허용 정수 | NaN이 섞인 정수 열 |


# 핵심 변환 함수
'''
df["col"].astype                # 일반 타입 변환
pd.to_numeric(df["col"])        # 문자열 → 숫자 (에러 처리 가능)
pd.to_datetime(df["col"])       # 문자열 → datetime
df["col"].astype("category")    # 범주형 변환
'''

import numpy as np
import pandas as pd


# 2-1. dtype 확인과 기본 변환
# CSV에서 읽어온 것처럼 문자열이 섞인 데이터
df = pd.DataFrame({
    "user_id": ["1001", "1002", "1003", "1004", "1005"],
    "revenue": ["49000", "19000", "N/A", "199000", "49000"],
    "signup_date": ["2024-01-15", "2024-02-20", "2024-03-10", "2024-01-05", "2024-04-01"],
    "is_premium": ["True", "False", "True", "True", "False"],
    "plan": ["pro", "basic", "pro", "enterprise", "pro"],
    "sessions": [15, 8, None, 25, 12],
})

print(df.dtypes)
# user_id        object ← 문자열!
# revenue        object ← 문자열! ("N/A" 때문)
# signup_date    object ← 문자열!
# is_premium     object ← 문자열!
# plan           object
# sessions       float64 ← None 때문에 float

# ── astype: 기본 변환 ──
df["user_id"] = df["user_id"].astype(int)
print(df["user_id"].dtype)

# ── pd.to_numeric: 숫자 변환 (에러 처리) ──
df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")   # "N/A" → NaN
print(df["revenue"])
# 0     49000.0
# 1     19000.0
# 2         NaN  ← "N/A"가 NaN으로
# 3    199000.0
# 4     49000.0

# errors 옵션:
# "raise"  → 에러 발생 (기본값)
# "coerce" → 변환 불가 값을 NaN으로
# "ignore" → 변환 불가 시 원본 유지

# ── pd.to_datetime: 날짜 변환 ──
df["signup_date"] = pd.to_datetime(df["signup_date"])
print(df["signup_date"].dtype)  # datetime64[ns]

# ── 불리언 변환 ──
df["is_premium"] = df["is_premium"].map({"True" : True, "False" : False})
print(df["is_premium"].dtype)  # bool

print(df.dtypes)
# user_id          int64
# revenue        float64
# signup_date    datetime64[ns]
# is_premium        bool
# plan            object
# sessions       float64


# 2-2. category 타입
# ── 문자열 → category ──
df["plan"] = df["plan"].astype("category")
print(df["plan"].dtype)     # dategory
print(df["plan"].cat.categories)  # ['basic', 'enterprise', 'pro']
# : .cat : 해당 열이 범주형 데이터(Categorical)일 때 사용하는 accessor
# : .categories : 가능한 모든 카테고리 목록 반환
# : cat.categories : 정의된 전체 카테고리
# vs. unique() ; 실제 등장한 값

# ── 순서 있는 카테고리 (Ordered) ──
plan_order = ["basic", "pro", "enterprise"]
df["plan"] = pd.Categorical(df["plan"], categories=plan_order, ordered=True)

# 순서 비교 가능
print(df["plan"] >= "pro")
# 0     True
# 1    False
# 2     True
# 3     True
# 4     True
# "plan": ["pro", "basic", "pro", "enterprise", "pro"],

# ── 메모리 절약 효과 ──
big_series = pd.Series(np.random.choice(["A", "B", "C"], size=100000))
print(f"object :     {big_series.memory_usage():,} bytes")
print(f"categories : {big_series.astype('category').memory_usage():,} bytes")
# category가 약 10배 작음

# | 구분 | object | category |
# | ---- | ------ | ---------|
# | 내부저장 | Python 객체 (문자열 등) | 정수 코드 + 카테고리 테이블 |
# | 메모리 | 큼 | 작음 |
# | 중복값 처리 | 그대로 저장 | 하나만 저장 + 코드로 참조 |
# | 연산 속도 | 느림 | 빠름 (특히 groupby, 비교) |
# | 정렬 기준 | 문자열 기준 | 정의된 카테고리 순서 가능 |
# | 저장 방식 | 매번 따로 저장 | 있는 카테고리만 저장, 나머지는 정수 index 참조 |


# 2-3. Nullable Integer (Int64)
# 일반 int는 NaN 불가 → float으로 강제 변환됨
s = pd.Series([1, 2, None, 4])
print(s.dtype)  # float64 (None 때문에)

# Nullable Integer 타입 : NaN + 정수 공존
s_nullable = pd.Series([1, 2, None, 4], dtype="Int64")
print(s_nullable)
# 0       1
# 1       2
# 2    <NA>
# 3       4
# dtype: Int64

# 실무 활용: 유저 수 같은 정수인데 결측이 있는 경우
df["sessions"] = df["sessions"].astype("Int64")
print(df["sessions"])


# 2-4. 실무 패턴: CSV 읽기 시 dtype 지정
# ── 읽기 시 미리 지정 (권장) ──
# df = pd.read_csv("data.csv", dtype={
#     "user_id": int,
#     "plan": "category",
#     "revenue": float,
# }, parse_dates=["signup_date"])

# ── 읽은 후 일괄 변환 ──
def clean_dtypes(df):
    """DataFrame의 dtype을 자동 최적화"""
    for col in df.select_dtypes(include=["object"]):
        n_unique = df[col].nunique()
        n_total = len(df[col])
        # 고유값 비율이 50% 미만이면 category로
        if n_unique / n_total < 0.5:
            df[col] = df[col].astype("category")
    return df


# ================================================================================================
# 연습 문제
# Lv.1 기본

# 문제 1-1) dtype 확인 & 변환
import pandas as pd

df = pd.DataFrame({
    "order_id": ["ORD001", "ORD002", "ORD003"],
    "amount": ["15000", "23000", "8500"],
    "quantity": [3, None, 5],
    "date": ["2024-01-15", "2024-02-20", "2024-03-10"],
    "status": ["완료", "취소", "완료"],
})

# 1. 모든 열의 dtype 확인
print(df.dtypes)

# 2. amount를 숫자(int)로 변환
df["amount"] = df["amount"].astype(int)

# 3. quantity를 Nullable Int64로 변환
df["quantity"] = df["quantity"].astype("Int64")

# 4. date를 datetime으로 변환
df["date"] = pd.to_datetime(df["date"])

# 5. status를 category로 변환
df["status"] = df["status"].astype("category")

# 6. 최종 dtypes 확인
print(df.dtypes)


# ================================================
# Lv.2 응용 — 복합 개념 조합

# 문제 2-1) 지저분한 데이터 정제
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "user_id": [1001, 1002, 1003, 1004, 1005],
    "revenue": ["₩49,000", "₩19,000", "-", "₩199,000", "₩49,000"],
    "signup_date": ["2024/01/15", "24-02-20", "2024.03.10", "Jan 5, 2024", "2024-04-01"],
    "age_group": ["20대", "30대", "20대", "40대", "30대"],
    "churn_flag": [0, 1, 0, 0, 1],
})

# 1. revenue: "₩", 콤마 제거 후 숫자 변환 ("-"는 NaN)
df["revenue"] = df["revenue"].str.replace("₩", "").str.replace(",", "")
df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")

# 2. signup_date: 다양한 형식을 datetime으로 통일
df["signup_date"] = pd.to_datetime(df["signup_date"], format="mixed", dayfirst=False)
# : format : 문자열마다 다른 날짜 형식 섞여 있을때 사용
# : dayfirst : 01/02
# : False - MM/DD / True - DD/MM

# 3. age_group: 순서 있는 category (20대 < 30대 < 40대)
df["age_group"] = pd.Categorical(
    df["age_group"], categories=["20대", "30대", "40대"], ordered=True
)

# 4. churn_flag: bool 변환
df["churn_flag"] = df["churn_flag"].astype(bool)

# 5. 정제 후 dtypes와 head() 출력
print(df.dtypes)
print(df.head(5))

'''
py 03_pandas_dtype_conversion.py
'''