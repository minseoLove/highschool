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

# 음성 안내 기능 (개선된 버전)
def speak_text(text, speed=1.0):
    if st.session_state.get('voice_enabled', False):
        # 텍스트 정리
        clean_text = text.replace("**", "").replace("*", "").replace("#", "").replace("•", "").replace("🔍", "").replace("⚠️", "").replace("💨", "").replace("🌊", "").replace("🎒", "").replace("👥", "").replace("📱", "").replace("🚫", "").replace("👫", "").replace("🏠", "").replace("🚗", "")
        
        # 음성 안내 표시
        st.info(f"🔊 음성 안내: {clean_text[:100]}...")
        
        # JavaScript로 음성 합성
        speech_js = f"""
        <div id="speech-container">
            <script>
            function speakText() {{
                if ('speechSynthesis' in window) {{
                    // 기존 음성 중지
                    window.speechSynthesis.cancel();
                    
                    // 새로운 음성 생성
                    var utterance = new SpeechSynthesisUtterance(`{clean_text}`);
                    utterance.lang = 'ko-KR';
                    utterance.rate = {speed};
                    utterance.pitch = 1.0;
                    utterance.volume = 0.8;
                    
                    // 음성 시작 이벤트
                    utterance.onstart = function() {{
                        console.log('음성 안내 시작');
                    }};
                    
                    // 음성 완료 이벤트
                    utterance.onend = function() {{
                        console.log('음성 안내 완료');
                    }};
                    
                    // 음성 오류 이벤트
                    utterance.onerror = function(event) {{
                        console.error('음성 안내 오류:', event.error);
                        alert('음성 안내 기능을 사용할 수 없습니다. 브라우저 설정을 확인해주세요.');
                    }};
                    
                    // 음성 재생
                    window.speechSynthesis.speak(utterance);
                }} else {{
                    alert('이 브라우저는 음성 안내를 지원하지 않습니다.');
                }}
            }}
            
            // 페이지 로드 후 자동 실행
            speakText();
            </script>
        </div>
        """
        
        # JavaScript 실행
        st.components.v1.html(speech_js, height=50)
        
        # 음성 제어 버튼 제공
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⏹️ 음성 중지", key=f"stop_speech_{hash(text)}"):
                stop_speech_js = """
                <script>
                if ('speechSynthesis' in window) {
                    window.speechSynthesis.cancel();
                }
                </script>
                """
                st.components.v1.html(stop_speech_js, height=0)
                st.success("음성이 중지되었습니다.")
        
        with col2:
            if st.button("🔄 다시 듣기", key=f"replay_speech_{hash(text)}"):
                speak_text(text, speed)
    else:
        st.warning("🔊 음성 안내가 비활성화되어 있습니다. 사이드바에서 활성화해주세요.")

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

# 재난 행동요령 데이터
@st.cache_data
def get_disaster_guides():
    guides = {}
    
    # 지진 가이드
    guides["지진"] = {
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
    }
    
    # 태풍 가이드
    guides["태풍"] = {
        "summary": [
            "1. TV, 라디오로 태풍 정보를 수시로 확인하세요",
            "2. 위험지역(산간, 계곡, 하천)은 절대 접근하지 마세요",
            "3. 강풍에 대비해 창문을 보강하고 실외 물건을 실내로 옮기세요",
            "4. 침수 위험 시 즉시 높은 곳으로 대피하세요"
        ],
        "preparation": [
            "🔍 태풍 정보 확인 및 대피 계획 수립",
            "• TV, 라디오, 인터넷, 스마트폰의 안전디딤돌 앱을 통해 태풍의 진로와 도달 시간을 수시로 확인한다.",
            "• 가족과 함께 미리 대피 장소와 대피 경로를 정해 둔다.",
            "",
            "⚠️ 위험지역 피하기",
            "• 산간, 계곡, 하천, 방파제 등 위험지역은 절대 접근하지 않는다.",
            "• 저지대, 상습침수지역, 산사태 위험지역, 지하공간, 낡은 건물 등도 피해야 한다.",
            "• 등산, 야영, 물놀이, 낚시 등 야외 활동은 즉시 중단하고 안전한 곳으로 이동한다.",
            "",
            "💨 강풍 대비",
            "• 낡고 약한 창문은 미리 교체하거나 보강한다.",
            "• 유리창에는 유리 파편 피해를 줄이기 위해 안전필름을 붙인다.",
            "• 창문 틀과 유리창 사이 틈새를 보강하고, 테이프로 유리를 창틀에 단단히 고정한다.",
            "",
            "🌊 침수 대비",
            "• 집 주변 하수구나 배수구는 미리 점검하고 막힌 곳은 뚫는다.",
            "• 지하주차장, 건물 지하공간 등은 모래주머니, 물막이판 등을 이용해 침수에 대비한다.",
            "",
            "🎒 비상용품 준비",
            "• 구급약, 손전등, 배터리, 휴대용 라디오, 식수, 간편식 등을 비상배낭에 준비해둔다.",
            "• 상수도 중단에 대비해 욕조 등에 물을 미리 받아둔다."
        ],
        "during": [
            "📱 외출 자제 및 정보 확인",
            "• 외출을 삼가고 기상 상황, 거주 지역 주변 위험 정보, 재난 정보를 수시로 확인한다.",
            "",
            "🚫 절대 접근하지 말아야 할 위험지역",
            "• 침수된 도로, 지하차도, 교량 등은 차량과 보행자의 진입을 금지하고 주변 사람들에게도 알린다.",
            "• 산간, 계곡, 하천변, 해안가 등은 급류에 휩쓸릴 수 있으므로 접근하지 않고 즉시 벗어난다.",
            "",
            "🏠 실내 안전 수칙",
            "• 건물의 출입문과 창문을 닫아 파손을 막고, 유리창에서 떨어진 위치에 머문다.",
            "• 강풍 피해를 줄이기 위해 창문이 없는 욕실이나 집 안쪽으로 이동한다."
        ],
        "after": [
            "👨‍👩‍👧‍👦 가족·지인 안전 확인 및 위험지역 접근 금지",
            "• 가족과 지인에게 연락하여 안전 여부를 확인합니다.",
            "• 연락이 되지 않고 실종이 의심될 경우, 경찰서에 신고합니다.",
            "",
            "🏠 집으로 복귀 시 점검 및 신고",
            "• 대피 후 집으로 돌아왔을 때에는 집과 주변 시설의 안전 여부를 먼저 확인하고 출입합니다.",
            "• 파손된 시설물(주택, 상하수도, 도로 등)은 시·군·구청 또는 주민센터에 신고합니다."
        ]
    }
    
    # 호우 가이드
    guides["호우"] = {
        "summary": [
            "1. 우리 지역의 침수, 산사태 위험지역을 미리 확인하세요",
            "2. 안전디딤돌 앱으로 기상정보를 실시간 확인하세요",
            "3. 침수지역과 위험지역은 절대 접근하지 마세요",
            "4. 대피 권고 시 즉시 안전한 곳으로 이동하세요"
        ],
        "preparation": [
            "🗺️ 우리 지역의 위험요소를 사전에 확인하고 공유합니다",
            "• 내가 살고 있는 지역의 홍수, 침수, 산사태, 해일 등 위험요소를 미리 확인합니다.",
            "",
            "📱 재난정보를 실시간으로 수신할 수 있도록 준비합니다",
            "• TV, 라디오, 스마트폰 앱(안전디딤돌 등)을 통해 기상특보·홍수·산사태 등 재난 정보를 실시간으로 받을 수 있도록 준비합니다."
        ],
        "forecast": [
            "📺 기상정보를 주변 사람들과 함께 공유합니다",
            "• TV, 라디오, 인터넷, 스마트폰(안전디딤돌 앱 등)을 활용해 호우 예보 지역과 시간을 미리 확인합니다.",
            "",
            "🏃 위험지역에 있다면 함께 안전한 곳으로 이동합니다",
            "• 산간, 계곡, 하천, 방파제 등에서 야영이나 물놀이 중일 경우 즉시 중단합니다."
        ],
        "during": [
            "📱 외출은 자제하고 정보를 수시로 확인·공유합니다",
            "• 스마트폰 등으로 기상정보를 지속적으로 확인합니다.",
            "",
            "🏠 실내에서는 미리 안전 수칙을 숙지하고 대비합니다",
            "• 건물의 출입문과 창문은 단단히 닫아 파손을 막습니다."
        ],
        "after": [
            "👨‍👩‍👧‍👦 가족과 지인의 안전 여부를 확인합니다",
            "• 가족 및 지인에게 연락하여 안전 여부를 확인합니다.",
            "",
            "🏠 피해 여부를 주변 사람들과 함께 확인합니다",
            "• 대피 후 귀가했을 경우, 집의 구조적 안전 여부를 먼저 확인하고 출입합니다."
        ]
    }
    
    # 화재 가이드
    guides["화재"] = {
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
    
    return guides

# 상세 행동요령 페이지 표시 함수
def show_detailed_guide(disaster, guide):
    st.markdown(f"# 🚨 {disaster} 상세 행동요령")
    
    if disaster == "태풍":
        # 태풍 3단계
        tab1, tab2, tab3 = st.tabs(["📋 태풍 예보 시", "🌀 태풍 특보 중", "✅ 태풍 이후"])
        
        with tab1:
            st.markdown("## 🔍 태풍 예보 시 준비사항")
            for action in guide["preparation"]:
                if action.startswith(("🔍", "⚠️", "💨", "🌊", "🎒", "👥")):
                    st.markdown(f"### {action}")
                elif action.startswith("•"):
                    st.write(action)
                elif action == "":
                    st.write("")
                else:
                    st.write(action)
        
        with tab2:
            st.markdown("## 🌀 태풍 특보 중 행동수칙")
            for action in guide["during"]:
                if action.startswith(("📱", "🚫", "👫", "🏠", "🚗")):
                    st.markdown(f"### {action}")
                elif action.startswith("•"):
                    st.write(action)
                elif action == "":
                    st.write("")
                else:
                    st.write(action)
        
        with tab3:
            st.markdown("## ✅ 태풍 이후 복구활동")
            for action in guide["after"]:
                if action.startswith(("👨‍👩‍👧‍👦", "🏠", "⚠️")):
                    st.markdown(f"### {action}")
                elif action.startswith("•"):
                    st.write(action)
                elif action.startswith("  -"):
                    st.write(action)
                elif action == "":
                    st.write("")
                else:
                    st.write(action)
    
    elif disaster == "호우":
        # 호우 4단계
        tab1, tab2, tab3, tab4 = st.tabs(["📋 호우 사전준비", "🌧️ 호우 예보 시", "⚡ 호우 특보 중", "✅ 호우 이후"])
        
        with tab1:
            st.markdown("## 🗺️ 호우 사전준비")
            for action in guide["preparation"]:
                if action.startswith(("🗺️", "📱", "🏃", "🎒", "🔍")):
                    st.markdown(f"### {action}")
                elif action.startswith("•"):
                    st.write(action)
                elif action == "":
                    st.write("")
                else:
                    st.write(action)
        
        with tab2:
            st.markdown("## 🌧️ 호우 예보 시")
            for action in guide["forecast"]:
                if action.startswith(("📺", "🏃", "🚗", "🎒", "🏠")):
                    st.markdown(f"### {action}")
                elif action.startswith("•"):
                    st.write(action)
                elif action == "":
                    st.write("")
                else:
                    st.write(action)
        
        with tab3:
            st.markdown("## ⚡ 호우 특보 중")
            for action in guide["during"]:
                if action.startswith(("📱", "🏠", "⚠️")):
                    st.markdown(f"### {action}")
                elif action.startswith("•"):
                    st.write(action)
                elif action == "":
                    st.write("")
                else:
                    st.write(action)
        
        with tab4:
            st.markdown("## ✅ 호우 이후")
            for action in guide["after"]:
                if action.startswith(("👨‍👩‍👧‍👦", "🏠", "⚠️")):
                    st.markdown(f"### {action}")
                elif action.startswith("•"):
                    st.write(action)
                elif action.startswith("  -"):
                    st.write(action)
                elif action == "":
                    st.write("")
                else:
                    st.write(action)
    
    else:
        # 기존 2단계 형식 (지진, 화재 등)
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("## ⚡ 즉시 행동")
            for action in guide["immediate"]:
                st.write(action)
        
        with col2:
            st.markdown("## 🏃‍♂️ 대피 행동")
            for action in guide["evacuation"]:
                st.write(action)
    
    # 메인 페이지로 돌아가기 버튼
    st.markdown("---")
    if st.button("⬅️ 재난 행동요령 목록으로 돌아가기", key="back_to_main"):
        st.session_state.show_detailed_page = False
        st.session_state.selected_disaster_detail = None
        st.rerun()

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
        
        # 음성 안내 설정
        st.markdown("### 🔊 음성 안내 설정")
        voice_enabled = st.checkbox("음성 안내 활성화", value=st.session_state.voice_enabled)
        st.session_state.voice_enabled = voice_enabled
        
        if voice_enabled:
            st.success("✅ 음성 안내가 활성화되었습니다")
            
            # 음성 속도 조절
            voice_speed = st.slider("음성 속도", 0.5, 2.0, 1.0, 0.1)
            st.session_state.voice_speed = voice_speed
            
            # 음성 테스트
            if st.button("🔊 음성 테스트"):
                speak_text("음성 안내 시스템이 정상 작동합니다. 재난 발생 시 이 시스템을 통해 중요한 안내를 받을 수 있습니다.")
            
            # 음성 안내 사용법
            with st.expander("📖 음성 안내 사용법"):
                st.write("• 각 버튼을 클릭하면 자동으로 음성 안내가 시작됩니다")
                st.write("• '⏹️ 음성 중지' 버튼으로 언제든 중지할 수 있습니다")
                st.write("• '🔄 다시 듣기' 버튼으로 반복 재생 가능합니다")
                st.write("• 크롬, 엣지, 사파리 브라우저에서 최적화되어 있습니다")
        else:
            st.info("음성 안내를 사용하려면 위 체크박스를 선택하세요")
        
        # 고대비 모드
        st.markdown("### 🌓 시각 설정")
        high_contrast = st.checkbox("고대비 모드", value=st.session_state.high_contrast)
        st.session_state.high_contrast = high_contrast
        
        if high_contrast:
            st.markdown("""
            <style>
            .stApp {
                background-color: #000000 !important;
                color: #FFFFFF !important;
            }
            .stSelectbox > div > div {
                background-color: #333333 !important;
                color: #FFFFFF !important;
            }
            </style>
            """, unsafe_allow_html=True)
            st.success("✅ 고대비 모드가 활성화되었습니다")
    
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
                "지진해일": {"icon": "🌊", "description": "고지대로 긴급 대피"},
                "해일": {"icon": "🌊", "description": "해안에서 멀리 떨어진 고지대로 대피"},
                "폭염": {"icon": "🌡️", "description": "시원한 실내나 그늘에서 휴식"}
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
                        "지진해일": "tsunami",
                        "해일": "tsunami",
                        "폭염": "earthquake"  # 폭염은 실내 대피소 사용
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
        
        # 상세 페이지가 활성화된 경우
        if st.session_state.get('show_detailed_page', False) and st.session_state.get('selected_disaster_detail'):
            disaster_guides = get_disaster_guides()
            selected_disaster = st.session_state.selected_disaster_detail
            guide = disaster_guides[selected_disaster]
            show_detailed_guide(selected_disaster, guide)
        
        else:
            # 기본 목록 페이지
            disaster_guides = get_disaster_guides()
            
            for disaster, guide in disaster_guides.items():
                with st.expander(f"🚨 {disaster} 발생 시", expanded=False):
                    # 기본 요약 정보 표시
                    st.write("### 📝 핵심 행동요령")
                    for action in guide["summary"]:
                        st.write(action)
                    
                    # 상세 내용 보기 버튼
                    st.markdown("---")
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        if st.button(f"📖 {disaster} 상세 행동요령 보기", key=f"detail_{disaster}"):
                            st.session_state.show_detailed_page = True
                            st.session_state.selected_disaster_detail = disaster
                            st.rerun()
                    
                    with col2:
                        if st.button(f"🔊 {disaster} 음성안내", key=f"voice_{disaster}"):
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
