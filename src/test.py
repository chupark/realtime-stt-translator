import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

src_path = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, src_path)
from translator.translation_service import PapagoTranslator

def is_non_empty_text(text):
    return len(''.join(text.split())) > 0

def main():
    translation_service = PapagoTranslator()
    
    print("실시간 음성 인식을 시작합니다. 종료하려면 Ctrl+C를 누르세요.")

    try:
  
        translated_text = translation_service.translate(text="""나는 <span translate="no">#비티에스를</span> 좋아합니다.""")
        print(f"한글 : {translated_text}")

    except KeyboardInterrupt:
        print("프로그램을 종료합니다.")


if __name__ == "__main__":
    main()