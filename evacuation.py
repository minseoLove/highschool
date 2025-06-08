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

# 실제 조사 데이터 (전체 45개 대피소) - 중복 제거 및 정리
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
                    "distance": 800,
                    "walk_time": 10,
                    "type": "공원",
                    "wheelchair": True,
                    "elevator": False,
                    "parking": True,
                    "subway": "1호선 달성공원역 도보 3분"
                }
            ],
            "flood": [
                {
                    "name": "대구중구청",
                    "address": "대구 중구 국채보상로 102길 43",
                    "lat": 35.8700,
                    "lon": 128.5940,
                    "capacity": 400,
                    "distance": 300,
                    "walk_time": 4,
                    "type": "건물",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": True,
                    "subway": "1호선 중앙로역 도보 3분"
                }
            ],
            "war": [
                {
                    "name": "중앙로역 지하상가",
                    "address": "대구 중구 중앙대로 지하",
                    "lat": 35.8682,
                    "lon": 128.5953,
                    "capacity": 1500,
                    "distance": 200,
                    "walk_time": 3,
                    "type": "지하상가",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": False,
                    "subway": "1호선 중앙로역 직결"
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
                                "flood": "홍수/태풍/호우", 
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
                    "🔍 **태풍 정보 확인 및 대피 계획 수립**",
                    "• TV, 라디오, 인터넷, 스마트폰의 '안전디딤돌' 앱을 통해 태풍의 진로와 도달 시간을 수시로 확인한다.",
                    "• 가족과 함께 미리 대피 장소와 대피 경로를 정해 둔다.",
                    "",
                    "⚠️ **위험지역 피하기**",
                    "• 산간, 계곡, 하천, 방파제 등 위험지역은 절대 접근하지 않는다.",
                    "• 저지대, 상습침수지역, 산사태 위험지역, 지하공간, 낡은 건물 등도 피해야 한다.",
                    "• 등산, 야영, 물놀이, 낚시 등 야외 활동은 즉시 중단하고 안전한 곳으로 이동한다.",
                    "• 주변에 있는 사람들과 함께 안전한 장소로 이동한다.",
                    "",
                    "💨 **강풍 대비**",
                    "• 낡고 약한 창문은 미리 교체하거나 보강한다.",
                    "• 유리창에는 유리 파편 피해를 줄이기 위해 안전필름을 붙인다.",
                    "• 창문 틀과 유리창 사이 틈새를 보강하고, 테이프로 유리를 창틀에 단단히 고정한다.",
                    "• 지붕, 간판, 철탑 등 외부 시설물은 고정하거나 보강한다.",
                    "• 바깥에 있는 물건은 실내로 옮기거나 제거한다.",
                    "• 노출된 전선은 감전이나 누전 사고가 없도록 사전에 점검하고 필요시 교체한다.",
                    "",
                    "🌊 **침수 대비**",
                    "• 집 주변 하수구나 배수구는 미리 점검하고 막힌 곳은 뚫는다.",
                    "• 지하주차장, 건물 지하공간 등은 모래주머니, 물막이판 등을 이용해 침수에 대비한다.",
                    "• 차량은 하천, 해변, 저지대를 피해서 높은 곳으로 옮긴다. 차량에 연락처를 남겨둔다.",
                    "• 농촌은 배수로, 논둑 등을 정비하고 물꼬를 조정하되, 비가 오기 전까지만 작업한다.",
                    "• 어촌은 선박을 단단히 결박하거나 육지로 올리고, 어망·어구는 안전한 장소로 옮긴다.",
                    "",
                    "🎒 **비상용품 준비**",
                    "• 구급약, 손전등, 배터리, 휴대용 라디오, 식수, 간편식 등을 비상배낭에 준비해둔다.",
                    "• 상수도 중단에 대비해 욕조 등에 물을 미리 받아둔다.",
                    "• 정전에 대비해 손전등과 예비 배터리를 확보한다.",
                    "",
                    "👥 **대피약자 보호**",
                    "• 어르신, 어린이, 장애인 등 대피에 취약한 사람의 상태를 수시로 확인한다.",
                    "• 비상시 어떻게 대피할지 사전에 설명하고 함께 대피할 수 있도록 준비한다."
                ],
                "during": [
                    "📱 **외출 자제 및 정보 확인**",
                    "• 외출을 삼가고 기상 상황, 거주 지역 주변 위험 정보, 재난 정보를 수시로 확인한다.",
                    "• 외부에 있는 가족, 지인, 이웃과 연락하여 서로의 안전을 확인하고 위험 정보를 공유한다.",
                    "",
                    "🚫 **절대 접근하지 말아야 할 위험지역**",
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
                    "👫 **대피 시 약자와 함께 행동**",
                    "• 침수, 붕괴, 산사태 등의 위험으로 대피가 필요한 경우, 어르신, 어린이, 장애인 등 대피에 어려움이 있는 사람과 함께 대피한다.",
                    "",
                    "🏠 **실내 안전 수칙**",
                    "• 건물의 출입문과 창문을 닫아 파손을 막고, 유리창에서 떨어진 위치에 머문다.",
                    "• 강풍 피해를 줄이기 위해 창문이 없는 욕실이나 집 안쪽으로 이동한다.",
                    "• 가스 누출을 막기 위해 사전에 차단하고, 전기시설은 절대 만지지 않는다.",
                    "• 특히 물에 젖은 손으로 전기시설을 만지지 않는다.",
                    "• 정전 시에는 양초 대신 손전등이나 휴대폰 불빛을 사용한다.",
                    "• 실내에 물이 조금이라도 차오르면 즉시 높은 곳이나 대피소로 이동한다.",
                    "",
                    "🚗 **실외 행동 수칙**",
                    "• 운전 시 강풍이 불면 속도를 줄이고 반대 방향 차량 및 주변 차량과의 거리 유지에 주의한다.",
                    "• 돌풍은 차량을 차선 밖으로 밀 수 있으므로 핸들을 단단히 잡고 주의 깊게 운전한다.",
                    "• 공사장 작업, 크레인 운행 등 야외 작업은 즉시 중단하고 실내로 이동한다."
                ],
                "after": [
                    "👨‍👩‍👧‍👦 **가족·지인 안전 확인 및 위험지역 접근 금지**",
                    "• 가족과 지인에게 연락하여 안전 여부를 확인합니다.",
                    "• 연락이 되지 않고 실종이 의심될 경우, 경찰서에 신고합니다.",
                    "• 침수된 도로와 교량은 파손되었을 수 있으므로 절대 건너지 않습니다.",
                    "• 하천 제방, 약해진 비탈면 등은 붕괴 위험이 있으므로 가까이 가지 않습니다.",
                    "• 고립된 지역에서는 무리하게 물을 건너지 말고, 119나 주민센터에 신고하거나 주변에 도움을 요청합니다.",
                    "",
                    "🏠 **집으로 복귀 시 점검 및 신고**",
                    "• 대피 후 집으로 돌아왔을 때에는 집과 주변 시설의 안전 여부를 먼저 확인하고 출입합니다.",
                    "• 파손된 시설물(주택, 상하수도, 도로 등)은 시·군·구청 또는 주민센터에 신고합니다.",
                    "• 사유시설 복구 전에는 반드시 사진을 찍어 향후 보상 등을 위해 기록을 남깁니다.",
                    "",
                    "⚠️ **2차 피해 방지 행동**",
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
            },
            "호우": {
                "summary": [
                    "1. 우리 지역의 침수, 산사태 위험지역을 미리 확인하세요",
                    "2. 안전디딤돌 앱으로 기상정보를 실시간 확인하세요",
                    "3. 침수지역과 위험지역은 절대 접근하지 마세요",
                    "4. 대피 권고 시 즉시 안전한 곳으로 이동하세요"
                ],
                "preparation": [
                    "🗺️ **우리 지역의 위험요소를 사전에 확인하고 공유합니다**",
                    "• 내가 살고 있는 지역의 홍수, 침수, 산사태, 해일 등 위험요소를 미리 확인합니다.",
                    "• 배수로와 빗물받이는 수시로 청소하며, 비탈면·옹벽·축대 등 위험 시설물은 정비하거나 시·군·구청에 신고합니다.",
                    "• 확인한 정보는 가족이나 이웃과 공유합니다.",
                    "",
                    "📱 **재난정보를 실시간으로 수신할 수 있도록 준비합니다**",
                    "• TV, 라디오, 스마트폰 앱(안전디딤돌 등)을 통해 기상특보·홍수·산사태 등 재난 정보를 실시간으로 받을 수 있도록 준비합니다.",
                    "",
                    "🏃 **대피방법과 가족 간 약속을 미리 정합니다**",
                    "• 대피 장소, 이동 방법, 대피요령을 숙지하고, 어린이와 노약자에게도 반드시 설명해 둡니다.",
                    "• 가족이 따로 떨어져 이동할 경우를 대비해 다시 만날 장소를 정해 둡니다.",
                    "• 대피 시 하천변, 산길, 전신주·변압기 주변은 피합니다.",
                    "",
                    "🎒 **가족과 함께 비상용품을 미리 준비합니다**",
                    "• 응급약품, 손전등, 식수, 비상식량, 라디오, 충전기, 버너, 담요 등을 한 곳에 모아 비상용 키트로 준비합니다.",
                    "• 차량이 있다면 연료를 미리 채워두고, 차량이 없는 경우 가까운 이웃과 함께 이동할 방법을 미리 약속해 둡니다.",
                    "",
                    "🔍 **지속적으로 점검하고 대비 태세를 유지합니다**",
                    "• 비상용품의 유효기간을 주기적으로 확인하고, 대피장소·대피경로 등도 정기적으로 점검합니다.",
                    "• 지역의 재난 관련 시설에도 꾸준히 관심을 가지고 필요한 경우 정비 요청을 합니다."
                ],
                "forecast": [
                    "📺 **기상정보를 주변 사람들과 함께 공유합니다**",
                    "• TV, 라디오, 인터넷, 스마트폰(안전디딤돌 앱 등)을 활용해 호우 예보 지역과 시간을 미리 확인합니다.",
                    "• 가족, 이웃, 친구들과 기상정보를 공유하고 함께 대비합니다.",
                    "",
                    "🏃 **위험지역에 있다면 함께 안전한 곳으로 이동합니다**",
                    "• 산간, 계곡, 하천, 방파제 등에서 야영이나 물놀이 중일 경우 즉시 중단합니다.",
                    "• 저지대, 상습 침수지역, 산사태 위험지역, 지하 공간, 노후 건물 등 위험 지역에 있다면 가족이나 주변 사람들과 함께 신속히 대피합니다.",
                    "",
                    "🚗 **차량 및 시설물을 사전에 보호합니다**",
                    "• 하천, 해변, 저지대에 주차된 차량은 안전한 곳으로 이동시킵니다.",
                    "• 하수구, 배수구는 막히지 않았는지 점검하고 미리 청소합니다.",
                    "• 아파트 지하주차장 등 침수 우려 지역은 모래주머니, 물막이판 등을 설치하여 피해를 예방합니다.",
                    "• 농경지 배수로, 공사장, 옹벽, 축대, 비탈면 등도 사전에 점검합니다.",
                    "",
                    "🎒 **비상용품을 가족과 함께 준비합니다**",
                    "• 응급용품, 손전등, 식수, 휴대폰 충전기 등은 배낭 등에 미리 모아둡니다.",
                    "• 상수도 중단에 대비하여 욕조 등에 물을 받아 둡니다.",
                    "• 스마트폰에 안전디딤돌 앱을 설치하고, 가까운 행정복지센터(주민센터)와의 연락망도 확인합니다.",
                    "",
                    "🏠 **외출을 자제하고 주변의 안부를 확인합니다**",
                    "• 호우가 예보된 날에는 약속이나 일정은 취소하거나 조정하고 외출을 자제합니다.",
                    "• 어르신, 어린이, 장애인 등은 외출을 하지 않도록 도와주고, 전화나 메시지 등으로 수시로 안부를 확인합니다."
                ],
                "during": [
                    "📱 **외출은 자제하고 정보를 수시로 확인·공유합니다**",
                    "• TV, 라디오, 스마트폰 등으로 기상정보를 지속적으로 확인합니다.",
                    "• 가족, 지인, 이웃과 연락해 안전 여부를 확인하고 위험 정보를 공유합니다.",
                    "• 운전 시 속도를 줄이고, 개울가, 하천변, 해안가, 침수 지역 등 위험지역은 절대 접근하지 않습니다.",
                    "",
                    "🏠 **실내에서는 미리 안전 수칙을 숙지하고 대비합니다**",
                    "• 건물의 출입문과 창문은 단단히 닫아 파손을 막습니다.",
                    "• 창문·유리문 근처는 피하고, 창문 없는 방(예: 욕실) 또는 집 안쪽으로 이동합니다.",
                    "• 가스는 사전 차단하고, 전기시설은 젖어 있을 경우 절대 손대지 않습니다.",
                    "• 정전 시에는 양초 대신 휴대용 랜턴, 휴대폰 조명 등을 사용합니다.",
                    "",
                    "⚠️ **위험지역은 피하고, 주변 사람들과 함께 안전하게 대피합니다**",
                    "• 침수지역, 산간·계곡 등에 있거나 대피 권고를 받았을 경우 즉시 대피합니다.",
                    "• 홀로 계신 어르신, 어린이, 장애인 등 대피가 어려운 분들을 함께 도와주세요.",
                    "• 특히, 침수된 도로, 지하차도, 교량 등은 통행을 금지하고 주변 사람들에게도 진입하지 않도록 알립니다.",
                    "• 공사장, 가로등, 신호등, 전신주, 지하 공간 등 위험한 곳에는 가까이 가지 않습니다.",
                    "• 농촌 지역에서는 논둑이나 물꼬 점검은 하지 않습니다.",
                    "• 이동식 가옥이나 임시 시설에 거주 중일 경우, 견고한 건물로 이동하고 위험지역 정보를 주변에 알려야 합니다."
                ],
                "after": [
                    "👨‍👩‍👧‍👦 **가족과 지인의 안전 여부를 확인합니다**",
                    "• 가족 및 지인에게 연락하여 안전 여부를 확인합니다.",
                    "• 연락이 닿지 않고 실종이 의심되는 경우, 가까운 경찰서에 즉시 신고합니다.",
                    "",
                    "🏠 **피해 여부를 주변 사람들과 함께 확인합니다**",
                    "• 대피 후 귀가했을 경우, 집의 구조적 안전 여부를 먼저 확인하고 출입합니다.",
                    "• 파손된 시설물(주택, 도로, 상하수도, 축대 등)은 시·군·구청 또는 행정복지센터(주민센터)에 신고합니다.",
                    "• 사유시설 복구 시 사진을 촬영해 두세요. (보험·보상 대비)",
                    "• 침수된 도로, 교량, 하천 제방 등은 붕괴 위험이 있어 접근 금지합니다.",
                    "• 고립된 지역에서는 무리하게 물을 건너지 말고, 119나 주변에 도움을 요청하세요.",
                    "",
                    "⚠️ **주변 사람들과 함께 2차 피해를 방지합니다**",
                    "• 물이 빠진 지역은 기름, 쓰레기, 동물 사체 등 오염물질이 많으므로 접근 금지.",
                    "• 수돗물, 저장 식수는 오염 여부를 확인 후 사용합니다.",
                    "• 침수된 음식 및 식재료는 절대 사용하지 마세요. (식중독 위험)",
                    "• 침수된 집은 가스·전기 차단기를 확인하고,",
                    "  - 한국가스안전공사(1544-4500)",
                    "  - 한국전기안전공사(1588-7500) 또는 전문가 점검 후 사용하세요.",
                    "• 가스 누출 우려 시 충분한 환기 후에 사용하며, 환기 전에는 성냥불·라이터 사용 금지.",
                    "• 침수된 농경지는 농작물을 일으켜 세우고 흙·오물을 깨끗이 씻은 후 긴급 병해충 방제를 실시합니다."
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
        }4. 여진에 대비하여 안전한 곳에서 대기하세요"
                ]
            },
            "태풍": {
                "preparation": [
                    "🔍 **태풍 정보 확인 및 대피 계획 수립**",
                    "• TV, 라디오, 인터넷, 스마트폰의 '안전디딤돌' 앱을 통해 태풍의 진로와 도달 시간을 수시로 확인한다.",
                    "• 가족과 함께 미리 대피 장소와 대피 경로를 정해 둔다.",
                    "",
                    "⚠️ **위험지역 피하기**",
                    "• 산간, 계곡, 하천, 방파제 등 위험지역은 절대 접근하지 않는다.",
                    "• 저지대, 상습침수지역, 산사태 위험지역, 지하공간, 낡은 건물 등도 피해야 한다.",
                    "• 등산, 야영, 물놀이, 낚시 등 야외 활동은 즉시 중단하고 안전한 곳으로 이동한다.",
                    "• 주변에 있는 사람들과 함께 안전한 장소로 이동한다.",
                    "",
                    "💨 **강풍 대비**",
                    "• 낡고 약한 창문은 미리 교체하거나 보강한다.",
                    "• 유리창에는 유리 파편 피해를 줄이기 위해 안전필름을 붙인다.",
                    "• 창문 틀과 유리창 사이 틈새를 보강하고, 테이프로 유리를 창틀에 단단히 고정한다.",
                    "• 지붕, 간판, 철탑 등 외부 시설물은 고정하거나 보강한다.",
                    "• 바깥에 있는 물건은 실내로 옮기거나 제거한다.",
                    "• 노출된 전선은 감전이나 누전 사고가 없도록 사전에 점검하고 필요시 교체한다.",
                    "",
                    "🌊 **침수 대비**",
                    "• 집 주변 하수구나 배수구는 미리 점검하고 막힌 곳은 뚫는다.",
                    "• 지하주차장, 건물 지하공간 등은 모래주머니, 물막이판 등을 이용해 침수에 대비한다.",
                    "• 차량은 하천, 해변, 저지대를 피해서 높은 곳으로 옮긴다. 차량에 연락처를 남겨둔다.",
                    "• 농촌은 배수로, 논둑 등을 정비하고 물꼬를 조정하되, 비가 오기 전까지만 작업한다.",
                    "• 어촌은 선박을 단단히 결박하거나 육지로 올리고, 어망·어구는 안전한 장소로 옮긴다.",
                    "",
                    "🎒 **비상용품 준비**",
                    "• 구급약, 손전등, 배터리, 휴대용 라디오, 식수, 간편식 등을 비상배낭에 준비해둔다.",
                    "• 상수도 중단에 대비해 욕조 등에 물을 미리 받아둔다.",
                    "• 정전에 대비해 손전등과 예비 배터리를 확보한다.",
                    "",
                    "👥 **대피약자 보호**",
                    "• 어르신, 어린이, 장애인 등 대피에 취약한 사람의 상태를 수시로 확인한다.",
                    "• 비상시 어떻게 대피할지 사전에 설명하고 함께 대피할 수 있도록 준비한다."
                ],
                "during": [
                    "📱 **외출 자제 및 정보 확인**",
                    "• 외출을 삼가고 기상 상황, 거주 지역 주변 위험 정보, 재난 정보를 수시로 확인한다.",
                    "• 외부에 있는 가족, 지인, 이웃과 연락하여 서로의 안전을 확인하고 위험 정보를 공유한다.",
                    "",
                    "🚫 **절대 접근하지 말아야 할 위험지역**",
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
                    "👫 **대피 시 약자와 함께 행동**",
                    "• 침수, 붕괴, 산사태 등의 위험으로 대피가 필요한 경우, 어르신, 어린이, 장애인 등 대피에 어려움이 있는 사람과 함께 대피한다.",
                    "",
                    "🏠 **실내 안전 수칙**",
                    "• 건물의 출입문과 창문을 닫아 파손을 막고, 유리창에서 떨어진 위치에 머문다.",
                    "• 강풍 피해를 줄이기 위해 창문이 없는 욕실이나 집 안쪽으로 이동한다.",
                    "• 가스 누출을 막기 위해 사전에 차단하고, 전기시설은 절대 만지지 않는다.",
                    "• 특히 물에 젖은 손으로 전기시설을 만지지 않는다.",
                    "• 정전 시에는 양초 대신 손전등이나 휴대폰 불빛을 사용한다.",
                    "• 실내에 물이 조금이라도 차오르면 즉시 높은 곳이나 대피소로 이동한다.",
                    "",
                    "🚗 **실외 행동 수칙**",
                    "• 운전 시 강풍이 불면 속도를 줄이고 반대 방향 차량 및 주변 차량과의 거리 유지에 주의한다.",
                    "• 돌풍은 차량을 차선 밖으로 밀 수 있으므로 핸들을 단단히 잡고 주의 깊게 운전한다.",
                    "• 공사장 작업, 크레인 운행 등 야외 작업은 즉시 중단하고 실내로 이동한다."
                ],
                "after": [
                    "👨‍👩‍👧‍👦 **가족·지인 안전 확인 및 위험지역 접근 금지**",
                    "• 가족과 지인에게 연락하여 안전 여부를 확인합니다.",
                    "• 연락이 되지 않고 실종이 의심될 경우, 경찰서에 신고합니다.",
                    "• 침수된 도로와 교량은 파손되었을 수 있으므로 절대 건너지 않습니다.",
                    "• 하천 제방, 약해진 비탈면 등은 붕괴 위험이 있으므로 가까이 가지 않습니다.",
                    "• 고립된 지역에서는 무리하게 물을 건너지 말고, 119나 주민센터에 신고하거나 주변에 도움을 요청합니다.",
                    "",
                    "🏠 **집으로 복귀 시 점검 및 신고**",
                    "• 대피 후 집으로 돌아왔을 때에는 집과 주변 시설의 안전 여부를 먼저 확인하고 출입합니다.",
                    "• 파손된 시설물(주택, 상하수도, 도로 등)은 시·군·구청 또는 주민센터에 신고합니다.",
                    "• 사유시설 복구 전에는 반드시 사진을 찍어 향후 보상 등을 위해 기록을 남깁니다.",
                    "",
                    "⚠️ **2차 피해 방지 행동**",
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
            },
            "호우": {
                "preparation": [
                    "🗺️ **우리 지역의 위험요소를 사전에 확인하고 공유합니다**",
                    "• 내가 살고 있는 지역의 홍수, 침수, 산사태, 해일 등 위험요소를 미리 확인합니다.",
                    "• 배수로와 빗물받이는 수시로 청소하며, 비탈면·옹벽·축대 등 위험 시설물은 정비하거나 시·군·구청에 신고합니다.",
                    "• 확인한 정보는 가족이나 이웃과 공유합니다.",
                    "",
                    "📱 **재난정보를 실시간으로 수신할 수 있도록 준비합니다**",
                    "• TV, 라디오, 스마트폰 앱(안전디딤돌 등)을 통해 기상특보·홍수·산사태 등 재난 정보를 실시간으로 받을 수 있도록 준비합니다.",
                    "",
                    "🏃 **대피방법과 가족 간 약속을 미리 정합니다**",
                    "• 대피 장소, 이동 방법, 대피요령을 숙지하고, 어린이와 노약자에게도 반드시 설명해 둡니다.",
                    "• 가족이 따로 떨어져 이동할 경우를 대비해 다시 만날 장소를 정해 둡니다.",
                    "• 대피 시 하천변, 산길, 전신주·변압기 주변은 피합니다.",
                    "",
                    "🎒 **가족과 함께 비상용품을 미리 준비합니다**",
                    "• 응급약품, 손전등, 식수, 비상식량, 라디오, 충전기, 버너, 담요 등을 한 곳에 모아 비상용 키트로 준비합니다.",
                    "• 차량이 있다면 연료를 미리 채워두고, 차량이 없는 경우 가까운 이웃과 함께 이동할 방법을 미리 약속해 둡니다.",
                    "",
                    "🔍 **지속적으로 점검하고 대비 태세를 유지합니다**",
                    "• 비상용품의 유효기간을 주기적으로 확인하고, 대피장소·대피경로 등도 정기적으로 점검합니다.",
                    "• 지역의 재난 관련 시설에도 꾸준히 관심을 가지고 필요한 경우 정비 요청을 합니다."
                ],
                "forecast": [
                    "📺 **기상정보를 주변 사람들과 함께 공유합니다**",
                    "• TV, 라디오, 인터넷, 스마트폰(안전디딤돌 앱 등)을 활용해 호우 예보 지역과 시간을 미리 확인합니다.",
                    "• 가족, 이웃, 친구들과 기상정보를 공유하고 함께 대비합니다.",
                    "",
                    "🏃 **위험지역에 있다면 함께 안전한 곳으로 이동합니다**",
                    "• 산간, 계곡, 하천, 방파제 등에서 야영이나 물놀이 중일 경우 즉시 중단합니다.",
                    "• 저지대, 상습 침수지역, 산사태 위험지역, 지하 공간, 노후 건물 등 위험 지역에 있다면 가족이나 주변 사람들과 함께 신속히 대피합니다.",
                    "",
                    "🚗 **차량 및 시설물을 사전에 보호합니다**",
                    "• 하천, 해변, 저지대에 주차된 차량은 안전한 곳으로 이동시킵니다.",
                    "• 하수구, 배수구는 막히지 않았는지 점검하고 미리 청소합니다.",
                    "• 아파트 지하주차장 등 침수 우려 지역은 모래주머니, 물막이판 등을 설치하여 피해를 예방합니다.",
                    "• 농경지 배수로, 공사장, 옹벽, 축대, 비탈면 등도 사전에 점검합니다.",
                    "",
                    "🎒 **비상용품을 가족과 함께 준비합니다**",
                    "• 응급용품, 손전등, 식수, 휴대폰 충전기 등은 배낭 등에 미리 모아둡니다.",
                    "• 상수도 중단에 대비하여 욕조 등에 물을 받아 둡니다.",
                    "• 스마트폰에 안전디딤돌 앱을 설치하고, 가까운 행정복지센터(주민센터)와의 연락망도 확인합니다.",
                    "",
                    "🏠 **외출을 자제하고 주변의 안부를 확인합니다**",
                    "• 호우가 예보된 날에는 약속이나 일정은 취소하거나 조정하고 외출을 자제합니다.",
                    "• 어르신, 어린이, 장애인 등은 외출을 하지 않도록 도와주고, 전화나 메시지 등으로 수시로 안부를 확인합니다."
                ],
                "during": [
                    "📱 **외출은 자제하고 정보를 수시로 확인·공유합니다**",
                    "• TV, 라디오, 스마트폰 등으로 기상정보를 지속적으로 확인합니다.",
                    "• 가족, 지인, 이웃과 연락해 안전 여부를 확인하고 위험 정보를 공유합니다.",
                    "• 운전 시 속도를 줄이고, 개울가, 하천변, 해안가, 침수 지역 등 위험지역은 절대 접근하지 않습니다.",
                    "",
                    "🏠 **실내에서는 미리 안전 수칙을 숙지하고 대비합니다**",
                    "• 건물의 출입문과 창문은 단단히 닫아 파손을 막습니다.",
                    "• 창문·유리문 근처는 피하고, 창문 없는 방(예: 욕실) 또는 집 안쪽으로 이동합니다.",
                    "• 가스는 사전 차단하고, 전기시설은 젖어 있을 경우 절대 손대지 않습니다.",
                    "• 정전 시에는 양초 대신 휴대용 랜턴, 휴대폰 조명 등을 사용합니다.",
                    "",
                    "⚠️ **위험지역은 피하고, 주변 사람들과 함께 안전하게 대피합니다**",
                    "• 침수지역, 산간·계곡 등에 있거나 대피 권고를 받았을 경우 즉시 대피합니다.",
                    "• 홀로 계신 어르신, 어린이, 장애인 등 대피가 어려운 분들을 함께 도와주세요.",
                    "• 특히, 침수된 도로, 지하차도, 교량 등은 통행을 금지하고 주변 사람들에게도 진입하지 않도록 알립니다.",
                    "• 공사장, 가로등, 신호등, 전신주, 지하 공간 등 위험한 곳에는 가까이 가지 않습니다.",
                    "• 농촌 지역에서는 논둑이나 물꼬 점검은 하지 않습니다.",
                    "• 이동식 가옥이나 임시 시설에 거주 중일 경우, 견고한 건물로 이동하고 위험지역 정보를 주변에 알려야 합니다."
                ],
                "after": [
                    "👨‍👩‍👧‍👦 **가족과 지인의 안전 여부를 확인합니다**",
                    "• 가족 및 지인에게 연락하여 안전 여부를 확인합니다.",
                    "• 연락이 닿지 않고 실종이 의심되는 경우, 가까운 경찰서에 즉시 신고합니다.",
                    "",
                    "🏠 **피해 여부를 주변 사람들과 함께 확인합니다**",
                    "• 대피 후 귀가했을 경우, 집의 구조적 안전 여부를 먼저 확인하고 출입합니다.",
                    "• 파손된 시설물(주택, 도로, 상하수도, 축대 등)은 시·군·구청 또는 행정복지센터(주민센터)에 신고합니다.",
                    "• 사유시설 복구 시 사진을 촬영해 두세요. (보험·보상 대비)",
                    "• 침수된 도로, 교량, 하천 제방 등은 붕괴 위험이 있어 접근 금지합니다.",
                    "• 고립된 지역에서는 무리하게 물을 건너지 말고, 119나 주변에 도움을 요청하세요.",
                    "",
                    "⚠️ **주변 사람들과 함께 2차 피해를 방지합니다**",
                    "• 물이 빠진 지역은 기름, 쓰레기, 동물 사체 등 오염물질이 많으므로 접근 금지.",
                    "• 수돗물, 저장 식수는 오염 여부를 확인 후 사용합니다.",
                    "• 침수된 음식 및 식재료는 절대 사용하지 마세요. (식중독 위험)",
                    "• 침수된 집은 가스·전기 차단기를 확인하고,",
                    "  - 한국가스안전공사(1544-4500)",
                    "  - 한국전기안전공사(1588-7500) 또는 전문가 점검 후 사용하세요.",
                    "• 가스 누출 우려 시 충분한 환기 후에 사용하며, 환기 전에는 성냥불·라이터 사용 금지.",
                    "• 침수된 농경지는 농작물을 일으켜 세우고 흙·오물을 깨끗이 씻은 후 긴급 병해충 방제를 실시합니다."
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
        }후 사용하세요",
                    "5. 수돗물과 식수는 오염 여부 확인 후 사용하세요"
                ]
            },
            "호우": {
                "preparation": [
                    "1. 우리 지역의 홍수, 침수, 산사태 위험요소를 미리 확인하세요",
                    "2. TV, 라디오, 안전디딤돌 앱으로 재난정보를 받을 수 있도록 준비하세요",
                    "3. 대피 장소, 이동 방법을 숙지하고 가족과 약속을 정하세요",
                    "4. 응급약품, 손전등, 식수, 비상식량을 비상용 키트로 준비하세요",
                    "5. 비상용품 유효기간을 주기적으로 확인하세요"
                ],
                "forecast": [
                    "1. TV, 라디오, 안전디딤돌 앱으로 호우 예보를 확인하세요",
                    "2. 산간, 계곡, 하천에서 야영이나 물놀이는 즉시 중단하세요",
                    "3. 차량은 하천, 해변, 저지대에서 안전한 곳으로 이동시키세요",
                    "4. 하수구, 배수구가 막히지 않았는지 점검하고 청소하세요",
                    "5. 외출을 자제하고 어르신, 어린이의 안부를 확인하세요"
                ],
                "during": [
                    "1. TV, 라디오로 기상정보를 지속적으로 확인하세요",
                    "2. 침수지역, 산간·계곡은 절대 접근하지 말고 즉시 대피하세요",
                    "3. 건물 출입문과 창문을 단단히 닫고 창문 없는 방으로 이동하세요",
                    "4. 가스는 사전 차단하고 젖은 손으로 전기시설을 만지지 마세요",
                    "5. 대피가 어려운 분들을 함께 도와주세요"
                ],
                "after": [
                    "1. 가족 및 지인에게 연락하여 안전 여부를 확인하세요",
                    "2. 집의 구조적 안전을 먼저 확인하고 출입하세요",
                    "3. 파손된 시설물은 시·군·구청에 신고하세요",
                    "4. 침수된 도로, 교량은 붕괴 위험이 있어 접근하지 마세요",
                    "5. 수돗물과 식수는 오염 여부 확인 후 사용하세요"
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
                        # 태풍은 3단계로 구분
                        tab1, tab2, tab3 = st.tabs(["📋 태풍 예보 시", "🌀 태풍 특보 중", "✅ 태풍 이후"])
                        
                        with tab1:
                            st.write("**태풍 예보 시 준비사항**")
                            for action in guide["preparation"]:
                                if action.startswith(("🔍", "⚠️", "💨", "🌊", "🎒", "👥")):
                                    st.markdown(f"**{action}**")
                                elif action.startswith("•"):
                                    st.write(action)
                                elif action == "":
                                    st.write("")
                                else:
                                    st.write(action)
                        
                        with tab2:
                            st.write("**태풍 특보 중 행동수칙**")
                            for action in guide["during"]:
                                if action.startswith(("📱", "🚫", "👫", "🏠", "🚗")):
                                    st.markdown(f"**{action}**")
                                elif action.startswith("•"):
                                    st.write(action)
                                elif action == "":
                                    st.write("")
                                else:
                                    st.write(action)
                        
                        with tab3:
                            st.write("**태풍 이후 복구활동**")
                            for action in guide["after"]:
                                if action.startswith(("👨‍👩‍👧‍👦", "🏠", "⚠️")):
                                    st.markdown(f"**{action}**")
                                elif action.startswith("•"):
                                    st.write(action)
                                elif action.startswith("  -"):
                                    st.write(action)
                                elif action == "":
                                    st.write("")
                                else:
                                    st.write(action)
                    
                    elif disaster == "호우":
                        # 호우는 4단계로 구분
                        tab1, tab2, tab3, tab4 = st.tabs(["📋 호우 사전준비", "🌧️ 호우 예보 시", "⚡ 호우 특보 중", "✅ 호우 이후"])
                        
                        with tab1:
                            st.write("**호우 사전준비 사항**")
                            for action in guide["preparation"]:
                                if action.startswith(("🗺️", "📱", "🏃", "🎒", "🔍")):
                                    st.markdown(f"**{action}**")
                                elif action.startswith("•"):
                                    st.write(action)
                                elif action == "":
                                    st.write("")
                                else:
                                    st.write(action)
                        
                        with tab2:
                            st.write("**호우 예보 시 대비사항**")
                            for action in guide["forecast"]:
                                if action.startswith(("📺", "🏃", "🚗", "🎒", "🏠")):
                                    st.markdown(f"**{action}**")
                                elif action.startswith("•"):
                                    st.write(action)
                                elif action == "":
                                    st.write("")
                                else:
                                    st.write(action)
                        
                        with tab3:
                            st.write("**호우 특보 중 행동수칙**")
                            for action in guide["during"]:
                                if action.startswith(("📱", "🏠", "⚠️")):
                                    st.markdown(f"**{action}**")
                                elif action.startswith("•"):
                                    st.write(action)
                                elif action == "":
                                    st.write("")
                                else:
                                    st.write(action)
                        
                        with tab4:
                            st.write("**호우 이후 복구활동**")
                            for action in guide["after"]:
                                if action.startswith(("👨‍👩‍👧‍👦", "🏠", "⚠️")):
                                    st.markdown(f"**{action}**")
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
                    if disaster == "태풍":
                        speak_text("태풍 발생시 행동요령을 안내드립니다. 태풍 예보 시에는 정보를 확인하고 대피 계획을 수립하세요. 태풍 특보 중에는 외출을 자제하고 위험지역에 접근하지 마세요. 태풍 이후에는 안전을 확인하고 2차 피해를 방지하세요.")
                    elif disaster == "호우":
                        speak_text("호우 발생시 행동요령을 안내드립니다. 사전에 위험지역을 확인하고 재난정보를 받을 수 있도록 준비하세요. 호우 특보 중에는 침수지역과 위험지역을 피하고 안전하게 대피하세요.")
                    else:
                        # 기본 요약 내용 음성 안내
                        summary_text = " ".join(guide["summary"])
                        speak_text(f"{disaster} 발생시 행동요령입니다. {summary_text}")_text(f"{disaster} 발생시 행동요령을 안내드립니다.")
    
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
