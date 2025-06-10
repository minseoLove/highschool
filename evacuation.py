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

# 음성 안내 기능
def speak_text(text, custom_speed=None):
    """개선된 음성 안내 기능"""
    if st.session_state.get('voice_enabled', False):
        # 음성 속도 설정 (사이드바 설정값 우선 사용)
        speed = custom_speed if custom_speed else st.session_state.get('voice_speed', 1.0)
        
        # 텍스트 정리 (이모지와 마크다운 제거)
        clean_text = text.replace("**", "").replace("*", "").replace("#", "").replace("•", "")
        clean_text = clean_text.replace("🔍", "").replace("⚠️", "").replace("💨", "").replace("🌊", "")
        clean_text = clean_text.replace("🎒", "").replace("👥", "").replace("📱", "").replace("🚫", "")
        clean_text = clean_text.replace("👫", "").replace("🏠", "").replace("🚗", "").replace("🔊", "")
        clean_text = clean_text.replace("✅", "").replace("❌", "").replace("📍", "").replace("🏥", "")
        
        # 긴 텍스트는 자르기 (300자 제한)
        if len(clean_text) > 300:
            clean_text = clean_text[:297] + "..."
        
        # 음성 안내 표시
        st.info(f"🔊 음성 안내 (속도: {speed}x): {clean_text[:50]}{'...' if len(clean_text) > 50 else ''}")
        
        # 고유한 ID 생성 (충돌 방지)
        speech_id = f"speech_{abs(hash(text)) % 10000}_{int(time.time() * 1000) % 10000}"
        
        # JavaScript로 음성 합성 (개선된 버전)
        speech_js = f"""
        <div id="{speech_id}">
            <script>
            (function() {{
                // 전역 음성 상태 관리
                if (!window.currentSpeech) {{
                    window.currentSpeech = null;
                    window.speechQueue = [];
                }}
                
                function speakText_{speech_id}() {{
                    try {{
                        // 기존 음성 중지
                        if (window.speechSynthesis) {{
                            window.speechSynthesis.cancel();
                        }}
                        
                        if ('speechSynthesis' in window) {{
                            // 새로운 음성 생성
                            var utterance = new SpeechSynthesisUtterance(`{clean_text}`);
                            utterance.lang = 'ko-KR';
                            utterance.rate = {speed};
                            utterance.pitch = 1.0;
                            utterance.volume = 0.9;
                            
                            // 현재 음성 저장
                            window.currentSpeech = utterance;
                            
                            // 이벤트 핸들러
                            utterance.onstart = function() {{
                                console.log('음성 재생 시작: {speech_id}');
                            }};
                            
                            utterance.onend = function() {{
                                console.log('음성 재생 완료: {speech_id}');
                                window.currentSpeech = null;
                            }};
                            
                            utterance.onerror = function(event) {{
                                console.error('음성 오류:', event.error);
                                window.currentSpeech = null;
                            }};
                            
                            // 음성 재생 (약간의 지연 후)
                            setTimeout(function() {{
                                if (window.speechSynthesis) {{
                                    window.speechSynthesis.speak(utterance);
                                }}
                            }}, 100);
                            
                        }} else {{
                            console.error('브라우저가 음성 합성을 지원하지 않습니다.');
                        }}
                    }} catch (error) {{
                        console.error('음성 재생 중 오류:', error);
                    }}
                }}
                
                // 전역 중지 함수
                window.stopCurrentSpeech = function() {{
                    if (window.speechSynthesis) {{
                        window.speechSynthesis.cancel();
                        window.currentSpeech = null;
                        console.log('음성 중지됨');
                    }}
                }};
                
                // 음성 재생 실행
                speakText_{speech_id}();
            }})();
            </script>
        </div>
        """
        
        # JavaScript 실행
        st.components.v1.html(speech_js, height=0)
        
        # 음성 제어 버튼들 (더 안정적으로 구현)
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("⏹️ 음성 중지", key=f"stop_{speech_id}"):
                # 즉시 음성 중지
                stop_js = """
                <script>
                try {
                    if (window.speechSynthesis) {
                        window.speechSynthesis.cancel();
                    }
                    if (window.stopCurrentSpeech) {
                        window.stopCurrentSpeech();
                    }
                    console.log('음성 중지 버튼 클릭됨');
                } catch(e) {
                    console.error('음성 중지 오류:', e);
                }
                </script>
                """
                st.components.v1.html(stop_js, height=0)
                st.success("✅ 음성이 중지되었습니다.")
        
        with col2:
            if st.button("🔄 다시 듣기", key=f"replay_{speech_id}"):
                # 다시 듣기 (재귀 호출 방지)
                st.rerun()
        
        with col3:
            # 속도 조절 버튼
            if st.button("⚡ 빠르게", key=f"fast_{speech_id}"):
                st.session_state.voice_speed = min(2.0, st.session_state.get('voice_speed', 1.0) + 0.2)
                speak_text(text, st.session_state.voice_speed)
                
    else:
        st.warning("🔊 음성 안내가 비활성화되어 있습니다. 사이드바에서 활성화해주세요.")

def show_privacy_consent():
    """개인정보 활용동의 페이지"""
    st.markdown('<h1 class="main-header">🚨 재난 대피소 안내 시스템</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 18px; color: #6B7280;">안전한 대피를 위한 맞춤형 안내 서비스</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("## 📋 개인정보 활용동의")
    
    with st.expander("📖 개인정보 처리방침 전문 보기 (필독)", expanded=True):
        st.markdown("""
        ### 🔐 **개인정보 처리방침**
        
        **📍 수집하는 개인정보 항목**
        - 현재 위치 정보 (지역 선택)
        - 연령대 정보  
        - 장애 유형 (해당 시)
        - 보호자 연락처 (고령자/장애인용, 선택사항)
        
        **🎯 개인정보 수집 및 이용 목적**
        - 재난 발생 시 최적의 대피소 안내
        - 사용자 특성에 맞는 맞춤형 안전 정보 제공
        - 접근성을 고려한 대피 경로 안내
        
        **⏰ 개인정보 보유 및 이용기간**
        - 서비스 이용 기간 동안만 임시 저장
        - 브라우저 종료 시 모든 정보 자동 삭제
        - 별도 서버 저장 없음 (로컬 세션만 활용)
        
        **🔒 개인정보 보호 조치**
        - 모든 정보는 브라우저 내에서만 처리
        - 외부 서버 전송 없음
        - 제3자 제공 절대 금지
        """)
    
    st.markdown("---")
    st.markdown("### ✅ **동의 항목**")
    
    essential_consent = st.checkbox(
        "개인정보 수집 및 이용에 동의합니다. (필수)", 
        key="privacy_essential_consent"
    )
    
    optional_consent = st.checkbox(
        "맞춤형 안전정보 제공을 위한 개인정보 활용에 동의합니다. (선택)", 
        key="privacy_optional_consent"
    )
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("❌ 동의하지 않음", type="secondary", key="privacy_disagree"):
            st.warning("⚠️ 필수 개인정보 처리에 동의하지 않으면 서비스를 이용할 수 없습니다.")
    
    with col2:
        if st.button("✅ 동의하고 시작", type="primary", disabled=not essential_consent, key="privacy_agree"):
            if essential_consent:
                st.session_state.privacy_consent = True
                st.session_state.privacy_essential_agreed = essential_consent
                st.session_state.privacy_optional_agreed = optional_consent
                st.session_state.consent_timestamp = datetime.now()
                
                st.success("✅ 개인정보 활용동의가 완료되었습니다!")
                time.sleep(1)
                st.rerun()

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
                    "name": "강남구청 광장",
                    "address": "서울 강남구 학동로 426",
                    "lat": 37.5172,
                    "lon": 127.0473,
                    "capacity": 1500,
                    "distance": 600,
                    "walk_time": 8,
                    "type": "공원",
                    "wheelchair": True,
                    "elevator": False,
                    "parking": True,
                    "subway": "7호선 강남구청역 도보 1분"
                },
                {
                    "name": "선릉공원",
                    "address": "서울 강남구 선릉로 100길 1",
                    "lat": 37.5044,
                    "lon": 127.0486,
                    "capacity": 2000,
                    "distance": 900,
                    "walk_time": 12,
                    "type": "공원",
                    "wheelchair": True,
                    "elevator": False,
                    "parking": True,
                    "subway": "2호선/분당선 선릉역 도보 5분"
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
                    "name": "강남문화재단",
                    "address": "서울 강남구 강남대로 지하 390",
                    "lat": 37.4979,
                    "lon": 127.0276,
                    "capacity": 800,
                    "distance": 500,
                    "walk_time": 6,
                    "type": "문화시설",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": True,
                    "subway": "2호선/신분당선 강남역 도보 3분"
                },
                {
                    "name": "코엑스 컨벤션센터",
                    "address": "서울 강남구 영동대로 513",
                    "lat": 37.5115,
                    "lon": 127.0595,
                    "capacity": 5000,
                    "distance": 1200,
                    "walk_time": 15,
                    "type": "컨벤션센터",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": True,
                    "subway": "2호선 삼성역 도보 8분"
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
                    "name": "선릉역 지하도상가",
                    "address": "서울 강남구 선릉로 지하 428",
                    "lat": 37.5044,
                    "lon": 127.0486,
                    "capacity": 1500,
                    "distance": 800,
                    "walk_time": 10,
                    "type": "지하상가",
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
                    "name": "탑골공원",
                    "address": "서울 종로구 종로 99",
                    "lat": 37.5702,
                    "lon": 126.9883,
                    "capacity": 1000,
                    "distance": 400,
                    "walk_time": 5,
                    "type": "공원",
                    "wheelchair": False,
                    "elevator": False,
                    "parking": False,
                    "subway": "1호선 종각역 도보 3분"
                },
                {
                    "name": "광화문 광장",
                    "address": "서울 종로구 세종대로 175",
                    "lat": 37.5720,
                    "lon": 126.9769,
                    "capacity": 5000,
                    "distance": 800,
                    "walk_time": 10,
                    "type": "광장",
                    "wheelchair": True,
                    "elevator": False,
                    "parking": True,
                    "subway": "5호선 광화문역 도보 1분"
                }
            ],
            "flood": [
                {
                    "name": "종로구청",
                    "address": "서울 종로구 종로 1길 36",
                    "lat": 37.5735,
                    "lon": 126.9788,
                    "capacity": 300,
                    "distance": 300,
                    "walk_time": 4,
                    "type": "관공서",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": True,
                    "subway": "1호선 종각역 도보 5분"
                }
            ],
            "war": [
                {
                    "name": "지하철 종각역 대합실",
                    "address": "서울 종로구 종로 지하 51",
                    "lat": 37.5702,
                    "lon": 126.9883,
                    "capacity": 2000,
                    "distance": 200,
                    "walk_time": 3,
                    "type": "지하철역",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": False,
                    "subway": "1호선 종각역 직결"
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
                    "distance": 300,
                    "walk_time": 4,
                    "type": "해변광장",
                    "wheelchair": True,
                    "elevator": False,
                    "parking": True,
                    "subway": "부산지하철 2호선 해운대역 도보 3분"
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
                    "subway": "부산지하철 2호선 센텀시티역 도보 5분"
                },
                {
                    "name": "해운대스포츠센터",
                    "address": "부산 해운대구 해운대해변로 84",
                    "lat": 35.1598,
                    "lon": 129.1585,
                    "capacity": 2000,
                    "distance": 500,
                    "walk_time": 6,
                    "type": "운동장",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": True,
                    "subway": "부산지하철 2호선 해운대역 도보 7분"
                }
            ],
            "flood": [
                {
                    "name": "해운대구청사",
                    "address": "부산 해운대구 해운대로 570",
                    "lat": 35.1631,
                    "lon": 129.1635,
                    "capacity": 200,
                    "distance": 400,
                    "walk_time": 5,
                    "type": "관공서 고지대",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": True,
                    "subway": "부산지하철 2호선 해운대역 도보 6분"
                },
                {
                    "name": "LCT 더샵",
                    "address": "부산 해운대구 우동 1394",
                    "lat": 35.1587,
                    "lon": 129.1604,
                    "capacity": 1000,
                    "distance": 200,
                    "walk_time": 3,
                    "type": "고층건물 3층 이상",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": True,
                    "subway": "부산지하철 2호선 해운대역 도보 2분"
                },
                {
                    "name": "달맞이길 공원",
                    "address": "부산 해운대구 달맞이길",
                    "lat": 35.1535,
                    "lon": 129.1732,
                    "capacity": 800,
                    "distance": 1200,
                    "walk_time": 15,
                    "type": "고지대 공원 (해발 30m)",
                    "wheelchair": False,
                    "elevator": False,
                    "parking": True,
                    "subway": "부산지하철 2호선 해운대역 도보 20분"
                }
            ],
            "war": [
                {
                    "name": "해운대역 지하상가",
                    "address": "부산 해운대구 해운대로 지하",
                    "lat": 35.1593,
                    "lon": 129.1586,
                    "capacity": 2000,
                    "distance": 100,
                    "walk_time": 2,
                    "type": "지하상가",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": False,
                    "subway": "부산지하철 2호선 해운대역 직결"
                },
                {
                    "name": "센텀시티역 지하공간",
                    "address": "부산 해운대구 센텀중앙로 지하",
                    "lat": 35.1693,
                    "lon": 129.1295,
                    "capacity": 1800,
                    "distance": 600,
                    "walk_time": 8,
                    "type": "지하상가",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": False,
                    "subway": "부산지하철 2호선 센텀시티역 직결"
                }
            ]
        },
        
        "부산진구": {
            "earthquake": [
                {
                    "name": "서면 시민공원",
                    "address": "부산 부산진구 중앙대로 지하",
                    "lat": 35.1579,
                    "lon": 129.0596,
                    "capacity": 2500,
                    "distance": 400,
                    "walk_time": 5,
                    "type": "공원",
                    "wheelchair": True,
                    "elevator": False,
                    "parking": True,
                    "subway": "부산지하철 1,2호선 서면역 도보 5분"
                },
                {
                    "name": "부산시민공원",
                    "address": "부산 부산진구 시민공원로 73",
                    "lat": 35.1663,
                    "lon": 129.0535,
                    "capacity": 8000,
                    "distance": 800,
                    "walk_time": 10,
                    "type": "대형공원",
                    "wheelchair": True,
                    "elevator": False,
                    "parking": True,
                    "subway": "부산지하철 1호선 부전역 도보 12분"
                }
            ],
            "flood": [
                {
                    "name": "부산진구청",
                    "address": "부산 부산진구 시민공원로 30",
                    "lat": 35.1622,
                    "lon": 129.0539,
                    "capacity": 400,
                    "distance": 600,
                    "walk_time": 8,
                    "type": "관공서",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": True,
                    "subway": "부산지하철 1호선 부전역 도보 10분"
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
                    "subway": "부산지하철 1,2호선 서면역 직결"
                },
                {
                    "name": "양정역 지하공간",
                    "address": "부산 부산진구 양정로 지하",
                    "lat": 35.1697,
                    "lon": 129.0720,
                    "capacity": 1500,
                    "distance": 300,
                    "walk_time": 4,
                    "type": "지하철역",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": False,
                    "subway": "부산지하철 1호선 양정역 직결"
                }
            ]
        },
        
        "대구중구": {
            "earthquake": [
                {
                    "name": "국채보상운동기념공원",
                    "address": "대구 중구 공평로",
                    "lat": 35.8682,
                    "lon": 128.5953,
                    "capacity": 3000,
                    "distance": 500,
                    "walk_time": 7,
                    "type": "공원",
                    "wheelchair": True,
                    "elevator": False,
                    "parking": True,
                    "subway": "대구1호선 중앙로역 도보 8분"
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
                    "subway": "대구1호선 달성공원역 도보 3분"
                }
            ],
            "flood": [
                {
                    "name": "대구중구청",
                    "address": "대구 중구 국채보상로 102길 88",
                    "lat": 35.8703,
                    "lon": 128.5911,
                    "capacity": 300,
                    "distance": 400,
                    "walk_time": 5,
                    "type": "관공서",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": True,
                    "subway": "대구1호선 중앙로역 도보 6분"
                }
            ],
            "war": [
                {
                    "name": "반월당 지하상가",
                    "address": "대구 중구 달구벌대로 지하",
                    "lat": 35.8581,
                    "lon": 128.5933,
                    "capacity": 2500,
                    "distance": 200,
                    "walk_time": 3,
                    "type": "지하상가",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": False,
                    "subway": "대구1,2호선 반월당역 직결"
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
                    "distance": 1200,
                    "walk_time": 15,
                    "type": "축구장",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": True,
                    "subway": "1호선 수원역 도보 18분"
                },
                {
                    "name": "효원공원",
                    "address": "경기 수원시 팔달구 인계로 178",
                    "lat": 37.2642,
                    "lon": 127.0286,
                    "capacity": 2000,
                    "distance": 500,
                    "walk_time": 7,
                    "type": "공원",
                    "wheelchair": True,
                    "elevator": False,
                    "parking": True,
                    "subway": "1호선 수원역 도보 8분"
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
                    "subway": "1호선 화서역 도보 20분"
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
                    "type": "관공서",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": True,
                    "subway": "1호선 수원역 도보 10분"
                },
                {
                    "name": "팔달구청",
                    "address": "경기 수원시 팔달구 효원로 1",
                    "lat": 37.2658,
                    "lon": 127.0298,
                    "capacity": 500,
                    "distance": 400,
                    "walk_time": 5,
                    "type": "관공서",
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
                    "distance": 100,
                    "walk_time": 2,
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
                    "distance": 300,
                    "walk_time": 4,
                    "type": "지하상가",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": False,
                    "subway": "1호선 수원역 도보 5분"
                }
            ]
        },
        
        "성남시": {
            "earthquake": [
                {
                    "name": "분당중앙공원",
                    "address": "경기 성남시 분당구 야탑로 215",
                    "lat": 37.3515,
                    "lon": 127.1240,
                    "capacity": 4000,
                    "distance": 600,
                    "walk_time": 8,
                    "type": "대형공원",
                    "wheelchair": True,
                    "elevator": False,
                    "parking": True,
                    "subway": "분당선 야탑역 도보 8분"
                },
                {
                    "name": "탄천종합운동장",
                    "address": "경기 성남시 분당구 탄천로 215",
                    "lat": 37.4058,
                    "lon": 127.1235,
                    "capacity": 6000,
                    "distance": 1000,
                    "walk_time": 12,
                    "type": "운동장",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": True,
                    "subway": "분당선 수내역 도보 15분"
                },
                {
                    "name": "성남종합운동장",
                    "address": "경기 성남시 중원구 성남대로 1",
                    "lat": 37.4198,
                    "lon": 127.1265,
                    "capacity": 4500,
                    "distance": 800,
                    "walk_time": 10,
                    "type": "운동장",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": True,
                    "subway": "분당선 이매역 도보 12분"
                }
            ],
            "flood": [
                {
                    "name": "성남시청",
                    "address": "경기 성남시 중원구 성남대로 997",
                    "lat": 37.4198,
                    "lon": 127.1265,
                    "capacity": 1000,
                    "distance": 500,
                    "walk_time": 7,
                    "type": "관공서",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": True,
                    "subway": "분당선 이매역 도보 8분"
                },
                {
                    "name": "분당구청",
                    "address": "경기 성남시 분당구 야탑로 50",
                    "lat": 37.3515,
                    "lon": 127.1240,
                    "capacity": 600,
                    "distance": 400,
                    "walk_time": 5,
                    "type": "관공서",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": True,
                    "subway": "분당선 야탑역 도보 5분"
                }
            ],
            "war": [
                {
                    "name": "야탑역 지하상가",
                    "address": "경기 성남시 분당구 야탑로 지하",
                    "lat": 37.3515,
                    "lon": 127.1240,
                    "capacity": 2500,
                    "distance": 200,
                    "walk_time": 3,
                    "type": "지하상가",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": False,
                    "subway": "분당선 야탑역 직결"
                },
                {
                    "name": "서현역 지하상가",
                    "address": "경기 성남시 분당구 서현로 지하",
                    "lat": 37.3836,
                    "lon": 127.1230,
                    "capacity": 2000,
                    "distance": 600,
                    "walk_time": 8,
                    "type": "지하상가",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": False,
                    "subway": "분당선 서현역 직결"
                }
            ]
        },

        "중랑구": {
            "flood": [
                {
                    "name": "건영1차아파트 지하주차장",
                    "address": "서울특별시 중랑구 봉화산로48길 62 (상봉동)",
                    "lat": 37.5954,
                    "lon": 127.0855,
                    "capacity": 8875,
                    "distance": 300,
                    "walk_time": 4,
                    "type": "지하주차장 1~2층",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": True,
                    "subway": "7호선 상봉역 도보 5분"
                },
                {
                    "name": "SM해그린아파트 지하주차장",
                    "address": "서울특별시 중랑구 공릉로2나길 32-12 (묵동)",
                    "lat": 37.6126,
                    "lon": 127.0776,
                    "capacity": 2701,
                    "distance": 500,
                    "walk_time": 7,
                    "type": "지하주차장 1층",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": True,
                    "subway": "7호선 먹골역 도보 8분"
                },
                {
                    "name": "건영빌라트 지하주차장",
                    "address": "서울특별시 중랑구 동일로91가길 30 (면목동)",
                    "lat": 37.5847,
                    "lon": 127.0894,
                    "capacity": 478,
                    "distance": 800,
                    "walk_time": 10,
                    "type": "지하주차장 1층",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": True,
                    "subway": "7호선 면목본동역 도보 12분"
                }
            ],
            "earthquake": [
                {
                    "name": "봉화산 근린공원",
                    "address": "서울특별시 중랑구 상봉동 산1-1",
                    "lat": 37.5982,
                    "lon": 127.0901,
                    "capacity": 5000,
                    "distance": 600,
                    "walk_time": 8,
                    "type": "공원",
                    "wheelchair": False,
                    "elevator": False,
                    "parking": True,
                    "subway": "7호선 상봉역 도보 10분"
                },
                {
                    "name": "용마산 근린공원",
                    "address": "서울특별시 중랑구 면목동 산1-6",
                    "lat": 37.5729,
                    "lon": 127.0854,
                    "capacity": 3000,
                    "distance": 900,
                    "walk_time": 12,
                    "type": "공원",
                    "wheelchair": False,
                    "elevator": False,
                    "parking": True,
                    "subway": "7호선 사가정역 도보 15분"
                }
            ],
            "war": [
                {
                    "name": "중랑구청 지하공간",
                    "address": "서울특별시 중랑구 봉우재로 179",
                    "lat": 37.6063,
                    "lon": 127.0925,
                    "capacity": 1000,
                    "distance": 400,
                    "walk_time": 5,
                    "type": "관공서 지하공간",
                    "wheelchair": True,
                    "elevator": True,
                    "parking": True,
                    "subway": "7호선 면목본동역 도보 5분"
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
            "distance": 1300,
            "emergency_24": True,
            "beds": 1900,
            "subway": "지하철 2호선 삼성역 도보 10분",
            "specialties": ["응급의학과", "심장센터", "암센터"],
            "region": "강남구"
        },
        # 서울 종로구
        {
            "name": "서울대학교병원",
            "address": "서울 종로구 대학로 101",
            "phone": "1588-5700",
            "lat": 37.5792,
            "lon": 126.9965,
            "distance": 2800,
            "emergency_24": True,
            "beds": 1700,
            "subway": "지하철 4호선 혜화역 도보 10분",
            "specialties": ["응급의학과", "외상센터", "뇌신경센터"],
            "region": "종로구"
        },
        # 부산 해운대구
        {
            "name": "인제대학교 해운대백병원",
            "address": "부산 해운대구 해운대로 875",
            "phone": "1577-0007",
            "lat": 37.1581,
            "lon": 129.1754,
            "distance": 800,
            "emergency_24": True,
            "beds": 1000,
            "subway": "부산지하철 2호선 해운대역 도보 8분",
            "specialties": ["응급의학과", "외상센터", "심혈관센터"],
            "region": "해운대구"
        },
        {
            "name": "좋은문화병원",
            "address": "부산 해운대구 센텀중앙로 60",
            "phone": "051-630-0114",
            "lat": 35.1693,
            "lon": 129.1295,
            "distance": 500,
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
            "distance": 1500,
            "emergency_24": True,
            "beds": 1400,
            "subway": "부산지하철 1호선 서대신역 도보 15분",
            "specialties": ["응급의학과", "외상센터", "심혈관센터"],
            "region": "부산진구"
        },
        # 경기 수원시
        {
            "name": "아주대학교병원",
            "address": "경기 수원시 영통구 월드컵로 164",
            "phone": "1688-6114",
            "lat": 37.2813,
            "lon": 127.0438,
            "distance": 1000,
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
            "distance": 600,
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
            "phone": "1588-8700",
            "lat": 37.3520,
            "lon": 127.1244,
            "distance": 800,
            "emergency_24": True,
            "beds": 900,
            "subway": "분당선 미금역 도보 8분",
            "specialties": ["응급의학과", "외상센터", "소아응급실"],
            "region": "성남시"
        },
        {
            "name": "차의과학대학교 분당차병원",
            "address": "경기 성남시 분당구 야탑로 59",
            "phone": "031-780-5000",
            "lat": 37.3515,
            "lon": 127.1240,
            "distance": 500,
            "emergency_24": True,
            "beds": 800,
            "subway": "분당선 야탑역 도보 5분",
            "specialties": ["응급의학과", "심혈관센터", "암센터"],
            "region": "성남시"
        },
        # 대구 중구
        {
            "name": "대구가톨릭대학교병원",
            "address": "대구 남구 두류공원로 17길 33",
            "phone": "053-650-4000",
            "lat": 35.8469,
            "lon": 128.5650,
            "distance": 1200,
            "emergency_24": True,
            "beds": 1500,
            "subway": "대구2호선 두류역 도보 10분",
            "specialties": ["응급의학과", "외상센터", "심혈관센터"],
            "region": "대구중구"
        },
        # 서울 중랑구
        {
            "name": "중랑구 보건소",
            "address": "서울특별시 중랑구 봉우재로 179",
            "phone": "02-2094-0756",
            "lat": 37.6063,
            "lon": 127.0925,
            "distance": 400,
            "emergency_24": False,
            "beds": 50,
            "subway": "7호선 상봉역 도보 7분",
            "specialties": ["응급의학과", "내과", "소아과"],
            "region": "중랑구"
        },
        {
            "name": "면목종합병원",
            "address": "서울특별시 중랑구 동일로 912",
            "phone": "02-435-9971",
            "lat": 37.5847,
            "lon": 127.0894,
            "distance": 800,
            "emergency_24": True,
            "beds": 200,
            "subway": "7호선 면목본동역 도보 5분",
            "specialties": ["응급의학과", "내과", "외과", "정형외과"],
            "region": "중랑구"
        },
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
        ]
    }
    
    # 화재 가이드
    guides["화재"] = {
        "summary": [
            "1. 불이야!를 크게 외치고 119에 즉시 신고하세요",
            "2. 자세를 낮추고 벽을 따라 이동하세요",
            "3. 계단을 이용해 아래층으로 피하세요 (엘리베이터 금지)",
            "4. 연기가 많으면 젖은 수건으로 입과 코를 막으세요"
        ]
    }
    
    # 호우 가이드
    guides["호우"] = {
        "summary": [
            "1. 우리 지역의 침수, 산사태 위험지역을 미리 확인하세요",
            "2. 안전디딤돌 앱으로 기상정보를 실시간 확인하세요",
            "3. 침수지역과 위험지역은 절대 접근하지 마세요",
            "4. 대피 권고 시 즉시 안전한 곳으로 이동하세요"
        ]
    }
    
    # 해일 가이드
    guides["해일"] = {
        "summary": [
            "1. TV, 라디오로 해일특보를 수시로 확인하세요",
            "2. 해안 저지대 주민은 대피장소와 방법을 미리 숙지하세요",
            "3. 해일특보 또는 대피명령 시 즉시 고지대로 대피하세요",
            "4. 해안에서 2-3m 이상 높은 곳으로 이동하세요"
        ]
    }
    
    # 폭염 가이드
    guides["폭염"] = {
        "summary": [
            "1. TV, 라디오로 무더위 관련 정보를 수시로 확인하세요",
            "2. 오후 2-5시 실외 작업은 가급적 피하세요",
            "3. 카페인 음료나 주류는 피하고 생수나 이온음료를 마시세요",
            "4. 어지러움·두통 시 즉시 시원한 곳에서 휴식하세요"
        ]
    }
    
    return guides

def main():
    # 세션 상태 초기화
    if 'font_size' not in st.session_state:
        st.session_state.font_size = '보통'
    if 'voice_enabled' not in st.session_state:
        st.session_state.voice_enabled = False
    if 'high_contrast' not in st.session_state:
        st.session_state.high_contrast = False
    
    # 개인정보 동의 확인
    if not st.session_state.get('privacy_consent', False):
        load_css()
        show_privacy_consent()
        return
    
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
                                  ["", "강남구", "종로구","중랑구","해운대구", "부산진구", "대구중구", "수원시", "성남시"])
            
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
                "화재": {"icon": "🔥", "description": "신속히 건물 밖으로 대피"},
                "호우": {"icon": "🌧️", "description": "침수 위험지역 피하기"},
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
                        "화재": "earthquake",  # 화재는 넓은 공간 대피소 사용
                        "호우": "flood", 
                        "해일": "earthquake",  # 해일은 높은 건물 대피소 사용
                        "폭염": "flood"  # 폭염은 실내 대피소 사용
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
        
        location_filter = st.selectbox("지역별 병원 찾기", 
                                     ["전체", "강남구", "종로구","중랑구","해운대구", "부산진구", "대구중구", "수원시", "성남시"])
        
        hospital_data = load_hospital_data()
        
        # 지역 필터링
        if location_filter != "전체":
            filtered_hospitals = [h for h in hospital_data if h['region'] == location_filter]
        else:
            filtered_hospitals = hospital_data
        
        if not filtered_hospitals:
            st.warning(f"⚠️ {location_filter}에 등록된 병원이 없습니다.")
        
        for hospital in filtered_hospitals:
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
                    
                    if st.button("🔊 병원정보 듣기", key=f"listen_{hospital['name']}"):
                        speak_text(f"{hospital['name']}. 주소는 {hospital['address']}. 전화번호는 {hospital['phone']}입니다.")
    
    with tab3:
        st.subheader("📚 재난별 행동요령")
        
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
                        st.info("상세 행동요령은 행정안전부 국민재난안전포털에서 확인하실 수 있습니다.")
                
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
    <p><strong>총 데이터:</strong> 대피소 48개소 | 응급의료시설 15개소 | 8개 지역</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
