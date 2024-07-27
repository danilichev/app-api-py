from facenet_pytorch import MTCNN
from fastapi import UploadFile
from mivolo.model.mi_volo import MiVOLO, prepare_classification_images
from PIL import Image
from typing import Optional, Tuple
import cv2
import os
import torch

from src.config import config
from src.utils.files import write_temp_file


class AgeEstimator:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AgeEstimator, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        gpu_index = 0
        self.device = torch.device(gpu_index if torch.cuda.is_available() else "cpu")
        self.age_estimation_model = MiVOLO(
            config.mivolo_checkpoints_path,
            device=self.device,
            half=True,
            use_persons=False,
            verbose=True,
        )
        self.face_detection_model = MTCNN(device=self.device, post_process=False)

    async def estimate_age(
        self, image: UploadFile
    ) -> Tuple[Optional[int], Optional[str]]:
        try:
            img_path = await write_temp_file(image)
            base, ext = os.path.splitext(img_path)
            aligned_img_path = f"{base}_aligned{ext}"
            pil_img = Image.open(img_path)
            face_tensor = self.face_detection_model(
                pil_img, return_prob=False, save_path=aligned_img_path
            )

            if face_tensor is None:
                return None, "No face detected"

            cv2_img = cv2.imread(aligned_img_path)
            face_input = prepare_classification_images(
                [cv2_img],
                self.age_estimation_model.input_size,
                self.age_estimation_model.data_config["mean"],
                self.age_estimation_model.data_config["std"],
                device=self.age_estimation_model.device,
            )

            output = self.age_estimation_model.inference(face_input)
            age = output.item()

            meta = self.age_estimation_model.meta
            age = age * (meta.max_age - meta.min_age) + meta.avg_age

            return round(age), None
        except Exception as e:
            return None, str(e)
