import streamlit as st

# 앱 제목
st.title("🔢 초간단 사칙연산 계산기")
st.write("숫자를 입력하고 원하는 연산을 선택하세요.")

# 숫자 입력 받기 (기본값 0.0)
num1 = st.number_input("첫 번째 숫자 입력", value=0.0)
num2 = st.number_input("두 번째 숫자 입력", value=0.0)

# 연산자 선택 기능
operation = st.selectbox("연산자 선택", ["더하기 (+)", "빼기 (-)", "곱하기 (*)", "나누기 (/)"])

# 계산 버튼
if st.button("계산하기"):
    if operation == "더하기 (+)":
        result = num1 + num2
        st.success(f"결과: {num1} + {num2} = {result}")
        
    elif operation == "빼기 (-)":
        result = num1 - num2
        st.success(f"결과: {num1} - {num2} = {result}")
        
    elif operation == "곱하기 (*)":
        result = num1 * num2
        st.success(f"결과: {num1} × {num2} = {result}")
        
    elif operation == "나누기 (/)":
        if num2 == 0:
            st.error("⚠️ 오류: 0으로 나눌 수 없습니다!")
        else:
            result = num1 / num2
            st.success(f"결과: {num1} ÷ {num2} = {result}")
