# 1-5: 통계 함수 & 집계

# axis 개념 - 가장 중요!
'''
2차원 배열 (3, 7):    3행 x 7열

axis=0  → 행을 따라 (세로 방향) → 결과 shape: (7,)   "행을 압축"
axis=1  → 열을 따라 (가로 방향) → 결과 shape: (3,)   "열을 압축"
axis=None (기본값) → 전체를 하나의 값으로

"axis = N -> N번째 차원이 사라진다."
'''

'''
| 함수 | 설명 | PM 활용 예시|
| --- | --- | ------|
| np.sum | 합계 | 총 매출, 총 방문자 수
| np.mean | 평균 | 평균 DAU, 평균 전환율
| np.median | 중앙값 | 이상치에 강건한 대푯값
| np.std / np.var | 표준편차/분산 | 지표 변동성 파악
| np.min / np.max | 최솟값/최댓값 | 최저/최고 성과 일자
| np.armin / np.argmax | 최솟값/최댓값 인덱스 | 최저/최고 성과가 언제인지?
| np.percentile | 백분위수 | P50(중앙)
| np.cumsum / np.cumprod | 누적합 / 누적곱 | 누적 매출, 누적 성장
| np.unique | 고유값 + 빈도 | 카테고리 분포
| np.corrcoef | 상관계수 | 지표 간 상관관계
'''

# 2-1. 기본 통계 + axis

import numpy as np

# 3채널 × 7일 DAU
channel_dau = np.array([
    [1200, 1350, 1280, 1400, 1150, 980, 870],   # organic
    [800,  920,  850,  950,  780,  600, 520],    # paid
    [450,  580,  510,  620,  480,  720, 690],    # social
])  # shape: (3, 7)

# ── 전체 통계 ──
print(f"전체 합계: {np.sum(channel_dau):,}")       # 17,550
print(f"전체 평균: {np.mean(channel_dau):.1f}")     # 835.7
print(f"전체 중앙값: {np.median(channel_dau):.1f}") # 850.0

# ── axis=0: 채널별을 합쳐서 요일별 통계 ──
daily_total = np.sum(channel_dau, axis=0)      # shape: (7,)
daily_avg = np.mean(channel_dau, axis=0)
print(f"요일별 합계: {daily_total}")  # [2450 2850 2640 2970 2410 2300 2080]
print(f"요일별 평균: {np.round(daily_avg, 1)}")  # [816.7 950.  880.  990.  803.3 766.7 693.3]

# ── axis=1: 요일을 합쳐서 채널별 통계 ──
channel_total = np.sum(channel_dau, axis=1)    # shape: (3,)
channel_avg = np.mean(channel_dau, axis=1)
print(f"채널별 합계: {channel_total}")  # [8230 5420 4050]
print(f"채널별 평균: {np.round(channel_avg, 1)}")


# 위치 찾기 : argmin / argmax

revenue = np.array([1200, 1350, 980, 1500, 1420, 1100, 1680])
days = ["월", "화", "수", "목", "금", "토", "일"]

# 최고/최저 매출 날
best_day = np.argmax(revenue)
worst_day = np.argmin(revenue)
print(f"최고 매출: {days[best_day]}요일 ({revenue[best_day]:,}만원)")  # 일요일
print(f"최저 매출: {days[worst_day]}요일 ({revenue[worst_day]:,}만원)")  # 수요일

# ── 2차원에서 위치 찾기 ──
channel_dau = np.array([
    [1200, 1350, 1280, 1400, 1150, 980, 870],
    [800,  920,  850,  950,  780,  600, 520],
    [450,  580,  510,  620,  480,  720, 690],
])

# 전체에서 최대값 위치
flat_idx = np.argmax(channel_dau)
row, col = np.unravel_index(flat_idx, channel_dau.shape)
ch_names = ["organic", "paid", "social"]
print(f"최대 DAU: {ch_names[row]} {days[col]}요일 ({channel_dau[row, col]})")

# 채널별 최고 요일 (axis=1)
best_days_per_ch = np.argmax(channel_dau, axis=1)
for ch, day_idx in zip(ch_names, best_days_per_ch):
    print(f"  {ch}: {days[day_idx]}요일")


# 2-3. 백분위수 & 분포 파악

# 유저별 세션 시간 (초)
np.random.seed(42)
session_times = np.random.exponential(scale=120, size=1000)

# 기본 통계
print(f"평균: {np.mean(session_times):.1f}초")
print(f"중앙값: {np.median(session_times):.1f}초")
print(f"표준편차: {np.std(session_times):.1f}초")

# 백분위수 — 분포 이해에 핵심
percentiles = [10, 25, 50, 75, 90, 95, 99]
values = np.percentile(session_times, percentiles)
for p, v in zip(percentiles, values):
    print(f"  P{p}: {v:.1f}초")

# ⚠️ 평균 vs 중앙값 차이가 크면 → 분포가 치우쳐 있다 (right-skewed)
# → 대표값으로 중앙값이 더 적합


# 2-4. 누적 함수 : cumsum / cumprod

# ── 누적 매출 ──
daily_rev = np.array([120, 150, 95, 180, 165, 110, 200])
cum_rev = np.cumsum(daily_rev)
print(f"일별 매출 : {daily_rev}")
print(f"누적별 매출 : {cum_rev}")
# [120 270 365 545 710 820 1020]

# ── 누적 성장: 복리 계산 ──
# 주간 성장률: 5%, -2%, 8%, 3%, -1%
weekly_growth = np.array([0.05, -0.02, 0.08, 0.03, -0.01])
growth_factors = 1 + weekly_growth  # [1.05, 0.98, 1.08, 1.03, 0.99]
cumulative = np.cumprod(growth_factors)
print(f"누적 성장 배수: {np.round(cumulative, 4)}")
# [1.05   1.029  1.1113 1.1447 1.1332]
# → 5주 후 약 13.3% 성장


# 2-5. 상관관계 분석
np.random.seed(42)
weeks = 20

# 마케팅 비용과 매출 (상관관계가 있을 것으로 예상)
ad_spend = np.random.randint(500, 1500, size=weeks)
revenue = ad_spend * np.random.uniform(2.5, 3.5, size=weeks) + np.random.normal(0, 200, weeks)
print(ad_spend)
print(revenue)

# 상관계수 행렬
corr_matrix = np.corrcoef(ad_spend, revenue)
print(f"상관계수: {corr_matrix[0, 1]:.3f}")
# 0.8~0.9 수준 (강한 양의 상관관계)

# 여러 지표 간 상관관계
dau = np.random.randint(3000, 5000, size=weeks)
signups = dau * np.random.uniform(0.02, 0.05, size=weeks)

multi_corr = np.corrcoef([ad_spend, revenue, dau, signups])
print("상관계수 행렬:")
print(np.round(multi_corr, 2))


# ================================================================================================
# 연습 문제
# Lv.1 기본

# 문제 1-1) axis 연습
data = np.array([
    [10, 20, 30],
    [40, 50, 60],
    [70, 80, 90],
    [100, 110, 120],
])  # shape: (4, 3)

# 실행 전에 결과를 예측하세요:
# 1. np.sum(data)            → ? 780 (전체합)
print(np.sum(data))

# 2. np.sum(data, axis=0)    → ? (shape은?) (3, )
print(np.sum(data, axis=0).shape)

# 3. np.sum(data, axis=1)    → ? (shape은?) (4, )
print(np.sum(data, axis=1).shape)

# 4. np.mean(data, axis=0)   → ? 55, 65, 75
print(np.mean(data, axis=0))

# 5. np.max(data, axis=1)    → ? 30 60 90 120
print(np.max(data, axis=1))

# 6. np.argmax(data, axis=0) → ? 3 3 3 
print(np.argmax(data, axis=0))

# 문제 1-2) 기본 통계 계산
scores = np.array([78, 92, 65, 88, 71, 95, 83, 76, 90, 85, 
                   69, 94, 87, 73, 81, 96, 70, 84, 91, 77])

# 1. 평균, 중앙값, 표준편차 계산
print(f"평균 : {np.mean(scores):.1f}")
print(f"중앙값 : {np.median(scores):.1f}")
print(f"표준편차 : {np.std(scores):.1f}")

# 2. 최고점, 최저점과 그 인덱스
print(f"최고 : {np.max(scores)} (인덱스 {np.argmax(scores)})")
print(f"최저 : {np.min(scores)} (인덱스 {np.argmin(scores)})")

# 3. P25, P50, P75, P90 백분위수
for p in [25, 60, 75, 90]:
    print(f" P{p}: {np.percentile(scores, p):.1f}")

# np.percentile(a, q)
# a : 입력할 배열 또는 리스트 데이터
# q : 찾고자 하는 백분위 값

# 4. 80점 이상인 학생 수와 비율
above_80 = scores[scores >= 80]
print(f"80점 이상 : {len(above_80)}명 ({len(above_80)/len(scores)*100:.0f}%)")

# ================================================
# Lv.2 응용 — 복합 개념 조합

# 문제 2-1) 분기별 성과 분석
# 4개 팀 × 12개월 매출
np.random.seed(42)
monthly_sales = np.random.randint(80, 200, size=(4, 12))
team_names = ["Alpha", "Beta", "Gamma", "Delta"]
months = ["1월","2월","3월","4월","5월","6월","7월","8월","9월","10월","11월","12월"]

print(monthly_sales)

# 1. 팀별 연간 총매출 (axis=1)
annual = monthly_sales.sum(axis=0)
for name, total in zip(team_names, months):
    print(f"{name} : {total}")

# 2. 월별 전체 팀 합산 매출 (axis=0)
monthly_total = monthly_sales.sum(axis=0)
print(f"월별 합산 : {monthly_total}")

# 3. 각 팀의 최고 매출 월과 최저 매출 월 (argmax/argmin + months 매핑)
for i, name in enumerate(team_names):
    best = np.argmax(monthly_sales[i])
    worst = np.argmin(monthly_sales[i])
    print(f" {name} : 최고 {months[best]} ({monthly_sales[i, best]})")
    print(f"          최저 : {months[worst]} ({monthly_sales[i, worst]})")

# 4. 12개월을 (4, 4, 3)으로 reshape하여 팀별 분기별 합산 매출 계산
quarterly = monthly_sales.reshape(4, 4, 3).sum(axis=2)
print(f"분기별 매출 : \n{quarterly}")

# 5. 전 팀 중 분기별 최고 성과 팀 식별
for q in range(4):
    best_team = np.argmax(quarterly[:, q])
    print(f" Q{q+1} 최고 : {team_names[best_team]} ({quarterly[best_team, q]})")

'''
py 05_numpy_statistics.py
'''