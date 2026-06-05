import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="달달한 연애상담소", page_icon="💖", layout="centered")
st.title("💖 달달하고 명쾌한 연애상담소")
st.caption("연애 고민이 있나요? 무엇이든 편하게 털어놓으세요!")

# 2. Streamlit Secrets에서 API 키 불러오기 및 초기화
try:
    # 대시보드의 Secrets 환경변수나 .streamlit/secrets.toml에서 가져옴
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
except KeyError:
    st.error("API 키가 설정되지 않았습니다. Streamlit Secrets나 secrets.toml 파일을 확인해주세요.")
    st.stop()

# 3. 세션 상태(Session State)로 채팅 기록 유지
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. 이전 대화 기록 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. 사용자 입력 처리
if user_input := st.chat_input("고민을 이야기해주세요... (예: 썸남이 선톡을 안 해요)"):
    
    # 사용자가 보낸 메시지 화면에 표시 및 저장
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # AI의 답변 생성
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # gemini-2.5-flash-lite 모델 로드
            model = genai.GenerativeModel(
                model_name="gemini-2.5-flash-lite",
                system_instruction=(
                    "당신은 공감 능력이 뛰어나고 위트 있는 전문 연애 상담사입니다. "
                    "사용자의 고민에 진심으로 공감해주되, 가끔은 뼈 때리는(?) 명쾌한 조언도 아끼지 마세요. "
                    "친근한 말투(다정한 반말 혹은 해요체)를 섞어서 친구처럼 상담해주세요."
                )
            )
            
            # 대화 맥락 유지를 위해 이전 기록을 포함한 프롬프트 구성
            # (간단한 구현을 위해 최근 대화들을 텍스트로 엮어서 전달합니다)
            context = ""
            for msg in st.session_state.messages:
                role_label = "사용자" if msg["role"] == "user" else "상담사"
                context += f"{role_label}: {msg['content']}\n"
            
            # API 호출 및 스트리밍 답변 생성
            response = model.generate_content(context, stream=True)
            
            full_response = ""
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + "▌")
            
            # 최종 답변 표시 및 세션 저장
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            # 오류 처리
            error_msg = f"죄송합니다. 답변을 생성하는 중 오류가 발생했습니다. (오류 내용: {str(e)})"
            message_placeholder.markdown(error_msg)
