from concurrent import futures
import time
import logging
import grpc
import modelYolov8_pb2 as model_pb2
import modelYolov8_pb2_grpc as model_pb2_grpc
from app.inference import detect_yolov8_obb

logging.getLogger().setLevel(logging.INFO)


class ImageProcessorServicer(model_pb2_grpc.ImageProcessorServicer):
    def ProcessImage(self, request, context):
        input_image_paths = request.input_image_paths
        result = self.run_model(input_image_paths)
        return model_pb2.ImageResponse(entries=result)  # pylint: disable=E1101

    def run_model(self, input_s3_uri):
        result = detect_yolov8_obb(input_s3_uri)
        return result


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    model_pb2_grpc.add_ImageProcessorServicer_to_server(
        ImageProcessorServicer(), server
    )
    server.add_insecure_port("[::]:8061")
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()
