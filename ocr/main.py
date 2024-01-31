import numpy as np
from proto.grpc_server import GrpcServer
from services.services import road_detection
import cv2
from PIL import Image
import grpc
from proto import requests_pb2_grpc, requests_pb2

if __name__ == "__main__":
    grpc_server = GrpcServer(road_detection)
    grpc_server.run(port=8181)

    # img_array = np.array(Image.open('img.png'))[:,:,:3]
    # info = road_detection.analyze(img_array)
    # print(info)
    
    # cam = cv2.VideoCapture("road.mp4")
    # fps = round(cam.get(cv2.CAP_PROP_FPS))
    # current_frame = 0
    # result = []
    # while True:
    #     success, img_array = cam.read()
    #     if success:
    #         if current_frame % (1*fps) == 0:
    #             info = road_detection.predict(img_array)
    #             print(info)
    #         current_frame += 1
    #     else:
    #         cam.release()
    #         cv2.destroyAllWindows()
    #         break
