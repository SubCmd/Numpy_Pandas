# 1-4: 배열 변형 & 결합

# 배열 변형(Reshape)
# : 배열 원소 수는 유지한 채 shape(형태)만 바꾸는 것. (데이터 자체 변경 없음)
'''
(12,) → (3, 4)     12개 원소: 1차원 → 3행 4열
(3, 4) → (6, 2)    12개 원소: 형태만 변경
(3, 4) → (12,)     12개 원소: 2차원 → 1차원 (flatten)
'''

# 배열 결합(Concatenation)
# : 여러 배열을 하나로 합치는 것. 축(axis)에 따라 방향이 달라진다.

'''
| 함수 | 동작 | 축(axis)|
| --- | --- | ------|
| np.concatenate | 기존 축을 따라 이어붙이기 | 지정
| np.vstack | 세로(행 방향)로 따라 이어붙이기 | axis=0
| np.hstack | 가로(열 방향)로 이어붙이기 | axis=1
| np.column_stack | 1차원 배열들을 열로 합치기 | -
| np.split | 배열 분할 | 지정

vstack: 이번 주 데이터 아래에 다음 주 데이터 추가 (행 증가)
hstack: 기존 지표 옆에 새 지표 열 추가 (열 증가)
reshape: 12개월 데이터를 4분기 × 3개월로 재구조화
'''

# 2-1. reshape 기본

from calendar import day_name
import numpy as np

# 12개월 매출을 분기별로 재구조화
monthly_rev = np.array([8500, 9200, 8800, 9500, 10200, 11000,
                        10500, 11800, 12500, 13200, 12800, 14500])

# (12,) → (4, 3): 4분기 × 3개월
quarterly = monthly_rev.reshape(4, 3)
print(quarterly)
# [[ 8500  9200  8800]   Q1
#  [ 9500 10200 11000]   Q2
#  [10500 11800 12500]   Q3
#  [13200 12800 14500]]  Q4

# -1 사용: 자동 계산
auto_shape = monthly_rev.reshape(4, -1)   # -1 → 12/4 = 3
print(auto_shape.shape)  # (4, 3)

auto_shape2 = monthly_rev.reshape(-1, 6)  # -1 → 12/6 = 2
print(auto_shape2.shape)  # (2, 6)

# ── flatten vs ravel: 다차원 → 1차원 ──
flat1 = quarterly.flatten()   # 항상 Copy 반환
flat2 = quarterly.ravel()     # 가능하면 View 반환 (더 빠름)
print(flat1.shape)  # (12,)
print(flat2.shape)  # (12,)

# ── 전치(Transpose): 행 ↔ 열 교환 ──
print(quarterly.shape)     # (4, 3)
print(quarterly.T.shape)   # (3, 4)
# 용도: 분기×월 → 월×분기로 관점 전환


# 2-2. 차원 추가/제거

# ── np.newaxis / np.expand_dims: 차원 추가 ──
week_revenue = np.array([1200, 1350, 980, 1500, 1420])  # shape: (5,)

# 열 벡터로 변환 → 브로드캐스팅에 활용
col_vector = week_revenue[:, np.newaxis]    # shape: (5, 1)
col_vector2 = np.expand_dims(week_revenue, axis=1)  # 동일

print(col_vector.shape)  # (5, 1)

# ── np.squeeze: 크기 1인 차원 제거 ──
arr = np.array([[[1, 2, 3]]])  # shape: (1, 1, 3)
squeezed = np.squeeze(arr)
print(squeezed.shape)  # (3,)


# 2-3. 배열 결합

# ── vstack: 세로(행)로 쌓기 ──
week1 = np.array([[1200, 1350, 980, 1500, 1420]])   # (1, 5)
week2 = np.array([[1300, 1250, 1050, 1600, 1380]])  # (1, 5)
week3 = np.array([[1400, 1500, 1100, 1700, 1450]])

all_weeks = np.vstack([week1, week2, week3])
print(all_weeks.shape)  # (3, 5)
print(all_weeks)
# [[1200 1350  980 1500 1420]
#  [1300 1250 1050 1600 1380]
#  [1400 1500 1100 1700 1450]]

# ── hstack: 가로(열)로 이어붙이기 ──
dau = np.array([[3200], [3400], [3100]])          # (3, 1)
revenue = np.array([[1200], [1300], [1400]])       # (3, 1)
cvr = np.array([[3.2], [3.5], [3.1]])   

metrics = np.hstack([dau, revenue, cvr])
print(metrics.shape)  # (3, 3)
print(metrics)
# [[3200. 1200.    3.2]
#  [3400. 1300.    3.5]
#  [3100. 1400.    3.1]]

# ── column_stack: 1차원 배열들을 열로 합치기 (가장 편리) ──
dau_1d = np.array([3200, 3400, 3100])
rev_1d = np.array([1200, 1300, 1400])
cvr_1d = np.array([3.2, 3.5, 3.1])

table = np.column_stack([dau_1d, rev_1d, cvr_1d])
print(table.shape)  # (3, 3)
print(table)

# ── concatenate: axis 지정으로 유연하게 ──
data_jan = np.array([[100, 200],
                     [110, 210]])  # (2, 2)
data_feb = np.array([[120, 220],
                     [130, 230]])  # (2, 2)

# axis=0: 행 방향 결합
combined_rows = np.concatenate([data_jan, data_feb], axis=0)
print(combined_rows.shape)  # (4, 2)

# axis=1: 열 방향 결합
combined_cols = np.concatenate([data_jan, data_feb], axis=1)
print(combined_cols.shape)  # (2, 4)


# 2-4. 배열 분할

# ── np.split: 균등 분할 ──
yearly = np.arange(1, 13)  # [1, 2, ..., 12]
quarters = np.split(yearly, 4)  # 4등분
print(quarters)
# [array([1, 2, 3]), array([4, 5, 6]), array([7, 8, 9]), array([10, 11, 12])]

# ── np.array_split: 균등하지 않아도 분할 ──
data = np.arange(10)
parts = np.array_split(data, 3)
print(parts)
# [array([0, 1, 2, 3]), array([4, 5, 6]), array([7, 8, 9])]

# ── 인덱스 지정 분할 ──
metrics = np.array([100, 200, 300, 400, 500, 600, 700, 800])
part1, part2, part3 = np.split(metrics, [3, 6])  # 인덱스 3, 6에서 분할
print(part1)  # [100 200 300]
print(part2)  # [400 500 600]
print(part3)  # [700 800]


# ================================================================================================
# 연습 문제
# Lv.1 기본

# 문제 1-1) reshape 기초
# 1. np.arange(24)를 다음 shape으로 변형하세요: (4, 6), (6, 4), (2, 3, 4), (24, 1)
import numpy as np

arr = np.arange(24)

print(arr.reshape(4, 6).shape)
print(arr.reshape(6, 4).shape)
print(arr.reshape(2, 3, 4).shape)
print(arr.reshape(24, 1).shape)

# 2. (3, 8) shape 배열을 (8, 3)으로 바꾸는 두 가지 방법을 작성하세요 (reshape vs .T)
#    → 두 결과가 같은지 다른지 비교하고, 왜 다른지 설명
data = np.arange(24).reshape(3, 8)
reshaped = data.reshape(8, 3)
transposed = data.T
print(f"reshaped : {reshaped}")
print(f"transposed : {transposed}")
print(f"같은가? {np.array_equal(reshaped, transposed)}")
# reshaped : 원소 순서(메모리 순서)를 유지한채 shape만 변경
# transposed : 행/열 교환

# 3. (2, 3, 4) shape 배열의 flatten 결과 shape은?
arr_3d = np.arange(24).reshape(2, 3, 4)
flatten = arr_3d.flatten().shape
print(f"flatten : {flatten}")


# 문제 1-2) 결합 기초
a = np.array([10, 20, 30])
b = np.array([40, 50, 60])
c = np.array([70, 80, 90])

# 1. 세 배열을 세로로 쌓아서 (3, 3) 배열 생성
vstack = np.vstack([a, b, c])
print(vstack)

# 2. 세 배열을 가로로 이어붙여서 (9,) 배열 생성
hstack = np.hstack([a, b, c])
print(hstack)

# 3. 세 배열을 열로 합쳐서 (3, 3) 배열 생성
col_stack = np.column_stack([a, b, c])
print(col_stack)

# 4. 1번과 3번 결과가 같은가? 왜 같거나 다른가?
print(np.array_equal(vstack, col_stack))
# vstack : 각 배열이 "행"이 됨
# column_stack : 각 배열이 "열"이 됨
# vstack = column_stack.T


# ================================================
# Lv.2 응용 — 복합 개념 조합

# 문제 2-1) 주간 리포트 데이터 구조 변환
# 시나리오: 4주간 일별 매출이 1차원으로 나열되어 있습니다.

daily_rev = np.array([
    120, 135, 98, 150, 142, 110, 168,   # Week 1
    130, 145, 105, 160, 155, 115, 175,  # Week 2
    125, 140, 102, 155, 148, 108, 170,  # Week 3
    140, 155, 115, 170, 165, 125, 185,  # Week 4
])  # 28일, shape: (28,)

# 1. (4, 7) shape으로 reshape (4주 × 7일)
weekly = daily_rev.reshape(4, 7)
print(weekly.shape)

# 2. 각 주의 주말(토,일 = 인덱스 5,6)만 추출하여 (4, 2) 배열 생성
weekends = weekly[:, 5:]
print(f"주말 : {weekends.reshape(4, 2)}")

# 3. 주중(월~금)과 주말을 분리하여 각각의 주 평균 계산
weekday_avg = weekly[:, 0:5].mean(axis=1)
weekend_avg = weekends.mean(axis=1)
print(f"주중 평균 : {np.round(weekday_avg, 1)}")
print(f"주말 평균 : {np.round(weekend_avg, 1)}")

# 4. 전체를 전치(Transpose)한 뒤, 요일별(7행) × 주차별(4열)로 평균 비교
by_day = weekly.T
days_names = ["월", "화", "수", "목", "금", "토", "일"]
day_avg = by_day.mean(axis=1)
for name, avg in zip(days_names, day_avg):
    print(f"{name} : {avg}")
    
'''
py 04_numpy_reshape.py
'''