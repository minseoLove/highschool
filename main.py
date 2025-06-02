import streamlit as st
st.title('나의 첫 sreamlit 프로젝트!')
st.write('Hello streamlit')

import streamlit as st
import random

# 페이지 설정
st.set_page_config(
    page_title="🌟 MBTI 진로 탐험가 🌟",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일링
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .stSelectbox > div > div {
        background: linear-gradient(90deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
        border-radius: 20px;
        border: none;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    .career-card {
        background: linear-gradient(145deg, #ffffff, #f0f0f0);
        border-radius: 20px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        color: #333;
    }
    
    .mbti-title {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 30px;
    }
    
    .personality-desc {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .job-item {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        margin: 8px 0;
        border-radius: 15px;
        box-shadow: 0 4px 15px 0 rgba(31, 38, 135, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# MBTI 타입별 데이터
mbti_data = {
    "INTJ": {
        "name": "건축가형 🏗️",
        "emoji": "🧠💡🎯",
        "description": "전략적 사고와 독립성을 중시하는 혁신적인 계획가입니다! ✨",
        "careers": [
            "🔬 과학자/연구원 - 깊이 있는 연구와 혁신적 발견",
            "💻 소프트웨어 엔지니어 - 체계적인 시스템 설계",
            "🏢 경영 컨설턴트 - 전략적 비즈니스 솔루션",
            "📊 데이터 분석가 - 복잡한 데이터 패턴 발견",
            "🎨 건축가 - 창의적이고 기능적인 공간 설계",
            "⚖️ 변호사 - 논리적 법률 분석",
            "📈 투자 분석가 - 시장 트렌드 예측",
            "🎮 게임 디자이너 - 혁신적 게임 시스템 구축"
        ]
    },
    "INTP": {
        "name": "논리술사형 🔍",
        "emoji": "🤔💭🔬",
        "description": "논리적 사고와 지적 호기심이 넘치는 사색가입니다! 🌟",
        "careers": [
            "🔬 물리학자 - 우주의 법칙 탐구",
            "💻 프로그래머 - 혁신적 알고리즘 개발",
            "📚 철학자/연구원 - 깊이 있는 사상 연구",
            "🧪 화학자 - 분자 세계의 비밀 탐구",
            "📊 통계학자 - 수치 속 패턴 발견",
            "🎯 UX/UI 디자이너 - 사용자 경험 최적화",
            "📖 작가/편집자 - 창의적 글쓰기와 편집",
            "🤖 AI 연구원 - 인공지능 기술 개발"
        ]
    },
    "ENTJ": {
        "name": "통솔자형 👑",
        "emoji": "💪🎯🚀",
        "description": "천부적인 리더십과 야심찬 비전을 가진 지휘관입니다! ⭐",
        "careers": [
            "👔 CEO/경영진 - 기업 비전 실현과 조직 이끌기",
            "💼 경영 컨설턴트 - 비즈니스 전략 수립",
            "🏛️ 정치인 - 사회 변화 주도",
            "💰 투자은행가 - 금융 시장 리더십",
            "⚖️ 변호사 - 법정에서의 설득력",
            "🎬 영화 프로듀서 - 창작 프로젝트 총괄",
            "🏢 프로젝트 매니저 - 복합 프로젝트 관리",
            "🚀 스타트업 창업가 - 혁신적 비즈니스 구축"
        ]
    },
    "ENTP": {
        "name": "변론가형 🎭",
        "emoji": "💡🎪🌈",
        "description": "창의적이고 열정적인 혁신가이자 아이디어 뱅크입니다! 🎨",
        "careers": [
            "🚀 창업가 - 혁신적 비즈니스 아이디어 실현",
            "📺 방송인/MC - 창의적 방송 컨텐츠 제작",
            "📰 저널리스트 - 사회 이슈 탐구와 보도",
            "🎨 광고 기획자 - 창의적 마케팅 캠페인",
            "💻 제품 기획자 - 혁신적 제품 개발",
            "🎬 영화감독 - 창의적 스토리텔링",
            "🏢 마케팅 매니저 - 브랜드 전략 수립",
            "🎤 강연가 - 영감을 주는 메시지 전달"
        ]
    },
    "INFJ": {
        "name": "옹호자형 🕊️",
        "emoji": "💚🌱✨",
        "description": "이상주의적이고 원칙이 뚜렷한 선의의 옹호자입니다! 🌸",
        "careers": [
            "👩‍⚕️ 상담사/심리치료사 - 마음의 치유와 성장 도움",
            "✍️ 작가 - 깊이 있는 메시지 전달",
            "🎨 예술가 - 감정과 의미를 담은 작품 창작",
            "👩‍🏫 교사/교수 - 지식과 가치 전수",
            "🏥 의사 - 생명 구하고 치유하기",
            "🌍 사회복지사 - 사회적 약자 보호",
            "🎬 다큐멘터리 감독 - 사회 문제 조명",
            "📚 도서관 사서 - 지식의 보고 관리"
        ]
    },
    "INFP": {
        "name": "중재자형 🌺",
        "emoji": "🎨💝🦋",
        "description": "따뜻하고 창의적인 마음을 가진 이상주의자입니다! 🌈",
        "careers": [
            "🎨 그래픽 디자이너 - 시각적 아름다움 창조",
            "✍️ 소설가/시인 - 감성적 스토리텔링",
            "🎵 음악가/작곡가 - 멜로디로 감정 표현",
            "📸 사진작가 - 순간의 아름다움 포착",
            "👩‍⚕️ 심리상담사 - 마음의 상처 치유",
            "🌱 환경운동가 - 지구 보호 활동",
            "🎪 예술치료사 - 예술로 마음 치유",
            "📱 UX 디자이너 - 사용자 친화적 경험 설계"
        ]
    },
    "ENFJ": {
        "name": "선도자형 🌟",
        "emoji": "💖🤝🎭",
        "description": "카리스마 넘치는 지도자이자 사람들의 성장을 돕는 멘토입니다! 👥",
        "careers": [
            "👩‍🏫 교사/교육자 - 학생들의 성장 이끌기",
            "💼 인사관리자 - 조직 내 인재 육성",
            "🎤 연설가/강연자 - 영감을 주는 메시지 전달",
            "🎭 배우/연예인 - 감정 표현과 대중 소통",
            "👩‍⚕️ 간호사 - 환자 돌봄과 치유",
            "🏛️ 정治인 - 사회 발전을 위한 리더십",
            "📻 방송인 - 대중과의 소통과 정보 전달",
            "🌍 NGO 활동가 - 사회 변화 주도"
        ]
    },
    "ENFP": {
        "name": "활동가형 🎉",
        "emoji": "🌈🎪💫",
        "description": "열정적이고 창의적인 자유로운 영혼의 소유자입니다! 🎊",
        "careers": [
            "📺 방송인/연예인 - 활발한 에너지로 대중 즐겁게 하기",
            "🎨 창작자/아티스트 - 무한한 상상력 표현",
            "📝 카피라이터 - 창의적 광고 문구 제작",
            "🎪 이벤트 기획자 - 특별한 순간 연출",
            "👩‍💻 소셜미디어 매니저 - 온라인 커뮤니티 활성화",
            "🎬 영상 크리에이터 - 재미있는 콘텐츠 제작",
            "🏢 마케팅 전문가 - 브랜드 스토리텔링",
            "🎤 MC/사회자 - 행사 진행과 분위기 메이킹"
        ]
    },
    "ISTJ": {
        "name": "현실주의자형 📋",
        "emoji": "⚖️📊🏛️",
        "description": "책임감 강하고 신뢰할 수 있는 체계적인 실무자입니다! 💪",
        "careers": [
            "👩‍💼 회계사 - 정확한 재무 관리",
            "⚖️ 판사/법관 - 공정한 법 집행",
            "🏦 은행원 - 신뢰할 수 있는 금융 서비스",
            "👮‍♀️ 경찰관 - 사회 질서 유지",
            "📊 감사관 - 투명한 조직 운영 감시",
            "🏥 의료기록사 - 정확한 의료 정보 관리",
            "📚 사서 - 체계적인 정보 관리",
            "🏢 행정공무원 - 효율적인 공공 서비스"
        ]
    },
    "ISFJ": {
        "name": "수호자형 🛡️",
        "emoji": "💕🤱🌸",
        "description": "따뜻하고 헌신적인 마음으로 타인을 돌보는 보호자입니다! 🤗",
        "careers": [
            "👩‍⚕️ 간호사 - 환자 돌봄과 치유",
            "👩‍🏫 초등교사 - 아이들의 성장 도움",
            "🏥 물리치료사 - 신체 회복 도움",
            "👶 보육교사 - 어린이 발달 지원",
            "🍽️ 영양사 - 건강한 식단 관리",
            "📚 도서관 사서 - 지식 접근성 지원",
            "🏠 인테리어 디자이너 - 편안한 공간 창조",
            "🌱 사회복지사 - 도움이 필요한 분들 지원"
        ]
    },
    "ESTJ": {
        "name": "경영자형 💼",
        "emoji": "👔📈🎯",
        "description": "뛰어난 관리 능력과 리더십을 가진 조직의 기둥입니다! 🏆",
        "careers": [
            "👔 경영진/관리자 - 조직 운영과 목표 달성",
            "🏢 프로젝트 매니저 - 효율적 프로젝트 관리",
            "⚖️ 변호사 - 체계적 법률 서비스",
            "🏦 금융 매니저 - 자산 관리와 투자 전략",
            "🏛️ 공무원 - 효율적 행정 서비스",
            "🏥 병원 관리자 - 의료 시설 운영",
            "📊 품질관리자 - 제품/서비스 품질 보장",
            "🚚 물류 관리자 - 효율적 공급망 운영"
        ]
    },
    "ESFJ": {
        "name": "집정관형 🤝",
        "emoji": "💖👥🎪",
        "description": "사람들과의 조화를 중시하는 따뜻한 협력자입니다! 🌻",
        "careers": [
            "👩‍🏫 교사 - 학생들과의 소통과 교육",
            "🏥 간호사 - 환자와 가족 돌봄",
            "💼 인사담당자 - 직원 복지와 관계 관리",
            "🍽️ 호텔리어 - 고객 서비스와 만족",
            "👗 패션 코디네이터 - 스타일링과 이미지 메이킹",
            "🎉 웨딩플래너 - 특별한 순간 연출",
            "📞 고객서비스 매니저 - 고객 만족 극대화",
            "🏪 매장 관리자 - 고객 응대와 매장 운영"
        ]
    },
    "ISTP": {
        "name": "만능재주꾼형 🔧",
        "emoji": "⚙️🛠️🎯",
        "description": "실용적이고 융통성 있는 문제 해결의 달인입니다! 🔥",
        "careers": [
            "🔧 기계공학자 - 정밀한 기계 설계와 제작",
            "💻 시스템 관리자 - IT 인프라 구축과 관리",
            "🚗 자동차 정비사 - 차량 진단과 수리",
            "⚡ 전기기사 - 전기 시설 설치와 유지보수",
            "🏗️ 건축기사 - 실용적 건축물 설계",
            "🔬 실험실 기술자 - 정밀한 실험과 분석",
            "🎮 게임 프로그래머 - 게임 시스템 개발",
            "🛩️ 파일럿 - 항공기 조종과 운항"
        ]
    },
    "ISFP": {
        "name": "모험가형 🎨",
        "emoji": "🌺🎭🦋",
        "description": "예술적 감각과 개성이 뛰어난 자유로운 예술가입니다! 🌈",
        "careers": [
            "🎨 화가/일러스트레이터 - 아름다운 시각 예술 창작",
            "📸 사진작가 - 특별한 순간 포착",
            "💄 메이크업 아티스트 - 아름다움 연출",
            "🌸 플로리스트 - 꽃으로 감정 표현",
            "🎵 음악가 - 감성적 음악 연주와 작곡",
            "👗 패션 디자이너 - 개성 있는 의상 디자인",
            "🍰 파티시에 - 달콤한 디저트 창작",
            "🎪 댄서/안무가 - 몸짓으로 예술 표현"
        ]
    },
    "ESTP": {
        "name": "사업가형 🎯",
        "emoji": "⚡🎪🏃‍♂️",
        "description": "활동적이고 현실적인 순발력의 왕입니다! 🔥",
        "careers": [
            "💰 영업 관리자 - 뛰어난 설득력으로 성과 달성",
            "🎬 연예인/배우 - 무대 위에서 빛나는 퍼포먼스",
            "🏃‍♂️ 체육 강사/코치 - 운동 지도와 동기 부여",
            "🚑 응급구조사 - 신속한 응급 상황 대응",
            "🏪 매장 관리자 - 활발한 고객 응대",
            "🎪 이벤트 기획자 - 역동적인 행사 기획",
            "📺 리포터 - 현장감 있는 뉴스 전달",
            "🍽️ 요리사 - 창의적이고 즉흥적인 요리"
        ]
    },
    "ESFP": {
        "name": "연예인형 🌟",
        "emoji": "🎭🎉💃",
        "description": "자유롭고 활발한 무대의 스타입니다! ✨",
        "careers": [
            "🎭 배우/연예인 - 무대와 스크린에서 빛나기",
            "🎤 가수/뮤지션 - 음악으로 감동 전달",
            "📺 방송인/MC - 활발한 진행과 소통",
            "💃 댄서/안무가 - 몸짓으로 감정 표현",
            "🎪 이벤트 기획자 - 즐거운 행사 연출",
            "✈️ 승무원 - 친근한 서비스와 소통",
            "🏨 호텔리어 - 따뜻한 환대와 서비스",
            "👶 보육교사 - 아이들과 즐거운 시간"
        ]
    }
}

# 메인 타이틀
st.markdown('<h1 class="mbti-title">🌟 MBTI 진로 탐험가 🌟</h1>', unsafe_allow_html=True)

# 인트로 메시지
st.markdown("""
<div class="personality-desc">
    <h2 style="text-align: center;">✨ 당신의 성격에 딱 맞는 꿈의 직업을 찾아보세요! ✨</h2>
    <p style="text-align: center; font-size: 1.2em;">
        🎯 16가지 MBTI 유형별로 준비된 특별한 진로 추천! 🎯<br>
        💝 당신만의 독특한 재능을 발견하고 꿈을 실현해보세요! 💝
    </p>
</div>
""", unsafe_allow_html=True)

# 사이드바
with st.sidebar:
    st.markdown("### 🎨 MBTI 선택하기 🎨")
    st.markdown("---")
    
    # MBTI 선택
    selected_mbti = st.selectbox(
        "🌈 당신의 MBTI는?",
        options=['선택해주세요'] + list(mbti_data.keys()),
        help="모르시겠다면 온라인 MBTI 테스트를 받아보세요! 🧪"
    )
    
    st.markdown("---")
    st.markdown("### 🎪 재미있는 기능들")
    
    if st.button("🎲 랜덤 MBTI 체험"):
        selected_mbti = random.choice(list(mbti_data.keys()))
        st.success(f"🎉 {selected_mbti}가 선택되었어요!")
    
    st.markdown("---")
    st.markdown("""
    ### 💡 팁
    - 🔍 각 직업을 클릭하면 더 자세한 정보를 볼 수 있어요
    - 🌟 여러 MBTI를 비교해보세요
    - 💖 친구들과 함께 해보면 더 재미있어요!
    """)

# 메인 컨텐츠
if selected_mbti != '선택해주세요':
    data = mbti_data[selected_mbti]
    
    # MBTI 타입 소개
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div class="personality-desc">
            <h2 style="text-align: center; color: #ff6b6b;">
                {data['emoji']} {selected_mbti} - {data['name']} {data['emoji']}
            </h2>
            <p style="text-align: center; font-size: 1.3em; margin-top: 20px;">
                {data['description']}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 추천 직업들
    st.markdown("## 🎯 당신에게 완벽한 직업들 🎯")
    
    # 직업을 2열로 배치
    careers = data['careers']
    col1, col2 = st.columns(2)
    
    for i, career in enumerate(careers):
        if i % 2 == 0:
            with col1:
                st.markdown(f"""
                <div class="job-item">
                    <h4>{career}</h4>
                </div>
                """, unsafe_allow_html=True)
        else:
            with col2:
                st.markdown(f"""
                <div class="job-item">
                    <h4>{career}</h4>
                </div>
                """, unsafe_allow_html=True)
    
    # 추가 정보
    st.markdown("---")
    
    # 성공 스토리 섹션
    st.markdown("### 🌟 이런 분들이 성공하고 있어요! 🌟")
    
    success_stories = {
        "INTJ": "🧠 일론 머스크 - 혁신적인 사업가로 테슬라와 스페이스X 운영",
        "INTP": "🔬 알버트 아인슈타인 - 상대성 이론으로 물리학 혁명",
        "ENTJ": "💼 스티브 잡스 - 애플을 세계 최고 기업으로 성장",
        "ENTP": "🎭 로버트 다우니 주니어 - 창의적 연기로 할리우드 스타",
        "INFJ": "✍️ J.K. 롤링 - 해리포터로 전 세계 독자들에게 감동",
        "INFP": "🎨 빈센트 반 고흐 - 감성적 작품으로 예술사에 한 획",
        "ENFJ": "🌟 오프라 윈프리 - 미디어계의 여왕으로 많은 이들에게 영감",
        "ENFP": "🎪 엘런 드제너러스 - 유머와 따뜻함으로 사랑받는 방송인",
        "ISTJ": "⚖️ 워런 버핏 - 체계적 투자로 세계 최고 부자",
        "ISFJ": "💕 마더 테레사 - 사랑과 봉사로 노벨평화상 수상",
        "ESTJ": "👔 잭 웰치 - GE를 세계적 기업으로 성장시킨 경영자",
        "ESFJ": "🤝 테일러 스위프트 - 팬들과의 소통으로 최고의 가수",
        "ISTP": "🔧 마이클 조던 - 완벽한 기술로 농구 황제",
        "ISFP": "🎨 마이클 잭슨 - 예술적 감각으로 팝의 황제",
        "ESTP": "⚡ 도널드 트럼프 - 역동적 사업가에서 대통령까지",
        "ESFP": "💃 비욘세 - 무대 위의 카리스마로 세계적 스타"
    }
    
    st.info(f"🎉 {success_stories.get(selected_mbti, '많은 성공한 분들이 있어요!')}")
    
    # 발전 팁
    st.markdown("### 💪 성장을 위한 특별한 팁들! 💪")
    
    growth_tips = {
        "INTJ": ["🎯 장기적 목표 설정하기", "📚 꾸준한 자기계발", "🤝 팀워크 스킬 향상"],
        "INTP": ["⏰ 시간 관리 능력 기르기", "🗣️ 커뮤니케이션 스킬 향상", "📋 체계적 업무 처리"],
        "ENTJ": ["❤️ 감정적 공감 능력 개발", "👂 경청하는 자세", "⚖️ 일과 휴식의 균형"],
        "ENTP": ["📝 세부사항 관리 능력", "⏳ 지속성과 끈기", "🎯 우선순위 설정"],
        "INFJ": ["💪 스트레스 관리법 익히기", "🗣️ 자신의 의견 표현하기", "🌍 현실적 관점 기르기"],
        "INFP": ["⏰ 시간 관리와 계획성", "💪 자신감 키우기", "🎯 목표 구체화하기"],
        "ENFJ": ["🛡️ 개인 경계선 설정", "😌 자기 돌봄 시간 갖기", "🎯 객관적 판단력"],
        "ENFP": ["📋 체계적 업무 처리", "⏳ 집중력 향상", "💪 끝까지 해내는 끈기"],
        "ISTJ": ["🎨 창의성 개발", "🌈 유연한 사고", "🗣️ 소통 능력 향상"],
        "ISFJ": ["💪 자기 주장 능력", "🚫 거절하는 법 배우기", "🌟 자신의 가치 인정하기"],
        "ESTJ": ["🤗 유연성과 공감 능력", "😌 스트레스 관리", "🎨 창의적 사고 개발"],
        "ESFJ": ["💪 자기 의견 표현", "🛡️ 개인 시간 확보", "🎯 객관적 결정력"],
        "ISTP": ["🗣️ 감정 표현 능력", "👥 팀워크 협력", "📅 장기 계획 수립"],
        "ISFP": ["💪 자신감 키우기", "🗣️ 의견 표현하기", "⏰ 시간 관리 능력"],
        "ESTP": ["⏳ 장기적 사고", "📚 꾸준한 학습", "💭 신중한 판단력"],
        "ESFP": ["📋 체계적 계획", "💪 집중력 향상", "🎯 목표 설정과 달성"]
    }
    
    tips = growth_tips.get(selected_mbti, ["💪 꾸준한 노력", "🌟 자기 발견", "🎯 목표 설정"])
    
    for tip in tips:
        st.markdown(f"- {tip}")
    
    # 마무리 메시지
    st.markdown("---")
    st.markdown(f"""
    <div class="personality-desc">
        <h3 style="text-align: center;">🎉 {selected_mbti} 유형의 여러분을 응원합니다! 🎉</h3>
        <p style="text-align: center; font-size: 1.1em;">
            💫 당신만의 특별한 재능으로 세상을 더 아름답게 만들어가세요! 💫<br>
            🌈 모든 꿈은 이루어질 수 있습니다! 🌈
        </p>
    </div>
    """, unsafe_allow_html=True)

else:
    # MBTI 미선택 시 안내
    st.markdown("""
    <div class="personality-desc">
        <h2 style="text-align: center;">🤔 아직 MBTI를 선택하지 않으셨네요! 🤔</h2>
        <p style="text-align: center; font-size: 1.2em;">
            👈 왼쪽 사이드바에서 당신의 MBTI를 선택해주세요!<br>
            🎯 놀라운 진로 추천이 기다리고 있어요! 🎯
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # MBTI 소개 카드들
    st.markdown("### 🌟 MBTI 유형들을 미리 둘러보세요! 🌟")
    
    # 4x4 그리드로 MBTI 타입들 표시
    mbti_types = list(mbti_data.keys())
    
    for i in range(0, 16, 4):
        cols = st.columns(4)
        for j in range(4):
            if i + j < len(mbti_types):
                mbti_type = mbti_types[i + j]
                data = mbti_data[mbti_type]
                with cols[j]:
                    st.markdown(f"""
                    <div class="career-card" style="text-align: center; min-height: 120px;">
                        <h4>{mbti_type}</h4>
                        <p style="font-size: 1.5em;">{data['emoji']}</p>
                        <p style="font-size: 0.9em;">{data['name']}</p>
                    </div>
                    """, unsafe_allow_html=True)

# 푸터
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; background: rgba(255,255,255,0.1); border-radius: 15px; margin-top: 30px;">
    <h4>🌟 MBTI 진로 탐험가와 함께 꿈을 찾아가세요! 🌟</h4>
    <p>💝 당신의 미래가 더욱 밝고 아름답기를 응원합니다! 💝</p>
    <p>🎯 Made with ❤️ by Streamlit 🎯</p>
</div>
""", unsafe_allow_html=True)

  
