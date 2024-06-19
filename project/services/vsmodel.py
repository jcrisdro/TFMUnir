import torch
import os
import cv2
import pandas as pd
import base64
import shutil
import mimetypes

from datetime import datetime

from constants import CLASSESTOLABEL, LABELTOCLASSES, PATH_DIRECTORY, ROOT_PROJECT, COlORS

class VSModelService:
    """ training model adapter """

    def __init__(self) -> None:
        self.yolo_client = None
        # TODO: mover ubicacion de modelo a resources/models/yolov5n.model
        self.video_model = torch.hub.load("ultralytics/yolov5", model="yolov5n", pretrained=True)

    def __del__(self) -> None:
        print("VSModelService stopped")

    def picture_to_frame(self, file_dict: str = None):
        """ picture to frame """
        frame = cv2.imread(file_dict['path'])
        return frame

    def predict(self, frame: object = None):
        """ predict """
        predict = self.video_model(frame)
        df = predict.pandas().xyxy[0]
        df = df[df["confidence"] > 0.5]
        return df, frame

    # TODO: optimizar codigo e integrar predict y process
    def process(self, df: object = None, frame: object = None):
        """ process """
        objects = []
        for index in range(0, df.shape[0]):
            objects.append({'name': LABELTOCLASSES[df.iloc[index]['class']], 'distance': 0, 'color': COlORS[index]})
            bbox = df.iloc[index][["xmin", "ymin", "xmax", "ymax"]].values.astype(int)
            bbox = [bbox[0] + 10, bbox[1] - 10, bbox[2] - 10, bbox[3] - 10]
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255,255,0), 2)
            cv2.putText(
                img = frame, text = f"{df.iloc[index]['name']}: {round(df.iloc[index]['confidence'], 4)}",
                org=(bbox[0], bbox[1]-15), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2,
                color=COlORS[index], thickness=2)
            cv2.imshow("frame", frame)
        return {
            'objects': objects,
            'picture': base64.b64encode(cv2.imencode('.jpg', frame)[1]).decode('utf-8')
        }
    
    def load(self, file: object = None, path: str = None):
        """ load """
        now = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")
        try:
            if file:
                os.mkdir(f"{ROOT_PROJECT}/uploads/{now}")
                file_path = PATH_DIRECTORY / f"{now}/{now}.{file.filename.split('.')[-1]}"
                with file_path.open("wb") as fp:
                    shutil.copyfileobj(file.file, fp)
                    fp.write(file.file.read())
            elif path:
                file_path = PATH_DIRECTORY / f"{now}.{path.split('.')[-1]}"
                shutil.copy2(path, file_path)

            attr_file = {
                'path': f"{ROOT_PROJECT}/uploads/{now}/{now}.{file.filename.split('.')[-1]}", 
                'file_size': os.path.getsize(file_path),
                'content_type': mimetypes.guess_type(file_path)
                }

            response = {'frames': 1, 'key': now, 'language': None, 'transcription': None}
            return attr_file | response
        except Exception as e:
            return f"Exception: {e}"

