import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="🐱 MBTI 진로 탐험대",
    page_icon="🐱",
    layout="centered"
)

# CSS 꾸미기
st.markdown("""
<style>
.main {
    background-color: #FFF9F0;
}

.cat-box {
    background-color: #FFF0F5;
    padding: 20px;
    border-radius: 15px;
    border: 3px dashed #FFB6C1;
    margin-bottom: 15px;
}

.job-box {
    background-color: #F0FFF4;
    padding: 15px;
    border-radius: 12px;
    border-left: 8px solid #90EE90;
    margin-bottom: 10px;
}

h1 {
    text-align: center;
    color: #FF69B4;
}

.stButton > button {
    background-color: #FFD166;
    color: black;
    border-radius: 10px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# MBTI 데이터
mbti_jobs = {
    "INTJ": {
        "jobs": ["데이터 과학자", "연구원", "AI 개발자", "전략기획가"],
        "strength": "논리적 사고와 문제 해결 능력이 뛰어나요.",
        "tip": "수학, 과학, 프로그래밍 분야를 탐구해 보세요."
    },
    "INTP": {
        "jobs": ["프로그래머", "과학자", "발명가", "시스템 분석가"],
        "strength": "창의적인 아이디어와 분석력이 강해요.",
        "tip": "탐구 활동과 프로젝트 학습을 즐겨보세요."
    },
    "ENTJ": {
        "jobs": ["CEO", "변호사", "경영컨설턴트", "프로젝트 매니저"],
        "strength": "리더십과 추진력이 뛰어나요.",
        "tip": "토론과 리더 경험을 많이 쌓아보세요."
    },
    "ENTP": {
        "jobs": ["기업가", "마케팅 전문가", "PD", "기획자"],
        "strength": "새로운 아이디어를 만드는 능력이 뛰어나요.",
        "tip": "창업, 발표, 창의활동에 도전해 보세요."
    },
    "INFJ": {
        "jobs": ["상담사", "작가", "교사", "심리학자"],
        "strength": "공감 능력과 통찰력이 뛰어나요.",
        "tip": "사람을 돕는 활동에 참여해 보세요."
    },
    "INFP": {
        "jobs": ["작가", "예술가", "디자이너", "사회복지사"],
        "strength": "상상력과 감수성이 풍부해요.",
        "tip": "창작 활동을 꾸준히 해보세요."
    },
    "ENFJ": {
        "jobs": ["교사", "강사", "인사담당자", "상담사"],
        "strength": "사람들을 이끄는 능력이 뛰어나요.",
        "tip": "동아리와 봉사활동을 경험해 보세요."
    },
    "ENFP": {
        "jobs": ["크리에이터", "광고기획자", "기자", "방송인"],
        "strength": "열정과 창의력이 넘쳐요.",
        "tip": "다양한 체험 활동에 참여해 보세요."
    },
    "ISTJ": {
        "jobs": ["공무원", "회계사", "품질관리자", "행정전문가"],
        "strength": "책임감과 꼼꼼함이 강해요.",
        "tip": "계획적으로 목표를 관리해 보세요."
    },
    "ISFJ": {
        "jobs": ["간호사", "교사", "사회복지사", "행정직"],
        "strength": "배려심과 성실함이 뛰어나요.",
        "tip": "봉사와 협력 경험을 늘려보세요."
    },
    "ESTJ": {
        "jobs": ["경영자", "군인", "행정가", "프로젝트 관리자"],
        "strength": "조직 관리 능력이 뛰어나요.",
        "tip": "리더 역할을 적극 경험해 보세요."
    },
    "ESFJ": {
        "jobs": ["간호사", "교사", "서비스 관리자", "HR 담당자"],
        "strength": "친화력과 협동심이 강해요.",
        "tip": "사람들과 함께하는 활동을 즐겨보세요."
    },
    "ISTP": {
        "jobs": ["엔지니어", "정비사", "파일럿", "개발자"],
        "strength": "실용적인 문제 해결 능력이 뛰어나요.",
        "tip": "메이커 활동과 실습을 경험해 보세요."
    },
    "ISFP": {
        "jobs": ["디자이너", "사진작가", "요리사", "예술가"],
        "strength": "감각적이고 창의적이에요.",
        "tip": "예술·체험 활동을 많이 해보세요."
    },
    "ESTP": {
        "jobs": ["영업전문가", "기업가", "스포츠 지도자", "방송인"],
        "strength": "도전정신과 실행력이 뛰어나요.",
        "tip": "다양한 현장 경험을 해보세요."
    },
    "ESFP": {
        "jobs": ["연예인", "이벤트 기획자", "관광가이드", "유튜버"],
        "strength": "에너지와 사교성이 넘쳐요.",
        "tip": "발표와 공연 활동에 참여해 보세요."
    }
}

# 제목
st.title("🐱 MBTI 진로 탐험대 🐱")

st.markdown("""
<div class="cat-box">
<h3>😺 반가워요!</h3>
MBTI를 선택하면 고양이 진로 코치가 어울리는 직업을 추천해 줄게요!
</div>
""", unsafe_allow_html=True)

# MBTI 선택
selected_mbti = st.selectbox(
    "🐾 나의 MBTI를 선택하세요",
    list(mbti_jobs.keys())
)

if st.button("🐱 직업 추천 받기"):
    info = mbti_jobs[selected_mbti]

    st.balloons()

    st.success(f"🎉 {selected_mbti} 유형 결과!")

    st.markdown(f"""
    <div class="job-box">
    <h3>😺 추천 직업</h3>
    <ul>
    {''.join([f'<li>{job}</li>' for job in info['jobs']])}
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.info(f"💪 강점: {info['strength']}")
    st.warning(f"📚 진로 탐색 팁: {info['tip']}")

    st.markdown("---")

    st.markdown(
        f"🐾 고양이 코치의 한마디\n\n"
        f"**'{selected_mbti} 친구는 자신만의 특별한 재능을 가지고 있어요!'** 😻"
    )

st.markdown("---")
st.caption("🐱 MBTI 진로 탐험대 | 학생 진로교육용 웹앱")
