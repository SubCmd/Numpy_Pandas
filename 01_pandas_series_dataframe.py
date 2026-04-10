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



'''
py 01_pandas_series_dataframe.py
'''