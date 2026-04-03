# Numpy (Numerical Python)
# : 수치 연산을 위한 파이썬 라이브러리
# : 과학 계산, 데이터 분석, 머신 러닝 등 다양한 분야에서 사용

# PM/ 데이터 분석가?
# : Pandas 내부 엔진이 Numpy 배열 기반
# : 대용량 지표 데이터(DAU, 매출, 전활율 등)
# : scikit-learn, matplotlib 등
# : 순수 파이썬 리스트 대비 10 - 100배 빠른 연산 속도

# ndarray란? (N-dimensional array)
# : N차원 배열
# : 동일한 자료형의 다차원 배열을 표현하는 객체

# ================================================
# 1-1. 배열 생성 방법

import numpy as np

# == 리스트 생성 ==
# 일별 매출 데이터 (단위 : 만원)
daily_revenue = np.array([1200, 1350, 980, 1500, 1420, 1100, 1680])
print(daily_revenue)

print(f"shape: {daily_revenue.shape}")
print(f"ndim: {daily_revenue.ndim}")
print(f"dtype: {daily_revenue.dtype}")
print(f"size: {daily_revenue.size}")


# == 2차원 배열 : 주간 채널별 전환율 ==
# 행 : 채널(organic, paid, referral), 열 : 요일(월-금)
conversion_rates = np.array([
    [0.032, 0.028, 0.035, 0.031, 0.029],  # organic
    [0.045, 0.042, 0.048, 0.044, 0.041],  # paid
    [0.038, 0.036, 0.040, 0.037, 0.035],  # referral
])

print(f"shape: {conversion_rates.shape}")
print(f"ndim: {conversion_rates.ndim}")
print(f"dtype: {conversion_rates.dtype}")

# ================================================
# 1-2. 편의 생성 함수
# == zeros : 초기화 배열 (집계 결과 담을 빈 그릇) ==
weekly_metrics = np.zeros((4, 7))
print(weekly_metrics)

# ── ones: 1로 채운 배열 (가중치 초기값 등) ──
weights = np.ones(5)  # [1. 1. 1. 1. 1.]
print(weights)

# ── full: 특정 값으로 채우기 ──
# 기본 목표 전환율 3%로 초기화
target_cvr = np.full((3, 7), 0.03)
print(target_cvr)

# ── arange: 범위 배열 (파이썬 range의 NumPy 버전) ──
days = np.arange(1, 31)   # 1일 ~ 30일
print(days)  # [ 1  2  3 ... 30]

# ── linspace: 균등 간격 배열 ──
# 0%에서 100%까지 11개 구간 (0, 10, 20, ..., 100)
percentiles = np.linspace(0, 100, 11)
print(percentiles)  # [  0.  10.  20.  30. ... 100.]

# ================================================
# 1-3. dtype 지정과 변환
# ── 생성 시 dtype 지정 ──
user_ids = np.array([10001, 10002, 10003], dtype=np.int32)
print(user_ids.dtype)  # int32

revenue = np.array([1200, 1350, 980], dtype=np.float64)
print(revenue.dtype)  # float64

# ── dtype 변환: astype() ──
# 정수 매출을 실수로 변환 (비율 계산 시 필요)
daily_revenue_int = np.array([1200, 1350, 980])
daily_revenue_float = daily_revenue_int.astype(np.float64)
print(daily_revenue_float.dtype)  # float64

# ── 주요 dtype 종류 ──
# np.int32, np.int64     → 정수 (유저 수, 주문 건수)
# np.float32, np.float64 → 실수 (전환율, 매출, 비율)
# np.bool_               → 불리언 (이탈 여부, 구매 여부)
# np.str_                → 문자열 (거의 안 쓰고 Pandas 활용)

# ================================================
# 1-4. 속도 비교 : 리스트 vs NumPy
import time

size = 1_000_000

# ── Python 리스트 ──
py_list = list(range(size))
start = time.time()
result_list = [x * 2 for x in py_list]
list_time = time.time() - start

# ── NumPy 배열 ──
np_array = np.arange(size)
start = time.time()
result_np = np_array * 2
np_time = time.time() - start

print(f"Python 리스트: {list_time:.4f}초")
print(f"NumPy 배열:    {np_time:.4f}초")
print(f"NumPy가 {list_time / np_time:.0f}배 빠름")
# 대략 NumPy가 20~50배 빠름


# ================================================
# 연습 문제
# 1-1) 배열의 4가지 속성을 각각 출력
import numpy as np

days_new_users = np.array([150, 230, 180, 290, 310, 275, 340])
print(f"shape : {days_new_users.shape}")
print(f"ndim : {days_new_users.ndim}")
print(f"dtype : {days_new_users.dtype}")
print(f"size : {days_new_users.size}")

# 해당 배열을 float64 타입으로 변환한 새 배열 생성
new = days_new_users.astype(np.float64)
print(f"dtype : {new}")

# 문제 1-2) 편의 생성 함수 활용 

import numpy as np

# 1) 30일간의 일별 지표를 담을 빈 배열 (0으로 초기화, shape: (30,))
daily_users = np.zeros((30,))
print(daily_users)

# 2)  4주 × 7일 형태의 배열, 모든 값이 목표 DAU 500 (shape: (4, 7))
target_dau = np.full((4, 7), 500)
print(target_dau.shape)

# 3) 1부터 365까지의 정수 배열 (1년 365일)
year_days = np.arange(1, 366)
print(f"길이 : {year_days}")

# 4) 0에서 1 사이를 균등하게 나눈 21개의 값 (0.00, 0.05, 0.10, ..., 1.00)
ratio = np.linspace(0, 1, 21)
print(ratio)

'''
01_numpy.py
'''