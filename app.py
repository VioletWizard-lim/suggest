import streamlit as st

# 페이지 설정
st.set_page_config(page_title="한 줄 건의함", page_icon="📫")

st.title("📫 한 줄 건의함")
st.write("건의 사항을 자유롭게 남겨주세요. (익명으로 접수됩니다)")

# 세션 상태 초기화 (건의 내역 저장용 리스트)
if 'suggestions' not in st.session_state:
    st.session_state.suggestions = []

# 건의 입력 폼
with st.form("suggestion_form", clear_on_submit=True):
    suggestion_text = st.text_input("건의 내용", placeholder="여기에 한 줄 건의를 적어주세요.", label_visibility="collapsed")
    submitted = st.form_submit_button("제출하기")

    if submitted:
        if suggestion_text.strip():  # 빈 공백 제출 방지
            # 최신순 정렬을 위해 리스트의 맨 앞(0번 인덱스)에 추가
            st.session_state.suggestions.insert(0, suggestion_text.strip())
            st.success("건의가 성공적으로 제출되었습니다!")
        else:
            st.warning("내용을 입력한 후 제출해 주세요.")

st.divider()

# 접수된 건의 목록 출력
st.subheader("📋 등록된 건의")

if not st.session_state.suggestions:
    st.info("아직 등록된 건의가 없습니다.")
else:
    for suggestion in st.session_state.suggestions:
        # Streamlit 컨테이너를 사용해 건의 내역을 깔끔하게 박스 형태로 표시
        with st.container():
            st.markdown(f"💬 {suggestion}")