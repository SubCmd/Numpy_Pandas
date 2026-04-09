# 1-6: 난수 생성 & 선형대수 기초


# 1. 개념 및 정의
# 난수 생성 — 왜 PM/분석가에게 중요한가?

# 시뮬레이션: A/B 테스트 사전 설계 (표본 크기 산정, 검정력 분석)
# 테스트 데이터 생성: 분석 파이프라인 개발 시 현실적인 더미 데이터 필요
# 부트스트래핑: 통계적 추정의 신뢰구간 계산
# 재현성: seed를 고정하면 같은 난수를 재생성 → 리포트 재현 가능

'''
| 분포 | 함수 | PM 활용 예시|
| --- | --- | ------|
| 균등분포 | np.random.uniform(low, high) | 전환율 범위 시뮬레이션 |
| 정규분포 | np.random.normal(mean, std) | 매출, 세션 시간 (대칭 분포) |
| 포아송분포 | np.random.poisson(lam) | 일별 이벤트 수, 주문 건수 |
| 지수분포 | np.random.exponential(scale) | 체류 시간, 구매 간격 |
| 이항분포 | np.random.binomial(n, p) | 전환/비전환 시뮬레이션 |
| 정수균등 | np.random.randint(low, high) | DAU, 건수 등 정수 지표 |
'''

# 선형대수 기초 - PM에게 필요한 수준
# - 내적(dot product): 가중 평균 계산의 수학적 표현
# - 행렬 곱: 다차널 가중 합산, 점수 계산
# - 전치(transpose): 데이터 관점 전

# => 딥러닝/ML 단계에서 본격적으로 필요하며, 지금은 기초 개념만 잡는다.


# 2-1. 난수 생성 기본
3
import numpy as np

# ── 재현성 보장: seed 고정 ──
rng = np.random.default_rng(42)  # 최신 방식 (권장)
# 또는: np.random.seed(42)       # 레거시 방식

# ── 정수 난수 ──
dau = rng.integers(3000, 5001, size=7)       # 3000~5000, 7일
print(f"DAU: {dau}")

# ── 균등분포 실수 ──
cvr = rng.uniform(0.02, 0.05, size=7)        # 2~5% 전환율
print(f"전환율: {np.round(cvr, 3)}")

# ── 정규분포 ──
session_time = rng.normal(loc=180, scale=45, size=1000)  # 평균 3분, 표준편차 45초
print(f"세션 시간 평균: {session_time.mean():.1f}초")

# ── 포아송분포: 이산적 이벤트 횟수 ──
daily_orders = rng.poisson(lam=150, size=30)  # 하루 평균 150건
print(f"일별 주문: 평균 {daily_orders.mean():.1f}, 표준편차 {daily_orders.std():.1f}")

# ── 지수분포: 대기 시간, 체류 시간 ──
wait_time = rng.exponential(scale=30, size=1000)  # 평균 30초 대기
print(f"대기 시간 P50: {np.median(wait_time):.1f}초, P90: {np.percentile(wait_time, 90):.1f}초")
 



'''
py 06_numpy_random.py
'''