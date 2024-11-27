import os

CLOVA_API_KEY = os.getenv("CLOVA_API_KEY")
CLOVA_ENDPOINT = "clovaspeech-gw.ncloud.com:50051"

PAPAGO_CLIENT_ID = os.getenv("PAPAGO_CLIENT_ID")
PAPAGO_CLIENT_SECRET = os.getenv("PAPAGO_CLIENT_SECRET")
PAPAGO_ENDPOINT = "https://naveropenapi.apigw.ntruss.com/nmt/v1/translation"

SAMPLE_RATE = 16000
CHUNK_SIZE = 256

SPLIT_CONFIG = {
    "transcription": {
      "language": "ko"
    },
    # Keyword Boosting 설정 정보
    "keywordBoosting": {    # optional, top level key
      "boostings": [
        {
          "words": "",
          "weight": 1
        }
      ]
    },
    "semanticEpd": {
      "skipEmptyText": False,
      "useWordEpd": False,
      "usePeriodEpd": True,
      "gapThreshold": 500,
      "durationThreshold": 10000,
      "syllableThreshold": 0
    }
  }

class PapagoLang:
    KOREAN = 'ko'
    JAPANESE = 'ja'
    ENGLISH = 'en'

PAPAGO_LANG = PapagoLang()