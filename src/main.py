import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

src_path = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, src_path)
from stt.stt_service import RealtimeSTT
from translator.translation_service import PapagoTranslator

def is_non_empty_text(text):
    return len(''.join(text.split())) > 0

def main():
    stt_service = RealtimeSTT()
    translation_service = PapagoTranslator()
    
    print("실시간 음성 인식을 시작합니다. 종료하려면 Ctrl+C를 누르세요.")

    try:
        for text in stt_service.start_recognition():
            if is_non_empty_text(text):
                translated_text = translation_service.translate(text=text)
                print(f"한글 : {text}")
                print(f"일어 : {translated_text}")

    except KeyboardInterrupt:
        print("프로그램을 종료합니다.")
    finally:
        stt_service.channel.close()


if __name__ == "__main__":
    main()