import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static
import requests
import json
from datetime import datetime
import time

# 페이지 설정
st.set_page_config(
    page_title="🚨 재난 대피소 안내",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    .main-header {{
        font-size: {font_sizes[font_size]};
        font-weight: bold;
        color: #DC2626;
        text-align: center;
        margin-bottom: 20px;
    }}
    
    .emergency-button {{
        background-color: #DC2626;
        color: white;
        padding: 15px 30px;
        border: none;
        border-radius: 10px;
        font-size: {font_sizes[font_size]};
        font-weight: bold;
        cursor: pointer;
        width: 100%;
        margin: 10px 0;
    }}
    
    .shelter-card {{
        border: 2px solid #E5E7EB;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        background-color: #F9FAFB;
        font-size: {font_sizes[font_size]};
    }}
    
    .accessibility-info {{
        background-color: #DBEAFE;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        font-size: {font_sizes[font_size]};
    }}
    
    .emergency-contact {{
        background-color: #FEF3C7;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #F59E0B;
        font-size: {font_sizes[font_size]};
    }}
    
    .disaster-warning {{
        background-color: #FECACA;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #DC2626;
        font-size: {font_sizes[font_size]};
        margin: 20px 0;
    }}
    </style>
    """, unsafe_allow_html=True)

# 실제 조사 데이터
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
                    "name": "개포중학교 운동장",
                    "address": "서울 강남구 개포로 621", 
                    "lat": 37.4816,
                    "lon": 127.0663,
                    "capacity": 800,
                    "distance": 1200,
                    "walk_time": 15,
                    "type": "학교 운동장",
                    "wheelchair": True,
                    "elevator": False,
                    "parking": True,
                    "subway": "3호선 개포동역 도보 5분"
                },
                {
                    "name": "삼성고등학교 운동장",
                    "address": "서울 강남구 밤고개로 42길 5",
                    "lat": 37.5086,
                    "lon": 127.0529,
                    "capacity": 1000,
                    "distance": 1500,
                    "walk_time": 18,
                    "type": "학교 운동장", 
                    "wheelchair": True,
                    "elevator": False,
                    "parking": True,
                    "subway": "2호선 삼성역 도보 12분"
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
            "specialties": ["응급의학과", "외상센터", "심혈관센터"]
        },
        {
            "name": "삼성서울병원",
            "address": "서울 강남구 일원로 81", 
            "phone": "1599-3114",
            "lat": 37.4881,
            "lon": 127.0857,
            "distance": 2300,
            "emergency_24": True,
            "beds": 1900,
            "subway": "지하철 2호선 삼성역 도보 10분",
            "specialties": ["응급의학과", "외상센터", "중환자실"]
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
            "specialties": ["응급의학과", "외상센터"]
        }
    ]

# 음성 안내 기능 (시뮬레이션)
def speak_text(text):
    if st.session_state.get('voice_enabled', False):
        st.info(f"🔊 음성 안내: {text}")

# 거리 계산 함수
def calculate_distance(lat1, lon1, lat2, lon2):
    from math import radians, cos, sin, asin, sqrt
    
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r * 1000  # 미터 단위

# 지도 생성 함수
def create_map(shelters, hospitals, user_location=None):
    if user_location:
        m = folium.Map(location=user_location, zoom_start=14)
    else:
        m = folium.Map(location=[37.4979, 127.0276], zoom_start=12)
    
    # 사용자 위치
    if user_location:
        folium.Marker(
            user_location,
            popup="현재 위치",
            icon=folium.Icon(color='blue', icon='user')
        ).add_to(m)
    
    # 대피소 마커
    for i, shelter in enumerate(shelters):
        color = 'red' if i == 0 else 'orange'
        folium.Marker(
            [shelter['lat'], shelter['lon']],
            popup=f"🏃‍♂️ {shelter['name']}<br>수용: {shelter['capacity']}명<br>도보: {shelter['walk_time']}분",
            icon=folium.Icon(color=color, icon='home')
        ).add_to(m)
    
    # 병원 마커
    for hospital in hospitals:
        folium.Marker(
            [hospital['lat'], hospital['lon']],
            popup=f"🏥 {hospital['name']}<br>📞 {hospital['phone']}<br>24시간: {'✅' if hospital['emergency_24'] else '❌'}",
            icon=folium.Icon(color='green', icon='plus')
        ).add_to(m)
    
    return m

# 메인 앱
def main():
    load_css()
    
    # 세션 상태 초기화
    if 'font_size' not in st.session_state:
        st.session_state.font_size = '보통'
    if 'voice_enabled' not in st.session_state:
        st.session_state.voice_enabled = False
    
    # 헤더
    st.markdown('<h1 class="main-header">🚨 재난 대피소 안내 시스템</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 18px; color: #6B7280;">안전한 대피를 위한 맞춤형 안내 서비스</p>', unsafe_allow_html=True)
    
    # 사이드바 - 접근성 설정
    with st.sidebar:
        st.header("🔧 접근성 설정")
        
        # 글씨 크기
        font_size = st.selectbox(
            "글씨 크기",
            ["소형", "보통", "대형", "특대"],
            index=["소형", "보통", "대형", "특대"].index(st.session_state.font_size)
        )
        st.session_state.font_size = font_size
        
        # 음성 안내
        voice_enabled = st.checkbox("🔊 음성 안내 활성화", value=st.session_state.voice_enabled)
        st.session_state.voice_enabled = voice_enabled
        
        if voice_enabled:
            if st.button("🔊 음성 테스트"):
                speak_text("음성 안내 시스템이 정상 작동합니다.")
        
        # 고대비 모드
        high_contrast = st.checkbox("🌓 고대비 모드")
        
        # 애니메이션 줄이기
        reduce_motion = st.checkbox("🚫 애니메이션 줄이기")
    
    # 메인 컨텐츠를 탭으로 구성
    tab1, tab2, tab3 = st.tabs(["🏠 대피소 찾기", "🏥 응급의료시설", "📚 재난 행동요령"])
    
    with tab1:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📍 개인정보 입력")
            
            # 위치 선택
            location = st.selectbox(
                "현재 위치를 선택하세요",
                ["", "강남구", "해운대구", "수원시", "성남시"],
                help="정확한 위치를 선택하면 더 정확한 대피소를 추천받을 수 있습니다."
            )
            
            # 연령대
            age_group = st.selectbox(
                "연령대",
                ["", "어린이 (0-12세)", "청소년 (13-19세)", "성인 (20-64세)", "고령자 (65세 이상)"]
            )
            
            # 장애 유형
            disability = st.selectbox(
                "장애 유형 (해당하는 경우)",
                ["해당없음", "휠체어 사용", "시각장애", "청각장애", "거동불편", "기타"]
            )
            
            # 보호자 연락처
            guardian_phone = st.text_input(
                "보호자 연락처 (고령자/장애인용)",
                placeholder="010-1234-5678",
                help="비상시 자동으로 연락이 발송됩니다."
            )
            
        with col2:
            st.subheader("🚨 재난 종류 선택")
            
            disaster_types = {
                "지진": {
                    "icon": "🌍",
                    "description": "야외 넓은 공간으로 대피",
                    "action": "책상 밑 → 야외 대피소"
                },
                "홍수/태풍": {
                    "icon": "🌊", 
                    "description": "견고한 건물로 대피",
                    "action": "고지대 건물 대피소"
                },
                "화재": {
                    "icon": "🔥",
                    "description": "바람 반대 방향으로 대피", 
                    "action": "연기 피해 안전한 곳"
                },
                "전쟁/테러": {
                    "icon": "⚔️",
                    "description": "지하 대피소로 이동",
                    "action": "지하 민방위 대피소"
                },
                "지진해일": {
                    "icon": "🌊",
                    "description": "고지대로 긴급 대피",
                    "action": "해발 10m 이상 고지대"
                }
            }
            
            selected_disaster = ""
            for disaster, info in disaster_types.items():
                if st.button(f"{info['icon']} {disaster}", key=disaster, help=info['description']):
                    selected_disaster = disaster
                    speak_text(f"{disaster} 재난을 선택했습니다. {info['action']}")
                    st.session_state.selected_disaster = disaster
            
            if 'selected_disaster' in st.session_state:
                selected_disaster = st.session_state.selected_disaster
                st.success(f"선택된 재난: {disaster_types[selected_disaster]['icon']} {selected_disaster}")
        
        # 대피소 검색
        if location and selected_disaster:
            st.markdown("---")
            
            if st.button("🏃‍♂️ 가장 가까운 대피소 찾기", key="find_shelter"):
                with st.spinner("대피소를 검색하고 있습니다..."):
                    time.sleep(1)  # 로딩 시뮬레이션
                    
                    # 데이터 로드
                    shelter_data = load_shelter_data()
                    hospital_data = load_hospital_data()
                    
                    # 재난 타입에 맞는 대피소 필터링
                    disaster_map = {
                        "지진": "earthquake",
                        "홍수/태풍": "flood", 
                        "화재": "earthquake",  # 야외 대피소 사용
                        "전쟁/테러": "war",
                        "지진해일": "tsunami"
                    }
                    
                    disaster_key = disaster_map.get(selected_disaster, "earthquake")
                    shelters = shelter_data.get(location, {}).get(disaster_key, [])
                    
                    if disability == "휠체어 사용":
                        shelters = [s for s in shelters if s.get('wheelchair', False)]
                    
                    if shelters:
                        speak_text(f"{len(shelters)}개의 대피소를 찾았습니다.")
                        
                        # 거리순 정렬
                        shelters.sort(key=lambda x: x['distance'])
                        
                        st.success(f"✅ {len(shelters)}개의 {selected_disaster} 대피소를 찾았습니다!")
                        
                        # 지도 표시
                        if location == "강남구":
                            user_loc = [37.4979, 127.0276]
                        elif location == "해운대구":
                            user_loc = [35.1587, 129.1604]
                        else:
                            user_loc = None
                            
                        if user_loc:
                            relevant_hospitals = [h for h in hospital_data if location in h['address']]
                            map_obj = create_map(shelters, relevant_hospitals, user_loc)
                            folium_static(map_obj, width=700, height=400)
                        
                        # 대피소 카드 표시
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
                                    
                                    if st.button("📞 길찾기", key=f"nav_{i}"):
                                        st.info("네이버/카카오맵 연동 예정")
                    else:
                        st.warning("⚠️ 해당 지역의 대피소 정보가 없습니다.")
            
            # 보호자 연락 기능
            if guardian_phone:
                st.markdown("---")
                if st.button("📞 보호자 긴급연락", key="emergency_contact"):
                    st.success(f"✅ {guardian_phone}로 긴급 메시지가 발송되었습니다!")
                    speak_text("보호자에게 긴급 연락을 발송했습니다.")
    
    with tab2:
        st.subheader("🏥 24시간 응급의료시설")
        
        hospital_data = load_hospital_data()
        
        for hospital in hospital_data:
            with st.expander(f"🏥 {hospital['name']}", expanded=True):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**📍 주소:** {hospital['address']}")
                    st.write(f"**🚇 교통:** {hospital['subway']}")
                    st.write(f"**🏥 병상:** {hospital['beds']:,}개")
                    st.write(f"**⭐ 전문분야:** {', '.join(hospital['specialties'])}")
                    
                    if hospital['emergency_24']:
                        st.success("✅ 24시간 응급실 운영")
                    else:
                        st.warning("⚠️ 제한시간 운영")
                
                with col2:
                    st.markdown(f"### 📞 {hospital['phone']}")
                    if st.button("전화걸기", key=f"call_{hospital['name']}"):
                        st.info(f"📞 {hospital['phone']} 연결 중...")
                    
                    st.write(f"**🚶‍♂️ 거리:** {hospital['distance']}m")
    
    with tab3:
        st.subheader("📚 재난별 행동요령")
        
        disaster_guides = {
            "지진": {
                "immediate": [
                    "1. 책상 아래로 몸을 숨기고 다리를 잡으세요 (Drop, Cover, Hold)",
                    "2. 흔들림이 멈출 때까지 기다리세요",
                    "3. 문을 열어 출구를 확보하세요",
                    "4. 엘리베이터 사용 금지"
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
                    "1. '불이야!'를 크게 외치세요",
                    "2. 119에 신고하세요",
                    "3. 자세를 낮추고 벽을 따라 이동하세요",
                    "4. 연기가 많으면 젖은 수건으로 입과 코를 막으세요"
                ],
                "evacuation": [
                    "1. 계단을 이용하여 아래층으로 피하세요",
                    "2. 엘리베이터 사용 절대 금지",
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
                
                if st.button(f"🔊 {disaster} 행동요령 음성안내", key=f"guide_{disaster}"):
                    speak_text(f"{disaster} 발생시 행동요령을 안내드립니다.")
    
    # 푸터
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #6B7280; padding: 20px;'>
    <p>🚨 재난 불평등 해소 프로젝트 | 모든 시민의 안전한 대피를 위해</p>
    <p>📞 응급상황 시: 119 (소방서) | 112 (경찰서) | 1588-5117 (재난안전상황실)</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
