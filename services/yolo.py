import cv2
import torch

class YoloDetector:

    def __init__(self) -> None:
        self.model = torch.hub.load("ultralytics/yolov5", model="yolov5n", pretrained=True)


    def detect(self):
        cap = cv2.VideoCapture(0)

        while cap.isOpened():

            status, frame = cap.read()
            if not status or (cv2.waitKey(10) & 0xFF == ord('q')):
                break

            pred = self.model(frame)
            
            df = pred.pandas().xyxy[0]
            df = df[df["confidence"] > 0.5]

            for i in range(df.shape[0]):
                bbox = df.iloc[i][["xmin", "ymin", "xmax", "ymax"]].values.astype(int)

                cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255,0,0), 2)
                cv2.putText(img=frame, 
                            text=f"{df.iloc[i]['name']}: {round(df.iloc[i]['confidence'], 4)}", 
                            org=(bbox[0], bbox[1]-15), 
                            fontFace=cv2.FONT_HERSHEY_PLAIN, 
                            fontScale=2, 
                            color=(255,255,255), 
                            thickness=2)


            cv2.imshow("frame", frame)
    
        
