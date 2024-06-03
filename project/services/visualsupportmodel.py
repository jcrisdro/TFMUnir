import torch
from yolo import YoloDetector

class VisualSupportModelService:

    def __init__(self) -> None:
        self.yolo = YoloDetector()

    def trainning(self):
        # TODO:
        # @victor: Este metodo es el encargado de entrenar tu modelo, es decir, aca recibes el data set que 
        # requieras entrenar, si en caso de necesitar subir imagenes o archivos por el estilo, cargalo en la ruta
        # resources/carpeta y si tu modelo genera un archivo lo puedes guardar en resources/models/carpeta
        pass

    def predict(self, frame):
        # TODO: 
        # @victor: Este metodo es la salida del entrenamiento de tu modelo, es decir, aca recibes el 
        # el set de imagenes y las procesas para obtener el modelo entrenado.
        self.yolo.predict(frame)
        