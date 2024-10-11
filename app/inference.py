import logging
import os
from typing import Dict, List
import uuid
from ultralytics import YOLO
from app.config import (
    CONFIDENCE,
    STREAM,
    DICT_CLASSES,
)
from app.utils import create_directory


def detect_yolov8_obb(list_images: List[str]) -> List[Dict]:
    task_id = str(uuid.uuid4())
    logging.info("worker_init")
    logging.info("Initialization YOLOv8")
    model = YOLO("/object-detection/app/weights/best.pt")
    temp_path = os.path.join(os.path.dirname(list_images[0]), task_id)
    create_directory(temp_path)
    processing_status = []
    for image_path in list_images:
        list_classes = list(DICT_CLASSES.values())
        res_output = {
            "image_path": image_path,
            "processed": False,
            "result_path": None,
        }
        result = model(
            image_path,
            classes=list_classes,
            conf=CONFIDENCE,
            stream=STREAM,
        )
        result = [res for res in result][0]
        logging.info("Save results of %s", result.path)
        res_output_path = os.path.join(
            temp_path, os.path.basename(result.path).split(".tif")[0] + ".txt"
        )
        result.save_txt(res_output_path, save_conf=True)
        if os.path.exists(res_output_path):
            res_output = {
                "image_path": image_path,
                "processed": True,
                "result_path": res_output_path,
            }
        else:
            res_output = {
                "image_path": image_path,
                "processed": True,
                "result_path": None,
            }
        processing_status.append(res_output)
    return processing_status
