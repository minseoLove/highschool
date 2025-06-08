import streamlit as st
import streamlit.components.v1

# 페이지 설정 - 반드시 첫 번째로!
st.set_page_config(
    page_title="🚨 재난 대피소 안내",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

import pandas as pd
import numpy as np
from datetime import datetime
import time

# folium 관련 패키지 선택적 import
try:
    import folium
    from streamlit_folium import folium_static
    FOLIUM_AVAILABLE = True
except ImportError:
    FOLIUM_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

# CSS 스타일링 (접근성 고려)
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
    /* 전체 앱 글씨 크기 조절 */
    .stApp {{
        font-size: {font_sizes[font_size]} !important;
    }}
    
    /* 메인 헤더 */
    .main-header {{
        font-size: calc({font_sizes[font_size]} * 2) !important;
        font-weight: bold;
        color: #DC2626;
        text-align: center;
        margin-bottom: 20px;
    }}
    
    /* 서브 헤더 */
    .stApp h1, .stApp h2, .stApp h3 {{
        font-size: calc({font_sizes[font_size]} * 1.5) !important;
    }}
    
    /* 일반 텍스트 */
    .stApp p, .stApp div, .stApp span, .stApp label {{
        font-size: {font_sizes[font_size]} !important;
    }}
    
    /* 버튼 */
    .stButton > button {{
        font-size: {font_sizes[font_size]} !important;
        padding: 10px 20px !important;
    }}
    
    /* 선택박스 */
    .stSelectbox > div > div {{
        font-size: {font_sizes[font_size]} !important;
    }}
    
    /* 입력창 */
    .stTextInput > div > div > input {{
        font-size: {font_sizes[font_size]} !important;
    }}
    
    /* 체크박스 */
    .stCheckbox > label {{
        font-size: {font_sizes[font_size]} !important;
    }}
    
    /* 탭 */
    .stTabs [data-baseweb="tab-list"] button {{
        font-size: {font_sizes[font_size]} !important;
    }}
    
    /* 확장창 */
    .streamlit-expanderHeader {{
        font-size: {font_sizes[font_size]} !important;
    }}
    
    /* 사이드바 */
    .css-1d391kg {{
        font-size: {font_sizes[font_size]} !important;
    }}
    
    /* 알림 메시지 */
    .stAlert {{
        font-size: {font_sizes[font_size]} !important;
    }}
    
    /* 성공/경고/에러 메시지 */
    .stSuccess, .stWarning, .stError, .stInfo {{
        font-size: {font_sizes[font_size]} !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 실제 조사 데이터 (전체)
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
                },
                {
                    "name": "개포중학교",
                    "address": "서울 강남구 개포로 621", 
                    "lat": 37.4816,
                    "lon": 127.0663,
                    "capacity": 800,
                    "distance": 1200,
                    "walk_time": 15,
                    "type": "야외운동장",
                    "wheelchair": True,
                    "elevator": False,
                    "parking": True,
                    "subway": "3호선 개포동역 도보 5분"
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
        },
        "해운대구": {
            "earthquake": [
                {
                    "name": "해운대해수욕장 광장",
                    "address": "부산 해운대구 우동 1394",
                    "lat": 35.1587,
                    "lon": 129.1604,
                    "capacity": 10000,
                    "distance": 400,
                    "walk_time": 5,
                    "type": "해변광장",
                    "wheelchair": True,
                    "elevator": False,
                    "parking": True,
                    "subway": "2호선 해운대역 도보 3분"
                }
            ],
            "tsunami": [
                {
                    "name": "장산 등산로 입구",
                    "address": "부산 해운대구 장산로",
                    "lat": 35.1820,
                    "lon": 129.1945,
                    "capacity": 1500,
                    "distance": 2100,
                    "walk_time": 25,
                    "type": "고지대",
                    "elevation": "해발 50m",
                    "wheelchair": False,
                    "elevator": False,
                    "parking": True,
                    "subway": "2호선 장산역 도보 15분"
                },
                {
                    "name": "달맞이길 공원",
                    "address": "부산 해운대구 달맞이길",
                    "lat": 35.1535,
                    "lon": 129.1732,
                    "capacity": 800,
                    "distance": 1800,
                    "walk_time": 22,
                    "type": "고지대 공원",
                    "elevation": "해발 30m",
                    "wheelchair": False,
                    "elevator": False,
                    "parking": True,
                    "subway": "2호선 해운대역 도보 20분"
                }
            ]
        },
        "대구중구": {
            "earthquake": [
                {
                    "name": "국채보상운동기념공원",
                    "address": "대구 중구 공평로 30",
                    "lat": 35.8682,
                    "lon": 128.5953,
                    "capacity": 3000,
                    "distance": 500,
                    "walk_time": 6,
                    "type": "공원",
                    "wheelchair": True,
                    "elevator": False,
                    "parking": True,
                    "subway": "1호선 중앙로역 도보 5분"
                }
            ]
        }
    }

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
        },
        {
            "name": "인제대학교 해운대백병원",
            "address": "부산 해운대구 해운대로 875",
            "phone": "051-797-0369",
            "lat": 35.1581,
            "lon": 129.1754,
            "distance": 800,
            "emergency_24": True, 
            "beds": 1000,
            "subway": "부산지하철 2호선 해운대역 도보 8분",
            "specialties": ["응급의학과", "외상센터"],
            "region": "해운대구"
        },
        {
            "name": "대구가톨릭대학교병원",
            "address": "대구 남구 두류공원로 17길 33",
            "phone": "053-650-4114",
            "lat": 35.8469,
            "lon": 128.5650,
            "distance": 1200,
            "emergency_24": True,
            "beds": 1500,
            "subway": "2호선 두류역 도보 10분",
            "specialties": ["응급의학과", "외상센터", "심혈관센터"],
            "region": "대구중구"
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

# 메인 앱
def main():
    if not FOLIUM_AVAILABLE:
        st.warning("🗺️ 지도 기능을 위해 다음 명령어를 실행해주세요: pip install folium streamlit-folium")
    
    # 세션 상태 초기화
    if 'font_size' not in st.session_state:
        st.session_state.font_size = '보통'
    if 'voice_enabled' not in st.session_state:
        st.session_state.voice_enabled = False
    if 'high_contrast' not in st.session_state:
        st.session_state.high_contrast = False
    
    # CSS 로드 (글씨 크기 반영)
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
            index=["소형", "보통", "대형", "특대"].index(st.session_state.font_size),
            help="화면의 모든 글씨 크기가 변경됩니다."
        )
        
        # 글씨 크기가 변경되면 즉시 적용
        if font_size != st.session_state.font_size:
            st.session_state.font_size = font_size
            st.rerun()  # 페이지 새로고침하여 CSS 재적용
        
        # 실시간 글씨 크기 미리보기 (각 크기별로 실제 크기 표시)
        st.markdown("**📝 글씨 크기 미리보기:**")
        st.markdown(f"""
        <div style="border: 2px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 10px; background-color: #f8f9fa;">
        <p style="font-size: 14px !important; margin: 8px 0; color: {'#DC2626' if font_size == '소형' else '#666'}; line-height: 1.2;">
        {'🔴 ' if font_size == '소형' else '⚪ '}소형: 안전한 대피를 위해
        </p>
        <p style="font-size: 18px !important; margin: 10px 0; color: {'#DC2626' if font_size == '보통' else '#666'}; line-height: 1.3;">
        {'🔴 ' if font_size == '보통' else '⚪ '}보통: 안전한 대피를 위해
        </p>
        <p style="font-size: 22px !important; margin: 12px 0; color: {'#DC2626' if font_size == '대형' else '#666'}; line-height: 1.4;">
        {'🔴 ' if font_size == '대형' else '⚪ '}대형: 안전한 대피를 위해
        </p>
        <p style="font-size: 28px !important; margin: 15px 0; color: {'#DC2626' if font_size == '특대' else '#666'}; line-height: 1.5; font-weight: bold;">
        {'🔴 ' if font_size == '특대' else '⚪ '}특대: 안전한 대피를 위해
        </p>
        <hr style="margin: 15px 0; border: 1px solid #ddd;">
        <p style="color: #DC2626; font-weight: bold; font-size: 16px !important; text-align: center; background-color: #FEF2F2; padding: 10px; border-radius: 5px;">
        ✅ 현재 선택: {font_size}
        </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 음성 안내
        voice_enabled = st.checkbox("🔊 음성 안내 활성화", value=st.session_state.voice_enabled)
        st.session_state.voice_enabled = voice_enabled
        
        if voice_enabled and st.button("🔊 음성 테스트"):
            speak_text("음성 안내 시스템이 정상 작동합니다. 현재 글씨 크기는 " + font_size + "입니다.")
        
        st.markdown("---")
        
        # 고대비 모드
        high_contrast = st.checkbox("🌓 고대비 모드", value=st.session_state.high_contrast)
        st.session_state.high_contrast = high_contrast
        
        if high_contrast:
            st.markdown("""
            <style>
            /* 고대비 모드 - 검정 배경 + 흰 글씨 */
            .stApp {
                background-color: #000000 !important;
                color: #FFFFFF !important;
            }
            
            .stApp .main {
                background-color: #000000 !important;
                color: #FFFFFF !important;
            }
            
            .stApp div, .stApp p, .stApp span, .stApp h1, .stApp h2, .stApp h3 {
                background-color: #000000 !important;
                color: #FFFFFF !important;
            }
            
            /* 사이드바도 고대비 */
            .css-1d391kg {
                background-color: #1a1a1a !important;
                color: #FFFFFF !important;
            }
            
            /* 버튼 고대비 */
            .stButton > button {
                background-color: #333333 !important;
                color: #FFFFFF !important;
                border: 2px solid #FFFFFF !important;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # 고대비 모드 상태 표시
            st.success("🌓 고대비 모드가 활성화되었습니다!")
        
        # 애니메이션 줄이기
        reduce_motion = st.checkbox("🚫 애니메이션 줄이기", value=st.session_state.get('reduce_motion', False))
        st.session_state.reduce_motion = reduce_motion
        
        if reduce_motion:
            st.markdown("""
            <style>
            /* 모든 애니메이션과 전환 효과 제거 */
            *, *::before, *::after {
                animation-duration: 0s !important;
                animation-delay: 0s !important;
                transition-duration: 0s !important;
                transition-delay: 0s !important;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # 애니메이션 줄이기 상태 표시
            st.success("🚫 애니메이션이 모두 비활성화되었습니다!")
    
    # 메인 탭들
    tab1, tab2, tab3 = st.tabs(["🏠 대피소 찾기", "🏥 응급의료시설", "📚 재난 행동요령"])
    
    with tab1:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📍 개인정보 입력")
            
            location = st.selectbox("현재 위치를 선택하세요", 
                                  ["", "강남구", "해운대구", "대구중구"])
            
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
                "홍수/태풍": {"icon": "🌊", "description": "견고한 건물로 대피"},
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
                        "홍수/태풍": "flood", 
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
                                    
                                    if 'elevation' in shelter:
                                        st.write(f"**⛰️ 고도:** {shelter['elevation']}")
                                
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
                        
                        # 지역별 사용 가능한 재난 타입 안내
                        available_disasters = list(shelter_data.get(location, {}).keys())
                        if available_disasters:
                            disaster_names = {
                                "earthquake": "지진",
                                "flood": "홍수/태풍", 
                                "war": "전쟁/테러",
                                "tsunami": "지진해일"
                            }
                            available_list = [disaster_names.get(d, d) for d in available_disasters]
                            st.info(f"💡 {location}에서 사용 가능한 재난 타입: {', '.join(available_list)}")
            
            if guardian_phone:
                st.markdown("---")
                if st.button("📞 보호자 긴급연락"):
                    st.success(f"✅ {guardian_phone}로 긴급 메시지가 발송되었습니다!")
                    speak_text("보호자에게 긴급 연락을 발송했습니다.")
    
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
        
        disaster_guides = {
            "지진": {
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
            "화재": {
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
        
        for disaster, guide in disaster_guides.items():
            with st.expander(f"🚨 {disaster} 발생 시", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**⚡ 즉시 행동**")
                    for action in guide["immediate"]:
                        st.write(action)
                
                with col2:
                    st.write("**🏃‍♂️ 대피 행동**")
                    for action in guide["evacuation"]:
                        st.write(action)
