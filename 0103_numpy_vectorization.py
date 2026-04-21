# 1-3: 배열 연산 (Vectorization & Broadcasting)

# 벡터화 연산(Vectorizatino)
# : 반복문 없이 배열 전체에 한 번에 연산을 적용하는 것. 

'''
# 반복문 (느림)
result = []
for x in data:
    result.append(x * 1.1)

# 벡터화 (빠름)
result = data * 1.1
'''

# 브로드캐스팅(Broadcasting)
# : shape이 다른 배열 간 연산을 가능하게 해주는 NumPy의 자동 확장 규칙

# 브로드캐스팅 규칙 3가지
# 1. 차원 수가 다르면, 작은 쪽 앞에 1을 추가해서 차원을 맞춤
# 2. 특정 축 크기가 1이면, 다른 배열의 해당 축 크기에 맞춰 복제
# 3. 두 축의 크기가 다르고 어느 쪽도 1이 아니면 -> 에러
'''
(3, 5) + (5,)     → (3, 5) + (1, 5) → (3, 5)  ✅ 호환
(3, 5) + (3, 1)   → (3, 5)                    ✅ 호환  
(3, 5) + (3,)     → (3, 5) + (1, 3) → 에러!    ❌ 비호환
'''

# 유니버설 함수(ufunc)
# : 배열의 각 원소에 동일한 연산을 적용하는 NumPy 내장 함수 (벡터화 구현체)
# | 범주 | 함수 |
# |------|------|
# | 산술 | np.add, np.multiply, np.power
# | 비교 | np.greater, np.equal 
# | 수학 | np.sqrt, np.log, np.exp
# | 반올림 | np.round, np.floor, np.ceil

# ------------------------------------------------------------------
# 2-1. 기본 벡터화 연산
import numpy as np

# 일별 매출 (만원)
revenue = np.array([1200, 1350, 980, 1500, 1420, 1100, 1680])

# ── 스칼라 연산: 배열 전체에 동일 연산 ──
# 10% 성장 목표
target = revenue * 1.1
print(target)  # [1320. 1485. 1078. 1650. 1562. 1210. 1848.]

# VAT 제외 (부가세 10%)
net_revenue = revenue / 1.1
print(np.round(net_revenue, 1))  # [1090.9 1227.3 890.9 ...]

# ── 배열 간 연산: 같은 shape끼리 원소별(element-wise) 계산 ──
cost = np.array([800, 900, 750, 950, 880, 700, 1050])
profit = revenue - cost
print(profit)  # [400 450 230 550 540 400 630]

# 이익률
margin = profit / revenue * 100
print(np.round(margin, 1))  # [33.3 33.3 23.5 36.7 38.0 36.4 37.5]

# ── 비교 연산: 불리언 배열 반환 ──
print(revenue > 1200)  # [False  True False  True  True False  True]
print(margin >= 35)    # [False False False  True  True  True  True]

# ------------------------------------------------------------------
# 2-2. 브로드캐스팅 실전 예제

# ── 예제 1: 채널별 DAU에 요일 가중치 적용 ──
channel_dau = np.array([
    [1200, 1350, 1280, 1400, 1150, 980, 870],    # organic
    [800,  920,  850,  950,  780,  600, 520],    # paid
    [450,  580,  510,  620,  480,  720, 690],    # social
])  # shape: (3, 7)

# 요일별 가중치 (주말은 낮게)
day_weight = np.array([1.2, 1.1, 1.0, 1.0, 1.1, 0.8, 0.7])  # shape: (7,)

# 브로드캐스팅: (3, 7) * (7,) → (3, 7) * (1, 7) → (3, 7)
weighted_dau = channel_dau * day_weight
print(weighted_dau.shape)  # (3, 7)
print(np.round(weighted_dau, 0))
# [[1440. 1485. 1280. 1400. 1265.  784.  609.]
#  [ 960. 1012.  850.  950.  858.  480.  364.]
#  [ 540.  638.  510.  620.  528.  576.  483.]]


# ── 예제 2: 채널별 기준값으로 정규화 ──
# 각 채널의 월요일(첫 날) 대비 비율 계산
baseline = channel_dau[:, 0:1]  # shape: (3, 1) — 슬라이싱으로 2차원 유지!
print(baseline)
# [[1200]
#  [ 800]
#  [ 450]]

# 브로드캐스팅: (3, 7) / (3, 1) → (3, 7)
normalized = channel_dau / baseline
print(np.round(normalized, 2))
# [[1.   1.12 1.07 1.17 0.96 0.82 0.72]   organic 기준 : 비용 지불하지 않고 자연스럽게 발생한 유입
#  [1.   1.15 1.06 1.19 0.97 0.75 0.65]   paid 기준 : 비용을 지불하고 노출을 구매하는 방식
#  [1.   1.29 1.13 1.38 1.07 1.6  1.53]]  social 기준 : 페이스북, 인스타, 유튜브 등 플랫폼에서 이루어지는 활동

# ⚠️ 주의: channel_dau[:, 0]은 shape (3,)이 되어 의도와 다른 연산이 됨!
# [:, 0:1]로 (3, 1) shape을 유지하는 것이 핵심


# ── 예제 3: 행 합계/열 합계를 이용한 비율 계산 ──
# 각 셀이 해당 행 합계에서 차지하는 비율 (요일별 비중)
row_totals = channel_dau.sum(axis=1, keepdims=True)  # shape: (3, 1)
day_share = channel_dau / row_totals * 100
print(f"Organic 요일별 비중(%):\n{np.round(day_share[0], 1)}")
# [14.6 16.4 15.5 17.  14.  11.9 10.6]


# ------------------------------------------------------------------
# 2-3. 유니버설 함수 (ufunc) 활용
# ── 수학 함수 ──
revenue = np.array([1200, 1350, 980, 1500, 1420, 1100, 1680])

# 로그 변환 (스케일 축소, 시각화/분석용)
log_rev = np.log(revenue)
print(np.round(log_rev, 2))  # [7.09 7.21 6.89 7.31 7.26 7. 7.43]

# 제곱근
sqrt_rev = np.sqrt(revenue)
print(np.round(sqrt_rev, 1))  # [34.6 36.7 31.3 38.7 37.7 33.2 41.]

# ── 반올림 계열 ──
rates = np.array([3.245, 4.751, 2.999, 5.501])
print(np.round(rates, 1))   # [3.2 4.8 3.  5.5]  — 반올림
print(np.floor(rates))      # [3. 4. 2. 5.]       — 내림
print(np.ceil(rates))       # [4. 5. 3. 6.]       — 올림

# ── np.clip: 범위 제한 ──
# 이상치를 상한/하한으로 클리핑 (Winsorization) : outlier 영향을 줄이기 위해 극단적 값들을 특정 백분위수 값으로 대체
data = np.array([50, 120, 3, 200, 95, -10, 180, 250])
clipped = np.clip(data, 0, 200)
print(clipped)  # [ 50 120   3 200  95   0 180 200]

# ── np.maximum / np.minimum: 원소별 최대/최소 ──
plan_a = np.array([100, 200, 150, 300])
plan_b = np.array([120, 180, 160, 280])
best = np.maximum(plan_a, plan_b)
print(best)  # [120 200 160 300]  — 각 위치에서 더 큰 값

# ------------------------------------------------------------------
# 2-4. 실무 패턴: 전월 대비 성장률 계산
# 월별 매출 (12개월)
monthly_rev = np.array([
    8500, 9200, 8800, 9500, 10200, 11000,
    10500, 11800, 12500, 13200, 12800, 14500
])

# 전월 대비 성장률 (MoM Growth Rate)
# 방법: (이번달 - 지난달) / 지난달 × 100
mom_growth = (monthly_rev[1:] - monthly_rev[:-1]) / monthly_rev[:-1] * 100
print(f"MoM 성장률(%): {np.round(mom_growth, 1)}")
# [ 8.2 -4.3  8.   7.4  7.8 -4.5 12.4  5.9  5.6 -3.  13.3]

# 주의: 결과 길이가 원본보다 1 짧음 (12 → 11)
print(f"원본 길이: {len(monthly_rev)}, 성장률 길이: {len(mom_growth)}")

# 누적 성장 (1월 대비)
cumulative_growth = monthly_rev / monthly_rev[0] * 100 - 100
print(f"1월 대비 누적 성장률(%): {np.round(cumulative_growth, 1)}")
# [  0.    8.2   3.5  11.8  20.   29.4  23.5  38.8  47.1  55.3  50.6  70.6]


# ================================================================================================
# 연습 문제
# Lv.1 기본 

# 문제 1-1) 벡터화 연산 기초
# 데이터: 5개 상품의 원가와 판매가
cost = np.array([5000, 8000, 3000, 12000, 6500])
price = np.array([7500, 11000, 4200, 18000, 9100])

# 1. 각 상품의 이익 (판매가 - 원가)
profit = price - cost
print(f"이익: {profit}")

# 2. 각 상품의 이익률 (이익 / 판매가 × 100), 소수점 1자리 반올림
margin = np.round(profit / price * 100, 1)
print(f"이익률 : {margin}")

# 3. 이익률 30% 이상인 상품의 이익률만 추출
profit_30 = margin[margin >= 30]
print(f"30% 이상 : {profit_30}")

# 4. 모든 상품에 부가세(10%)를 포함한 최종 판매가
final_price = price * 1.1
print(f"최종 판매가 : {final_price}")


# 문제 1-2) 브로드캐스팅 shape 예측
a = np.ones((4, 3))
b = np.ones((3,))
c = np.ones((4, 1))
d = np.ones((1, 3))
e = np.ones((4,))

# 1. a + b   → shape: (4, 3)
print(np.shape(a + b))

# 2. a + c   → shape: (4, 3)
print(np.shape(a + c))

# 3. a + d   → shape: (4, 3)
print(np.shape(a + d))

# 4. c + d   → shape: (4, 3)
print(np.shape(c + d))

# 5. a + e   → shape: error  (⚠️ 주의)

# ================================================
# Lv.2 응용 — 복합 개념 조합

# 문제 2-1) 코호트별 리텐션 정규화
retention = np.array([
    [100, 45, 32, 25, 20, 18],   # 코호트 1
    [100, 52, 38, 30, 24, 21],   # 코호트 2
    [100, 48, 35, 28, 22, 19],   # 코호트 3
    [100, 55, 42, 35, 28, 25],   # 코호트 4
])  # shape: (4, 6) — 4코호트 × 6주

# 1. 각 코호트의 Week 1(인덱스 1) 대비 상대 리텐션율 계산
#   → Week 1 값을 100으로 놓았을 때 이후 주차의 비율
#   힌트: retention[:, 1:] / retention[:, 1:2] * 100
week01_base = retention[:, 1:2]
relative_retention = retention[:, 1:] / week01_base * 100
print(f"Week 1 대비 상대 리텐션율: {np.round(relative_retention, 1)}")

# 2. 전체 코호트 평균 리텐션율 (주차별 평균, axis=0)
avg_retention = retention.mean(axis=0)
print(f"평균 리텐션 : {avg_retention}")

# 3. 가장 리텐션이 좋은 코호트 (Week 5 기준) 찾기 → np.argmax
best_cohort = np.argmax(retention[:, 5])
print(f"Week 5 최고 코호트: 코호트 {best_cohort + 1} ({retention[best_cohort, 5]}%)")

# 4. 각 코호트의 주차별 이탈율 계산 (이전 주 대비 감소분)
churn_rate = retention[:, :-1] - retention[:, 1:]
print("주차별 이탈율")
print(churn_rate)


# 문제 2-2) 목표 달성률 대시보드 데이터 생성
targets = np.array([
    [500, 520, 540, 560],   # Team A 월별 목표
    [300, 310, 320, 330],   # Team B
    [400, 420, 440, 460],   # Team C
    [250, 260, 270, 280],   # Team D
])  # shape: (4, 4)

actuals = np.array([
    [480, 550, 510, 590],   # Team A 실적
    [320, 290, 340, 310],   # Team B
    [410, 400, 460, 470],   # Team C
    [230, 270, 260, 300],   # Team D
])


# 문제 2-2) 목표 달성률 대시보드 데이터 생성

targets = np.array([
    [500, 520, 540, 560],   # Team A 월별 목표
    [300, 310, 320, 330],   # Team B
    [400, 420, 440, 460],   # Team C
    [250, 260, 270, 280],   # Team D
])  # shape: (4, 4)

actuals = np.array([
    [480, 550, 510, 590],   # Team A 실적
    [320, 290, 340, 310],   # Team B
    [410, 400, 460, 470],   # Team C
    [230, 270, 260, 300],   # Team D
])

# 1. 달성률 계산: actuals / targets × 100 (소수점 1자리)
achievement = np.round(actuals / targets * 100, 1)
print("달성률")
print(achievement)

# 2. 목표 달성(100% 이상)한 셀의 개수
achieved = np.sum(achievement >= 100)
print(f"목표 달성 셀 : {achieved}개")

# 3. 팀별 평균 달성률 (axis=1)
team_avg = achievement.mean(axis=1)
team_names = ["A", "B", "C", "D"]
for name, avg in zip(team_names, team_avg):
    print(f"Team {name} : {avg:.1f}%")

# 4. 월별 평균 달성률 (axis=0)
month_avg = achievement.mean(axis=0)
for m, avg in zip(range(1, 5), month_avg):
    print(f"  {m}월: {avg:.1f}%")

# 5. 달성률이 가장 낮은 셀의 위치(팀, 월) → np.unravel_index, np.argmin
min_idx = np.argmin(achievement)
row, col = np.unravel_index(min_idx, achievement.shape)
print(f"최저: Team {team_names[row]}, {col+1}월 ({achievement[row, col]:.1f}%)")

# 6. 각 팀의 실적을 전월 대비 성장률로 변환
growth = (actuals[:, 1:] - actuals[:, :-1]) / actuals[:, :-1] * 100
print(f"전월 대비 성장률(%):\n{np.round(growth, 1)}")


'''
py 03_numpy_vectorization.py
'''