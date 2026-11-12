"""
한 줄 건의함 - Supabase 연결 버전
- 건의를 Supabase의 suggestions 테이블에 저장하고 불러옵니다.
- 키는 환경 변수 SUPABASE_URL, SUPABASE_KEY에서 불러옵니다.
"""
import os
from datetime import datetime
from zoneinfo import ZoneInfo

import streamlit as st
from supabase import create_client

st.set_page_config(page_title="한 줄 건의함", page_icon="📮")
st.title("📮 한 줄 건의함")
st.caption("학교에 바라는 점을 한 줄로 남겨 주세요. 이름은 적지 않아요.")

CATEGORIES = ["급식", "시설", "행사", "기타"]


# Supabase 연결 (한 번만 만들고 재사용)
@st.cache_resource
def get_client():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        st.error("환경 변수 SUPABASE_URL, SUPABASE_KEY가 없어요. Codespaces Secrets에 등록했는지 확인하세요.")
        st.stop()
    return create_client(url, key)


supabase = get_client()


def to_korean_time(text):
    """DB에 저장된 시간(UTC)을 한국 시간으로 바꾸기"""
    return datetime.fromisoformat(text).astimezone(ZoneInfo("Asia/Seoul")).strftime("%m/%d %H:%M")


# 건의 입력
with st.form("suggestion_form", clear_on_submit=True):
    category = st.selectbox("카테고리", CATEGORIES)
    content = st.text_input("건의 내용", placeholder="예) 매점 운영 시간을 늘려 주세요")
    submitted = st.form_submit_button("제출하기")

if submitted:
    if content.strip() == "":
        st.warning("내용을 입력해 주세요.")
    else:
        # 건의 저장 (id, likes, created_at은 DB가 자동으로 채움)
        supabase.table("suggestions").insert(
            {"content": content.strip(), "category": category}
        ).execute()
        st.success("건의가 등록되었어요!")

# 건의 불러오기 (최신순)
rows = (
    supabase.table("suggestions")
    .select("*")
    .order("created_at", desc=True)
    .execute()
    .data
)

st.subheader(f"건의 목록 ({len(rows)}개)")

if not rows:
    st.info("아직 건의가 없어요. 첫 번째 건의를 남겨 보세요!")

for row in rows:
    st.markdown(
        f"- **[{row['category']}]** {row['content']} · 👍 {row['likes']}  \n"
        f"  <small>{to_korean_time(row['created_at'])}</small>",
        unsafe_allow_html=True,
    )