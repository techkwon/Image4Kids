import streamlit as st
import random
import requests
import io
import base64
from PIL import Image
import json
import numpy as np
from streamlit_drawable_canvas import st_canvas
import os
from dotenv import load_dotenv
import time

# .env 파일 로드
load_dotenv()

# 페이지 설정
st.set_page_config(
    page_title="Image4Kids",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "이미지4키즈 - K-12 학생을 위한 안전한 AI 이미지 생성 플랫폼"
    }
)

# 테마 설정 - 라이트 모드 강제 적용
st.markdown("""
<script>
    localStorage.setItem('theme', 'light');
    localStorage.setItem('colorScheme', 'light');
</script>
""", unsafe_allow_html=True)

# 스타일 설정
st.markdown("""
<style>
    /* 라이트 모드 강제 적용 */
    [data-testid="stAppViewContainer"] {
        background-color: #f8f9fa !important;
    }
    [data-testid="stHeader"] {
        background-color: #f8f9fa !important;
    }
    [data-testid="stToolbar"] {
        background-color: #f8f9fa !important;
    }
    [data-testid="stSidebar"] {
        background-color: #e9ecef !important;
    }
    .main {
        background-color: #f8f9fa !important;
        color: #111111 !important;
    }
    h1, h2, h3, h4, h5, h6, p, li, div {
        color: #111111 !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #e9ecef;
        border-radius: 8px;
        color: #495057 !important;
        font-size: 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #91a7ff;
        color: white !important;
    }
    .css-18e3th9 {
        padding-top: 2rem;
    }
    .stButton>button {
        background-color: #5c7cfa;
        color: white !important;
        border-radius: 8px;
        font-weight: bold;
        padding: 10px 20px;
        border: none;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .stButton>button:hover {
        background-color: #4263eb;
    }
    .input-section {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        height: 100%;
        border: 1px solid #dee2e6;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .result-section {
        background-color: #f1f3f5;
        padding: 20px;
        border-radius: 10px;
        height: 100%;
    }
    .safety-message {
        padding: 8px;
        border-radius: 4px;
        margin-bottom: 10px;
        font-size: 14px;
        opacity: 0.8;
        color: #555;
        background-color: #f8f9fa;
        border-left: 3px solid #aaa;
    }
    .download-btn {
        display: inline-block;
        margin-top: 8px;
        padding: 5px 10px;
        background-color: #91a7ff;
        border-radius: 4px;
        color: white;
        text-decoration: none;
        font-size: 14px;
    }
    .download-btn:hover {
        background-color: #748ffc;
    }
    
    /* 그리기 영역 스타일 개선 */
    .canvas-container {
        width: 100%;
        margin: 20px auto;
        border: 5px solid #ff8787;
        border-radius: 10px;
        background-color: white;
        position: relative;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        overflow: visible !important;
    }
    
    .canvas-header {
        background-color: #ff8787;
        color: white !important;
        padding: 12px;
        text-align: center;
        font-weight: bold;
        font-size: 20px;
        border-radius: 5px 5px 0 0;
    }
    
    /* 캔버스 상호작용 영역이 확실히 보이도록 함 */
    canvas {
        cursor: crosshair !important;
        border: 3px solid #dee2e6 !important;
        margin: 10px auto !important;
        display: block !important;
        background-color: white !important;
    }
    
    /* Streamlit 캔버스 관련 클래스 강제 표시 */
    .stCanvas {
        display: block !important;
        width: 100% !important;
        margin: 0 auto !important;
    }
    
    /* 도구 모음 스타일링 */
    .drawing-tools {
        background-color: #f1f3f5;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    
    /* 버튼 그룹 스타일 */
    .button-group {
        margin-top: 15px;
        text-align: center;
    }
    
    /* 캔버스 관련 스타일 완전 재정의 */
    .canvas-area {
        margin: 20px auto;
        padding: 20px;
        background-color: #f8f9fa;
        border-radius: 10px;
        border: 4px solid #ff8787;
        text-align: center;
    }
    
    .canvas-title {
        background-color: #ff8787;
        color: white !important;
        padding: 10px;
        margin: -20px -20px 20px -20px;
        border-radius: 6px 6px 0 0;
        font-size: 18px;
        font-weight: bold;
    }
    
    /* 캔버스 직접 스타일링 */
    [data-testid="stCanvas"] {
        display: block !important;
        background-color: white !important;
        border: 2px dashed #dee2e6 !important;
        border-radius: 4px;
        margin: 0 auto !important;
    }
    
    /* 캔버스 컨테이너 스타일 수정 - 더 크고 뚜렷하게 */
    .drawing-canvas-container {
        width: 90% !important;
        margin: 20px auto !important;
        background-color: #ffffff !important;
        border: 2px solid #dee2e6 !important;
        border-radius: 8px !important;
        padding: 15px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
        position: relative !important;
        z-index: 10 !important;
        display: block !important;
        visibility: visible !important;
        min-height: 520px !important;
        clear: both !important;
    }
    
    /* 캔버스 자체 스타일링 강화 */
    [data-testid="stCanvas"] {
        display: block !important;
        background-color: #ffffff !important;
        border: 2px dashed #dee2e6 !important;
        margin: 0 auto !important;
        padding: 0 !important;
        position: relative !important;
        z-index: 100 !important;
        visibility: visible !important;
        opacity: 1 !important;
        min-height: 400px !important;
    }
    
    /* 지우개 버튼 스타일 수정 - 흰색 글씨로 확실하게 강조 */
    button {
        color: white !important;
        font-weight: bold !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3) !important;
    }
    
    /* 정보 메시지 스타일 개선 */
    .stAlert {
        font-weight: bold !important;
        font-size: 16px !important;
    }
    
    /* st.info 스타일 강화 */
    [data-testid="stInfoBox"] {
        background-color: #4dabf7 !important;
        color: white !important;
        border: none !important;
        padding: 10px !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2) !important;
        margin: 10px 0 !important;
    }
    
    /* 도구 영역 스타일 */
    .drawing-tools {
        background-color: #f1f3f5;
        padding: 15px;
        margin-bottom: 20px;
        border-radius: 8px;
        border: 2px solid #dee2e6;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    /* 버튼 간격 조정 */
    .drawing-tools > div {
        margin-right: 15px;
    }
    
    /* 지우개 버튼 스타일 수정 - 명확한 색상 대비 */
    [data-testid="baseButton-secondary"] {
        background-color: #5c7cfa !important;
        color: white !important;
        font-weight: bold !important;
        text-shadow: none !important;
    }
    
    /* 그리기 캔버스 통합 스타일 */
    .simple-canvas-area {
        width: 90%;
        margin: 0 auto;
        background-color: #ffffff;
        border: 15px solid #ff6b6b;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        position: relative;
    }
    
    /* 캔버스 내부 스타일 간소화 */
    canvas {
        background-color: white !important;
        cursor: crosshair !important;
        margin: 0 auto !important;
        display: block !important;
    }
    
    /* 완료 버튼 강조 */
    .complete-button {
        margin-top: 20px;
        text-align: center;
    }
    
    /* 상태 표시 메시지 */
    .mode-indicator {
        background-color: #ff8787;
        color: white;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        margin: 10px 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    /* 캔버스 스타일 업데이트 - 테두리 변경 */
    .big-canvas-area {
        width: 95%;
        margin: 0 auto;
        background-color: #ffffff;
        border: 2px solid #dee2e6;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        position: relative;
    }
</style>
""", unsafe_allow_html=True)

# API 키 관리
class KeyManager:
    def __init__(self, api_keys):
        self.api_keys = api_keys
        self.last_index = -1
    
    def get_random_key(self):
        if len(self.api_keys) == 0:
            return None
        
        if len(self.api_keys) == 1:
            return self.api_keys[0]
        
        index = self.last_index
        while index == self.last_index:
            index = random.randint(0, len(self.api_keys) - 1)
        
        self.last_index = index
        return self.api_keys[index]

# 안전 검사 함수
def check_prompt_safety(prompt, key_manager):
    """프롬프트의 안전성을 검사하는 함수"""
    
    SAFETY_PROMPT = """You are an AI content safety evaluator for K–12 education. The user will provide an image generation prompt. Your task is to:
    1. Analyze the prompt carefully and decide whether it is safe and appropriate for K–12 students (ages 5–18).
    2. If the prompt contains any inappropriate, harmful, violent, graphic, sexual, or otherwise unsuitable content for K–12 students, DO NOT return the original prompt.
       - Instead, return this exact safe prompt:  
         "A cute cartoon-style cat with big eyes holding a sign that says 'Sorry' in a friendly and apologetic way. The cat looks innocent and is surrounded by soft, pastel-colored backgrounds."
    3. If the prompt is safe and appropriate AND the prompt is in Korean, translate it to English and return the English translation.
    4. If the prompt is safe and appropriate AND already in English, return the user's original prompt exactly as it is, without modification."""
    
    FALLBACK_PROMPT = "A cute cartoon-style cat with big eyes holding a sign that says 'Sorry' in a friendly and apologetic way. The cat looks innocent and is surrounded by soft, pastel-colored backgrounds."
    
    try:
        api_key = key_manager.get_random_key()
        if api_key is None:
            return {"safe": False, "safePrompt": FALLBACK_PROMPT}
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": SAFETY_PROMPT},
                        {"text": f'User prompt: "{prompt}"'}
                    ]
                }
            ]
        }
        
        headers = {
            'Content-Type': 'application/json',
            'x-goog-api-key': api_key
        }
        
        response = requests.post(
            'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent',
            headers=headers,
            data=json.dumps(payload)
        )
        
        data = response.json()
        
        if 'candidates' not in data or len(data['candidates']) == 0 or 'content' not in data['candidates'][0]:
            return {"safe": False, "safePrompt": FALLBACK_PROMPT}
        
        checked_prompt = data['candidates'][0]['content']['parts'][0]['text'].strip()
        
        # 반환된 프롬프트가 대체 프롬프트와 일치하면 안전하지 않다고 판단
        is_safe = FALLBACK_PROMPT not in checked_prompt
        
        return {
            "safe": is_safe,
            "safePrompt": checked_prompt if is_safe else FALLBACK_PROMPT
        }
    except Exception as e:
        st.error(f"안전 검사 중 오류가 발생했습니다: {e}")
        return {"safe": False, "safePrompt": FALLBACK_PROMPT}

# 이미지 생성 함수
def generate_image(prompt, key_manager, num_images=4):
    """Gemini API를 사용하여 이미지를 생성하는 함수"""
    
    try:
        api_key = key_manager.get_random_key()
        if api_key is None:
            st.error("사용 가능한 API 키가 없습니다.")
            return None
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": f"Generate a detailed image of: {prompt}. The image should be high quality, colorful, and visually appealing for K-12 students."}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.8,
                "topP": 0.9,
                "maxOutputTokens": 2048,
                "responseModalities": ["Text", "Image"]
            }
        }
        
        headers = {
            'Content-Type': 'application/json',
            'x-goog-api-key': api_key
        }
        
        images = []
        progress_placeholder = st.empty()
        for i in range(num_images):
            progress_placeholder.info(f"이미지 {i+1}/{num_images}를 생성 중입니다... 잠시만 기다려주세요.")
            
            try:
                # 이미지 생성에 gemini-2.0-flash-exp-image-generation 모델 사용
                response = requests.post(
                    'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp-image-generation:generateContent',
                    headers=headers,
                    data=json.dumps(payload),
                    timeout=60
                )
                
                if response.status_code != 200:
                    st.warning(f"API 응답 오류 (상태 코드: {response.status_code}): {response.text}")
                    continue
                
                try:
                    data = response.json()
                except json.JSONDecodeError:
                    st.warning("API 응답을 JSON으로 파싱하는 데 실패했습니다.")
                    continue
                
                if 'candidates' in data and len(data['candidates']) > 0 and 'content' in data['candidates'][0]:
                    parts = data['candidates'][0]['content']['parts']
                    
                    image_found = False
                    for part in parts:
                        if 'inlineData' in part and 'data' in part['inlineData']:
                            try:
                                img_data = part['inlineData']['data']
                                img_bytes = base64.b64decode(img_data)
                                img = Image.open(io.BytesIO(img_bytes))
                                images.append(img)
                                image_found = True
                                break
                            except Exception as e:
                                st.warning(f"이미지 데이터 처리 중 오류: {str(e)}")
                    
                    if not image_found:
                        st.warning(f"이미지 {i+1}: API 응답에 이미지 데이터가 없습니다.")
                else:
                    st.warning(f"이미지 {i+1}: API 응답에 필요한 데이터가 포함되어 있지 않습니다.")
                    with st.expander("API 응답 상세 정보", expanded=False):
                        st.json(data)
            except requests.exceptions.RequestException as e:
                st.warning(f"이미지 {i+1} 생성 요청 중 오류: {str(e)}")
            except Exception as e:
                st.warning(f"이미지 {i+1} 생성 중 예상치 못한 오류: {str(e)}")
        
        progress_placeholder.empty()
        
        return images
    except Exception as e:
        st.error(f"이미지 생성 중 오류가 발생했습니다: {e}")
        return []

# 이미지와 프롬프트를 사용해 이미지 수정 함수
def modify_image(image, prompt, key_manager):
    """업로드된 이미지와 프롬프트를 사용하여 이미지를 수정하는 함수"""
    
    try:
        api_key = key_manager.get_random_key()
        if api_key is None:
            st.error("사용 가능한 API 키가 없습니다.")
            return None
        
        # 이미지 유효성 검사
        if image is None or not isinstance(image, Image.Image):
            st.error("유효한 이미지가 아닙니다.")
            return None
            
        # 이미지를 바이트로 변환
        try:
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
        except Exception as e:
            st.error(f"이미지 인코딩 중 오류: {str(e)}")
            return None
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": f"Modify this image based on the following prompt: {prompt}. Create a visually appealing version suitable for K-12 students."},
                        {
                            "inlineData": {
                                "mimeType": "image/png",
                                "data": img_str
                            }
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.8,
                "topP": 0.9,
                "maxOutputTokens": 2048,
                "responseModalities": ["Text", "Image"]
            }
        }
        
        headers = {
            'Content-Type': 'application/json',
            'x-goog-api-key': api_key
        }
        
        with st.spinner('이미지를 수정 중입니다...'):
            try:
                # 이미지 수정에 gemini-2.0-flash-exp-image-generation 모델 사용
                response = requests.post(
                    'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp-image-generation:generateContent',
                    headers=headers,
                    data=json.dumps(payload),
                    timeout=60
                )
                
                if response.status_code != 200:
                    st.warning(f"API 응답 오류 (상태 코드: {response.status_code}): {response.text}")
                    return None
                
                try:
                    data = response.json()
                except json.JSONDecodeError:
                    st.warning("API 응답을 JSON으로 파싱하는 데 실패했습니다.")
                    return None
                
                if 'candidates' in data and len(data['candidates']) > 0 and 'content' in data['candidates'][0]:
                    parts = data['candidates'][0]['content']['parts']
                    
                    for part in parts:
                        if 'inlineData' in part and 'data' in part['inlineData']:
                            try:
                                img_data = part['inlineData']['data']
                                img_bytes = base64.b64decode(img_data)
                                modified_img = Image.open(io.BytesIO(img_bytes))
                                return modified_img
                            except Exception as e:
                                st.warning(f"수정된 이미지 데이터 처리 중 오류: {str(e)}")
                                return None
                    
                    st.warning("API 응답에 이미지 데이터가 없습니다.")
                else:
                    st.warning("API 응답에 필요한 데이터가 포함되어 있지 않습니다.")
                    with st.expander("API 응답 상세 정보", expanded=False):
                        st.json(data)
                return None
            except requests.exceptions.RequestException as e:
                st.warning(f"이미지 수정 요청 중 오류: {str(e)}")
                return None
    except Exception as e:
        st.error(f"이미지 수정 중 오류가 발생했습니다: {e}")
        return None

# 메인 앱 인터페이스
def main():
    # 헤더
    st.title("이미지4키즈 (Image4Kids)")
    st.markdown("#### K-12 학생을 위한 안전한 AI 이미지 생성 플랫폼")
    
    # 시크릿에서 API 키 로드하는 부분 보강
    try:
        # Streamlit 시크릿에서 API 키 로드 시도
        env_api_keys = st.secrets.get("gemini", {}).get("api_keys", "")
        
        # 시크릿이 없으면 환경변수에서 시도
        if not env_api_keys:
            env_api_keys = os.getenv('GEMINI_API_KEYS', "")
        
        # API 키 분리 및 공백 제거
        api_keys = [key.strip() for key in env_api_keys.split(',') if key.strip()]
        
        # API 키가 없으면 메시지 표시
        if not api_keys:
            st.sidebar.error("API 키가 설정되지 않았습니다. Streamlit 시크릿이나 환경변수에 GEMINI_API_KEYS를 설정해주세요.")
    except Exception as e:
        st.sidebar.error(f"API 키 로드 중 오류 발생: {str(e)}")
        api_keys = []
    
    # API 키 입력 (환경변수에 키가 없거나 추가 키를 입력하는 경우를 위해)
    with st.sidebar:
        st.header("API 키 설정")
        
        if api_keys:
            st.success(f"{len(api_keys)}개의 API 키가 환경변수에서 로드되었습니다.")
            
        additional_keys = st.checkbox("추가 API 키 입력", value=not api_keys)
        
        if additional_keys:
            api_keys_text = st.text_area("Gemini API 키 (한 줄에 하나씩)", 
                                      placeholder="API 키를 여기에 입력하세요...",
                                      help="여러 API 키는 각각 새 줄에 입력하세요.")
            if api_keys_text:
                # 텍스트 영역에서 입력된 API 키 추가
                input_keys = [key.strip() for key in api_keys_text.split('\n') if key.strip()]
                api_keys.extend(input_keys)
        
        if not api_keys:
            st.warning("API 키가 필요합니다. 환경변수나 사이드바에 적어도 하나의 API 키를 입력해주세요.")
            st.stop()
    
    # 키 매니저 생성
    key_manager = KeyManager(api_keys)
    
    # 탭 기반 내비게이션
    tabs = st.tabs(["📝 AI로 그리기", "🎨 AI와 함께 그리기", "📤 AI로 수정하기"])
    
    # 탭 1: 텍스트-이미지 변환
    with tabs[0]:
        st.header("텍스트에서 이미지 생성하기")
        
        # 왼쪽-오른쪽 레이아웃
        left_col, right_col = st.columns([1, 2])
        
        with left_col:
            st.markdown('<div class="input-section">', unsafe_allow_html=True)
            st.markdown("원하는 대상을 설명하는 텍스트를 입력하면 AI가 그림을 그려줍니다.")
            
            text_prompt = st.text_area("이미지 설명", 
                                      placeholder="생성하고 싶은 이미지를 자세히 설명해보세요...",
                                      height=200)
            
            generate_button = st.button("이미지 생성", key="text_to_image_btn", use_container_width=True)
            
            # 추가 설정 섹션
            with st.expander("고급 설정"):
                num_images = st.slider("생성할 이미지 수", min_value=1, max_value=4, value=2)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with right_col:
            st.markdown('<div class="result-section">', unsafe_allow_html=True)
            
            if generate_button:
                if not text_prompt.strip():
                    st.warning("이미지 설명을 입력해주세요.")
                else:
                    # 안전성 검사
                    with st.spinner("입력 내용 처리 중..."):
                        safety_result = check_prompt_safety(text_prompt, key_manager)
                    
                    original_prompt = text_prompt
                    actual_prompt = safety_result["safePrompt"]
                    
                    # 안전하지 않은 프롬프트인 경우 이미지 수를 1개로 설정
                    images_to_generate = 1 if not safety_result["safe"] else num_images
                    
                    # 이미지 생성
                    with st.spinner("이미지를 생성 중입니다..."):
                        images = generate_image(actual_prompt, key_manager, num_images=images_to_generate)
                    
                    if images and len(images) > 0:
                        try:
                            # 안전하지 않은 프롬프트인 경우 작은 알림 표시
                            if not safety_result["safe"]:
                                st.markdown('<div class="safety-message">AI가 최적의 결과를 생성했습니다.</div>', unsafe_allow_html=True)
                            
                            st.success(f"{len(images)}개의 이미지가 생성되었습니다!")
                            
                            # 이미지 개수에 따라 열 수 조정
                            if len(images) <= 2:
                                img_cols = st.columns(len(images))
                            else:
                                rows = (len(images) + 1) // 2
                                img_cols = [st.columns(2) for _ in range(rows)]
                            
                            # 이미지 표시
                            for i, img in enumerate(images):
                                try:
                                    if img is not None and isinstance(img, Image.Image):  # 타입 체크 추가
                                        row, col = divmod(i, 2)
                                        
                                        # 레이아웃 설정에 따라 이미지 표시
                                        if len(images) <= 2:
                                            with img_cols[i]:
                                                st.image(img, caption=f"생성된 이미지 #{i+1}", use_container_width=True)
                                                
                                                # 이미지 다운로드 기능
                                                try:
                                                    buffered = io.BytesIO()
                                                    img.save(buffered, format="PNG")
                                                    img_str = base64.b64encode(buffered.getvalue()).decode()
                                                    
                                                    href = f'<a href="data:image/png;base64,{img_str}" download="generated_image{i+1}.png" class="download-btn">이미지 다운로드</a>'
                                                    st.markdown(href, unsafe_allow_html=True)
                                                except Exception as e:
                                                    st.warning(f"이미지 다운로드 준비 중 오류 발생: {str(e)}")
                                        else:
                                            with img_cols[row][col]:
                                                st.image(img, caption=f"생성된 이미지 #{i+1}", use_container_width=True)
                                                
                                                # 이미지 다운로드
                                                try:
                                                    buffered = io.BytesIO()
                                                    img.save(buffered, format="PNG")
                                                    img_str = base64.b64encode(buffered.getvalue()).decode()
                                                    
                                                    href = f'<a href="data:image/png;base64,{img_str}" download="generated_image{i+1}.png" class="download-btn">이미지 다운로드</a>'
                                                    st.markdown(href, unsafe_allow_html=True)
                                                except Exception as e:
                                                    st.warning(f"이미지 다운로드 준비 중 오류 발생: {str(e)}")
                                    else:
                                        st.warning(f"이미지 #{i+1}을 생성했으나 표시할 수 없습니다.")
                                except Exception as e:
                                    st.error(f"이미지 #{i+1} 표시 중 오류 발생: {str(e)}")
                        except Exception as e:
                            st.error(f"이미지 표시 중 오류 발생: {str(e)}")
                    else:
                        st.error("이미지 생성에 실패했습니다. 다시 시도해주세요.")
                        with st.expander("자세한 정보"):
                            st.info("API 서버에 문제가 있거나 프롬프트가 적절하지 않을 수 있습니다.")
            
            else:
                st.info("왼쪽에 이미지 설명을 입력하고 '이미지 생성' 버튼을 클릭하면 이곳에 결과가 표시됩니다.")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # 탭 2: 그리기 및 수정
    with tabs[1]:
        st.header("그림 그리기 및 AI로 수정하기")
        
        # 그림 그리기 상태 관리 - 단순화
        if 'drawing_mode' not in st.session_state:
            st.session_state.drawing_mode = True
        
        if 'current_image' not in st.session_state:
            st.session_state.current_image = None
        
        # 캔버스 표시 상태 관리 추가
        if 'show_canvas' not in st.session_state:
            st.session_state.show_canvas = False
        
        # 왼쪽-오른쪽 레이아웃 - 항상 유지
        left_col, right_col = st.columns([1, 1.2])
        
        # 왼쪽 컬럼 - 항상 컨트롤과 입력 필드 표시
        with left_col:
            st.markdown('<div class="input-section">', unsafe_allow_html=True)
            
            # 그리기 모드일 때
            if st.session_state.drawing_mode:
                st.markdown("### 그림 그리기")
                
                # 캔버스 열기 버튼
                if not st.session_state.show_canvas:
                    if st.button("🎨 캔버스 열기", use_container_width=True, type="primary"):
                        st.session_state.show_canvas = True
                        st.rerun()
                    
                    st.info("위 버튼을 클릭하면 그림을 그릴 수 있는 캔버스가 나타납니다.")
                else:
                    # 캔버스 닫기 버튼
                    if st.button("❌ 캔버스 닫기", key="close_canvas_btn"):
                        st.session_state.show_canvas = False
                        st.rerun()
                    
                    # 그리기 도구 - 펜 색상 선택기 추가
                    stroke_color_picker = st.color_picker("펜 색상", "#000000", key="stroke_color_picker")
                    stroke_width = st.slider("펜 두께", 1, 30, 5)
                    
                    # 지우개 버튼
                    eraser_button = st.button("지우개 모드", key="eraser_button")
                    if eraser_button:
                        st.session_state.eraser_mode = not st.session_state.get('eraser_mode', False)
                        st.rerun()
                    
                    # 전체 화면 지우기 버튼 추가
                    clear_button = st.button("🗑️ 전체 지우기", key="clear_canvas_btn", type="secondary")
                    if clear_button:
                        # 캔버스 키를 변경하여 새로운 캔버스 생성
                        st.session_state.canvas_key = f"canvas_{random.randint(1000, 9999)}"
                        st.rerun()
                    
                    # 지우개 모드 안내
                    if st.session_state.get('eraser_mode', False):
                        st.markdown("""
                        <div class="mode-indicator">
                            ✏️ 지우개 모드 활성화됨
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # 그림 완료 버튼
                    complete_button = st.button("✅ 그림 완료! 다음 단계로", use_container_width=True)
                
            else:
                # 결과 모드일 때
                st.markdown("### 그림 향상시키기")
                
                # 현재 그린 이미지 표시
                if st.session_state.current_image:
                    st.image(st.session_state.current_image, use_container_width=True, caption="내가 그린 그림")
                
                # 새로 그리기 버튼
                if st.button("🖌️ 다시 그리기", use_container_width=True):
                    st.session_state.drawing_mode = True
                    st.session_state.show_canvas = False  # 캔버스 먼저 숨기기
                    st.session_state.eraser_mode = False  # 지우개 모드 초기화
                    st.rerun()
                
                # 프롬프트 입력
                enhance_prompt = st.text_area("그림 향상 설명", 
                                        placeholder="AI가 그림을 어떻게 향상시키면 좋을지 설명해보세요...", 
                                        key="draw_enhance_prompt",
                                        height=100)
                
                # 향상 버튼
                enhance_button = st.button("✨ 그림 향상하기", key="enhance_drawing_btn", use_container_width=True)
                
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 오른쪽 컬럼 - 캔버스 또는 결과 표시
        with right_col:
            st.markdown('<div class="result-section">', unsafe_allow_html=True)
            
            # 그리기 모드일 때
            if st.session_state.drawing_mode:
                if st.session_state.show_canvas:
                    # 캔버스 설정
                    if st.session_state.get('eraser_mode', False):
                        stroke_color = "#ffffff"
                        stroke_width_val = 20
                    else:
                        stroke_color = stroke_color_picker
                        stroke_width_val = stroke_width
                    
                    # 캔버스 영역 안내
                    st.markdown("""
                    <div style="text-align:center; margin:15px 0; padding:15px; background-color:#f1f3f5; border-radius:8px;">
                        <h3 style="margin:0; color:#495057;">아래 영역을 클릭하여 그림을 그려보세요</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 캔버스 스타일
                    st.markdown("""
                    <style>
                    .big-canvas-area {
                        width: 95%;
                        margin: 0 auto;
                        background-color: #ffffff;
                        border: 2px solid #dee2e6;
                        border-radius: 15px;
                        padding: 20px;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                        position: relative;
                    }
                    </style>
                    """, unsafe_allow_html=True)
                    
                    # 캔버스 컨테이너
                    st.markdown('<div class="big-canvas-area">', unsafe_allow_html=True)
                    
                    # 캔버스 키 초기화
                    if 'canvas_key' not in st.session_state:
                        st.session_state.canvas_key = "canvas_main"
                    
                    # 실제 캔버스에서 canvas_main 대신 동적 키 사용
                    canvas_result = st_canvas(
                        fill_color="rgba(255, 255, 255, 0)",
                        stroke_width=stroke_width_val,
                        stroke_color=stroke_color,
                        background_color="#ffffff",
                        height=500,  # 높이
                        width=800,   # 너비
                        drawing_mode="freedraw",
                        key=st.session_state.canvas_key,
                        display_toolbar=False,
                    )
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # 버튼 클릭 처리 (완료 버튼이 왼쪽에 있지만 처리는 여기서 함)
                    if 'complete_button' in locals() and complete_button and canvas_result.image_data is not None:
                        # 이미지 데이터 처리
                        img_data = canvas_result.image_data
                        img_data = np.concatenate(
                            [img_data[:, :, :3], np.full((img_data.shape[0], img_data.shape[1], 1), 255, dtype=np.uint8)],
                            axis=2,
                        )
                        
                        # PIL 이미지로 변환
                        img = Image.fromarray(img_data.astype('uint8'), 'RGBA')
                        
                        # 그린 내용이 있는지 확인 (모든 픽셀이 하얀색인지 확인)
                        is_empty = True
                        for pixel in np.array(img).reshape(-1, 4):
                            if not np.array_equal(pixel[:3], [255, 255, 255]):
                                is_empty = False
                                break
                        
                        if not is_empty:
                            # 그린 이미지 저장
                            st.session_state.current_image = img
                            st.session_state.drawing_mode = False
                            st.session_state.show_canvas = False  # 캔버스 닫기
                            st.rerun()
                        else:
                            st.error("그림이 감지되지 않았습니다. 캔버스 영역에 그림을 그려주세요.")
                else:
                    st.markdown("""
                    <div style="text-align:center; margin:100px 0; padding:30px; background-color:#f8f9fa; border-radius:10px; border:2px dashed #adb5bd;">
                        <h2 style="color:#495057; margin-bottom:20px;">그림 그리기 준비</h2>
                        <p style="font-size:18px; margin-bottom:30px;">왼쪽의 '캔버스 열기' 버튼을 클릭하여 그림 그리기를 시작하세요.</p>
                        <img src="https://cdn-icons-png.flaticon.com/512/1250/1250615.png" width="100" style="opacity:0.5;">
                    </div>
                    """, unsafe_allow_html=True)
            else:
                # 결과 모드일 때 - 향상된 이미지 표시
                if 'enhance_button' in locals() and enhance_button:
                    if not enhance_prompt.strip():
                        st.warning("그림 향상 설명을 입력해주세요.")
                    else:
                        # 안전성 검사
                        with st.spinner("입력 내용 처리 중..."):
                            safety_result = check_prompt_safety(enhance_prompt, key_manager)
                        
                        original_prompt = enhance_prompt
                        actual_prompt = safety_result["safePrompt"]
                        
                        # 프롬프트 번역 정보 알림
                        if original_prompt != actual_prompt and safety_result["safe"]:
                            st.info(f"입력하신 프롬프트를 영어로 번역하여 처리했습니다.")
                        
                        # 이미지 수정
                        with st.spinner("그림을 향상시키는 중입니다..."):
                            modified_images = []
                            # 안전하지 않은 프롬프트인 경우 이미지 1개만 생성
                            images_to_generate = 1 if not safety_result["safe"] else 2
                            
                            for i in range(images_to_generate):
                                st.info(f"변형 이미지 {i+1}/{images_to_generate} 생성 중...")
                                modified_img = modify_image(st.session_state.current_image, actual_prompt, key_manager)
                                if modified_img:
                                    modified_images.append(modified_img)
                        
                        if modified_images and len(modified_images) > 0:
                            try:
                                # 안전하지 않은 프롬프트인 경우 작은 알림 표시
                                if not safety_result["safe"]:
                                    st.markdown('<div class="safety-message">입력 내용에 적절하지 않은 내용이 있어 AI가 안전한 대체 결과를 생성했습니다.</div>', unsafe_allow_html=True)
                                
                                # 결과 이미지 표시
                                st.subheader("AI로 향상된 그림")
                                img_cols = st.columns(len(modified_images))
                                for i, mod_img in enumerate(modified_images):
                                    try:
                                        if mod_img is not None and isinstance(mod_img, Image.Image):  # 타입 체크 추가
                                            with img_cols[i]:
                                                st.image(mod_img, caption=f"향상된 이미지 #{i+1}", use_container_width=True)
                                                
                                                # 이미지 다운로드
                                                try:
                                                    buffered = io.BytesIO()
                                                    mod_img.save(buffered, format="PNG")
                                                    img_str = base64.b64encode(buffered.getvalue()).decode()
                                                    
                                                    href = f'<a href="data:image/png;base64,{img_str}" download="enhanced_image{i+1}.png" class="download-btn">이미지 다운로드</a>'
                                                    st.markdown(href, unsafe_allow_html=True)
                                                except Exception as e:
                                                    st.warning(f"향상된 이미지 다운로드 준비 중 오류 발생: {str(e)}")
                                    except Exception as e:
                                        st.error(f"향상된 이미지 #{i+1} 표시 중 오류 발생: {str(e)}")
                            except Exception as e:
                                st.error(f"향상된 이미지 표시 중 오류 발생: {str(e)}")
                        else:
                            st.error("이미지를 향상시키는 데 문제가 발생했습니다. 다시 시도해주세요.")
                else:
                    st.info("왼쪽에서 그림 향상 설명을 입력하고 '그림 향상하기' 버튼을 클릭하면 결과가 여기에 표시됩니다.")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # 탭 3: 이미지 업로드 및 수정
    with tabs[2]:
        st.header("이미지 업로드 및 수정하기")
        
        # 왼쪽-오른쪽 레이아웃
        left_col, right_col = st.columns([1, 2])
        
        with left_col:
            st.markdown('<div class="input-section">', unsafe_allow_html=True)
            st.markdown("기존 이미지를 업로드하고 AI의 도움을 받아 수정해보세요.")
            
            uploaded_file = st.file_uploader("이미지 업로드", 
                                          type=["png", "jpg", "jpeg"], 
                                          help="최대 5MB 크기의 이미지를 업로드하세요.")
            
            if uploaded_file is not None:
                # 이미지 업로드 처리
                image = Image.open(uploaded_file)
                st.image(image, caption="업로드된 이미지", use_container_width=True)
                
                # 프롬프트 입력
                modify_prompt = st.text_area("이미지 수정 설명", 
                                         placeholder="이미지를 어떻게 수정하고 싶은지 설명해보세요...",
                                         key="modify_image_prompt",
                                         height=100)
                
                modify_button = st.button("이미지 수정하기", key="modify_image_btn", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with right_col:
            st.markdown('<div class="result-section">', unsafe_allow_html=True)
            
            if uploaded_file is not None:
                if modify_button:
                    if not modify_prompt.strip():
                        st.warning("이미지 수정 설명을 입력해주세요.")
                    else:
                        # 안전성 검사
                        with st.spinner("입력 내용 처리 중..."):
                            safety_result = check_prompt_safety(modify_prompt, key_manager)
                        
                        original_prompt = modify_prompt
                        actual_prompt = safety_result["safePrompt"]
                        
                        # 이미지 수정
                        with st.spinner("이미지를 수정 중입니다..."):
                            modified_img = modify_image(image, actual_prompt, key_manager)
                        
                        if modified_img:
                            # 안전하지 않은 프롬프트인 경우 작은 알림 표시
                            if not safety_result["safe"]:
                                st.markdown('<div class="safety-message">AI가 최적의 결과를 생성했습니다.</div>', unsafe_allow_html=True)
                                
                            # 원본과 수정된 이미지 비교 표시
                            st.subheader("원본과 수정된 이미지 비교")
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.image(image, caption="원본 이미지", use_container_width=True)
                            
                            with col2:
                                st.image(modified_img, caption="수정된 이미지", use_container_width=True)
                                
                                # 이미지 다운로드
                                buffered = io.BytesIO()
                                modified_img.save(buffered, format="PNG")
                                img_str = base64.b64encode(buffered.getvalue()).decode()
                                
                                href = f'<a href="data:image/png;base64,{img_str}" download="modified_image.png" class="download-btn">수정된 이미지 다운로드</a>'
                                st.markdown(href, unsafe_allow_html=True)
                else:
                    st.info("왼쪽에서 이미지를 업로드하고 수정 설명을 입력한 다음 '이미지 수정하기' 버튼을 클릭하면 이곳에 결과가 표시됩니다.")
            else:
                st.info("왼쪽에서 이미지를 업로드해주세요.")
            
            st.markdown('</div>', unsafe_allow_html=True)

# 앱 실행
if __name__ == "__main__":
    main() 