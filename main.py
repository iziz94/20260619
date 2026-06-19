```python
import streamlit as st
import random

st.set_page_config(
    page_title="🐱 MBTI 진로 탐험대",
    page_icon="🐱",
    layout="wide"
)

# ---------------------------
# 스타일
# ---------------------------
st.markdown("""
<style>

.stApp{
    background:#FFF9F2;
}

.title-box{
    background:linear-gradient(135deg,#FFD6E8,#FFF4C7);
    padding:25px;
    border-radius:20px;
    text-align:center;
    margin-bottom:20px;
}

.result-box{
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0 3px 10px rgba(0,0,0,0.1);
}

.cat-box{
    background:#FFF0F6;
    border-left:8px solid #FF69B4;
    padding:15px;
    border-radius:12px;
}

.score-box{
    background:#E8FFF1;
    padding:15px;
    border-radius:12px;
}

h1,h2,h3{
    color:#444;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# 데이터
# ---------------------------

mbti_data = {

    "INTJ":{
        "nickname":"🦉 전략 고양이",
        "desc":"계획적이고 분석적인 사고를 잘해요.",
        "jobs":["AI 개발자","데이터 과학자","연구원","전략기획가","로봇공학자"],
        "major":["컴퓨터공학","인공지능","수학","통계학"],
        "skills":["논리력","분석력","문제해결력"],
        "future":["AI 엔지니어","양자컴퓨팅 연구원","디지털 전략가"]
    },

    "INTP":{
        "nickname":"🔬 탐험 고양이",
        "desc":"아이디어와 호기심이 많아요.",
        "jobs":["과학자","프로그래머","시스템분석가","발명가","연구원"],
        "major":["물리학","컴퓨터공학","전자공학"],
        "skills":["창의력","탐구력","분석력"],
        "future":["AI 연구원","우주기술 연구원","데이터 엔지니어"]
    },

    "ENTJ":{
        "nickname":"👑 리더 고양이",
        "desc":"목표를 이루는 추진력이 강해요.",
        "jobs":["CEO","변호사","경영컨설턴트","프로젝트매니저"],
        "major":["경영학","법학","경제학"],
        "skills":["리더십","기획력","의사결정"],
        "future":["스타트업 창업가","ESG 경영전문가"]
    },

    "ENTP":{
        "nickname":"🚀 발명가 고양이",
        "desc":"새로운 아이디어를 만드는 것을 좋아해요.",
        "jobs":["기획자","기업가","광고전문가","PD"],
        "major":["경영학","미디어학","광고홍보학"],
        "skills":["창의력","소통능력","도전정신"],
        "future":["콘텐츠 크리에이터","메타버스 기획자"]
    },

    "INFJ":{
        "nickname":"🌙 공감 고양이",
        "desc":"사람의 마음을 잘 이해해요.",
        "jobs":["상담사","교사","심리학자","작가"],
        "major":["심리학","교육학","국문학"],
        "skills":["공감능력","통찰력","소통"],
        "future":["마음건강 코치","교육콘텐츠 개발자"]
    },

    "INFP":{
        "nickname":"🎨 감성 고양이",
        "desc":"상상력이 풍부하고 따뜻해요.",
        "jobs":["작가","예술가","디자이너","사회복지사"],
        "major":["디자인","문예창작","사회복지학"],
        "skills":["창의력","공감","표현력"],
        "future":["UX 디자이너","디지털 아티스트"]
    },

    "ENFJ":{
        "nickname":"🌟 멘토 고양이",
        "desc":"사람들을 성장시키는 힘이 있어요.",
        "jobs":["교사","강사","상담사","인사담당자"],
        "major":["교육학","심리학","행정학"],
        "skills":["리더십","소통","공감"],
        "future":["교육플랫폼 기획자","코칭전문가"]
    },

    "ENFP":{
        "nickname":"🌈 모험 고양이",
        "desc":"열정과 아이디어가 넘쳐요.",
        "jobs":["방송인","기자","광고기획자","크리에이터"],
        "major":["신문방송학","광고홍보학"],
        "skills":["창의력","소통","열정"],
        "future":["유튜브 크리에이터","브랜드 스토리텔러"]
    },

    "ISTJ":{
        "nickname":"📋 성실 고양이",
        "desc":"책임감이 강하고 꼼꼼해요.",
        "jobs":["공무원","회계사","행정전문가"],
        "major":["회계학","행정학"],
        "skills":["책임감","계획성","정확성"],
        "future":["정보보안 관리자"]
    },

    "ISFJ":{
        "nickname":"💖 배려 고양이",
        "desc":"친절하고 헌신적이에요.",
        "jobs":["간호사","교사","사회복지사"],
        "major":["간호학","사회복지학"],
        "skills":["배려","성실성","협력"],
        "future":["노인복지전문가"]
    },

    "ESTJ":{
        "nickname":"🏆 관리자 고양이",
        "desc":"체계적으로 조직을 운영해요.",
        "jobs":["경영자","행정가","군인"],
        "major":["경영학","행정학"],
        "skills":["관리능력","리더십"],
        "future":["스마트시티 관리자"]
    },

    "ESFJ":{
        "nickname":"🤝 친구 고양이",
        "desc":"사람들과 함께하는 것을 좋아해요.",
        "jobs":["교사","간호사","HR담당자"],
        "major":["교육학","간호학"],
        "skills":["친화력","협력"],
        "future":["조직문화 전문가"]
    },

    "ISTP":{
        "nickname":"🔧 기술자 고양이",
        "desc":"실습과 문제해결을 좋아해요.",
        "jobs":["엔지니어","정비사","파일럿"],
        "major":["기계공학","항공학"],
        "skills":["실무능력","분석력"],
        "future":["드론 엔지니어"]
    },

    "ISFP":{
        "nickname":"📸 예술 고양이",
        "desc":"감각적이고 창의적이에요.",
        "jobs":["사진작가","디자이너","요리사"],
        "major":["디자인","조리학"],
        "skills":["창의력","감성"],
        "future":["3D 아티스트"]
    },

    "ESTP":{
        "nickname":"⚡ 액션 고양이",
        "desc":"도전하고 행동하는 것을 좋아해요.",
        "jobs":["영업전문가","기업가","스포츠지도자"],
        "major":["체육학","경영학"],
        "skills":["실행력","도전정신"],
        "future":["e스포츠 매니저"]
    },

    "ESFP":{
        "nickname":"🎤 스타 고양이",
        "desc":"즐거움을 만드는 재능이 있어요.",
        "jobs":["연예인","MC","관광가이드"],
        "major":["공연예술","관광학"],
        "skills":["사교성","표현력"],
        "future":["콘텐츠 크리에이터"]
    }
}

# ---------------------------
# 헤더
# ---------------------------

st.markdown("""
<div class="title-box">
<h1>🐱 MBTI 진로 탐험대 🐱</h1>
<h4>고양이 진로 코치와 함께 미래 직업을 찾아보자!</h4>
</div>
""", unsafe_allow_html=True)

st.sidebar.title("🐾 MBTI 선택")

mbti = st.sidebar.selectbox(
    "나의 MBTI는?",
    list(mbti_data.keys())
)

cat_messages = [
    "😺 너의 재능은 분명 빛날 거야!",
    "🐾 한 걸음씩 꿈을 향해 가보자!",
    "😻 오늘도 멋진 미래를 준비하고 있구나!",
    "🐱 호기심은 최고의 능력이야!",
    "🌟 넌 생각보다 훨씬 큰 가능성을 가지고 있어!"
]

if st.sidebar.button("직업 추천 받기"):

    st.balloons()

    data = mbti_data[mbti]

    tab1, tab2, tab3, tab4 = st.tabs(
        ["🐱 MBTI 소개", "💼 추천 직업", "🎓 학과·역량", "🌈 미래 직업"]
    )

    with tab1:
        st.subheader(f"{mbti} - {data['nickname']}")
        st.write(data["desc"])

        score = random.randint(80, 100)

        st.markdown(
            f"""
            <div class="score-box">
            <h3>🎯 진로 적합도 점수</h3>
            <h2>{score}점</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    with tab2:
        st.subheader("💼 추천 직업")

        for job in data["jobs"]:
            st.success("🐾 " + job)

    with tab3:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🎓 추천 학과")
            for major in data["major"]:
                st.info(major)

        with col2:
            st.subheader("⭐ 필요한 역량")
            for skill in data["skills"]:
                st.warning(skill)

    with tab4:
        st.subheader("🌈 미래 유망 직업")

        for job in data["future"]:
            st.success("🚀 " + job)

    st.markdown("---")

    st.markdown(
        f"""
        <div class="cat-box">
        <h3>🐱 고양이 코치의 응원</h3>
        <h2>{random.choice(cat_messages)}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

else:
    st.info("👈 왼쪽에서 MBTI를 선택하고 버튼을 눌러보세요!")

st.markdown("---")
st.caption("🐱 MBTI 진로 탐험대 | 진로교육용 Streamlit 웹앱")
```
