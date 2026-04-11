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

'''
python 01_pandas_series_dataframe.py
'''