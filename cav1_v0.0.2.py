from services.emotions import Emotions
from services.trainner import Trainner


EMOTIONS = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
COLORS = {'angry': (0, 0, 255), 'disgust': (0, 128, 255), 'fear': (0, 255, 255), 'happy': (255, 0, 0), 
          'neutral': (255, 128, 0), 'sad': (255, 255, 0), 'surprise': (255, 255, 128)}
BATCH_SIZE = 128
EPOCHS = 3

if __name__ == '__main__':
    """
    Obtenemos las emociones
    """
    # emotion = Emotions(EMOTIONS, COLORS)


    trainner = Trainner(EMOTIONS, COLORS, EPOCHS, BATCH_SIZE)

    """
    Generamos archivo csv
    """
    # trainner.generate_csv(demo=False, counter=0)
    
    """
    Cargamos datos de las imagenes y entrenamos el modelo
    """
    response = trainner.load_dataset(demo=True, counter=0, classes=len(EMOTIONS))
    model = trainner.build_network((48, 48, 1), len(EMOTIONS), "categorical_crossentropy", "Adam", "accuracy")
    checkpoint_pattern = "model-ep{epoch:03d}-loss{loss:.3f}-val_loss{val_loss:.3f}.h5.keras"
    trainner.checkpoint_network(checkpoint_pattern=checkpoint_pattern)
    # print(model.summary())
