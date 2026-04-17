# 1-2. NumPy 인덱싱 & 슬라이싱
# 인덱싱(indexing)
# : 배열에서 특정 위치 원소를 선택 / 0부터 시작

# 슬라이싱(slicing)
# : 배열에서 연속된 범위 원소를 한 번에 선택 / (start:stop:step)

import numpy as np

# 기본 인덱싱 : 특정 범위 선택 / "이번 주 월요일 DAU 보여줘"
# 팬시 인덱싱 : 비연속적 여러 위치 한 번에 선택 / "월, 수, 금 DAU만 뽑아줘"
# 불리언 인덱싱 : 조건에 맞는 원소만 필터링 / "DAU 1000 이상 날만 필터링해줘"

# 뷰(view) vs. 복사(copy)
# 뷰 : 수정하면 원본도 변경 (슬라이싱 결과)
# 복사본 : 원본에 영향 없음 (팬시/불리언 인덱싱 결과)
# -> 독립 복사 필요시, arr[1:5].copy()



## 1차원 배열 - 기본 인덱싱 & 슬라이싱

# 일별 신규 가입자 수 (월-일, 7일)
signups = np.array([150, 230, 180, 290, 310, 275, 340])
#                    [0]  [1]  [2]  [3]  [4]  [5]  [6]
#                   [-7] [-6] [-5] [-4] [-3] [-2] [-1]

# ── 기본 인덱싱 ──
print(signups[0])    # 150  (월요일)
print(signups[-1])   # 340  (일요일)
print(signups[3])    # 290  (목요일)

# ── 슬라이싱: start:stop (stop은 미포함) ──
print(signups[0:3])   # [150 230 180]  월~수
print(signups[:3])    # [150 230 180]  처음부터 수요일까지
print(signups[5:])    # [275 340]      토~일
print(signups[-3:])   # [310 275 340]  금~일

# ── step 활용 ──
print(signups[::2])   # [150 180 310 340]  격일 (월, 수, 금, 일)
print(signups[::-1])  # [340 275 310 290 180 230 150]  역순



## 2차원 배열 - 행/열 선택

# 채널(3) × 요일(7) DAU 데이터
# 행: organic(0), paid(1), social(2)
# 열: 월(0) ~ 일(6)
channel_dau = np.array([
    [1200, 1350, 1280, 1400, 1150, 980, 870],   # organic
    [800,  920,  850,  950,  780,  600, 520],    # paid
    [450,  580,  510,  620,  480,  720, 690],    # social
])

# ── 단일 원소: [행, 열] ──
print(channel_dau[0, 0])    # 1200  (organic, 월요일)
print(channel_dau[2, 5])    # 720   (social, 토요일)

# ── 행 전체 선택 ──
print(channel_dau[0])       # [1200 1350 1280 1400 1150 980 870]  organic 전체
print(channel_dau[1, :])    # [800 920 850 950 780 600 520]  paid 전체 (명시적)

# ── 열 전체 선택 ──
print(channel_dau[:, 0])    # [1200 800 450]  월요일, 모든 채널
print(channel_dau[:, -1])   # [870 520 690]   일요일, 모든 채널

# ── 부분 범위 ──
print(channel_dau[0:2, 0:3])   # organic+paid의 월~수
# [[1200 1350 1280]
#  [ 800  920  850]]

print(channel_dau[:, :5])      # 평일(월~금)만, 모든 채널
# [[1200 1350 1280 1400 1150]
#  [ 800  920  850  950  780]
#  [ 450  580  510  620  480]]



# 2-3. 팬시 인덱싱(fancy indexing)

# ── 1차원: 비연속적 선택 ──
signups = np.array([150, 230, 180, 290, 310, 275, 340])

# 월, 수, 금만 선택
mwf = signups[[0, 2, 4]]
print(mwf)  # [150 180 310]

# 주말만 선택 (토, 일)
weekend = signups[[5, 6]]
print(weekend)  # [275 340]

# ── 2차원: 특정 행 여러 개 ──
channel_dau = np.array([
    [1200, 1350, 1280, 1400, 1150, 980, 870],
    [800,  920,  850,  950,  780,  600, 520],
    [450,  580,  510,  620,  480,  720, 690],
])

# organic과 social만 (paid 제외)
organic_social = channel_dau[[0, 2]]
print(organic_social.shape)  # (2, 7)

# ── 2차원: 특정 열 여러 개 (월, 수, 금) ──
mwf_all = channel_dau[:, [0, 2, 4]]
print(mwf_all)
# [[1200 1280 1150]
#  [ 800  850  780]
#  [ 450  510  480]]

# ── 2차원: 특정 좌표 여러 개 ──
# (0,0), (1,3), (2,6) 위치의 값
vals = channel_dau[[0, 1, 2], [0, 3, 6]]
print(vals)  # [1200 950 690]
# → organic 월요일, paid 목요일, social 일요일



# 2-4. 불리언 인덱싱 (Boolean Indexing) 가장 많이 씀

signups = np.array([150, 230, 180, 290, 310, 275, 340])

# ── 조건 마스크 생성 ──
mask = signups >= 250
print(mask)  # [False False False  True  True  True  True]
print(mask.dtype)  # bool

# ── 조건 필터링 ──
high_days = signups[mask]
print(high_days)  # [290 310 275 340]  → 가입자 250명 이상인 날

# ── 한 줄로 쓰기 (가장 많이 쓰는 패턴) ──
print(signups[signups >= 250])  # [290 310 275 340]

# ── 복합 조건: & (and), | (or), ~ (not) ──
# 주의: and/or 대신 &/| 사용, 각 조건을 괄호로 감싸야 함
# 200 이상 AND 300 미만
mid_range = signups[(signups >= 200) & (signups < 300)]
print(mid_range)  # [230 290 275]

# 150 이하 OR 300 이상
extreme = signups[(signups <= 150) | (signups >= 300)]
print(extreme)  # [150 310 340]

# 250 미만인 날 (NOT)
low_days = signups[~(signups >= 250)]
print(low_days)  # [150 230 180]

# ── 2차원 불리언 인덱싱 ──
channel_dau = np.array([
    [1200, 1350, 1280, 1400, 1150, 980, 870],
    [800,  920,  850,  950,  780,  600, 520],
    [450,  580,  510,  620,  480,  720, 690],
])

# DAU 1000 이상인 모든 값 (결과는 1차원으로 펼쳐짐)
high_dau = channel_dau[channel_dau >= 1000]
print(high_dau)  # [1200 1350 1280 1400 1150]



# 2-5. 뷰(View) vs 복사(Copy) 주의사항

original = np.array([100, 200, 300, 400, 500])

# ── 슬라이싱 = 뷰 (원본 연결됨) ──
slice_view = original[1:4]  # [200, 300, 400]
slice_view[0] = 999
print(original)  # [100 999 300 400 500]  ← 원본이 바뀜!

# ── 안전한 복사 ──
original = np.array([100, 200, 300, 400, 500])
slice_copy = original[1:4].copy()
slice_copy[0] = 999
print(original)  # [100 200 300 400 500]  ← 원본 안전

# ── 팬시 인덱싱 = 자동 복사 ──
original = np.array([100, 200, 300, 400, 500])
fancy = original[[1, 2, 3]]
fancy[0] = 999
print(original)  # [100 200 300 400 500]  ← 원본 안전



# 2-6. 조건부 값 변경 (실무에서 자주 사용)

revenue = np.array([1200, -50, 980, 1500, -30, 1100, 0])

# 음수 매출을 0으로 교정
revenue[revenue < 0] = 0
print(revenue)  # [1200    0  980 1500    0 1100    0]

# np.where: 조건에 따라 다른 값 할당
scores = np.array([85, 42, 91, 67, 73, 55, 88])

# 70점 이상 pass, 미만 fail (숫자 변환)
result = np.where(scores >= 70, 1, 0)
print(result)  # [1 0 1 0 1 0 1]

# np.where로 등급 분류 (중첩)
grade = np.where(scores >= 90, 'A',
         np.where(scores >= 70, 'B',
          np.where(scores >= 50, 'C', 'D')))
print(grade)  # ['B' 'D' 'A' 'C' 'B' 'C' 'B']


# ================================================================================================
# 연습 문제
# Lv.1 기본 — 문법 확인

# 1-1) 1차원 슬라이싱
'''
데이터: 최근 10일간 DAU
다음을 슬라이싱으로 추출하세요:
'''
dau = np.array([3200, 3450, 3100, 3800, 3650, 2900, 2700, 3500, 3750, 3900])
# 인덱스:         [0]   [1]   [2]   [3]   [4]   [5]   [6]   [7]   [8]   [9]

# 1. 첫 번째 날의 DAU
first_dau = dau[0]
print(first_dau)

# 2. 마지막 날의 DAU
last_dau = dau[-1]
print(last_dau)

# 3. 처음 3일 (1~3일)
first3_dau = dau[0:3]
print(first3_dau)

# 4. 마지막 4일 (7~10일)
last4_dau = dau[-4:]
print(last4_dau)

# 5. 짝수 인덱스만 (0, 2, 4, 6, 8일차)
even_dau = dau[::2]
print(even_dau)

# 6. 역순 배열
reverse_dau = dau[::-1]
print(reverse_dau)

# ================================================
# 1-2) 2차원 인덱싱

# 데이터: 3개 지역 × 4분기 매출 (억원)
sales = np.array([
    [45, 52, 48, 61],   # 서울
    [30, 35, 32, 40],   # 부산
    [20, 24, 22, 28],   # 대구
])

# 1. 서울의 Q4 매출
seoul_Q4 = sales[0, 3]
print(seoul_Q4)

# 2. 부산의 전체 분기 매출
busan_all = sales[1, :]
print(busan_all)

# 3. 모든 지역의 Q1 매출
all_Q1 = sales[:, 0]
print(all_Q1)

# 4. 서울+부산의 Q2~Q3 매출
seoul_busan_Q23 = sales[0:2, 1:3]
print(seoul_busan_Q23)

# 5. 대구의 Q3, Q4 매출
daegu_Q34 = sales[2, -2:]
print(daegu_Q34)

# ================================================
# 1-3) 불리언 인덱싱 기초

# 데이터: 일별 신규 설치 수
installs = np.array([120, 340, 85, 290, 510, 45, 380, 210, 670, 155])

# 200 이상인 값
over200 = installs[installs >= 200]
print(over200)

# 100 미만인 값
under100 = installs[installs < 100]
print(under100)

# 200 이상이면서 400 미만인 값
over200_under400 = installs[(installs >= 200) & (installs < 400)]
print(over200_under400)

# 100 미만이거나 500 이상인 값
under100_over500 = installs[(installs < 100) | (installs >= 500)]
print(under100_over500)


# ================================================
# Lv.2 응용 — 복합 개념 조합

# 문제 2-1) 이상치 탐지 및 처리

import numpy as np

# 시나리오: 일별 주문 건수 데이터에 이상치가 섞여 있습니다.
orders = np.array([150, 180, 5200, 165, 170, 155, -30, 190, 175, 6100, 160, 185])

# 1. 음수 값이 몇 개 있는지 확인
neg_count = np.sum(orders < 0)
print(f"음수 값 갯수 : {neg_count}")

# 2. 음수 값을 0으로 교정
orders[orders < 0] = 0
print(f"교정 이후 : {orders}")

# 3. 1000 이상인 이상치를 찾아 출력
outliers = orders[orders >= 1000]
print(f"1000 이상 이상치 : {outliers}")

# 4. 이상치(1000 이상)를 제외한 정상 데이터만 추출
normal = orders[(orders >= 0) & (orders < 1000)]
print(f"정상 데이터 : {normal}")

# 5. 정상 데이터의 평균(np.mean) 계산
normal_nonzero = orders[(orders > 0) & (orders < 1000)]
print(f"정상 데이터 평균(0 제외) : {np.mean(normal_nonzero):.1f}")
print(f"정상 데이터 평균(0 포함) : {np.mean(normal):.1f}")


# ================================================
# Lv.3 포트폴리오 — 실전 시나리오

# 문제 3-1) A/B 테스트 데이터 전처리
'''
시나리오:
A/B 테스트를 진행 중입니다. 14일간 control/variant 두 그룹의 전환율을 수집했지만,
데이터에 결측(-1로 표시)과 이상치가 포함되어 있습니다.
'''
np.random.seed(42)

# 14일간 데이터 생성
days = np.arange(1, 15)
control = np.array([3.2, 3.5, -1, 3.1, 3.4, 3.3, 15.0, 
                    3.6, 3.2, 3.5, -1, 3.4, 3.3, 3.7])
variant = np.array([3.8, -1, 4.1, 3.9, 4.2, 4.0, 3.7, 
                    4.3, -1, 4.1, 4.0, 16.5, 4.2, 4.4])


# 1. 결측(-1) 위치 확인: 각 그룹에서 결측인 날짜 인덱스를 추출
control_missing = np.where(control == -1)[0]
variant_missing = np.where(variant == -1)[0]
print(f"Control 결측치: {control_missing}")
print(f"Variant 결측치: {variant_missing}")

print(f"Control 결측 날짜 : Day {days[control_missing]}")
print(f"Variant 결측 날짜 : Day {days[variant_missing]}")

# 2. 이상치 탐지: 각 그룹에서 10.0 이상인 값의 위치와 값 출력
outlier_control_idx = np.where(control >= 10)[0]
outlier_variant_idx = np.where(variant >= 10)[0]
print(f"Control 이상치 : {days[outlier_control_idx]}, 값 : {control[outlier_control_idx]}")
print(f"Variant 이상치 : {days[outlier_variant_idx]}, 값 : {variant[outlier_variant_idx]}")

# 3. 유효 데이터 추출:
# - 양쪽 그룹 모두에서 결측(-1)이 아니고 이상치(10.0 이상)가 아닌 날만 선택
# - 유효한 날짜, control 값, variant 값을 각각 추출
valid_mask = np.where(
    (control != -1) &   # control 결측 아님
    (variant != -1) &   # variant 결측 아님
    (control < 10)  &   # control 이상치 아님
    (variant < 10)      # variant 이상치 아님
)
print(f"유효 데이터 마스크 : {valid_mask}")
print(f"유효 일수 : {np.sum(valid_mask)}일")

# 유효 데이터
valid_days = days[valid_mask]
valid_control = control[valid_mask]
valid_variant = variant[valid_mask]

# 4. 유효 데이터로 각 그룹의 평균 전환율 계산
control_mean = np.mean(valid_control)
variant_mean = np.mean(valid_variant)
print(f"control 평균 : {control_mean:.2f}%")
print(f"variant 평균 : {variant_mean:.2f}%")

# 5. variant - control 차이(lift)를 일별로 계산
lift = valid_variant - valid_control
print(f"일별 lift : {lift}")

# 6. lift가 양수인 날의 비율 계산 (variant가 이긴 날 %)
win_rate = np.mean(lift > 0)
print(f"Variant 승리 비율 : {win_rate:.1%}")


'''
💡 힌트:
- 두 조건을 결합할 때: valid_mask = condition1 & condition2
- np.mean(lift > 0)으로 비율 계산 가능 (True=1, False=0)
'''


'''
py 02_numpy_indexing.py
'''