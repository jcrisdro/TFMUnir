import cv2
import torch
from texToVoice import Speaker

classesToLabel = {
    "person" : 0,
    "bicycle" : 1,
    "car" : 2,
    "motorcycle" : 3,
    "airplane" : 4,
    "bus" : 5,
    "train" : 6,
    "truck" : 7,
    "boat" : 8,
    "traffic light" : 9,
    "fire hydrant" : 10,
    "stop sign" : 11,
    "parking meter" : 12,
    "bench" : 13,
    "bird" : 14,
    "cat" : 15,
    "dog" : 16,
    "horse" : 17,
    "sheep" : 18,
    "cow" : 19,
    "elephant" : 20,
    "bear" : 21,
    "zebra" : 22,
    "giraffe" : 23,
    "backpack" : 24,
    "umbrella" : 25,
    "handbag" : 26,
    "tie" : 27,
    "suitcase" : 28,
    "frisbee" : 29,
    "skis" : 30,
    "snowboard" : 31,
    "sports ball" : 32,
    "kite" : 33,
    "baseball bat" : 34,
    "baseball glove" : 35,
    "skateboard" : 36,
    "surfboard" : 37,
    "tennis racket" : 38,
    "bottle" : 39,
    "wine glass" : 40,
    "cup" : 41,
    "fork" : 42,
    "knife" : 43,
    "spoon" : 44,
    "bowl" : 45,
    "banana" : 46,
    "apple" : 47,
    "sandwich" : 48,
    "orange" : 49,
    "broccoli" : 50,
    "carrot" : 51,
    "hot dog" : 52,
    "pizza" : 53,
    "donut" : 54,
    "cake" : 55,
    "chair" : 56,
    "couch" : 57,
    "potted plant" : 58,
    "bed" : 59,
    "dining table" : 60,
    "toilet" : 61,
    "tv" : 62,
    "laptop" : 63,
    "mouse" : 64,
    "remote" : 65,
    "keyboard" : 66,
    "cell phone" : 67,
    "microwave" : 68,
    "oven" : 69,
    "toaster" : 70,
    "sink" : 71,
    "refrigerator" : 72,
    "book" : 73,
    "clock" : 74,
    "vase" : 75,
    "scissors" : 76,
    "teddy bear" : 77,
    "hair drier" : 78,
    "toothbrush" : 79
}


labelsToClass = {
    0 : "person" ,
    1 : "bicycle" ,
    2 : "car" ,
    3 : "motorcycle" ,
    4 : "airplane" ,
    5 : "bus" ,
    6 : "train" ,
    7 : "truck" ,
    8 : "boat" ,
    9 : "traffic light" ,
    10 : "fire hydrant" ,
    11 : "stop sign" ,
    12 : "parking meter" ,
    13 : "bench" ,
    14 : "bird" ,
    15 : "cat" ,
    16 : "dog" ,
    17 : "horse" ,
    18 : "sheep" ,
    19 : "cow" ,
    20 : "elephant" ,
    21 : "bear" ,
    22 : "zebra" ,
    23 : "giraffe" ,
    24 : "backpack" ,
    25 : "umbrella" ,
    26 : "handbag" ,
    27 : "tie" ,
    28 : "suitcase" ,
    29 : "frisbee" ,
    30 : "skis" ,
    31 : "snowboard" ,
    32 : "sports ball" ,
    33 : "kite" ,
    34 : "baseball bat" ,
    35 : "baseball glove" ,
    36 : "skateboard" ,
    37 : "surfboard" ,
    38 : "tennis racket" ,
    39 : "bottle" ,
    40 : "wine glass" ,
    41 : "cup" ,
    42 : "fork" ,
    43 : "knife" ,
    44 : "spoon" ,
    45 : "bowl" ,
    46 : "banana" ,
    47 : "apple" ,
    48 : "sandwich" ,
    49 : "orange" ,
    50 : "broccoli" ,
    51 : "carrot" ,
    52 : "hot dog" ,
    53 : "pizza" ,
    54 : "donut" ,
    55 : "cake" ,
    56 : "chair" ,
    57 : "couch" ,
    58 : "potted plant" ,
    59 : "bed" ,
    60 : "dining table" ,
    61 : "toilet" ,
    62 : "tv" ,
    63 : "laptop" ,
    64 : "mouse" ,
    65 : "remote" ,
    66 : "keyboard" ,
    67 : "cell phone" ,
    68 : "microwave" ,
    69 : "oven" ,
    70 : "toaster" ,
    71 : "sink" ,
    72 : "refrigerator" ,
    73 : "book" ,
    74 : "clock" ,
    75 : "vase" ,
    76 : "scissors" ,
    77 : "teddy bear" ,
    78 : "hair drier" ,
    79 : "toothbrush"
}

class YoloDetector:

    def __init__(self) -> None:
        #cargamos el modelo pre entrenado de yolo
        self.model = torch.hub.load("ultralytics/yolov5", model="yolov5n", pretrained=True)
        
        #filtramos según las clases que queremos que el modelo sea capaz de detectar
        self.classes_list = [classesToLabel["person"], classesToLabel["bicycle"], classesToLabel["car"], classesToLabel["motorcycle"], classesToLabel["bus"], classesToLabel["train"], classesToLabel["truck"], classesToLabel["traffic light"], 
                        classesToLabel["bench"], classesToLabel["backpack"], classesToLabel["handbag"], classesToLabel["suitcase"], classesToLabel["sports ball"], classesToLabel["skateboard"], classesToLabel["bottle"]]
        self.model.classes = [self.classes_list]
        print("YOLO initialized")


    def detect(self):
        #instanciamos la camara a tiempo real y el objeto speaker
        cap = cv2.VideoCapture(0)
        speaker = Speaker(language="en-US")

        while cap.isOpened():

            status, frame = cap.read()
            if not status or (cv2.waitKey(10) & 0xFF == ord('q')):
                break

            #obtenemos una predicción y filtramos unicamente con las predicciones con un 50% de confianza
            pred = self.model(frame)
            df = pred.pandas().xyxy[0]
            df = df[df["confidence"] > 0.5]

            if df.shape[0] > 0:
                #obtenemos el objeto mas cercano
                nearest_object = labelsToClass[df.iloc[0]['class']]

                #generamos una respuesta por voz 
                speaker.generateWithGoogle("You are infront of a " + nearest_object)

                #dibujamos la box que delimita al objeto detectado
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

            #mostramos elframe
            cv2.imshow("frame", frame)
    
        
