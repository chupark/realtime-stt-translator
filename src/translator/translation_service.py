import requests
from config import settings

class PapagoTranslator:
    def __init__(self):
        self.url = settings.PAPAGO_ENDPOINT
        self.headers = {
            "X-NCP-APIGW-API-KEY-ID": settings.PAPAGO_CLIENT_ID,
            "X-NCP-APIGW-API-KEY": settings.PAPAGO_CLIENT_SECRET,
            "Content-Type": "application/x-www-form-urlencoded"
        }

    def translate(self, text, source='ko', target='ja'):
        data = {
            "source": source,
            "target": target,
            "text": text
        }
        response = requests.post(self.url, headers=self.headers, data=data)
        if response.status_code == 200:
            result = response.json()
            return result['message']['result']['translatedText']
        else:
            print(f"번역 오류: {response.status_code}, {response.text}")
            return None