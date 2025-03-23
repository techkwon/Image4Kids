# Image4Kids (이미지4키즈)

K-12 학생을 위한 안전한 AI 이미지 생성 플랫폼입니다. 생성형 AI의 힘을 빌려 아이들이 상상력을 발휘하고 창의적인 이미지를 만들 수 있도록 도와줍니다.

## 주요 기능

1. **AI로 그리기**: 텍스트 설명을 통해 AI가 이미지를 생성합니다.
2. **AI와 함께 그리기**: 직접 그린 그림을 AI가 향상시켜 줍니다.
3. **AI로 수정하기**: 업로드한 이미지를 AI가 수정해 줍니다.

## 안전성

모든 프롬프트(입력 텍스트)는 K-12 학생에게 적합한 콘텐츠인지 검사합니다. 부적절한 내용이 감지되면 자동으로 안전한 이미지를 생성합니다.

## 로컬에서 실행하기

1. 저장소 클론:
   ```
   git clone https://github.com/techkwon/Image4Kids.git
   cd Image4Kids
   ```

2. 가상환경 설정 및 의존성 설치:
   ```
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Gemini API 키 설정:
   `.streamlit/secrets.toml` 파일을 만들고 다음과 같이 설정합니다:
   ```
   [gemini]
   api_keys = "YOUR_GEMINI_API_KEY_1,YOUR_GEMINI_API_KEY_2"
   ```

4. 앱 실행:
   ```
   streamlit run app.py
   ```

## Streamlit Cloud에 배포하기

1. Streamlit Cloud에서 새 앱 배포
2. GitHub 저장소와 main 브랜치 연결
3. 대시보드에서 Secrets 설정 (gemini.api_keys)
4. 배포 시작

## 기술 스택

- **프론트엔드/백엔드**: Streamlit
- **이미지 생성**: Google Gemini API
- **이미지 처리**: Pillow (PIL)
- **캔버스 드로잉**: Streamlit Drawable Canvas

## 라이선스

MIT License 