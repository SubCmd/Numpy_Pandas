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
print(rng)

# rng (random number generation) : generator 객체 -> 빠르고 안전하게 난수 생성
# : 병렬처리 및 고품질 난수 생성에 유리

# ── 정수 난수 ──
dau = rng.integers(3000, 5001, size=7)       # 3000~5000, 7일
print(f"DAU: {dau}")

# ── 균등분포 실수 ──
cvr = rng.uniform(0.02, 0.05, size=7)        # 2~5% 전환율 (conversion rate)
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
 

# 2-2. 현실적 테스트 데이터 생성

rng = np.random.default_rng(42)
n_days = 90 # 분기

# 트렌드 + 주기성 + 노이즈로 현실적인 DAU 생성
days = np.arange(n_days)
trend = 3000 + days * 15                          # 우상향 트렌드
weekly_cycle = 200 * np.sin(2 * np.pi * days / 7) # 주간 패턴
noise = rng.normal(0, 100, size=n_days)           # 랜덤 노이즈

realistic_dau = (trend + weekly_cycle + noise).astype(int)
realistic_dau = np.clip(realistic_dau, 0, None)   # 음수 방지 / np.clip : 최솟값, 최댓값을 제한(클리핑)하는 함수

print(f"DAU 범위: {realistic_dau.min()} ~ {realistic_dau.max()}")
print(f"평균: {realistic_dau.mean():.0f}, 추세: 상승")

# ── 복합 e-커머스 데이터 ──
n_users = 500
user_data = {
    "sessions":   rng.poisson(lam=5, size=n_users),
    "pageviews":  rng.poisson(lam=20, size=n_users),
    "time_min":   rng.exponential(scale=8, size=n_users),
    "purchases":  rng.binomial(n=10, p=0.15, size=n_users),
    "spend":      rng.exponential(scale=50000, size=n_users),
}

# 현실성 추가: 세션 0인 유저는 구매도 0
zero_sessions = user_data["sessions"] == 0
user_data["purchases"][zero_sessions] = 0
user_data["spend"][zero_sessions] = 0

print(f"세션 수 평균: {user_data["sessions"].mean():.1f}")
print(f"페이지 뷰 평균: {user_data["pageviews"].mean():.1f}")
print(f"최소 시간 평균: {user_data["time_min"].mean():.1f}")
print(f"구매수 평균 : {user_data["purchases"].mean():.1f}")
print(f"보낸 시간 평균 : {user_data["spend"].mean():.1f}")


# 2-3. 셔플과 샘플링

rng = np.random.default_rng(42)

# ── 셔플: A/B 테스트 그룹 배정 ──
user_ids = np.arange(1000)
rng.shuffle(user_ids)           # in-place(제자리) 방식 : 한 번 섞으면 원본 배열 자체가 변경됨. (그 섞인 상태 유지)
control = user_ids[:500]
variant = user_ids[500:]
print(f"Control 첫 5명: {control[:5]}")
print(f"Variant 첫 5명: {variant[:5]}")

# ── 비복원 샘플링 ──
sample = rng.choice(user_ids, size=100, replace=False)
print(f"샘플 크기: {len(sample)}, 고유값: {len(np.unique(sample))}")

# ── 복원 샘플링 (부트스트래핑) ──
# : 원본 데이터에서 복원 샘플링을 여러 번 반복
# : 각각 샘플로 통계량(평균, 분산 등) 계산
# 사용 예시 : 적은 데이터를 다시 뽑아서 가짜 분포 만들기
data = np.array([3.2, 3.5, 4.1, 3.8, 3.9, 4.2, 3.7])
n_bootstrap = 1000
boot_means = np.array([
    rng.choice(data, size=len(data), replace=True).mean()
    for _ in range(n_bootstrap)
])
# np.choice(갯수, 무작위 수, replace : 복원추출여부, a : 각 원소가 선택될 확률)

ci_lower = np.percentile(boot_means, 2.5)
ci_upper = np.percentile(boot_means, 97.5)
print(f"평균의 95% CI: [{ci_lower:.2f}, {ci_upper:.2f}]")


# 2-4. 선형대수 기초

# ── 내적(dot product): 가중 평균의 수학적 표현 ──
channel_revenue = np.array([500, 300, 200])      # 채널별 매출
weights = np.array([0.5, 0.3, 0.2])              # 가중치

weighted_total = np.dot(channel_revenue, weights)
print(f"가중 매출: {weighted_total}")  # 380.0
# = 500*0.5 + 300*0.3 + 200*0.2

# ── 행렬 곱: 스코어링 ──
# 3명의 유저 × 4개 행동 지표
user_behavior = np.array([
    [10, 5, 3, 1],    # 유저 A
    [2,  8, 6, 4],    # 유저 B
    [7,  3, 9, 2],    # 유저 C
])  # shape: (3, 4)

# 행동별 가중치 (참여도 점수 계산용)
score_weights = np.array([1, 2, 3, 5])  # shape: (4,)

# 유저별 종합 점수
scores = user_behavior @ score_weights   # @ = np.dot for 행렬
print(f"유저별 점수: {scores}")  # [34, 50, 46]
# A: 10*1 + 5*2 + 3*3 + 1*5 = 34

# ── 전치 + 행렬 곱: 공분산 계산의 기초 ──
X = np.array([[1, 2], [3, 4], [5, 6]])  # (3, 2)
XtX = X.T @ X  # (2, 3) × (3, 2) = (2, 2)
print(f"X^T × X:\n{XtX}")


# ================================================================================================
# 연습 문제
# Lv.1 기본

# 문제 1-1) 난수 생성
import numpy as np
rng = np.random.default_rng(42)

# 1. 1000명 유저의 일별 세션 수 생성 (포아송, 평균 6회)
sessions = rng.poisson(lam=6, size=1000)
print(f"평균 세션 : {sessions.mean():.2f}, 표준편차 : {sessions.std():.2f}")

# 2. 30일간의 전환율 데이터 생성 (균등분포, 2.5%~4.5%)
cvr = rng.uniform(0.025, 0.045, size=30)
print(f"전활율 평균 : {cvr.mean():.4f}, 표준편차 : {cvr.mean():.4f}")

# 3. 100명의 NPS 점수 생성 (정규분포, 평균 7.0, 표준편차 2.0)
#    → 0~10 범위로 클리핑
nps = rng.normal(loc=7.0, scale=2.0, size=100)
nps = np.clip(nps, 0, 10)
print(f"NPS 평균 : {nps.mean():.2f}, 표준편차 ; {nps.std():.2f}")


# 문제 1-2) 내적 활용
# 5개 기능의 사용 빈도와 만족도 가중치
usage = np.array([150, 80, 200, 50, 120])
satisfaction_weight = np.array([4.2, 3.8, 4.5, 3.0, 4.0])

# 1. 가중 만족도 점수 계산 (내적)
weighted_score = np.dot(usage, satisfaction_weight)
print(f"가중 점수 : {weighted_score}")      # 2,454.0

# 2. 전체 사용 빈도 합으로 나누어 가중 평균 만족도 계산
weighted_avg = weighted_score / np.sum(usage)
print(f"가중 평균 만족도 : {weighted_avg:.2f}")     # 4.11

# ================================================
# Lv.2 응용 — 복합 개념 조합

# 문제 2-1) A/B 테스트 시뮬레이션

# 시나리오: A/B 테스트 표본 크기와 효과를 시뮬레이션합니다.
import numpy as np
rng = np.random.default_rng(42)

n_users = 5000
n_sim = 1000

# Control 전환율: 3.0%
# Variant 전환율: 3.5% (목표 lift: +0.5%p)
# 각 그룹 5000명

# 1. control: 5000번 시행, 성공확률 0.03의 이항분포로 전환 여부 생성
#    variant: 5000번 시행, 성공확률 0.035
ctrl = rng.binomial(1, 0.03, size=n_users)
var = rng.binomial(1, 0.035, size=n_users)

# 2. 각 그룹의 실제 전환율 계산
print(f"Control CVR: {ctrl.mean():.4f}")
print(f"Variant CVR: {var.mean():.4f}")

# 3. 1000회 시뮬레이션 반복:
#    매 반복마다 control/variant 전환율 차이를 기록
diffs = np.zeros(n_sim)
for i in range(n_sim):
    c = rng.binomial(1, 0.03, size=n_users).mean()
    v = rng.binomial(1, 0.035, size=n_users).mean()
    diffs[i] = v - c

# 4. 전환율 차이의 평균, 표준편차, 95% CI 계산
print(f"\n=== 1000회 시뮬레이션 결과 ===")
print(f"차이 평균: {diffs.mean():.4f} ({diffs.mean()*100:.2f}%p)")
print(f"차이 표준편차: {diffs.std():.4f}")
ci_low = np.percentile(diffs, 2.5)
ci_high = np.percentile(diffs, 97.5)
print(f"95% CI: [{ci_low:.4f}, {ci_high:.4f}]")

# 5. 차이가 0보다 큰 비율 (= variant가 이긴 확률) 계산
win_rate = np.mean(diffs > 0)
print(f"Variant 승률: {win_rate:.1%}")


'''
py 06_numpy_random.py
'''