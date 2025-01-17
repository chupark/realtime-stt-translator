# 클로바 STT를 사용한 실시간 번역
Clova Speech의 실시간 음성인식과 Papago API를 활용한 실시간 한-일 번역 프로그램 입니다.  
STT만 필요할 경우 `src/main.py` 파일을 아래 사진과 같이 빨간색 박스 부분을 주석처리하여 사용합니다. 또한 [실행 방법](#실행-방법)의 환경변수 설정의 생략이 가능합니다. 자세한 내용은 [실행 방법](#실행-방법)참조.  
![alt text](images/image.png)

<br>

> 라이센스 정책에 따라 해당 데모 프로그램을 외부에 시연할 경우, "Naver Cloud Platform" 출처를 명시하셔야 합니다.
데모 프로그램에 커스텀 모델 추가 등 새로운 기능을 추가하여 시연할 경우에도 "Naver Cloud Platform" 출처를 명시하셔야 합니다.

<br>

# 실행 방법
```bash
## 가상 환경 만들기
python3 -m venv .venv

## 가상 환경 실행
# MAC / Linux
. .venv/bin/activate
# Windows
. .venv/Script/activate

## for mac
# MAC은 pyaudio 설치 전 portaudio 설치가 필요합니다.
brew install portaudio

## 의존성 설치
pip install -r requirements.txt
## 의존성 설치에 불구하고 실행이 안될 경우 아래 패키지 설치
pip install pyaudio
pip install grpcio
pip install --upgrade google-api-python-client


## 환경변수 입력
export CLOVA_API_KEY="<CLOVA_API_KEY>"
# STT만 사용할 경우, 아무 값이나 넣어도 됨
# 예시 export PAPAGO_CLIENT_ID="aa"
export PAPAGO_CLIENT_ID="<PAPAGO_CLIENT_ID>"
export PAPAGO_CLIENT_SECRET="<PAPAGO_CLIENT_SECRET>"

# 실행
python __main__.py
```