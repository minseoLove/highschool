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
# 기존 speak_text 함수를 이 코드로 교체하세요

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


# 사이드바 음성 설정 부분도 개선
def render_voice_settings():
    """개선된 음성 설정 사이드바"""
    st.markdown("### 🔊 음성 안내 설정")
    
    # 음성 활성화 토글
    voice_enabled = st.checkbox("음성 안내 활성화", value=st.session_state.get('voice_enabled', False))
    st.session_state.voice_enabled = voice_enabled
    
    if voice_enabled:
        st.success("✅ 음성 안내가 활성화되었습니다")
        
        # 음성 속도 조절 (더 세밀하게)
        voice_speed = st.slider("🎚️ 음성 속도", 0.3, 3.0, st.session_state.get('voice_speed', 1.0), 0.1)
        st.session_state.voice_speed = voice_speed
        
        # 실시간 속도 표시
        if voice_speed <= 0.7:
            speed_text = "🐌 매우 느림"
        elif voice_speed <= 1.0:
            speed_text = "🚶 보통"
        elif voice_speed <= 1.5:
            speed_text = "🏃 빠름"
        else:
            speed_text = "🚀 매우 빠름"
            
        st.caption(f"현재 속도: {speed_text}")
        
        # 음성 테스트 (개선된 버전)
        if st.button("🎤 음성 테스트"):
            test_text = f"음성 속도 {voice_speed}배로 테스트합니다. 재난 발생 시 이 시스템을 통해 중요한 안내를 받을 수 있습니다."
            speak_text(test_text)
        
        # 전체 음성 중지 버튼
        if st.button("🔇 모든 음성 중지"):
            stop_all_js = """
            <script>
            try {
                if (window.speechSynthesis) {
                    window.speechSynthesis.cancel();
                }
                console.log('모든 음성 중지됨');
            } catch(e) {
                console.error('음성 중지 오류:', e);
            }
            </script>
            """
            st.components.v1.html(stop_all_js, height=0)
            st.success("🔇 모든 음성이 중지되었습니다.")
        
        # 음성 안내 사용법
        with st.expander("📖 음성 안내 사용법"):
            st.write("✅ **기본 사용법:**")
            st.write("• 각 버튼 클릭 시 자동으로 음성 안내 시작")
            st.write("• '⏹️ 음성 중지' 버튼으로 즉시 중지 가능")
            st.write("• '🔄 다시 듣기' 버튼으로 반복 재생")
            st.write("")
            st.write("⚡ **속도 조절:**")
            st.write("• 슬라이더로 0.3배~3.0배 속도 조절")
            st.write("• '⚡ 빠르게' 버튼으로 즉시 속도 증가")
            st.write("")
            st.write("🌐 **브라우저 호환성:**")
            st.write("• 크롬, 엣지, 사파리 최적화")
            st.write("• 인터넷 연결 불필요 (오프라인 가능)")
            
    else:
        st.info("음성 안내를 사용하려면 위 체크박스를 선택하세요")

    # 개인정보 활용동의 함수 (main 함수 위에 추가)
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
        key="essential_consent"
    )
    
    optional_consent = st.checkbox(
        "맞춤형 안전정보 제공을 위한 개인정보 활용에 동의합니다. (선택)", 
        key="optional_consent"
    )
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("❌ 동의하지 않음", type="secondary"):
            st.warning("⚠️ 필수 개인정보 처리에 동의하지 않으면 서비스를 이용할 수 없습니다.")
    
    with col2:
        if st.button("✅ 동의하고 시작", type="primary", disabled=not essential_consent):
            if essential_consent:
                st.session_state.privacy_consent = True
                st.session_state.essential_consent = essential_consent
                st.session_state.optional_consent = optional_consent
                st.session_state.consent_timestamp = datetime.now()
                
                st.success("✅ 개인정보 활용동의가 완료되었습니다!")
                time.sleep(1)
                st.rerun()


# 메인 함수에서 사이드바 부분을 이렇게 교체하세요:
def main():
    # ... 기존 코드 ...
    
    # 사이드바
    with st.sidebar:
        st.header("🔧 접근성 설정")
        
        # 글씨 크기 조절 (기존 그대로)
        font_size = st.selectbox(
            "📝 글씨 크기", 
            ["소형", "보통", "대형", "특대"], 
            index=["소형", "보통", "대형", "특대"].index(st.session_state.font_size)
        )
        
        if font_size != st.session_state.font_size:
            st.session_state.font_size = font_size
            st.rerun()
        
        # 개선된 음성 설정
        render_voice_settings()
        
        # 고대비 모드 (기존 그대로)
        # ... 나머지 코드

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
        
        # 🆕 여기부터 새로 추가되는 지역들!
        
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
            "subway": "7호선 상봉역 도보 7분"
        }
    ]
}
# 병원 데이터
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
        # 서울 송파구
        {
            "name": "서울아산병원",
            "address": "서울 송파구 올림픽로 43길 88",
            "phone": "1688-7575",
            "lat": 37.5268,
            "lon": 127.1073,
            "distance": 2100,
            "emergency_24": True,
            "beds": 2700,
            "subway": "지하철 9호선 석촌고분역 도보 8분",
            "specialties": ["응급의학과", "외상센터", "소아응급실"],
            "region": "송파구"
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
        # 서울 서대문구
        {
            "name": "세브란스병원",
            "address": "서울 서대문구 연세로 50-1",
            "phone": "1599-1004",
            "lat": 37.5630,
            "lon": 126.9395,
            "distance": 3200,
            "emergency_24": True,
            "beds": 2400,
            "subway": "지하철 2호선 신촌역 도보 8분",
            "specialties": ["응급의학과", "심혈관센터", "암센터"],
            "region": "서대문구"
        },
        # 서울 성북구
        {
            "name": "고려대학교 안암병원",
            "address": "서울 성북구 고려대로 73",
            "phone": "1577-0083",
            "lat": 37.5901,
            "lon": 127.0265,
            "distance": 2900,
            "emergency_24": True,
            "beds": 1000,
            "subway": "지하철 6호선 안암역 도보 3분",
            "specialties": ["응급의학과", "외상센터"],
            "region": "성북구"
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
        # 부산 서구
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
        {
            "name": "동아대학교병원",
            "address": "부산 서구 대신공원로 26",
            "phone": "051-240-2000",
            "lat": 35.1043,
            "lon": 129.0321,
            "distance": 1400,
            "emergency_24": True,
            "beds": 800,
            "subway": "부산지하철 1호선 동대신역 도보 10분",
            "specialties": ["응급의학과", "내과", "외과"],
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
        # 대구 남구
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
        ],
        "preparation": [
            "🏠 1. 집 안에서 안전 확보하기",
            "• 탁자 아래 등 안전한 대피 장소를 미리 파악해 둡니다.",
            "• 유리창이나 넘어지기 쉬운 가구 주변은 위험하니 지진 발생 시 가까이 가지 않습니다.",
            "• 깨진 유리 등으로부터 다치지 않도록 두꺼운 실내화를 준비해 둡니다.",
            "• 난로나 위험물은 화재 예방을 위해 주의하여 관리합니다.",
            "",
            "🛡️ 2. 안전구역 확인하기",
            "• 취침 장소와 출입구 주변은 가구가 이동하거나 넘어지지 않도록 배치하여 통로와 안전구역을 확보합니다.",
            "• 무거운 가구(장롱, 피아노), 책상, 장식장, 컴퓨터, TV 등 낙하 위험이 있는 물건은 특별히 주의합니다.",
            "",
            "🔧 3. 집 안 물건 고정하기",
            "• 가구와 가전제품이 흔들려도 넘어지지 않도록 단단히 고정합니다.",
            "• TV, 꽃병 등 떨어질 수 있는 물건은 높은 곳에 두지 않습니다.",
            "• 그릇장 등 문을 고정해 내부 물건이 쏟아지지 않게 합니다.",
            "• 창문 유리에는 필름을 붙여 파손 시 안전하도록 합니다.",
            "",
            "🔍 4. 집 안전관리",
            "• 가스와 전기를 미리 점검합니다.",
            "• 건물과 담장을 수시로 점검하고 위험한 부분은 보수합니다.",
            "• 건물 균열 발견 시 전문가에게 문의해 보수 및 보강합니다.",
            "",
            "👥 5. 가족회의로 위급 상황 대비",
            "• 가스 및 전기 차단 방법을 가족 모두가 숙지합니다.",
            "• 머무는 곳 주변의 대피 가능한 넓은 공간을 미리 확인합니다.",
            "• 비상시 가족과 만날 장소와 연락 방법을 정해 둡니다.",
            "• 응급처치 방법을 반복 훈련하여 익힙니다.",
            "",
            "🎒 6. 비상용품 준비",
            "• 지진 대비 비상용품을 준비하고 보관 장소 및 사용법을 숙지합니다.",
            "• 화재 위험에 대비해 소화기를 준비하고 사용법을 알아둡니다."
        ],
        "during": [
            "🏠 집에 있을 때",
            "1. 탁자 아래로 들어가 다리를 꼭 잡고 머리 보호!",
            "2. 떨어질 수 있는 가구, TV 등에서 멀리 떨어지기.",
            "3. 주방에 있다면 즉시 가스 차단!",
            "4. 화장실이라면 문을 열고 바로 나와 대피.",
            "5. 욕실이라면 수건, 대야 등으로 머리 보호 후 즉시 이동.",
            "",
            "🏫 학교에 있을 때",
            "1. 책상 아래로 들어가 책상다리를 꼭 잡고 몸 웅크리기.",
            "2. 흔들림이 멈추면 선생님 지시에 따라 질서 있게 운동장으로 대피.",
            "3. 창문 근처는 피해서 이동.",
            "",
            "🏢 고층 건물에 있을 때",
            "1. 창문과 외벽에서 멀리 떨어지기.",
            "2. 낙하물에 주의하고 건물 밖으로 무리하게 탈출하지 않기.",
            "3. 진동이 멈출 때까지 안전한 장소에서 대기.",
            "",
            "💼 사무실에 있을 때",
            "1. 책상 아래로 들어가 몸 보호.",
            "2. 컴퓨터, 모니터 등 낙하물에 주의.",
            "",
            "🛒 백화점·마트에 있을 때",
            "1. 진열대에서 떨어져 낙하물 피하기.",
            "2. 기둥, 계단 근처로 이동.",
            "3. 에스컬레이터에 있으면 손잡이를 잡고 앉아서 버티기.",
            "4. 흔들림 멈추면 안내에 따라 침착히 대피.",
            "",
            "🎭 극장·경기장에 있을 때",
            "1. 자리에서 가방 등으로 머리 보호 후 움직이지 않기.",
            "2. 사람이 몰리지 않도록 안내에 따라 이동.",
            "",
            "🛗 엘리베이터 안에 있을 때",
            "1. 모든 층 버튼 누르고, 가장 먼저 열린 층에서 하차.",
            "2. 갇혔다면 인터폰이나 휴대전화로 구조 요청.",
            "3. 지진 시 엘리베이터 사용 금지!",
            "",
            "🚗 자동차 안에 있을 때",
            "1. 비상등 켜고 서서히 오른쪽에 정차.",
            "2. 라디오 정보 청취.",
            "3. 대피 시, 문 잠그지 말고 열쇠 꽂은 채 이동.",
            "4. 교량이나 고가도로 위는 피해서 주차.",
            "",
            "🚇 전철 안에 있을 때",
            "1. 손잡이, 기둥을 꼭 잡고 넘어지지 않게.",
            "2. 출구로 갑자기 뛰지 말고 안내에 따르기.",
            "",
            "🏔️ 산이나 바다에 있을 때",
            "1. 산사태나 낙석 우려 지역은 즉시 벗어나기.",
            "2. 지진해일 특보 시, 즉시 높은 곳으로 대피."
        ],
        "accessibility": [
            "👁️ 시력이 좋지 않거나 시각장애가 있는 경우",
            "• 라디오, 방송으로 상황 파악.",
            "• 주변 장애물 확인하며 천천히 이동.",
            "• 주변 사람에게 도움 요청.",
            "",
            "♿ 지체장애가 있는 경우",
            "• 이웃과 함께 대피.",
            "• 휠체어 바퀴 잠그고 머리 보호.",
            "• 움직일 수 없다면 안전한 곳에서 구조 기다리기.",
            "",
            "👂 청각장애가 있는 경우",
            "• 자막 방송, 휴대전화로 정보 수집.",
            "• 호루라기 등으로 위치 알리기.",
            "• 주변 사람에게 청각장애 알리기.",
            "",
            "🧠 발달장애, 정신장애가 있는 경우",
            "• 뛰지 않고 침착하게 행동.",
            "• 미리 정한 행동 따라가기.",
            "• 결정이 어려우면 주변에 도움 요청."
        ],
        "after": [
            "👥 1. 가족과 주변 사람의 안전부터 확인",
            "• 가족과 함께 있는 경우: 서로 다친 곳은 없는지 확인합니다.",
            "• 부상자가 있다면: 119에 신고하고, 이웃과 협력해 응급처치를 합니다.",
            "• 혼자 있을 경우, 주변 구조 요청 및 자가 상태 점검.",
            "",
            "🏠 2. 귀가 여부는 신중히 결정",
            "• 공공기관 안내 방송, 라디오 등 신뢰 가능한 정보를 먼저 확인합니다.",
            "• 귀가 전 꼭 확인해야 할 것:",
            "  - 내가 가려는 건물이나 지역에 피해가 있는가?",
            "  - 여진 가능성은 없는가?",
            "  - 도로는 통제 중이거나 낙하물 위험이 있는가?",
            "• 도보 이동 시, 주변 건물 상태·전신주·간판 등 낙하물 유의.",
            "",
            "🔍 3. 귀가 후, 건물 내부 안전 점검",
            "들어가기 전",
            "• 건물에 균열, 기울어짐, 콘크리트 낙하 흔적이 보인다면 절대 들어가지 마세요.",
            "• 지자체가 파견한 피해시설물 위험도 평가단의 '위험' 판정이 있으면 출입 금지!",
            "",
            "들어간 뒤 확인할 것",
            "• 가정 또는 사무실에서: 가구나 물건이 쓰러져 2차 피해 유발 가능 → 문을 열 때 특히 조심!",
            "• 전기, 수도, 가스 등 시설물 점검 필수",
            "",
            "⚠️ 4. 꼭 점검해야 할 시설 항목",
            "가스",
            "• 가스 냄새가 나거나 소리가 들릴 경우:",
            "  1. 창문을 열고, 2. 밸브를 잠근 뒤, 3. 즉시 대피 후 전문가에게 확인 요청",
            "• 점검 전에는 절대 사용 금지!",
            "",
            "전기",
            "• 이상이 있다면 엘리베이터 절대 사용 금지.",
            "• 정전된 경우: 1. 손전등 사용 (성냥, 촛불 금지) 2. 차단기 내리고, 3. 전선 상태 확인",
            "",
            "수도/하수도",
            "• 수도관이 파손되었거나 이상이 의심되면: 밸브 잠금",
            "• 하수관 점검 전까지 수도꼭지, 변기 사용 금지",
            "",
            "📞 5. 피해가 확인되면 반드시 신고",
            "• 피해시설은 즉시 해당 기관(시·군·구청, 시설물관리공단 등)에 신고합니다.",
            "• 공공 시설물, 도로, 가스 배관 등도 발견 시 알리기.",
            "",
            "📻 6. 정보는 반드시 공신력 있는 경로에서",
            "• TV, 라디오, 정부·지자체 알림을 통해 지진 관련 정보를 수시로 확인합니다.",
            "• SNS나 이웃발 유언비어에 휘둘리지 않기.",
            "",
            "⚠️ 추가 주의사항",
            "• 여진은 본진 이후 수 시간~수일 내 발생 가능 → 계속 주의 유지!",
            "• 건물 밖이라도 담벼락, 유리창, 간판, 고가 전기선 등 낙하물 주의.",
            "• 가급적 안전이 확보된 대피소에서 대기하다가 귀가 여부 판단하세요."
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
    
    # 해일 가이드
    guides["해일"] = {
        "summary": [
            "1. TV, 라디오로 해일특보를 수시로 확인하세요",
            "2. 해안 저지대 주민은 대피장소와 방법을 미리 숙지하세요",
            "3. 해일특보 또는 대피명령 시 즉시 고지대로 대피하세요",
            "4. 해안에서 2-3m 이상 높은 곳으로 이동하세요"
        ],
        "preparation": [
            "📺 해일특보 사전 대비",
            "• TV나 라디오 등을 통해 기상상황과 해일특보를 수시로 확인합니다.",
            "• 해안 저지대 주민은 대피장소와 대피방법을 미리 숙지합니다.",
            "• 가까운 행정기관 연락처를 가족 모두가 알 수 있는 곳에 비치합니다.",
            "• 이웃 간 연락 방법도 평소에 공유합니다.",
            "• 공사 중인 현장에서는 즉시 작업을 중지하고, 기자재는 안전한 곳으로 이동시킵니다."
        ],
        "during": [
            "🌊 해일특보 또는 대피명령 시",
            "• 기상청, 시·군·구청, 소방서 등의 대피명령이 있으면 즉시 대피합니다.",
            "• 해일이 발생할 경우 즉시 해안에서 멀리 떨어진 고지대로 이동합니다.",
            "• 1층보다는 2층, 2층보다는 3층, 경우에 따라 지붕이 더 안전할 수 있습니다.",
            "• 목조 주택은 위험하므로, 벽돌 또는 철근콘크리트 건물로 대피합니다.",
            "• 급경사가 없고 지형이 높은 곳을 선택해 대피합니다.",
            "• 해안에서 2~3m 이상 고지대는 비교적 안전합니다."
        ],
        "warning_info": [
            "⚠️ 해일특보 기준",
            "• 해일주의보: 천문조, 폭풍, 저기압 등의 복합 영향으로 해수면이 상승하여 기준 이상일 때 발효",
            "• 해일경보: 해수면 상승이 더 심각할 것으로 예상될 때 발효",
            "",
            "❓ 자주 묻는 질문 (Q&A)",
            "Q. 폭풍해일 피해를 줄이기 위한 행동요령은?",
            "A. 평소에 대피장소와 방법을 미리 알아두고, 기상정보나 해일경보를 수시로 확인하며, 폭풍해일이 예상되면 즉시 높은 곳으로 대피합니다."
        ]
    }
    
    # 폭염 가이드
    guides["폭염"] = {
        "summary": [
            "1. TV, 라디오로 무더위 관련 정보를 수시로 확인하세요",
            "2. 오후 2-5시 실외 작업은 가급적 피하세요",
            "3. 카페인 음료나 주류는 피하고 생수나 이온음료를 마시세요",
            "4. 어지러움·두통 시 즉시 시원한 곳에서 휴식하세요"
        ],
        "preparation": [
            "📋 사전 준비",
            "",
            "🔍 1. 기상상황 수시 확인",
            "• TV, 라디오, 인터넷 등을 통해 무더위 관련 정보 확인",
            "• 가족 및 이웃과 정보 공유",
            "",
            "🏥 2. 온열질환에 대한 이해와 대응",
            "• 열사병, 열경련, 땀띠, 울열증, 화상 등의 증상과 대처법 숙지",
            "• 인근 병원 연락처 사전 확보",
            "• 어린이, 노약자, 심뇌혈관질환자 등 취약계층 건강관리 주의",
            "",
            "🧰 3. 폭염 대비 용품 준비",
            "• 에어컨, 선풍기 등 냉방기기 점검",
            "• 창문에 커튼, 햇빛 차단 필름 등 설치",
            "• 외출 대비 모자, 썬크림, 햇빛 가리개 준비",
            "• 정전에 대비해 손전등, 부채, 비상식음료, 휴대용 라디오 준비",
            "• 단수 대비 생수 확보, 생활용수는 욕조에 미리 저장",
            "• 오래된 주택은 변압기 점검으로 과부하 예방",
            "• 장거리 운행 시 도로, 철도 상태 확인 후 이동 여부 판단",
            "",
            "⚠️ 무더위 안전수칙",
            "• 실내외 온도차는 5℃ 이내 유지 → 적정 실내 냉방온도: 26~28℃",
            "• 카페인 음료나 주류는 피하고, 생수나 이온음료 섭취",
            "• 오후 2~5시 실외 작업은 가급적 피함",
            "• 상하기 쉬운 음식은 실외 장시간 방치 금지",
            "",
            "👥 취약계층 돌봄",
            "• 어린이, 노약자 등 취약계층의 건강상태 및 대응방안을 사전에 확인",
            "• 폭염 중에는 수시로 안부 확인하고 이상 유무 점검"
        ],
        "during": [
            "🏠 일반 가정에서는",
            "• 야외활동 자제, 외출 시 창 넓은 모자 + 가벼운 옷차림 + 물병 필수",
            "• 카페인 음료·술 금지, 생수나 이온음료 자주 마시기",
            "• 냉방 안 되는 실내는 햇빛 가리기 + 맞바람으로 환기",
            "• 차 안에 어린이나 노약자 절대 방치 금지",
            "• 장시간 외출 시 거동 불편자 안부 확인 및 주변에 도움 요청",
            "• 어지러움·두통·근육경련 시 즉시 시원한 곳에서 휴식 + 천천히 수분 섭취",
            "",
            "🏢 직장에서는",
            "• 휴식은 짧고 자주, 점심시간 10~15분 낮잠 권장",
            "• 외부 행사 및 스포츠 경기 자제",
            "• 가벼운 복장 착용 권장",
            "• 냉방 어려운 실내는 햇빛 차단 + 환기",
            "• 실외 작업장(건설 현장 등)은 → 물·그늘·휴식 원칙 준수, → 오후 2~5시 '무더위 휴식시간제' 시행",
            "",
            "🏫 학교에서는",
            "• 에어컨 등 냉방 불가 시 단축수업, 휴교 등 검토",
            "• 실내는 햇빛 차단 + 선풍기 + 환기",
            "• 체육활동, 소풍 등 야외활동은 자제",
            "• 식중독 예방 위한 급식 위생 철저 관리",
            "",
            "🐄 축사 및 양식장에서는",
            "• 지속적인 환기 및 적정 사육 밀도 유지",
            "• 물 분무 장치로 복사열 차단",
            "• 양식 어류는 수온 관리(예: 얼음 투입)",
            "• 가축·어류 폐사 시 신속히 방역기관에 신고",
            "",
            "🏛️ 무더위쉼터 이용",
            "• 냉방이 안 되거나 외출 중일 때는 → 가까운 무더위쉼터로 이동해 폭염을 피하세요.",
            "• 위치는 '안전디딤돌 앱' 또는 시군구 홈페이지에서 확인 가능"
        ],
        "heat_diseases": [
            "🌡️ 더위질병 상식",
            "",
            "🚨 열사병 (Heat Stroke)",
            "정의 및 증상: 체온조절 중추 마비, 의식장애·혼수, 땀 없음·건조한 피부·고체온(>40℃), 두통·오한·빠른 맥박/호흡·저혈압",
            "응급 대처: ✅ 119 신고 ✅ 시원한 곳으로 이동 ✅ 옷을 느슨하게, 몸에 물 적시기 ✅ 목·겨드랑이·서혜부에 얼음찜질",
            "",
            "😰 열탈진 (Heat Exhaustion)",
            "정의 및 증상: 과도한 발한 → 수분/염분 손실, 차고 젖은 피부·체온 ≤40℃, 무력감·근육경련·구토·어지럼",
            "응급 대처: ✅ 시원한 장소에서 휴식 ✅ 수분 보충(물) ✅ 시원한 샤워 ✅ 1시간 내 회복 안 될 시 병원 방문",
            "",
            "💪 열경련 (Heat Cramp)",
            "정의 및 증상: 나트륨 부족 → 근육경련 (팔·다리·복부 등), 고온 환경에서 과격한 활동 후 발생",
            "응급 대처: ✅ 시원한 장소에서 휴식 ✅ 수분 보충 ✅ 경련 부위 마사지 ⚠ 1시간 이상 지속·심장질환자·저염식 환자는 응급실로",
            "",
            "😵 열실신 (Heat Syncope)",
            "정의 및 증상: 체표 혈류 증가 → 뇌 혈류 감소, 어지럼증·일시적 의식소실, 갑자기 일어날 때 주로 발생",
            "응급 대처: ✅ 평평한 곳에 눕힘 ✅ 다리를 머리보다 높게 ✅ 의식 있을 경우 물 천천히 섭취",
            "",
            "🦵 열부종 (Heat Edema)",
            "정의 및 증상: 체표 혈류 증가 + 정체 → 손·발·다리 부종, 주로 오래 앉거나 서 있을 때 발생",
            "응급 대처: ✅ 시원한 장소에서 휴식 ✅ 부종 부위를 심장보다 높게 올리기",
            "",
            "🔴 열발진/땀띠 (Heat Rash)",
            "정의 및 증상: 땀구멍 막힘 → 작은 붉은 발진 또는 물집, 목·가슴·사타구니·팔 등 접히는 부위",
            "응급 대처: ✅ 시원하고 건조하게 유지 ✅ 땀띠 전용 파우더·연고 사용"
        ],
        "key_points": [
            "📌 폭염 예보 시 꼭 기억하세요!",
            "• 독거노인, 취약계층 안부 확인",
            "• 야외활동은 최대한 피하고, 수분 섭취는 충분히",
            "• 증상 발생 시 즉시 시원한 곳에서 휴식"
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

    elif disaster == "해일":
        # 해일 2단계
        tab1, tab2 = st.tabs(["📋 해일 사전 대비", "🌊 해일특보 시"])
        
        with tab1:
            st.markdown("## 📺 해일 사전 대비")
            for action in guide["preparation"]:
                if action.startswith("📺"):
                    st.markdown(f"### {action}")
                elif action.startswith("•"):
                    st.write(action)
                elif action == "":
                    st.write("")
                else:
                    st.write(action)
        
        with tab2:
            st.markdown("## 🌊 해일특보 또는 대피명령 시")
            for action in guide["during"]:
                if action.startswith("🌊"):
                    st.markdown(f"### {action}")
                elif action.startswith("•"):
                    st.write(action)
                elif action == "":
                    st.write("")
                else:
                    st.write(action)
            
            # 해일 특보 기준 및 Q&A
            st.markdown("---")
            st.markdown("## 📖 추가 정보")
            for action in guide["warning_info"]:
                if action.startswith(("⚠️", "❓")):
                    st.markdown(f"### {action}")
                elif action.startswith(("Q.", "A.")):
                    st.markdown(f"**{action}**")
                elif action.startswith("•"):
                    st.write(action)
                elif action == "":
                    st.write("")
                else:
                    st.write(action)

    elif disaster == "폭염":
        # 폭염 3단계
        tab1, tab2, tab3 = st.tabs(["📋 폭염 사전 대비", "🌡️ 폭염 시 행동요령", "🏥 더위질병 상식"])
        
        with tab1:
            st.markdown("## 📋 폭염 사전 대비")
            for action in guide["preparation"]:
                if action.startswith(("🔍", "🏥", "🧰", "⚠️", "👥")):
                    st.markdown(f"### {action}")
                elif action.startswith("•"):
                    st.write(action)
                elif action == "":
                    st.write("")
                else:
                    st.write(action)
        
        with tab2:
            st.markdown("## 🌡️ 폭염 시 행동요령")
            for action in guide["during"]:
                if action.startswith(("🏠", "🏢", "🏫", "🐄", "🏛️")):
                    st.markdown(f"### {action}")
                elif action.startswith("•"):
                    st.write(action)
                elif action == "":
                    st.write("")
                else:
                    st.write(action)
            
            # 핵심 포인트
            st.markdown("---")
            for action in guide["key_points"]:
                if action.startswith("📌"):
                    st.markdown(f"### {action}")
                elif action.startswith("•"):
                    st.write(action)
                elif action == "":
                    st.write("")
                else:
                    st.write(action)
        
        with tab3:
            st.markdown("## 🏥 더위질병 상식")
            for action in guide["heat_diseases"]:
                if action.startswith("🌡️"):
                    st.markdown(f"### {action}")
                elif action.startswith(("🚨", "😰", "💪", "😵", "🦵", "🔴")):
                    st.markdown(f"#### {action}")
                elif action.startswith(("정의 및 증상:", "응급 대처:")):
                    st.markdown(f"**{action}**")
                elif action == "":
                    st.write("")
                else:
                    st.write(action)
    
    else:
        # 지진은 4단계로 처리
        if disaster == "지진":
            tab1, tab2, tab3, tab4 = st.tabs(["📋 평상시 대비", "🚨 지진 발생 시", "♿ 장애인 행동요령", "✅ 지진 대피 후"])
            
            with tab1:
                st.markdown("## 📋 평상시 지진 대비")
                for action in guide["preparation"]:
                    if action.startswith(("🏠", "🛡️", "🔧", "🔍", "👥", "🎒")):
                        st.markdown(f"### {action}")
                    elif action.startswith("•"):
                        st.write(action)
                    elif action == "":
                        st.write("")
                    else:
                        st.write(action)
            
            with tab2:
                st.markdown("## 🚨 지진 발생 시 상황별 행동요령")
                for action in guide["during"]:
                    if action.startswith(("🏠", "🏫", "🏢", "💼", "🛒", "🎭", "🛗", "🚗", "🚇", "🏔️")):
                        st.markdown(f"### {action}")
                    elif action.startswith(("1.", "2.", "3.", "4.", "5.")):
                        st.write(action)
                    elif action == "":
                        st.write("")
                    else:
                        st.write(action)
            
            with tab3:
                st.markdown("## ♿ 몸이 불편하신 분의 행동요령")
                for action in guide["accessibility"]:
                    if action.startswith(("👁️", "♿", "👂", "🧠")):
                        st.markdown(f"### {action}")
                    elif action.startswith("•"):
                        st.write(action)
                    elif action == "":
                        st.write("")
                    else:
                        st.write(action)
            
            with tab4:
                st.markdown("## ✅ 지진 대피 후 행동요령")
                for action in guide["after"]:
                    if action.startswith(("👥", "🏠", "🔍", "⚠️", "📞", "📻")):
                        st.markdown(f"### {action}")
                    elif action.startswith("•"):
                        st.write(action)
                    elif action.startswith("  -"):
                        st.write(action)
                    elif action == "":
                        st.write("")
                    else:
                        st.write(action)
        
        # 기존 화재 등 다른 재난들은 2단계 형식 유지
        else:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("## ⚡ 즉시 행동")
                if "immediate" in guide:
                    for action in guide["immediate"]:
                        st.write(action)
                else:
                    st.write("즉시 행동 정보가 없습니다.")
            
            with col2:
                st.markdown("## 🏃‍♂️ 대피 행동")
                if "evacuation" in guide:
                    for action in guide["evacuation"]:
                        st.write(action)
                else:
                    st.write("대피 행동 정보가 없습니다.")
    
    # 메인 페이지로 돌아가기 버튼
    st.markdown("---")
    if st.button("⬅️ 재난 행동요령 목록으로 돌아가기", key="back_to_main"):
        st.session_state.show_detailed_page = False
        st.session_state.selected_disaster_detail = None
        st.rerun()

# 개인정보 활용동의 함수 (main 함수 위에 추가)
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
        key="essential_consent"
    )
    
    optional_consent = st.checkbox(
        "맞춤형 안전정보 제공을 위한 개인정보 활용에 동의합니다. (선택)", 
        key="optional_consent"
    )
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("❌ 동의하지 않음", type="secondary"):
            st.warning("⚠️ 필수 개인정보 처리에 동의하지 않으면 서비스를 이용할 수 없습니다.")
    
    with col2:
        if st.button("✅ 동의하고 시작", type="primary", disabled=not essential_consent):
            if essential_consent:
                st.session_state.privacy_consent = True
                st.session_state.essential_consent = essential_consent
                st.session_state.optional_consent = optional_consent
                st.session_state.consent_timestamp = datetime.now()
                
                st.success("✅ 개인정보 활용동의가 완료되었습니다!")
                time.sleep(1)
                st.rerun()
# 메인 앱
# main() 함수 시작 부분에 추가 (세션 상태 초기화 다음)
def main():
    # 세션 상태 초기화
    if 'font_size' not in st.session_state:
        st.session_state.font_size = '보통'
    if 'voice_enabled' not in st.session_state:
        st.session_state.voice_enabled = False
    if 'high_contrast' not in st.session_state:
        st.session_state.high_contrast = False
    
    # 🆕 개인정보 동의 확인 추가
    if not st.session_state.get('privacy_consent', False):
        load_css()
        show_privacy_consent()
        return
    
    # 기존 코드 계속...
    
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
    <p><strong>총 데이터:</strong> 대피소 48개소 | 응급의료시설 15개소 | 11개 지역</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
