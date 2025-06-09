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
            "• 주변에 있는 사람들과 함께 안전한 장소로 이동한다.",
            "",
            "💨 강풍 대비",
            "• 낡고 약한 창문은 미리 교체하거나 보강한다.",
            "• 유리창에는 유리 파편 피해를 줄이기 위해 안전필름을 붙인다.",
            "• 창문 틀과 유리창 사이 틈새를 보강하고, 테이프로 유리를 창틀에 단단히 고정한다.",
            "• 지붕, 간판, 철탑 등 외부 시설물은 고정하거나 보강한다.",
            "• 바깥에 있는 물건은 실내로 옮기거나 제거한다.",
            "• 노출된 전선은 감전이나 누전 사고가 없도록 사전에 점검하고 필요시 교체한다.",
            "",
            "🌊 침수 대비",
            "• 집 주변 하수구나 배수구는 미리 점검하고 막힌 곳은 뚫는다.",
            "• 지하주차장, 건물 지하공간 등은 모래주머니, 물막이판 등을 이용해 침수에 대비한다.",
            "• 차량은 하천, 해변, 저지대를 피해서 높은 곳으로 옮긴다. 차량에 연락처를 남겨둔다.",
            "• 농촌은 배수로, 논둑 등을 정비하고 물꼬를 조정하되, 비가 오기 전까지만 작업한다.",
            "• 어촌은 선박을 단단히 결박하거나 육지로 올리고, 어망·어구는 안전한 장소로 옮긴다.",
            "",
            "🎒 비상용품 준비",
            "• 구급약, 손전등, 배터리, 휴대용 라디오, 식수, 간편식 등을 비상배낭에 준비해둔다.",
            "• 상수도 중단에 대비해 욕조 등에 물을 미리 받아둔다.",
            "• 정전에 대비해 손전등과 예비 배터리를 확보한다.",
            "",
            "👥 대피약자 보호",
            "• 어르신, 어린이, 장애인 등 대피에 취약한 사람의 상태를 수시로 확인한다.",
            "• 비상시 어떻게 대피할지 사전에 설명하고 함께 대피할 수 있도록 준비한다."
        ],
        "during": [
            "📱 외출 자제 및 정보 확인",
            "• 외출을 삼가고 기상 상황, 거주 지역 주변 위험 정보, 재난 정보를 수시로 확인한다.",
            "• 외부에 있는 가족, 지인, 이웃과 연락하여 서로의 안전을 확인하고 위험 정보를 공유한다.",
            "",
            "🚫 절대 접근하지 말아야 할 위험지역",
            "• 침수된 도로, 지하차도, 교량 등은 차량과 보행자의 진입을 금지하고 주변 사람들에게도 알린다.",
            "• 산간, 계곡, 하천변, 해안가 등은 급류에 휩쓸릴 수 있으므로 접근하지 않고 즉시 벗어난다.",
            "• 공사장, 가로등, 신호등, 전신주, 지하공간 등은 사고 위험이 높으므로 접근하지 않는다.",
            "• 비탈면, 옹벽, 축대 등은 붕괴 위험이 있으므로 근처에 가지 않는다.",
            "• 이동식 가옥이나 임시 시설 거주자는 견고한 건물로 즉시 이동하고 주변 사람들에게 위험을 알린다.",
            "• 산사태 위험지역에서는 경보가 없더라도 징후가 보이면 즉시 자발적으로 대피한다.",
            "• 농촌에서는 논둑이나 물꼬를 확인하러 나가지 않는다.",
            "• 어촌에서는 선박을 묶거나 어구 등을 이동시키기 위해 나가지 않는다.",
            "• 운항 중인 선박은 위치를 주변 선박이나 해경에 알리고, 태풍 경로에서 최대한 멀리 벗어난다.",
            "",
            "👫 대피 시 약자와 함께 행동",
            "• 침수, 붕괴, 산사태 등의 위험으로 대피가 필요한 경우, 어르신, 어린이, 장애인 등 대피에 어려움이 있는 사람과 함께 대피한다.",
            "",
            "🏠 실내 안전 수칙",
            "• 건물의 출입문과 창문을 닫아 파손을 막고, 유리창에서 떨어진 위치에 머문다.",
            "• 강풍 피해를 줄이기 위해 창문이 없는 욕실이나 집 안쪽으로 이동한다.",
            "• 가스 누출을 막기 위해 사전에 차단하고, 전기시설은 절대 만지지 않는다.",
            "• 특히 물에 젖은 손으로 전기시설을 만지지 않는다.",
            "• 정전 시에는 양초 대신 손전등이나 휴대폰 불빛을 사용한다.",
            "• 실내에 물이 조금이라도 차오르면 즉시 높은 곳이나 대피소로 이동한다.",
            "",
            "🚗 실외 행동 수칙",
            "• 운전 시 강풍이 불면 속도를 줄이고 반대 방향 차량 및 주변 차량과의 거리 유지에 주의한다.",
            "• 돌풍은 차량을 차선 밖으로 밀 수 있으므로 핸들을 단단히 잡고 주의 깊게 운전한다.",
            "• 공사장 작업, 크레인 운행 등 야외 작업은 즉시 중단하고 실내로 이동한다."
        ],
        "after": [
            "👨‍👩‍👧‍👦 가족·지인 안전 확인 및 위험지역 접근 금지",
            "• 가족과 지인에게 연락하여 안전 여부를 확인합니다.",
            "• 연락이 되지 않고 실종이 의심될 경우, 경찰서에 신고합니다.",
            "• 침수된 도로와 교량은 파손되었을 수 있으므로 절대 건너지 않습니다.",
            "• 하천 제방, 약해진 비탈면 등은 붕괴 위험이 있으므로 가까이 가지 않습니다.",
            "• 고립된 지역에서는 무리하게 물을 건너지 말고, 119나 주민센터에 신고하거나 주변에 도움을 요청합니다.",
            "",
            "🏠 집으로 복귀 시 점검 및 신고",
            "• 대피 후 집으로 돌아왔을 때에는 집과 주변 시설의 안전 여부를 먼저 확인하고 출입합니다.",
            "• 파손된 시설물(주택, 상하수도, 도로 등)은 시·군·구청 또는 주민센터에 신고합니다.",
            "• 사유시설 복구 전에는 반드시 사진을 찍어 향후 보상 등을 위해 기록을 남깁니다.",
            "",
            "⚠️ 2차 피해 방지 행동",
            "• 물이 빠질 때는 기름, 동물 사체 등 오염물질이 포함될 수 있으므로 접근을 피합니다.",
            "• 수돗물과 식수는 반드시 오염 여부를 확인 후 사용하고, 침수된 음식은 버립니다.",
            "• 침수된 주택은 가스와 전기 차단기를 확인한 후,",
            "  - 가스는 한국가스안전공사(1544-4500)",
            "  - 전기는 한국전기안전공사(1588-7500) 또는 전문가에게 안전점검 후에 사용합니다.",
            "• 가스 누출 가능성이 있는 공간은 충분히 환기하고, 성냥이나 라이터는 환기 전까지 사용 금지입니다.",
            "• 침수된 논·밭은 배수 후 작물 세우기, 병해충 방제 및 흙·오물 제거 작업을 실시합니다.",
            "• 파손된 전기시설은 감전 위험이 있으니 절대 만지지 말고, 119나 지자체에 연락하여 조치합니다.",
            "• 전력선이 차량에 닿은 경우, 차 안에 그대로 머물며 금속 부분에 접촉하지 않도록 주의합니다.",
            "• 119에 신고하고 주변에도 위험을 알립니다."
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
            "• 배수로와 빗물받이는 수시로 청소하며, 비탈면·옹벽·축대 등 위험 시설물은 정비하거나 시·군·구청에 신고합니다.",
            "• 확인한 정보는 가족이나 이웃과 공유합니다.",
            "",
            "📱 재난정보를 실시간으로 수신할 수 있도록 준비합니다",
            "• TV, 라디오, 스마트폰 앱(안전디딤돌 등)을 통해 기상특보·홍수·산사태 등 재난 정보를 실시간으로 받을 수 있도록 준비합니다.",
            "",
            "🏃 대피방법과 가족 간 약속을 미리 정합니다",
            "• 대피 장소, 이동 방법, 대피요령을 숙지하고, 어린이와 노약자에게도 반드시 설명해 둡니다.",
            "• 가족이 따로 떨어져 이동할 경우를 대비해 다시 만날 장소를 정해 둡니다.",
            "• 대피 시 하천변, 산길, 전신주·변압기 주변은 피합니다.",
            "",
            "🎒 가족과 함께 비상용품을 미리 준비합니다",
            "• 응급약품, 손전등, 식수, 비상식량, 라디오, 충전기, 버너, 담요 등을 한 곳에 모아 비상용 키트로 준비합니다.",
            "• 차량이 있다면 연료를 미리 채워두고, 차량이 없는 경우 가까운 이웃과 함께 이동할 방법을 미리 약속해 둡니다.",
            "",
            "🔍 지속적으로 점검하고 대비 태세를 유지합니다",
            "• 비상용품의 유효기간을 주기적으로 확인하고, 대피장소·대피경로 등도 정기적으로 점검합니다.",
            "• 지역의 재난 관련 시설에도 꾸준히 관심을 가지고 필요한 경우 정비 요청을 합니다."
        ],
        "flood_forecast": [
            "🏘️ 취약지역 거주자",
            "• 지역주민: 저지대, 상습침수지역에 거주하는 주민은 기상정보를 수시로 확인하며 대피 준비를 합니다.",
            "  ※ 사전 대피가 필요할 경우 전기와 가스를 차단하고 대피합니다.",
            "• 상가: 많은 비가 예보되면 음식점 등 상가는 거리의 간판이나 전기 시설물을 건물 안으로 옮깁니다.",
            "• 마을관리자: 마을 이장, 통·반장은 마을방송 또는 비상연락망을 통해 외출 자제를 당부하고, 비상 시 마을 주변 대피 장소를 미리 안내합니다.",
            "",
            "🏠 지하공간 거주자",
            "• 비상 상황에 대비하여 방범창 절단용 공구(절단기 등)를 사전에 준비합니다.",
            "• 침수 공간에서 탈출이 어려울 경우를 대비해 부유용품(구명조끼, 튜브, 대형 스티로폼 등)을 준비합니다.",
            "• 지하역사, 지하주차장 등 공동 시설의 비상구 위치를 파악하고 비상 대피 경로를 익혀둡니다.",
            "",
            "🏢 공동주택 관리자",
            "• 평상시: 물막이 판, 모래주머니, 양수기 등을 비치하고, 신속한 설치를 위해 수방 자재 담당자를 지정합니다.",
            "• 지하공간 침수가 빠르게 진행되므로 출입구가 여러 개일 경우 각 출입구마다 담당자를 지정하여 관리합니다.",
            "• 침수 피해가 예상되면 대피 장소를 사전에 안내하고, 차량 이동은 호우 전에만 가능하도록 안내합니다.",
            "• 물막이 판 설치 시간을 안내하고 설치 후에는 차량 이동이 불가함을 알립니다.",
            "• 독거노인, 장애인 등 안전 취약계층의 대피 시 필요한 정보를 사전에 공지하고 인터폰, 전화 등을 이용해 수시로 안전 상태를 확인합니다.",
            "",
            "🚗 차량 이용자",
            "• 비상시 탈출을 위한 차량용 망치 등을 준비합니다.",
            "• 침수 예상 지하 주차장 이용을 금지하고, 하천변, 해변가, 저지대 등에 주차된 차량은 안전한 곳으로 이동시킵니다.",
            "• 지역 당국이 대피를 권고하거나 명령할 경우 둔치 주차장에 있는 차량을 이동시키고, 대피 안내 연락을 위해 차량에 연락처를 남깁니다."
        ],
        "flood_warning": [
            "🚶‍♂️ 보행자",
            "• 침수 지역은 절대 접근하지 않습니다.",
            "• 물 깊이나 도로 상태를 알 수 없고, 특히 밤에는 시야 확보가 어려워 위험합니다.",
            "• 물이 혼탁하면 위험 물체가 신체를 해칠 수 있습니다.",
            "• 보행 가능한 수위는 무릎 높이(약 50cm)까지이며, 물살이 강하면 15cm라도 움직이기 어렵습니다.",
            "• 물이 흘러오면 즉시 근처 건물 2층 이상이나 높은 곳으로 대피합니다.",
            "• 하수도, 맨홀 근처는 추락 및 휩쓸림 사고 위험이 있으니 접근 금지합니다.",
            "• 침수 도로 보행 시에는 느리고 안정적인 걸음으로, 도로 중심보다는 건물 외벽을 잡고 이동합니다.",
            "• 긴 막대기로 맨홀이나 장애물을 확인하며, 맨홀 뚜껑 근처는 위험하니 피합니다.",
            "• 신호등, 가로등, 입간판 등 전기시설물에서 최소 2~3m 거리 유지하며 보행합니다.",
            "• 전기설비 및 금속 구조물 주변은 감전 위험이 있으므로 주의합니다.",
            "",
            "🏠 지하공간 이용자",
            "• (반지하주택, 지하 역사·상가) 바닥에 물이 조금이라도 차거나 하수구 역류 시 즉시 대피합니다.",
            "• 집 안으로 물이 들어오면 출입문을 열어두고, 외부 수심이 무릎 이상이면 전기 차단 후 여러 명이 힘을 합쳐 문을 열고 대피합니다.",
            "• 난간 등 신체 지지할 곳을 잡고 이동하며, 정전 시 승강기 이용 금지입니다.",
            "• 대피가 불가능할 경우:",
            "  - 반지하주택은 방범창을 절단기로 자르고 탈출을 시도합니다.",
            "  - 지하 역사·상가는 비상통로로 우회하여 탈출합니다.",
            "  - 실패 시 전기, 가스 차단 후 119에 도움 요청하고, 물에 뜨는 물건을 활용해 구조를 기다립니다.",
            "• (지하계단) 물이 정강이 높이(약 30~40cm)만 차도 성인 이동이 어렵고, 어린이 및 노약자는 발목 높이만 돼도 즉시 대피합니다.",
            "• 대피 시 운동화 착용을 권장하며, 장화는 안에 물이 차 어려우니 피합니다. 마땅한 신발이 없으면 맨발로 난간을 잡고 이동합니다.",
            "• (지하주차장) 물이 조금이라도 차오르면 차량은 두고 신속히 탈출합니다.",
            "• 빗물이 들어오면 차량 이동 금지, 사람만 대피합니다.",
            "• 지하주차장 진입은 절대 금지입니다.",
            "",
            "🏢 공동주택 관리자",
            "• 기상청 특보를 예의주시하며 많은 비가 예상되면 신속히 물막이 판과 모래주머니를 설치합니다.",
            "• 물막이 판과 모래주머니 설치 후 지하공간 침수가 예상되면 즉시 대피를 안내하고, 지하주차장 진입은 금지합니다.",
            "• 대피 시에는 높은 층이나 가까운 대피시설로 안내하고, 대피 약자가 있을 경우 도움을 요청해 함께 대피시킵니다.",
            "",
            "🚗 차량 이용자",
            "• 차량 침수 시 타이어 높이 2/3 이상 잠기기 전에 차량을 안전한 곳으로 이동합니다.",
            "• 이동 불가 시 시동 꺼지기 전에 창문이나 썬루프를 열어둡니다.",
            "• 차량 침수 시 문이 열리지 않으면 목받침 하단 철재봉으로 유리창을 깨고 탈출합니다.",
            "• 유리창을 못 깰 경우 차량 내외부 수위 차가 30cm 이하가 될 때까지 기다립니다.",
            "• 탈출 후 높은 곳으로 대피하고, 없으면 차량 지붕 위에서 119에 연락합니다.",
            "• 침수 도로 운전 시 저단 기어로 빠르게 벗어납니다.",
            "• 차량을 두고 대피 시 차 열쇠를 눈에 잘 띄는 곳에 두고 문은 잠그지 않습니다.",
            "• 지하차도 침수 시 절대 진입하지 않고, 진입했다면 차량을 두고 신속히 대피합니다.",
            "• 비상점멸등을 켜 뒤 차량에 위험 알립니다.",
            "• 급류가 있는 세월교는 차량 진입 금지이며, 고립 시 반대쪽 문을 열거나 창문을 깨고 탈출합니다."
        ],
        "forecast": [
            "📺 기상정보를 주변 사람들과 함께 공유합니다",
            "• TV, 라디오, 인터넷, 스마트폰(안전디딤돌 앱 등)을 활용해 호우 예보 지역과 시간을 미리 확인합니다.",
            "• 가족, 이웃, 친구들과 기상정보를 공유하고 함께 대비합니다.",
            "",
            "🏃 위험지역에 있다면 함께 안전한 곳으로 이동합니다",
            "• 산간, 계곡, 하천, 방파제 등에서 야영이나 물놀이 중일 경우 즉시 중단합니다.",
            "• 저지대, 상습 침수지역, 산사태 위험지역, 지하 공간, 노후 건물 등 위험 지역에 있다면 가족이나 주변 사람들과 함께 신속히 대피합니다.",
            "",
            "🚗 차량 및 시설물을 사전에 보호합니다",
            "• 하천, 해변, 저지대에 주차된 차량은 안전한 곳으로 이동시킵니다.",
            "• 하수구, 배수구는 막히지 않았는지 점검하고 미리 청소합니다.",
            "• 아파트 지하주차장 등 침수 우려 지역은 모래주머니, 물막이판 등을 설치하여 피해를 예방합니다.",
            "• 농경지 배수로, 공사장, 옹벽, 축대, 비탈면 등도 사전에 점검합니다.",
            "",
            "🎒 비상용품을 가족과 함께 준비합니다",
            "• 응급용품, 손전등, 식수, 휴대폰 충전기 등은 배낭 등에 미리 모아둡니다.",
            "• 상수도 중단에 대비하여 욕조 등에 물을 받아 둡니다.",
            "• 스마트폰에 안전디딤돌 앱을 설치하고, 가까운 행정복지센터(주민센터)와의 연락망도 확인합니다.",
            "",
            "🏠 외출을 자제하고 주변의 안부를 확인합니다",
            "• 호우가 예보된 날에는 약속이나 일정은 취소하거나 조정하고 외출을 자제합니다.",
            "• 어르신, 어린이, 장애인 등은 외출을 하지 않도록 도와주고, 전화나 메시지 등으로 수시로 안부를 확인합니다."
        ],
        "during": [
            "📱 외출은 자제하고 정보를 수시로 확인·공유합니다",
            "• 스마트폰 등으로 기상정보를 지속적으로 확인합니다.",
            "• 가족, 지인, 이웃과 연락해 안전 여부를 확인하고 위험 정보를 공유합니다.",
            "• 운전 시 속도를 줄이고, 개울가, 하천변, 해안가, 침수 지역 등 위험지역은 절대 접근하지 않습니다.",
            "",
            "🏠 실내에서는 미리 안전 수칙을 숙지하고 대비합니다",
            "• 건물의 출입문과 창문은 단단히 닫아 파손을 막습니다.",
            "• 창문·유리문 근처는 피하고, 창문 없는 방(예: 욕실) 또는 집 안쪽으로 이동합니다.",
            "• 가스는 사전 차단하고, 전기시설은 젖어 있을 경우 절대 손대지 않습니다.",
            "• 정전 시에는 양초 대신 휴대용 랜턴, 휴대폰 조명 등을 사용합니다.",
            "",
            "⚠️ 위험지역은 피하고, 주변 사람들과 함께 안전하게 대피합니다",
            "• 침수지역, 산간·계곡 등에 있거나 대피 권고를 받았을 경우 즉시 대피합니다.",
            "• 홀로 계신 어르신, 어린이, 장애인 등 대피가 어려운 분들을 함께 도와주세요.",
            "• 특히, 침수된 도로, 지하차도, 교량 등은 통행을 금지하고 주변 사람들에게도 진입하지 않도록 알립니다.",
            "• 공사장, 가로등, 신호등, 전신주, 지하 공간 등 위험한 곳에는 가까이 가지 않습니다.",
            "• 농촌 지역에서는 논둑이나 물꼬 점검은 하지 않습니다.",
            "• 이동식 가옥이나 임시 시설에 거주 중일 경우, 견고한 건물로 이동하고 위험지역 정보를 주변에 알려야 합니다."
        ],
        "after": [
            "👨‍👩‍👧‍👦 가족과 지인의 안전 여부를 확인합니다",
            "• 가족 및 지인에게 연락하여 안전 여부를 확인합니다.",
            "• 연락이 닿지 않고 실종이 의심되는 경우, 가까운 경찰서에 즉시 신고합니다.",
            "",
            "🏠 피해 여부를 주변 사람들과 함께 확인합니다",
            "• 대피 후 귀가했을 경우, 집의 구조적 안전 여부를 먼저 확인하고 출입합니다.",
            "• 파손된 시설물(주택, 도로, 상하수도, 축대 등)은 시·군·구청 또는 행정복지센터(주민센터)에 신고합니다.",
            "• 사유시설 복구 시 사진을 촬영해 두세요. (보험·보상 대비)",
            "• 침수된 도로, 교량, 하천 제방 등은 붕괴 위험이 있어 접근 금지합니다.",
            "• 고립된 지역에서는 무리하게 물을 건너지 말고, 119나 주변에 도움을 요청하세요.",
            "",
            "⚠️ 주변 사람들과 함께 2차 피해를 방지합니다",
            "• 물이 빠진 지역은 기름, 쓰레기, 동물 사체 등 오염물질이 많으므로 접근 금지.",
            "• 수돗물, 저장 식수는 오염 여부를 확인 후 사용합니다.",
            "• 침수된 음식 및 식재료는 절대 사용하지 마세요. (식중독 위험)",
            "• 침수된 집은 가스·전기 차단기를 확인하고,",
            "  - 한국가스안전공사(1544-4500)",
            "  - 한국전기안전공사(1588-7500) 또는 전문가 점검 후 사용하세요.",
            "• 가스 누출 우려 시 충분한 환기 후에 사용하며, 환기 전에는 성냥불·라이터 사용 금지.",
            "• 침수된 농경지는 농작물을 일으켜 세우고 흙·오물을 깨끗이 씻은 후 긴급 병해충 방제를 실시합니다."
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
        
        # 침수 상세 정보 추가 탭
        if disaster == "호우":
            st.markdown("---")
            st.markdown("## 🌊 침수 상세 행동요령")
            
            flood_tab1, flood_tab2 = st.tabs(["🏠 호우 예보 시 침수 대비", "⚠️ 호우 주의보/경보 시 침수 대응"])
            
            with flood_tab1:
                st.markdown("### 🏠 호우 예보 시 침수 대비")
                for action in guide["flood_forecast"]:
                    if action.startswith(("🏘️", "🏠", "🏢", "🚗")):
                        st.markdown(f"#### {action}")
                    elif action.startswith("•"):
                        st.write(action)
                    elif action.startswith("  "):
                        st.write(action)
                    elif action == "":
                        st.write("")
                    else:
                        st.write(action)
            
            with flood_tab2:
                st.markdown("### ⚠️ 호우 주의보/경보 시 침수 대응")
                for action in guide["flood_warning"]:
                    if action.startswith(("🚶‍♂️", "🏠", "🏢", "🚗")):
                        st.markdown(f"#### {action}")
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
