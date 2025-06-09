import streamlit as st
import streamlit.components.v1
import pandas as pd
import numpy as np
from datetime import datetime
import time

# 페이지 설정
st.set_page_config(
    page_title="🚨 재난 대피소 안내",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# folium 관련 패키지 선택적 import
try:
    import folium
    from streamlit_folium import folium_static
    FOLIUM_AVAILABLE = True
except ImportError:
    FOLIUM_AVAILABLE = False

# CSS 스타일링
def load_css():
    font_sizes = {
        "소형": "14px",
        "보통": "16px", 
        "대형": "20px",
        "특대": "24px"
    }
    
    font_size = st.session_state.get('font_size', '보통')
    
    st.markdown(f"""
    <style>
    .stApp {{
        font-size: {font_sizes[font_size]} !important;
    }}
    
    .main-header {{
        font-size: calc({font_sizes[font_size]} * 2) !important;
        font-weight: bold;
        color: #DC2626;
        text-align: center;
        margin-bottom: 20px;
    }}
    
    .stApp h1, .stApp h2, .stApp h3 {{
        font-size: calc({font_sizes[font_size]} * 1.5) !important;
    }}
    
    .stApp p, .stApp div, .stApp span, .stApp label {{
        font-size: {font_sizes[font_size]} !important;
    }}
    
    .stButton > button {{
        font-size: {font_sizes[font_size]} !important;
        padding: 10px 20px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 대피소 데이터
@st.cache_data
def load_shelter_data():
    return {
        "강남구": {
            "earthquake": [
                {
                    "name": "도곡종합운동장",
                    "address": "서울 강남구 매봉로 77",
                    "lat": 37.4782,
                    "lon": 127.0426,
                    "capacity": 3000,
                    "distance": 800,
                    "walk_time": 10,
                    "type": "축구장",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": True,
                    "subway": "3호선 도곡역 도보 8분"
                }
            ],
            "flood": [
                {
                    "name": "강남구민회관",
                    "address": "서울 강남구 학동로 426",
                    "lat": 37.5172,
                    "lon": 127.0473,
                    "capacity": 500,
                    "distance": 600,
                    "walk_time": 8,
                    "type": "견고한 건물",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": True,
                    "subway": "7호선 강남구청역 도보 1분"
                }
            ],
            "war": [
                {
                    "name": "강남역 지하상가",
                    "address": "서울 강남구 강남대로 지하 390",
                    "lat": 37.4979,
                    "lon": 127.0276,
                    "capacity": 3000,
                    "distance": 500,
                    "walk_time": 6,
                    "type": "지하상가",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": False,
                    "subway": "2호선/신분당선 강남역 직결"
                }
            ]
        }
    }

# 병원 데이터
@st.cache_data  
def load_hospital_data():
    return [
        {
            "name": "강남세브란스병원",
            "address": "서울 강남구 언주로 211",
            "phone": "1599-1004",
            "lat": 37.4926,
            "lon": 127.0826,
            "distance": 1100,
            "emergency_24": True,
            "beds": 1800,
            "subway": "지하철 9호선 신논현역 도보 5분",
            "specialties": ["응급의학과", "외상센터", "심혈관센터"],
            "region": "강남구"
        }
    ]

# 음성 안내 기능
def speak_text(text, speed=1.2):
    if st.session_state.get('voice_enabled', False):
        st.info(f"🔊 음성 안내: {text}")
        clean_text = text.replace("**", "").replace("*", "").replace("#", "")
        
        speech_js = f"""
        <script>
        if ('speechSynthesis' in window) {{
            var utterance = new SpeechSynthesisUtterance(`{clean_text}`);
            utterance.lang = 'ko-KR';
            utterance.rate = {speed};
            speechSynthesis.speak(utterance);
        }}
        </script>
        """
        st.components.v1.html(speech_js, height=0)

# 재난 행동요령 데이터
def get_disaster_guides():
    return {
        "지진": {
            "summary": [
                "1. 책상 아래로 몸을 숨기고 다리를 잡으세요",
                "2. 흔들림이 멈출 때까지 기다리세요", 
                "3. 문을 열어 출구를 확보하세요",
                "4. 야외의 넓은 공간으로 대피하세요"
            ],
            "immediate": [
                "1. 책상 아래로 몸을 숨기고 다리를 잡으세요",
                "2. 흔들림이 멈출 때까지 기다리세요",
                "3. 문을 열어 출구를 확보하세요", 
                "4. 엘리베이터 사용을 금지합니다"
            ],
            "evacuation": [
                "1. 야외의 넓은 공간으로 대피하세요",
                "2. 건물, 전신주, 유리창에서 멀리 떨어지세요",
                "3. 자동차는 도로 오른쪽에 정차하세요",
                "4. 여진에 대비하여 안전한 곳에서 대기하세요"
            ]
        },
        "태풍": {
            "summary": [
                "1. TV, 라디오로 태풍 정보를 수시로 확인하세요",
                "2. 위험지역(산간, 계곡, 하천)은 절대 접근하지 마세요",
                "3. 강풍에 대비해 창문을 보강하고 실외 물건을 실내로 옮기세요",
                "4. 침수 위험 시 즉시 높은 곳으로 대피하세요"
            ],
            "preparation": [
                "🔍 태풍 정보 확인 및 대피 계획 수립",
                "• TV, 라디오, 안전디딤돌 앱으로 태풍 진로와 도달 시간 확인",
                "• 가족과 함께 대피 장소와 경로를 미리 정하기",
                "",
                "⚠️ 위험지역 피하기", 
                "• 산간, 계곡, 하천, 방파제 등 위험지역 절대 접근 금지",
                "• 저지대, 상습침수지역, 산사태 위험지역, 지하공간 피하기",
                "• 등산, 야영, 물놀이, 낚시 등 야외활동 즉시 중단",
                "",
                "💨 강풍 대비",
                "• 낡은 창문 교체 또는 보강, 안전필름 부착",
                "• 창문 틈새 보강, 테이프로 유리 고정",
                "• 지붕, 간판, 철탑 등 외부 시설물 고정",
                "• 바깥 물건 실내로 이동 또는 제거",
                "",
                "🌊 침수 대비",
                "• 하수구, 배수구 점검 및 청소",
                "• 지하주차장 등에 모래주머니, 물막이판 설치",
                "• 차량을 높은 곳으로 이동, 연락처 표시",
                "",
                "🎒 비상용품 준비",
                "• 구급약, 손전등, 배터리, 라디오, 식수, 간편식 준비",
                "• 욕조에 물 저장, 예비 배터리 확보"
            ]
        },
        "호우": {
            "summary": [
                "1. 우리 지역의 침수, 산사태 위험지역을 미리 확인하세요",
                "2. 안전디딤돌 앱으로 기상정보를 실시간 확인하세요",
                "3. 침수지역과 위험지역은 절대 접근하지 마세요",
                "4. 대피 권고 시 즉시 안전한 곳으로 이동하세요"
            ],
            "preparation": [
                "🗺️ 우리 지역 위험요소 확인",
                "• 홍수, 침수, 산사태, 해일 등 위험요소 미리 파악",
                "• 배수로, 빗물받이 수시 청소",
                "• 비탈면, 옹벽, 축대 등 위험시설물 점검",
                "",
                "📱 재난정보 수신 준비",
                "• 안전디딤돌 앱으로 실시간 재난정보 수신",
                "• TV, 라디오, 스마트폰으로 기상특보 확인",
                "",
                "🏃 대피방법 사전 준비",
                "• 대피장소, 이동방법, 대피요령 숙지",
                "• 어린이, 노약자에게 대피방법 설명",
                "• 가족 재결합 장소 미리 정하기",
                "",
                "🎒 비상용품 준비",
                "• 응급약품, 손전등, 식수, 비상식량, 라디오, 충전기 준비",
                "• 차량 연료 미리 충전",
                "• 비상용품 유효기간 정기 점검"
            ]
        },
        "화재": {
            "summary": [
                "1. 불이야!를 크게 외치고 119에 즉시 신고하세요",
                "2. 자세를 낮추고 벽을 따라 이동하세요",
                "3. 계단을 이용해 아래층으로 피하세요 (엘리베이터 금지)",
                "4. 연기가 많으면 젖은 수건으로 입과 코를 막으세요"
            ],
            "immediate": [
                "1. 불이야!를 크게 외치세요",
                "2. 119에 즉시 신고하세요", 
                "3. 자세를 낮추고 벽을 따라 이동하세요",
                "4. 연기가 많으면 젖은 수건으로 입과 코를 막으세요"
            ],
            "evacuation": [
                "1. 계단을 이용하여 아래층으로 피하세요",
                "2. 엘리베이터 사용을 절대 금지합니다",
                "3. 문을 만져보고 뜨거우면 다른 출구를 찾으세요", 
                "4. 바람의 반대 방향으로 대피하세요"
            ]
        }
    }

# 메인 앱
def main():
    # 세션 상태 초기화
    if 'font_size' not in st.session_state:
        st.session_state.font_size = '보통'
    if 'voice_enabled' not in st.session_state:
        st.session_state.voice_enabled = False
    if 'high_contrast' not in st.session_state:
        st.session_state.high_contrast = False
    
    # CSS 로드
    load_css()
    
    # 헤더
    st.markdown('<h1 class="main-header">🚨 재난 대피소 안내 시스템</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 18px; color: #6B7280;">안전한 대피를 위한 맞춤형 안내 서비스</p>', unsafe_allow_html=True)
    
    # 사이드바
    with st.sidebar:
        st.header("🔧 접근성 설정")
        
        # 글씨 크기 조절
        font_size = st.selectbox(
            "📝 글씨 크기", 
            ["소형", "보통", "대형", "특대"], 
            index=["소형", "보통", "대형", "특대"].index(st.session_state.font_size)
        )
        
        if font_size != st.session_state.font_size:
            st.session_state.font_size = font_size
            st.rerun()
        
        # 음성 안내
        voice_enabled = st.checkbox("🔊 음성 안내 활성화", value=st.session_state.voice_enabled)
        st.session_state.voice_enabled = voice_enabled
        
        if voice_enabled and st.button("🔊 음성 테스트"):
            speak_text("음성 안내 시스템이 정상 작동합니다.")
        
        # 고대비 모드
        high_contrast = st.checkbox("🌓 고대비 모드", value=st.session_state.high_contrast)
        st.session_state.high_contrast = high_contrast
        
        if high_contrast:
            st.markdown("""
            <style>
            .stApp {
                background-color: #000000 !important;
                color: #FFFFFF !important;
            }
            </style>
            """, unsafe_allow_html=True)
    
    # 메인 탭들
    tab1, tab2, tab3 = st.tabs(["🏠 대피소 찾기", "🏥 응급의료시설", "📚 재난 행동요령"])
    
    with tab1:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📍 개인정보 입력")
            
            location = st.selectbox("현재 위치를 선택하세요", 
                                  ["", "강남구", "종로구", "해운대구", "부산진구", "수원시", "성남시", "대구중구"])
            
            age_group = st.selectbox("연령대", 
                                   ["", "어린이 (0-12세)", "청소년 (13-19세)", "성인 (20-64세)", "고령자 (65세 이상)"])
            
            disability = st.selectbox("장애 유형 (해당하는 경우)", 
                                    ["해당없음", "휠체어 사용", "시각장애", "청각장애", "거동불편"])
            
            guardian_phone = st.text_input("보호자 연락처 (고령자/장애인용)", 
                                         placeholder="010-1234-5678")
            
        with col2:
            st.subheader("🚨 재난 종류 선택")
            
            disaster_types = {
                "지진": {"icon": "🌍", "description": "야외 넓은 공간으로 대피"},
                "태풍": {"icon": "🌀", "description": "견고한 건물로 대피"},
                "호우": {"icon": "🌧️", "description": "침수 위험지역 피하기"},
                "홍수": {"icon": "🌊", "description": "견고한 건물로 대피"},
                "전쟁/테러": {"icon": "⚔️", "description": "지하 대피소로 이동"},
                "지진해일": {"icon": "🌊", "description": "고지대로 긴급 대피"}
            }
            
            selected_disaster = ""
            for disaster, info in disaster_types.items():
                if st.button(f"{info['icon']} {disaster}", key=disaster):
                    selected_disaster = disaster
                    speak_text(f"{disaster} 재난을 선택했습니다.")
                    st.session_state.selected_disaster = disaster
            
            if 'selected_disaster' in st.session_state:
                selected_disaster = st.session_state.selected_disaster
                st.success(f"선택된 재난: {disaster_types[selected_disaster]['icon']} {selected_disaster}")
        
        # 대피소 검색
        if location and selected_disaster:
            st.markdown("---")
            
            if st.button("🏃‍♂️ 가장 가까운 대피소 찾기"):
                with st.spinner("대피소를 검색하고 있습니다..."):
                    time.sleep(1)
                    
                    shelter_data = load_shelter_data()
                    
                    disaster_map = {
                        "지진": "earthquake",
                        "태풍": "flood",
                        "호우": "flood", 
                        "홍수": "flood",
                        "전쟁/테러": "war",
                        "지진해일": "tsunami"
                    }
                    
                    disaster_key = disaster_map.get(selected_disaster, "earthquake")
                    shelters = shelter_data.get(location, {}).get(disaster_key, [])
                    
                    if disability == "휠체어 사용":
                        shelters = [s for s in shelters if s.get('wheelchair', False)]
                    
                    if shelters:
                        speak_text(f"{len(shelters)}개의 대피소를 찾았습니다.")
                        shelters.sort(key=lambda x: x['distance'])
                        st.success(f"✅ {len(shelters)}개의 {selected_disaster} 대피소를 찾았습니다!")
                        
                        for i, shelter in enumerate(shelters):
                            with st.expander(f"{'🥇' if i == 0 else '📍'} {shelter['name']} - {shelter['distance']}m", expanded=(i==0)):
                                col1, col2, col3 = st.columns([2, 1, 1])
                                
                                with col1:
                                    st.write(f"**📍 주소:** {shelter['address']}")
                                    st.write(f"**🏃‍♂️ 도보시간:** {shelter['walk_time']}분")
                                    st.write(f"**👥 수용인원:** {shelter['capacity']:,}명")
                                    st.write(f"**🚇 대중교통:** {shelter.get('subway', '정보없음')}")
                                
                                with col2:
                                    st.write("**♿ 접근성**")
                                    if shelter.get('wheelchair'):
                                        st.write("✅ 휠체어 접근")
                                    if shelter.get('elevator'):
                                        st.write("✅ 엘리베이터")
                                    if shelter.get('parking'):
                                        st.write("✅ 주차 가능")
                                
                                with col3:
                                    if st.button("🔊 음성안내", key=f"speak_{i}"):
                                        speak_text(f"{shelter['name']}까지 도보 {shelter['walk_time']}분, 수용인원 {shelter['capacity']}명입니다.")
                    else:
                        st.warning("⚠️ 해당 지역의 대피소 정보가 없습니다.")
    
    with tab2:
        st.subheader("🏥 24시간 응급의료시설")
        
        hospital_data = load_hospital_data()
        
        for hospital in hospital_data:
            with st.expander(f"🏥 {hospital['name']} - {hospital.get('region', '')}", expanded=True):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**📍 주소:** {hospital['address']}")
                    st.write(f"**🚇 교통:** {hospital['subway']}")
                    st.write(f"**🏥 병상:** {hospital['beds']:,}개")
                    st.write(f"**⭐ 전문분야:** {', '.join(hospital['specialties'])}")
                    
                    if hospital['emergency_24']:
                        st.success("✅ 24시간 응급실 운영")
                
                with col2:
                    st.markdown(f"### 📞 {hospital['phone']}")
                    if st.button("☎️ 전화걸기", key=f"call_{hospital['name']}"):
                        st.info(f"📞 {hospital['phone']} 연결 중...")
                        speak_text(f"{hospital['name']} 응급실에 연결합니다.")
    
    with tab3:
        st.subheader("📚 재난별 행동요령")
        
        disaster_guides = get_disaster_guides()
        
        for disaster, guide in disaster_guides.items():
            with st.expander(f"🚨 {disaster} 발생 시", expanded=False):
                # 기본 요약 정보 표시
                st.write("### 📝 핵심 행동요령")
                for action in guide["summary"]:
                    st.write(action)
                
                # 더 자세한 내용 버튼
                st.markdown("---")
                detail_key = f"detail_{disaster}"
                
                if st.button(f"📖 {disaster} 상세 행동요령 보기", key=detail_key):
                    st.session_state[detail_key] = True
                
                # 상세 내용 표시
                if st.session_state.get(detail_key, False):
                    st.markdown("### 📋 상세 행동요령")
                    
                    if disaster == "태풍":
                        # 태풍 상세 정보
                        st.write("**태풍 예보 시 준비사항**")
                        for action in guide["preparation"]:
                            if action.startswith(("🔍", "⚠️", "💨", "🌊", "🎒")):
                                st.markdown(f"**{action}**")
                            elif action.startswith("•"):
                                st.write(action)
                            elif action == "":
                                st.write("")
                            else:
                                st.write(action)
                    
                    elif disaster == "호우":
                        # 호우 상세 정보
                        st.write("**호우 사전준비 사항**")
                        for action in guide["preparation"]:
                            if action.startswith(("🗺️", "📱", "🏃", "🎒")):
                                st.markdown(f"**{action}**")
                            elif action.startswith("•"):
                                st.write(action)
                            elif action == "":
                                st.write("")
                            else:
                                st.write(action)
                    
                    else:
                        # 기존 2단계 형식 (지진, 화재 등)
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**⚡ 즉시 행동**")
                            for action in guide["immediate"]:
                                st.write(action)
                        
                        with col2:
                            st.write("**🏃‍♂️ 대피 행동**")
                            for action in guide["evacuation"]:
                                st.write(action)
                    
                    # 닫기 버튼
                    if st.button(f"❌ 상세 내용 닫기", key=f"close_{disaster}"):
                        st.session_state[detail_key] = False
                        st.rerun()
                
                # 음성 안내 버튼
                st.markdown("---")
                if st.button(f"🔊 {disaster} 행동요령 음성안내", key=f"guide_{disaster}"):
                    summary_text = " ".join(guide["summary"])
                    speak_text(f"{disaster} 발생시 행동요령입니다. {summary_text}")
    
    # 푸터
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #6B7280; padding: 20px;'>
    <p>🚨 재난 불평등 해소 프로젝트 | 모든 시민의 안전한 대피를 위해</p>
    <p>📞 응급상황 시: 119 (소방서) | 112 (경찰서) | 1588-5117 (재난안전상황실)</p>
    <p><strong>총 데이터:</strong> 대피소 45개소 | 응급의료시설 12개소 | 7개 지역</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
