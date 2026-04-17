# Phase 2-6: 문자열 처리 (.str)

# 개념 및 정의
# .str접근자란?
# : Pandas Series의 문자열 메서드에 접근하는 방법.
# : 파이썬 내장 str 메서드를 벡터화해서 시리즈 전체에 적용

'''
# ❌ 반복문
[s.upper() for s in df["name"]]

# ✅ 벡터화
df["name"].str.upper()
'''

# 주요 메서드 분류
# | 함수 | 메서드 | 용도 |
# | ---- | ------------------------- | ------------------ |
# | 변환 | lower, upper, title, strip | 대소문자, 공백 제거 |
# | 검색 | contains, startswith, endswith, find | 패턴 포함 여부 |
# | 추출 | extract, split, slice, get | 부분 문자열 추출 |
# | 치환 | replace, pad, zfill | 문자열 교체, 패딩 |
# | 분할 | split, partition | 구분자로 분리 | 
# | 정보 | len, count, isdigit, isalpha | 길이, 횟수, 타입 확인 |


# 2-1. 기본 변환 & 정리
import pandas as pd

channels = pd.Series(["  Organic ", "PAID_search", "Social Media", 
                       "email ", " Referral"])

# 공백 제거 + 소문자
clean = channels.str.strip().str.lower()
print(clean)
# 0        organic
# 1    paid_search
# 2   social media
# 3          email
# 4       referral

# 공백 → 언더스코어
clean = clean.str.replace(" ", "_")

# 특정 문자 제거
prices = pd.Series(["₩49,000", "₩19,000", "₩199,000"])
numbers = prices.str.replace("₩", "").str.replace(",", "")
print(numbers)  # ["49000", "19000", "199000"]


# 검색 & 필터링
events = pd.Series([
    "page_view_home", "page_view_product", "signup_email",
    "signup_social", "purchase_complete", "page_view_cart",
    "checkout_start", "purchase_failed"
])

# contains : 포함 여부
print(events.str.contains("page_view"))
# [True, True, False, False, False, True, False, False]

# 필터링
page_views = events[events.str.contains("page_view")]
print(page_views.tolist())  # 배열/시리즈를 리스트로 변환
# ['page_view_home', 'page_view_product', 'page_view_cart']

# startswith / endswith
signups = events[events.str.startswith("signup")]
failures = events[events.str.endswith("failed")]
print(f"signups : {signups}")
print(f"failures : {failures}")

# 정규표현식 (regex=True가 기본)
purchase_events = events[events.str.contains("purchase|checkout")]
print(purchase_events)


# 2-3. 분할 & 추출
# ── split: 구분자로 분할 ──
events = pd.Series(["page_view_home", "signup_email", "purchase_complete"])

# split → 리스트 Series
split_result = events.str.split("_")
print(split_result)
# 0     [page, view, home]
# 1        [signup, email]
# 2    [purchase, complete]

# 특정 위치 요소 추출
print(events.str.split("_").str[0])   # ['page', 'signup', 'purchase']
print(events.str.split("_").str[-1])  # ['home', 'email', 'complete']

# expand=True → 바로 DataFrame으로
split_df = events.str.split("_", expand=True)
print(split_df)
#          0         1         2
# 0     page      view      home
# 1   signup     email      None
# 2  purchase  complete     None

# n= 으로 분할 횟수 제한
events.str.split("_", n=1, expand=True)  # 첫 _ 에서만 분할

# ── extract: 정규표현식 그룹 추출 ──
urls = pd.Series([
    "/product/123/detail",
    "/product/456/review",
    "/category/electronics",
])

# 제품 ID 추출
product_ids = urls.str.extract(r"/product/(\d+)/")
print(product_ids)
#        0
# 0    123
# 1    456
# 2    NaN  ← 매칭 안 됨

# 여러 그룹 추출
parts = urls.str.extract(r"/(\w+)/(\w+)")
print(parts)
#          0            1
# 0   product          123
# 1   product          456
# 2  category  electronics

# ── slice: 위치 기반 부분 문자열 ──
codes = pd.Series(["KR-2024-001", "US-2024-002", "JP-2024-003"])
print(codes.str[:2])       # ['KR', 'US', 'JP']
print(codes.str[3:7])      # ['2024', '2024', '2024']
print(codes.str[-3:])      # ['001', '002', '003']

utm_sources = pd.Series([
    "utm_source=google&utm_medium=cpc&utm_campaign=spring_sale",
    "utm_source=facebook&utm_medium=social&utm_campaign=brand_awareness",
    "utm_source=newsletter&utm_medium=email&utm_campaign=weekly_digest",
])

# source 추출
source = utm_sources.str.extract(r"utm_source=(\w+)")
medium = utm_sources.str.extract(r"utm_medium=(\w+)")
campaign = utm_sources.str.extract(r"utm_campaign=([\w]+)")

utm_df = pd.DataFrame({
    "source": source[0],
    "medium": medium[0],
    "campaign": campaign[0],
})
print(utm_df)


# ================================================================================================
# 연습 문제
# Lv.1 기본

emails = pd.Series([
    "  John.Doe@Gmail.COM  ",
    "jane_smith@YAHOO.com",
    " Bob.Lee@company.co.kr",
    "alice@Outlook.COM ",
])

# 1. 공백 제거 + 전체 소문자 변환
emails_clean = emails.str.strip().str.lower()
print(emails_clean)

# 2. @ 기준으로 분할하여 [이름, 도메인] DataFrame 생성
df = emails.str.split("@", expand=True)
df.columns = ["name", "domain"]
print(df.columns)

# 3. gmail.com 도메인인 이메일만 필터링
gmail_only = emails_clean[emails_clean.str.endswith("gmail.com")]
print(gmail_only)

# 4. 이메일 길이(문자수) Series 생성
lengths = emails_clean.str.len()
print(lengths)

'''
py 06_pandas_string_methods.py
'''