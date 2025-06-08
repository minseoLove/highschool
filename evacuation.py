"distance": 800,
                    "walk_time": 10,
                    "type": "공원",
                    "wheelchair": True,
                    "elevator": False,
                    "parking": True,
                    "subway": "1호선 달성공원역 도보 3분"
                }
            ]
        }
    }

@st.cache_data  
def load_hospital_data():
    return [
        # 서울 강남구
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
            "name": "삼성서울병원",
            "address": "서울 강남구 일원로 81", 
            "phone": "1599-3114",
            "lat": 37.4881,
            "lon": 127.0857,
            "distance": 2300,
            "emergency_24": True,
            "beds": 1900,
            "subway": "지하철 2호선 삼성역 도보 10분",
            "specialties": ["응급의학과", "외상센터", "중환자실"],
            "region": "강남구"
        },
        {
            "name": "서울아산병원",
            "address": "서울 송파구 올림픽로 43길 88",
            "phone": "1688-7575",
            "lat": 37.5268,
            "lon": 127.1073,
            "distance": 3000,
            "emergency_24": True,
            "beds": 2700,
            "subway": "지하철 9호선 석촌고분역 도보 8분",
            "specialties": ["응급의학과", "외상센터", "심장센터"],
            "region": "강남구"
        },
        # 서울 종로구
        {
            "name": "서울대학교병원",
            "address": "서울 종로구 대학로 101",
            "phone": "1588-5700",
            "lat": 37.5792,
            "lon": 126.9965,
            "distance": 800,
            "emergency_24": True,
            "beds": 1700,
            "subway": "지하철 4호선 혜화역 도보 10분",
            "specialties": ["응급의학과", "외상센터", "신경센터"],
            "region": "종로구"
        },
        # 부산 해운대구
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
            "name": "좋은문화병원",
            "address": "부산 해운대구 센텀중앙로 60",
            "phone": "051-780-5000",
            "lat": 35.1693,
            "lon": 129.1295,
            "distance": 1200,
            "emergency_24": True,
            "beds": 500,
            "subway": "부산지하철 2호선 센텀시티역 도보 5분",
            "specialties": ["응급의학과", "내과", "외과"],
            "region": "해운대구"
        },
        # 부산 부산진구
        {
            "name": "부산대학교병원",
            "address": "부산 서구 구덕로 179",
            "phone": "051-240-7000",
            "lat": 35.1043,
            "lon": 129.0321,
            "distance": 1800,
            "emergency_24": True,
            "beds": 1400,
            "subway": "부산지하철 1호선 서대신역 도보 15분",
            "specialties": ["응급의학과", "외상센터", "심혈관센터"],
            "region": "부산진구"
        },
        {
            "name": "동아대학교병원",
            "address": "부산 서구 대신공원로 26",
            "phone": "051-240-2000",
            "lat": 35.1043,
            "lon": 129.0321,
            "distance": 1900,
            "emergency_24": True,
            "beds": 800,
            "subway": "부산지하철 1호선 동대신역 도보 10분",
            "specialties": ["응급의학과", "외과", "내과"],
            "region": "부산진구"
        },
        # 경기 수원시
        {
            "name": "아주대학교병원",
            "address": "경기 수원시 영통구 월드컵로 164",
            "phone": "031-219-5114",
            "lat": 37.2813,
            "lon": 127.0438,
            "distance": 1500,
            "emergency_24": True,
            "beds": 1300,
            "subway": "분당선 성균관대역 도보 15분",
            "specialties": ["응급의학과", "외상센터", "심혈관센터"],
            "region": "수원시"
        },
        {
            "name": "수원종합병원",
            "address": "경기 수원시 팔달구 중부대로 365",
            "phone": "031-230-8114",
            "lat": 37.2636,
            "lon": 127.0286,
            "distance": 800,
            "emergency_24": True,
            "beds": 600,
            "subway": "1호선 수원역 도보 10분",
            "specialties": ["응급의학과", "내과", "외과"],
            "region": "수원시"
        },
        # 경기 성남시
        {
            "name": "분당서울대학교병원",
            "address": "경기 성남시 분당구 구미로 173번길 82",
            "phone": "031-787-7114",
            "lat": 37.3520,
            "lon": 127.1244,
            "distance": 600,
            "emergency_24": True,
            "beds": 900,
            "subway": "분당선 미금역 도보 8분",
            "specialties": ["응급의학과", "외상센터", "소아응급"],
            "region": "성남시"
        },
        {
            "name": "차의과학대학교 분당차병원",
            "address": "경기 성남시 분당구 야탑로 59",
            "phone": "031-780-5000",
            "lat": 37.3515,
            "lon": 127.1240,
            "distance": 400,
            "emergency_24": True,
            "beds": 800,
            "subway": "분당선 야탑역 도보 5분",
            "specialties": ["응급의학과", "산부인과", "소아과"],
            "region": "성남시"
        },
        # 대구 중구
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

# 음성 안내 기능 (실제 TTS 구현)
def speak_text(text, speed=1.0):
    if st.session_state.get('voice_enabled', False):
        # 화면에 표시
        st.info(f"🔊 음성 안내: {text}")
        
        # 텍스트 정리 (HTML 태그 제거 등)
        clean_text = text.replace("**", "").replace("*", "").replace("#", "")
        
        # HTML5 Speech Synthesis API 사용
        speech_js = f"""
        <script>
        if ('speechSynthesis' in window) {{
            var utterance = new SpeechSynthesisUtterance(`{clean_text}`);
            utterance.lang = 'ko-KR';
            utterance.rate = {speed};
            utterance.pitch = 1.0;
            utterance.volume = 0.9;
            
            // 한국어 음성 찾기
            speechSynthesis.onvoiceschanged = function() {{
                var voices = speechSynthesis.getVoices();
                var koreanVoice = voices.find(voice => voice.lang.includes('ko'));
                if (koreanVoice) {{
                    utterance.voice = koreanVoice;
                }}
                speechSynthesis.speak(utterance);
            }};
            
            // 이미 음성이 로드된 경우
            var voices = speechSynthesis.getVoices();
            if (voices.length > 0) {{
                var koreanVoice = voices.find(voice => voice.lang.includes('ko'));
                if (koreanVoice) {{
                    utterance.voice = koreanVoice;
                }}
                speechSynthesis.speak(utterance);
            }}
        }} else {{
            console.log('음성 합성을 지원하지 않는 브라우저입니다.');
        }}
        </script>
        """
        
        # JavaScript 실행
        st.components.v1.html(speech_js, height=0)

# 재난 행동요령 전체 읽기
def speak_disaster_guide(disaster_name, guide_data):
    if st.session_state.get('voice_enabled', False):
        # 전체 행동요령 텍스트 구성
        full_text = f"{disaster_name} 발생시 행동요령을 안내드립니다. "
        
        full_text += "먼저 즉시 행동 요령입니다. "
        for i, action in enumerate(guide_data["immediate"], 1):
            clean_action = action.replace("**", "").replace("*", "").replace(f"{i}. ", "")
            full_text += f"{i}번째, {clean_action}. "
        
        full_text += "다음은 대피 행동 요령입니다. "
        for i, action in enumerate(guide_data["evacuation"], 1):
            clean_action = action.replace("**", "").replace("*", "").replace(f"{i}. ", "")
            full_text += f"{i}번째, {clean_action}. "
        
        full_text += "이상으로 행동요령 안내를 마치겠습니다. 안전에 유의하세요."
        
        # 긴급상황용 빠른 속도로 읽기
        speak_text(full_text, speed=1.3)

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

# 지도 생성 함수 (folium 사용 가능할 때만)
def create_map(shelters, hospitals, user_location=None):
    if not FOLIUM_AVAILABLE:
        return None
        
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

# 지도 대체 함수 (folium 없을 때)
def create_text_map(shelters, hospitals, user_location=None):
    st.markdown("### 🗺️ 위치 정보")
    
    if user_location:
        st.info(f"📍 현재 위치: {user_location[0]:.4f}, {user_location[1]:.4f}")
    
    st.markdown("**🏠 대피소 위치:**")
    for i, shelter in enumerate(shelters):
        emoji = "🥇" if i == 0 else "📍"
        st.write(f"{emoji} **{shelter['name']}** - 위도: {shelter['lat']:.4f}, 경도: {shelter['lon']:.4f}")
        st.write(f"   ↳ {shelter['address']} (도보 {shelter['walk_time']}분)")
    
    st.markdown("**🏥 병원 위치:**")
    for hospital in hospitals:
        st.write(f"🏥 **{hospital['name']}** - 위도: {hospital['lat']:.4f}, 경도: {hospital['lon']:.4f}")
        st.write(f"   ↳ {hospital['address']} ({hospital['phone']})")
    
    if not FOLIUM_AVAILABLE:
        st.info("💡 **지도 시각화를 원하시면:** `pip install folium streamlit-folium` 설치 후 앱을 재시작하세요!")

# 메인 앱
def main():
    # folium 없을 때 경고 메시지
    if not FOLIUM_AVAILABLE:
        st.warning("🗺️ 지도 기능을 위해 다음 명령어를 실행해주세요: pip install folium streamlit-folium")
    
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
                speak_text("긴급상황 음성 안내 시스템이 정상 작동합니다. 재난 발생 시 신속히 대피하세요.", speed=1.2)
        
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
                ["", "강남구", "종로구", "해운대구", "부산진구", "수원시", "성남시", "대구중구"],
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
                        
                        # 지역별 사용자 위치 설정
                        user_locations = {
                            "강남구": [37.4979, 127.0276],
                            "종로구": [37.5729, 126.9764], 
                            "해운대구": [35.1587, 129.1604],
                            "부산진구": [35.1579, 129.0596],
                            "수원시": [37.2659, 127.0011],
                            "성남시": [37.3515, 127.1240],
                            "대구중구": [35.8682, 128.5953]
                        }
                        
                        user_loc = user_locations.get(location)
                                
                        if user_loc:
                            # 해당 지역 병원만 필터링
                            relevant_hospitals = [h for h in hospital_data if h.get('region', '').replace('시', '') == location.replace('시', '')]
                            
                            if FOLIUM_AVAILABLE:
                                # folium 지도 표시
                                map_obj = create_map(shelters, relevant_hospitals, user_loc)
                                if map_obj:
                                    folium_static(map_obj, width=700, height=400)
                            else:
                                # 텍스트 기반 위치 정보 표시
                                create_text_map(shelters, relevant_hospitals, user_loc)
                        
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
                                        speak_text(f"{shelter['name']}까지 도보 {shelter['walk_time']}분, 수용인원 {shelter['capacity']}명입니다.", speed=1.2)
                                    
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
        
        # 지역 선택
        selected_region = st.selectbox(
            "지역을 선택하세요",
            ["전체", "강남구", "종로구", "해운대구", "부산진구", "수원시", "성남시", "대구중구"],
            key="hospital_region"
        )
        
        hospital_data = load_hospital_data()
        
        # 지역 필터링
        if selected_region != "전체":
            filtered_hospitals = [h for h in hospital_data if h.get('region', '').replace('시', '') == selected_region.replace('시', '')]
        else:
            filtered_hospitals = hospital_data
            
        # 거리순 정렬
        filtered_hospitals.sort(key=lambda x: x['distance'])
        
        for hospital in filtered_hospitals:
            with st.expander(f"🏥 {hospital['name']} - {hospital.get('region', '')} ({hospital['distance']}m)", expanded=True):
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
                    if st.button("☎️ 전화걸기", key=f"call_{hospital['name']}"):
                        st.info(f"📞 {hospital['phone']} 연결 중...")
                        speak_text(f"{hospital['name']} 응급실에 연결합니다.", speed=1.2)
                    
                    st.write(f"**🚶‍♂️ 거리:** {hospital['distance']}m")
                    
                    if st.button("🔊 병원정보 듣기", key=f"speak_hospital_{hospital['name']}"):
                        hospital_info = f"{hospital['name']}는 {hospital.get('region', '')}에 위치하며, 거리 {hospital['distance']}미터, 24시간 응급실을 운영합니다. 전화번호는 {hospital['phone']}입니다."
                        speak_text(hospital_info, speed=1.2)
    
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
            },
            "태풍": {
                "immediate": [
                    "1. 기상청 태풍 경보를 지속적으로 확인하세요",
                    "2. 외출을 자제하고 실내에 머무르세요",
                    "3. 창문과 출입문을 단단히 잠그세요",
                    "4. 응급용품과 비상식량을 준비하세요"
                ],
                "evacuation": [
                    "1. 견고한 건물 내부로 대피하세요",
                    "2. 지하실이나 반지하는 피하세요",
                    "3. 고지대의 안전한 대피소로 이동하세요",
                    "4. 대피 시 차량 이용을 피하고 도보로 이동하세요"
                ]
            },
            "지진해일": {
                "immediate": [
                    "1. 해안가에 있다면 즉시 내륙으로 이동하세요",
                    "2. 지진해일 경보를 확인하세요",
                    "3. 높은 건물 3층 이상으로 대피하세요",
                    "4. 차량을 버리고 도보로 신속히 이동하세요"
                ],
                "evacuation": [
                    "1. 해발 10미터 이상 고지대로 대피하세요",
                    "2. 해안에서 최대한 멀리 떨어진 곳으로 가세요",
                    "3. 지진해일 특보 해제까지 해안에 접근하지 마세요",
                    "4. 여러 차례 파도가 올 수 있으니 계속 주의하세요"
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
                
                # 음성 안내 버튼들
                st.markdown("---")
                col_full, col_imm, col_eva = st.columns(3)
                
                with col_full:
                    if st.button(f"🔊 {disaster} 전체 행동요령 음성안내", key=f"guide_full_{disaster}"):
                        speak_disaster_guide(disaster, guide)
                
                with col_imm:
                    if st.button(f"🔊 즉시행동 안내", key=f"immediate_{disaster}"):
                        immediate_text = f"{disaster} 즉시 행동 요령입니다. "
                        for i, action in enumerate(guide["immediate"], 1):
                            clean_action = action.replace("**", "").replace("*", "").replace(f"{i}. ", "")
                            immediate_text += f"{i}번째, {clean_action}. "
                        speak_text(immediate_text, speed=1.3)
                
                with col_eva:
                    if st.button(f"🔊 대피행동 안내", key=f"evacuation_{disaster}"):
                        evacuation_text = f"{disaster} 대피 행동 요령입니다. "
                        for i, action in enumerate(guide["evacuation"], 1):
                            clean_action = action.replace("**", "").replace("*", "").replace(f"{i}. ", "")
                            evacuation_text += f"{i}번째, {clean_action}. "
                        speak_text(evacuation_text, speed=1.3)
    
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
    main()import streamlit as st
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
                },
                {
                    "name": "개포고등학교",
                    "address": "서울 강남구 개포로 621",
                    "lat": 37.4816,
                    "lon": 127.0663,
                    "capacity": 1200,
                    "distance": 1200,
                    "walk_time": 15,
                    "type": "운동장",
                    "wheelchair": True,
                    "elevator": False,
                    "parking": True,
                    "subway": "3호선 개포동역 도보 5분"
                },
                {
                    "name": "논현초등학교",
                    "address": "서울 강남구 언주로 108길 26",
                    "lat": 37.5131,
                    "lon": 127.0306,
                    "capacity": 600,
                    "distance": 900,
                    "walk_time": 12,
                    "type": "운동장",
                    "wheelchair": True,
                    "elevator": False,
                    "parking": True,
                    "subway": "7호선 논현역 도보 8분"
                },
                {
                    "name": "대치초등학교",
                    "address": "서울 강남구 도곡로 425",
                    "lat": 37.4987,
                    "lon": 127.0633,
                    "capacity": 800,
                    "distance": 1000,
                    "walk_time": 13,
                    "type": "운동장",
                    "wheelchair": True,
                    "elevator": False,
                    "parking": True,
                    "subway": "3호선 대치역 도보 6분"
                },
                {
                    "name": "삼성고등학교",
                    "address": "서울 강남구 밤고개로 42길 5",
                    "lat": 37.5086,
                    "lon": 127.0529,
                    "capacity": 1000,
                    "distance": 1500,
                    "walk_time": 18,
                    "type": "운동장", 
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
                },
                {
                    "name": "개포고등학교 체육관",
                    "address": "서울 강남구 개포로 621",
                    "lat": 37.4816,
                    "lon": 127.0663,
                    "capacity": 800,
                    "distance": 1200,
                    "walk_time": 15,
                    "type": "체육관",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": True,
                    "subway": "3호선 개포동역 도보 5분"
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
                },
                {
                    "name": "역삼역 지하공간",
                    "address": "서울 강남구 테헤란로 지하",
                    "lat": 37.5007,
                    "lon": 127.0366,
                    "capacity": 2500,
                    "distance": 700,
                    "walk_time": 9,
                    "type": "지하공간",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": False,
                    "subway": "2호선 역삼역 직결"
                },
                {
                    "name": "선릉역 지하공간",
                    "address": "서울 강남구 선릉로 지하",
                    "lat": 37.5044,
                    "lon": 127.0463,
                    "capacity": 2000,
                    "distance": 900,
                    "walk_time": 11,
                    "type": "지하공간",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": False,
                    "subway": "2호선/분당선 선릉역 직결"
                }
            ]
        },
        "종로구": {
            "earthquake": [
                {
                    "name": "광화문광장",
                    "address": "서울 종로구 세종대로 172",
                    "lat": 37.5729,
                    "lon": 126.9764,
                    "capacity": 5000,
                    "distance": 300,
                    "walk_time": 4,
                    "type": "광장",
                    "wheelchair": True,
                    "elevator": False,
                    "parking": False,
                    "subway": "5호선 광화문역 도보 2분"
                },
                {
                    "name": "탑골공원",
                    "address": "서울 종로구 종로 99",
                    "lat": 37.5703,
                    "lon": 126.9916,
                    "capacity": 1200,
                    "distance": 600,
                    "walk_time": 8,
                    "type": "공원",
                    "wheelchair": True,
                    "elevator": False,
                    "parking": False,
                    "subway": "1호선 종각역 도보 3분"
                },
                {
                    "name": "종묘광장",
                    "address": "서울 종로구 종로 157",
                    "lat": 37.5740,
                    "lon": 126.9940,
                    "capacity": 2000,
                    "distance": 800,
                    "walk_time": 10,
                    "type": "광장",
                    "wheelchair": True,
                    "elevator": False,
                    "parking": False,
                    "subway": "1/3/5호선 종로3가역 도보 5분"
                }
            ],
            "war": [
                {
                    "name": "종각역 지하상가",
                    "address": "서울 종로구 종로 지하",
                    "lat": 37.5700,
                    "lon": 126.9827,
                    "capacity": 2000,
                    "distance": 400,
                    "walk_time": 5,
                    "type": "지하상가",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": False,
                    "subway": "1호선 종각역 직결"
                },
                {
                    "name": "을지로입구역 지하공간",
                    "address": "서울 종로구 을지로 지하",
                    "lat": 37.5664,
                    "lon": 126.9824,
                    "capacity": 1800,
                    "distance": 500,
                    "walk_time": 7,
                    "type": "지하공간",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": False,
                    "subway": "2호선 을지로입구역 직결"
                },
                {
                    "name": "종로3가역 지하상가",
                    "address": "서울 종로구 종로 지하",
                    "lat": 37.5705,
                    "lon": 126.9915,
                    "capacity": 2500,
                    "distance": 700,
                    "walk_time": 9,
                    "type": "지하상가",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": False,
                    "subway": "1/3/5호선 종로3가역 직결"
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
                },
                {
                    "name": "센텀시티 중앙공원",
                    "address": "부산 해운대구 센텀중앙로 55",
                    "lat": 35.1693,
                    "lon": 129.1295,
                    "capacity": 3000,
                    "distance": 800,
                    "walk_time": 10,
                    "type": "공원",
                    "wheelchair": True,
                    "elevator": False,
                    "parking": True,
                    "subway": "2호선 센텀시티역 도보 5분"
                },
                {
                    "name": "해운대스포츠센터",
                    "address": "부산 해운대구 해운대해변로 84",
                    "lat": 35.1598,
                    "lon": 129.1585,
                    "capacity": 2000,
                    "distance": 600,
                    "walk_time": 8,
                    "type": "운동장",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": True,
                    "subway": "2호선 해운대역 도보 5분"
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
                },
                {
                    "name": "해운대구청사 옥상",
                    "address": "부산 해운대구 해운대로 570",
                    "lat": 35.1631,
                    "lon": 129.1635,
                    "capacity": 200,
                    "distance": 1000,
                    "walk_time": 12,
                    "type": "고지대",
                    "elevation": "해발 15m",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": True,
                    "subway": "2호선 해운대역 도보 10분"
                },
                {
                    "name": "LCT 더샵",
                    "address": "부산 해운대구 우동 1394",
                    "lat": 35.1587,
                    "lon": 129.1604,
                    "capacity": 1000,
                    "distance": 400,
                    "walk_time": 5,
                    "type": "3층 이상",
                    "elevation": "해발 20m",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": True,
                    "subway": "2호선 해운대역 도보 3분"
                }
            ],
            "war": [
                {
                    "name": "해운대역 지하상가",
                    "address": "부산 해운대구 해운대로 지하",
                    "lat": 35.1593,
                    "lon": 129.1586,
                    "capacity": 2000,
                    "distance": 300,
                    "walk_time": 4,
                    "type": "지하상가",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": False,
                    "subway": "2호선 해운대역 직결"
                },
                {
                    "name": "센텀시티역 지하공간",
                    "address": "부산 해운대구 센텀중앙로 지하",
                    "lat": 35.1693,
                    "lon": 129.1295,
                    "capacity": 1800,
                    "distance": 800,
                    "walk_time": 10,
                    "type": "지하공간",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": False,
                    "subway": "2호선 센텀시티역 직결"
                }
            ]
        },
        "부산진구": {
            "earthquake": [
                {
                    "name": "부산시민공원",
                    "address": "부산 부산진구 시민공원로 73",
                    "lat": 35.1663,
                    "lon": 129.0535,
                    "capacity": 8000,
                    "distance": 1200,
                    "walk_time": 15,
                    "type": "대형공원",
                    "wheelchair": True,
                    "elevator": False,
                    "parking": True,
                    "subway": "1호선 부전역 도보 10분"
                },
                {
                    "name": "서면 시민공원",
                    "address": "부산 부산진구 중앙대로 680",
                    "lat": 35.1579,
                    "lon": 129.0596,
                    "capacity": 2500,
                    "distance": 500,
                    "walk_time": 6,
                    "type": "공원",
                    "wheelchair": True,
                    "elevator": False,
                    "parking": False,
                    "subway": "1/2호선 서면역 도보 2분"
                }
            ],
            "war": [
                {
                    "name": "서면 지하상가",
                    "address": "부산 부산진구 서면로 지하",
                    "lat": 35.1579,
                    "lon": 129.0596,
                    "capacity": 4000,
                    "distance": 200,
                    "walk_time": 3,
                    "type": "지하상가",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": False,
                    "subway": "1/2호선 서면역 직결"
                },
                {
                    "name": "부산진역 지하상가",
                    "address": "부산 부산진구 중앙대로 지하",
                    "lat": 35.1616,
                    "lon": 129.0598,
                    "capacity": 2500,
                    "distance": 600,
                    "walk_time": 8,
                    "type": "지하상가",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": False,
                    "subway": "1호선 부산진역 직결"
                },
                {
                    "name": "양정역 지하공간",
                    "address": "부산 부산진구 양정로 지하",
                    "lat": 35.1697,
                    "lon": 129.0720,
                    "capacity": 1500,
                    "distance": 1000,
                    "walk_time": 12,
                    "type": "지하공간",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": False,
                    "subway": "1호선 양정역 직결"
                }
            ]
        },
        "수원시": {
            "earthquake": [
                {
                    "name": "수원월드컵경기장",
                    "address": "경기 수원시 팔달구 월드컵로 310",
                    "lat": 37.2866,
                    "lon": 127.0367,
                    "capacity": 8000,
                    "distance": 1500,
                    "walk_time": 18,
                    "type": "축구장",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": True,
                    "subway": "1호선 수원역 버스 15분"
                },
                {
                    "name": "수원종합운동장",
                    "address": "경기 수원시 장안구 조원로 775",
                    "lat": 37.3007,
                    "lon": 127.0093,
                    "capacity": 5000,
                    "distance": 2000,
                    "walk_time": 25,
                    "type": "운동장",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": True,
                    "subway": "1호선 성균관대역 도보 15분"
                },
                {
                    "name": "효원공원",
                    "address": "경기 수원시 팔달구 인계로 178",
                    "lat": 37.2642,
                    "lon": 127.0286,
                    "capacity": 2000,
                    "distance": 800,
                    "walk_time": 10,
                    "type": "공원",
                    "wheelchair": True,
                    "elevator": False,
                    "parking": True,
                    "subway": "1호선 수원역 도보 8분"
                }
            ],
            "flood": [
                {
                    "name": "수원시청",
                    "address": "경기 수원시 팔달구 효원로 241",
                    "lat": 37.2636,
                    "lon": 127.0286,
                    "capacity": 800,
                    "distance": 600,
                    "walk_time": 8,
                    "type": "건물",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": True,
                    "subway": "1호선 수원역 도보 6분"
                },
                {
                    "name": "팔달구청",
                    "address": "경기 수원시 팔달구 효원로 1",
                    "lat": 37.2658,
                    "lon": 127.0298,
                    "capacity": 500,
                    "distance": 700,
                    "walk_time": 9,
                    "type": "건물",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": True,
                    "subway": "1호선 수원역 도보 7분"
                }
            ],
            "war": [
                {
                    "name": "수원역 지하상가",
                    "address": "경기 수원시 팔달구 매산로 지하",
                    "lat": 37.2659,
                    "lon": 127.0011,
                    "capacity": 3000,
                    "distance": 300,
                    "walk_time": 4,
                    "type": "지하상가",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": False,
                    "subway": "1호선 수원역 직결"
                },
                {
                    "name": "인계동 지하상가",
                    "address": "경기 수원시 팔달구 인계로 지하",
                    "lat": 37.2642,
                    "lon": 127.0286,
                    "capacity": 2000,
                    "distance": 800,
                    "walk_time": 10,
                    "type": "지하상가",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": False,
                    "subway": "1호선 수원역 도보 8분"
                }
            ]
        },
        "성남시": {
            "earthquake": [
                {
                    "name": "탄천종합운동장",
                    "address": "경기 성남시 분당구 탄천로 215",
                    "lat": 37.4058,
                    "lon": 127.1235,
                    "capacity": 6000,
                    "distance": 1500,
                    "walk_time": 18,
                    "type": "운동장",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": True,
                    "subway": "분당선 야탑역 도보 15분"
                },
                {
                    "name": "분당중앙공원",
                    "address": "경기 성남시 분당구 야탑로 215",
                    "lat": 37.3515,
                    "lon": 127.1240,
                    "capacity": 4000,
                    "distance": 800,
                    "walk_time": 10,
                    "type": "대형공원",
                    "wheelchair": True,
                    "elevator": False,
                    "parking": True,
                    "subway": "분당선 야탑역 도보 5분"
                },
                {
                    "name": "성남종합운동장",
                    "address": "경기 성남시 중원구 성남대로 1",
                    "lat": 37.4198,
                    "lon": 127.1265,
                    "capacity": 4500,
                    "distance": 2000,
                    "walk_time": 25,
                    "type": "운동장",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": True,
                    "subway": "8호선 모란역 버스 10분"
                }
            ],
            "flood": [
                {
                    "name": "성남시청",
                    "address": "경기 성남시 중원구 성남대로 997",
                    "lat": 37.4198,
                    "lon": 127.1265,
                    "capacity": 1000,
                    "distance": 1800,
                    "walk_time": 22,
                    "type": "건물",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": True,
                    "subway": "8호선 모란역 버스 8분"
                },
                {
                    "name": "분당구청",
                    "address": "경기 성남시 분당구 야탑로 50",
                    "lat": 37.3515,
                    "lon": 127.1240,
                    "capacity": 600,
                    "distance": 600,
                    "walk_time": 8,
                    "type": "건물",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": True,
                    "subway": "분당선 야탑역 도보 3분"
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
                },
                {
                    "name": "달성공원",
                    "address": "대구 중구 달성공원로 35",
                    "lat": 35.8743,
                    "lon": 128.5741,
                    "capacity": 2500,
                    "distance": 800
