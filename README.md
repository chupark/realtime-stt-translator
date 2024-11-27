# 클로바 STT를 사용한 실시간 번역

# 실행 방법
```bash
# 가상 환경 만들기
python3 -m venv .venv

# 가상 환경 실행
. .venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# 환경변수 입력
export CLOVA_API_KEY="<CLOVA_API_KEY>"
export PAPAGO_CLIENT_ID="<PAPAGO_CLIENT_ID>"
export PAPAGO_CLIENT_SECRET="<PAPAGO_CLIENT_SECRET>"

# 실행
python __main__.py
```