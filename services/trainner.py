import os, cv2, csv, glob
import numpy as np
import matplotlib.pyplot as plt

from tensorflow.keras.utils import (img_to_array, to_categorical)
from tensorflow.keras.models import (Model, load_model)
from tensorflow.keras.layers import (Input, Conv2D, ELU, BatchNormalization, MaxPooling2D, Dropout, Flatten, Dense, 
                                     Softmax)
from tensorflow.keras.optimizers import (Adam)
from tensorflow.keras.callbacks import (ModelCheckpoint)
from tensorflow.keras.preprocessing.image import (ImageDataGenerator)



# from tensorflow.keras.preprocessing.image import (img_to_array, ImageDataGenerator)


class Trainner:
    
    def __init__(self, emotions, colors, epochs, batch_size) -> None:
        self.emotions = emotions
        self.colors = colors
        self.img_size = (48, 48)
        self.kernel_size = (3, 3)
        self.ki = 'he_normal'
        self.train_images = []
        self.train_labels = []
        self.test_images = []
        self.test_labels = []
        self.validate_images = []
        self.validate_labels = []
        self.model = None
        self.epochs = epochs
        self.batch_size = batch_size
        np.set_printoptions(threshold=np.inf)

    def __del__(self) -> None:
        pass

    def build_network(self, input_shape, classes, loss: str = None, optimizer: str = None, metrics: list = None):
        input = Input(shape=input_shape)

        x = Conv2D(filters=32, kernel_size=self.kernel_size, padding='same', kernel_initializer=self.ki)(input)
        x = ELU()(x)
        x = BatchNormalization(axis=-1)(x)

        x = Conv2D(filters=32, kernel_size=self.kernel_size, padding='same', kernel_initializer=self.ki)(x)
        x = ELU()(x)
        x = BatchNormalization(axis=-1)(x)
        x = MaxPooling2D(pool_size=(2, 2))(x)
        x = Dropout(rate=0.25)(x)

        x = Conv2D(filters=64, kernel_size=self.kernel_size, padding='same', kernel_initializer=self.ki)(x)
        x = ELU()(x)
        x = BatchNormalization(axis=-1)(x)

        x = Conv2D(filters=64, kernel_size=self.kernel_size, padding='same', kernel_initializer=self.ki)(x)
        x = ELU()(x)
        x = BatchNormalization(axis=-1)(x)
        x = MaxPooling2D(pool_size=(2, 2))(x)
        x = Dropout(rate=0.25)(x)

        x = Conv2D(filters=128, kernel_size=self.kernel_size, padding='same', kernel_initializer=self.ki)(x)
        x = ELU()(x)
        x = BatchNormalization(axis=-1)(x)

        x = Conv2D(filters=128, kernel_size=self.kernel_size, padding='same', kernel_initializer=self.ki)(x)
        x = ELU()(x)
        x = BatchNormalization(axis=-1)(x)
        x = MaxPooling2D(pool_size=(2, 2))(x)
        x = Dropout(rate=0.25)(x)

        x = Flatten()(x)
        x = Dense(units=64, kernel_initializer=self.ki)(x)
        x = ELU()(x)
        x = BatchNormalization(axis=-1)(x)
        x = Dropout(rate=0.5)(x)

        x = Dense(units=64, kernel_initializer=self.ki)(x)
        x = ELU()(x)
        x = BatchNormalization(axis=-1)(x)
        x = Dropout(rate=0.5)(x)

        x = Dense(units=classes, kernel_initializer=self.ki)(x)
        output = Softmax()(x)

        if optimizer is None or loss is None:
            self.model = Model(input, output)
        if optimizer == "Adam":
            self.model = Model(input, output)
            self.model.compile(loss=loss, optimizer=Adam(learning_rate=0.003), metrics=[metrics])
        return self.model
        # model.compile(loss='categorical_crossentropy', optimizer=Adam(lr=0.003), metrics=['accuracy'])

    def checkpoint_network(self, checkpoint_pattern: str = None):
        best_checkpoint, accuracy = None, 0
        try:
            checkpoint = ModelCheckpoint(f"model/{checkpoint_pattern}", monitor='val_loss', verbose=1, save_best_only=True, mode='min')
            train_augmenter = ImageDataGenerator(rotation_range=10, zoom_range=0.1, horizontal_flip=True, rescale=1. / 255., fill_mode='nearest')
            train_gen = train_augmenter.flow(self.train_images, self.train_labels, batch_size=self.batch_size)
            train_steps = len(self.train_images)
            print(f"train_steps: {train_steps}")

            validate_augmenter = ImageDataGenerator(rescale=1. / 255.)
            validate_gen = validate_augmenter.flow(self.validate_images, self.validate_labels, batch_size=self.batch_size)
            validate_steps = len(self.validate_images)
            print(f"validate_steps: {validate_steps}")
            
            self.model.fit(train_gen, steps_per_epoch=train_steps, validation_data=validate_gen, epochs=self.epochs, verbose=1, callbacks=[checkpoint])
            test_augmenter = ImageDataGenerator(rescale=1. / 255.)
            test_gen = test_augmenter.flow(self.test_images, self.test_labels, batch_size=self.batch_size)
            test_steps = len(self.test_images)
            print(f"test_steps: {test_steps}")

            # best_checkpoint = sorted(list(glob.glob('./*.h5')), reverse=True)[0]
            # print(f"best_checkpoint: {best_checkpoint}")
            
            # best_model = load_model(best_checkpoint)
            # print(f"best_model: {best_model}")

            # _, accuracy = best_model.evaluate(test_gen, steps=test_steps)
        except Exception as e:
            print(f"checkpoint {e}")
        finally:
            print(f'Cargando el mejor modelo: {best_checkpoint}')
            print(f'Accuracy: {accuracy * 100:.2f}%')

    def load_dataset(self, demo: bool = False, counter: int = 10, classes: int = 0):
        csv_path = 'resources/data/fer2013/fer2013.csv'
        if demo is True:
            csv_path = 'resources/data/dem2013/dem2013.csv'

        total = 0
        
        with open(csv_path, 'r') as file:
            for line in csv.DictReader(file):
                label = int(self.emotions.index(line['emotion']))
                try:
                    image = img_to_array(
                        self.array2img(arr_image=line['pixels'], label_image=line['emotion'], show_image=False), 
                        data_format="channels_last",
                        dtype=None)
                    total = total + 1
                except Exception as e:
                    counter = counter + 1
                    print(f"{line['usage']} \t {label} {e} ")

                if counter > 0:
                    image_counter = self.array2img(arr_image=line['pixels'], label_image=line['emotion'], show_image=True)
                    self.show_image(im_array=image_counter, label=line['emotion'])
                    counter = counter - 1

                if line['usage'] == 'Training':
                    self.train_images.append(image)
                    self.train_labels.append(label)
                elif line['usage'] == 'PrivateTest':
                    self.validate_images.append(image)
                    self.validate_labels.append(label)
                else:
                    self.test_images.append(image)
                    self.test_labels.append(label)

        self.train_images = np.array(self.train_images)
        self.validate_images = np.array(self.validate_images)
        self.test_images = np.array(self.test_images)

        self.train_labels = to_categorical(np.array(self.train_labels), classes)
        self.validate_labels = to_categorical(np.array(self.validate_labels), classes)
        self.test_labels = to_categorical(np.array(self.test_labels), classes)

        # print(f"{self.train_images} {self.train_labels}")
        # print(f"{self.validate_images} {self.validate_labels}")
        # print(f"{self.test_images} {self.test_labels}")
        return (self.train_images, self.train_labels), (self.validate_images, self.validate_labels), (self.test_images, self.test_labels)

    def generate_csv(self, demo: bool = False, counter: int = 10):
        name = 'fer2013' if demo is False else 'dem2013'
        csv_path = f'resources/data/{name}/{name}.csv'
        os.remove(csv_path) if os.path.exists(csv_path) else None

        options = [
            {'name': 'training path', 'path': f'resources/data/{name}/train', 'usage': 'Training'},
            {'name': 'testing path', 'path': f'resources/data/{name}/test', 'usage': 'PrivateTest'},
        ]

        with open(csv_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["emotion", "size", "pixels", "usage", "path"])
            
            for option in options:
                emotions = [emotion for emotion in os.listdir(option.get('path')) if emotion != '.DS_Store']
                for (emotion, img_store) in [(emotion, os.listdir(f"{option.get('path')}/{emotion}"))for emotion in emotions]:
                    for img in [img for img in img_store if img != '.DS_Store']:
                        path_image = f"{option.get('path')}/{emotion}/{img}"
                        shape, px, counter = self.img2array(path_image, False, counter)
                        writer.writerow([emotion, shape, px, option.get('usage'), path_image])

    # Utils
    def img2array(self, path_image: str = None, gray: bool = True, counter: int = 0):
        image_gray = cv2.imread(path_image) if gray is True else cv2.imread(path_image, cv2.IMREAD_GRAYSCALE)
        if image_gray is not None:
            self.show_image(im_array=image_gray, label=path_image) if counter > 0 else None
            xstring = []
            for x in range(0, self.img_size[0]):
                for y in range(0, self.img_size[1]):
                    xstring.append(int(image_gray[x, y]))
            return f"{self.img_size[0]} {self.img_size[1]}", "-".join(str(e) for e in xstring), counter - 1
        return None, None, 0
    
    def array2img(self, arr_image: str = None, label_image: str = None, show_image: bool = True) -> None:
        new_img = np.ones(self.img_size)
        arr_image = arr_image.split("-")
        for x in range(0, self.img_size[0]):
            for y in range(0, self.img_size[1]):
                pixel = arr_image.pop(0)
                new_img[x][y] = int(pixel)
        if show_image is True:
            self.show_image(im_array=new_img.astype(np.uint8), label=label_image)
        return new_img.astype(np.uint8)

    def show_image(self, im_array, label):
        cv2.imshow(label, im_array)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
