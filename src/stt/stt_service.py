import grpc
import json
import pyaudio
import time
from config import settings
from proto import nest_pb2, nest_pb2_grpc
import socket
import requests

class RealtimeSTT:
    def __init__(self):
        self.initialize_connection()

    def initialize_connection(self):
        self.channel = grpc.secure_channel(settings.CLOVA_ENDPOINT, grpc.ssl_channel_credentials())
        self.stub = nest_pb2_grpc.NestServiceStub(self.channel)
        self.metadata = [
            ('authorization', f'Bearer {settings.CLOVA_API_KEY}'),
        ]

    def check_internet_connection(self):
        try:
            # DNS 확인을 통한 인터넷 연결 체크
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False

    def wait_for_internet(self):
        while not self.check_internet_connection():
            print("인터넷 연결이 끊겼습니다. 재연결을 기다리는 중...")
            time.sleep(5)  # 5초마다 재확인
        print("인터넷이 다시 연결되었습니다. 프로그램을 재시작합니다.")

    def generate_request(self):
        yield nest_pb2.NestRequest(
            type=nest_pb2.RequestType.CONFIG,
            config=nest_pb2.NestConfig(
                config=json.dumps(settings.SPLIT_CONFIG)
            )
        )

        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=settings.SAMPLE_RATE, input=True, frames_per_buffer=settings.CHUNK_SIZE)

        try:
            while True:
                data = stream.read(settings.CHUNK_SIZE)
                yield nest_pb2.NestRequest(
                    type=nest_pb2.RequestType.DATA,
                    data=nest_pb2.NestData(
                        chunk=data,
                        extra_contents=json.dumps({"seqId": 0, "epFlag": False})
                    )
                )
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()

    def start_recognition(self):
        while True:
            try:
                responses = self.stub.recognize(self.generate_request(), metadata=self.metadata)
                for response in responses:
                    response_data = json.loads(response.contents)
                    if 'transcription' in response_data:
                        yield response_data['transcription']['text']

            except grpc.RpcError as e:
                print(f"gRPC 오류 발생: {e.code()}")
                self.wait_for_internet()
                # 연결 재설정
                try:
                    self.channel.close()
                except:
                    pass
                self.initialize_connection()
                continue  # 루프를 계속 실행

            except Exception as e:
                print(f"예상치 못한 오류 발생: {str(e)}")
                self.wait_for_internet()
                continue

    def run(self):
        print("실시간 음성 인식을 시작합니다. 종료하려면 Ctrl+C를 누르세요.")
        while True:
            try:
                for text in self.start_recognition():
                    if len(text) != 0:
                        return text
            except KeyboardInterrupt:
                print("프로그램을 종료합니다.")
                break
            finally:
                try:
                    self.channel.close()
                except:
                    pass