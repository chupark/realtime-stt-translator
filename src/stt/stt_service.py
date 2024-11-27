# import grpc
# import json
# import pyaudio
# import webrtcvad
# from config import settings
# from proto import nest_pb2, nest_pb2_grpc
# import logging
# import os

# logging.basicConfig(level=logging.INFO)
# os.environ['GRPC_ENABLE_FORK_SUPPORT'] = '0'

# class RealtimeSTT:
#     def __init__(self):
#         try:
#             self.channel = grpc.secure_channel(settings.CLOVA_ENDPOINT, grpc.ssl_channel_credentials())
#             self.stub = nest_pb2_grpc.NestServiceStub(self.channel)
#             self.metadata = [
#                 ('authorization', f'Bearer {settings.CLOVA_API_KEY}'),
#             ]
#             self.vad = webrtcvad.Vad(3)  # VAD 감도 설정 (0-3, 3이 가장 민감함)
#             self.frame_duration = 30  # ms
#             self.sample_rate = 16000  # Hz
#             self.frame_size = int(self.sample_rate * self.frame_duration / 1000)
#         except Exception as e:
#             logging.error(f"초기화 중 오류 발생: {e}")
#             raise

#     def generate_request(self):
#         yield nest_pb2.NestRequest(
#             type=nest_pb2.RequestType.CONFIG,
#             config=nest_pb2.NestConfig(
#                 config=json.dumps(settings.SPLIT_CONFIG)
#             )
#         )

#         p = pyaudio.PyAudio()
#         stream = p.open(format=pyaudio.paInt16, channels=1, rate=self.sample_rate, input=True, frames_per_buffer=self.frame_size)

#         try:
#             while True:
#                 frame = stream.read(self.frame_size)
#                 try:
#                     if self.vad.is_speech(frame, self.sample_rate):
#                         yield nest_pb2.NestRequest(
#                             type=nest_pb2.RequestType.DATA,
#                             data=nest_pb2.NestData(
#                                 chunk=frame,
#                                 extra_contents=json.dumps({"seqId": 0, "epFlag": False})
#                             )
#                         )
#                 except webrtcvad.Error as e:
#                     logging.error(f"WebRTC VAD 오류: {e}")
#                 except Exception as e:
#                     logging.error(f"프레임 처리 중 오류 발생: {e}")
#         except Exception as e:
#             logging.error(f"오디오 스트림 처리 중 오류 발생: {e}")
#         finally:
#             stream.stop_stream()
#             stream.close()
#             p.terminate()

#     def start_recognition(self):
#         try:
#             responses = self.stub.recognize(self.generate_request(), metadata=self.metadata)
#             for response in responses:
#                 response_data = json.loads(response.contents)
#                 # logging.info(f"서버 응답: {response_data}")
#                 if 'transcription' in response_data:
#                     yield response_data['transcription']['text']
#         except grpc.RpcError as e:
#             logging.error(f"gRPC 오류 발생: {e}")
#         except Exception as e:
#             logging.error(f"인식 중 예기치 않은 오류 발생: {e}")

#     def run(self):
#         logging.info("실시간 음성 인식을 시작합니다. 종료하려면 Ctrl+C를 누르세요.")
#         try:
#             for text in self.start_recognition():
#                 if len(text) != 0:
#                     return text
#         except KeyboardInterrupt:
#             logging.info("사용자에 의해 프로그램이 종료되었습니다.")
#         except Exception as e:
#             logging.error(f"실행 중 예기치 않은 오류 발생: {e}")
#         finally:
#             self.channel.close()



import grpc
import json
import pyaudio
from config import settings
from proto import nest_pb2, nest_pb2_grpc

class RealtimeSTT:
    def __init__(self):
        self.channel = grpc.secure_channel(settings.CLOVA_ENDPOINT, grpc.ssl_channel_credentials())
        self.stub = nest_pb2_grpc.NestServiceStub(self.channel)
        self.metadata = [
            ('authorization', f'Bearer {settings.CLOVA_API_KEY}'),
        ]

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
        responses = self.stub.recognize(self.generate_request(), metadata=self.metadata)
        for response in responses:
            response_data = json.loads(response.contents)
            if 'transcription' in response_data:
                yield response_data['transcription']['text']

    def run(self):
        print("실시간 음성 인식을 시작합니다. 종료하려면 Ctrl+C를 누르세요.")
        try:
            for text in self.start_recognition():
                if len(text) != 0 :
                    return text
        except KeyboardInterrupt:
            print("프로그램을 종료합니다.")
        finally:
            self.channel.close()
