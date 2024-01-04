import os
from dotenv import load_dotenv
import numpy as np
from keras.models import Sequential, load_model
from keras.layers import Conv2D, MaxPool2D, Dense, Flatten
from keras.preprocessing.image import ImageDataGenerator
from keras.applications.vgg16 import VGG16
from keras.models import Model
from rich.progress import Progress
from engine.config import CATEGORIES, MODEL_PATH, TEST_PATH, TRAIN_PATH
from skimage.transform import resize
from skimage.io import imread


class RoadDetectionModel:
    def __init__(self):
        load_dotenv()
        self.categories = CATEGORIES
        self.train_path = TRAIN_PATH
        self.test_path = TEST_PATH
        self.model = load_model(MODEL_PATH)

    def train(self):
        with Progress() as progress:
            train_task = progress.add_task("[cyan]Training model", total=9, start=True)

            X_train = []
            y_train = []
            progress.update(train_task, description="[cyan]Loading training data ...")

            for category in self.categories:
                path = os.path.join(self.train_path, category)
                images = os.listdir(path)
                for img in images:
                    img_path = os.path.join(path, img)
                    img_array = imread(img_path)
                    img_resized = resize(
                        img_array, (150, 150, 1)
                    )  # normalization also happens
                    X_train.append(img_resized)
                    y_train.append(self.categories.index(category))

                progress.update(train_task, advance=1)

            X_train = np.array(X_train)
            y_train = np.array(y_train)

            # Preparation of testing set
            X_test = []
            y_test = []

            for category in self.categories:
                path = os.path.join(self.test_path, category)
                images = os.listdir(path)
                progress.update(train_task, description="[cyan]Loading test data ...")

                for img in images:
                    img_path = os.path.join(path, img)
                    img_array = imread(img_path)
                    img_resized = resize(
                        img_array, (150, 150, 1)
                    )  # normalization also happens
                    X_test.append(img_resized)
                    y_test.append(self.categories.index(category))

                progress.update(train_task, advance=1)

            X_test = np.array(X_test)
            y_test = np.array(y_test)

            progress.update(
                train_task, advance=1, description="[cyan]Building CNN Model..."
            )
            # CNN Model
            model = Sequential()
            model.add(Conv2D(32, (3, 3), input_shape=(150, 150, 1), activation="relu"))
            model.add(MaxPool2D(2, 2))
            model.add(Conv2D(64, (3, 3), activation="relu"))
            model.add(MaxPool2D(2, 2))
            model.add(Conv2D(128, (3, 3), strides=2, activation="relu"))
            model.add(MaxPool2D(2, 2))
            model.add(Flatten())
            model.add(Dense(50, activation="relu"))
            model.add(Dense(3, activation="softmax"))

            progress.update(
                train_task, advance=1, description="[cyan]Compiling Model..."
            )
            # Training
            model.compile(
                optimizer="adam",
                loss="sparse_categorical_crossentropy",
                metrics=["accuracy"],
            )
            model.fit(X_train, y_train, epochs=10, verbose=0)

            progress.update(
                train_task, advance=1, description="[cyan]Model Training Complete."
            )

            # Model Evaluation
            progress.update(
                train_task, advance=1, description="[cyan]Evaluating Model..."
            )
            model.evaluate(X_test, y_test, verbose=0)

            # Save Trained Model
            progress.update(
                train_task, advance=1, description="[cyan]Saving Trained Model..."
            )
            model.save(MODEL_PATH)

            progress.update(train_task, description="[green]Model Trained")

    def predict(self, img):
        img = resize(img, (150, 150, 1))
        img = img.reshape(1, 150, 150, 1)

        y = self.model.predict(img)
        ind = y.argmax()

        return self.categories[ind]

    def apply_transfer_learning(self):
        train_datagen = ImageDataGenerator(
            rescale=1 / 255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True
        )

        test_datagen = ImageDataGenerator(rescale=1 / 255)

        training_set = train_datagen.flow_from_directory(
            self.train_path, target_size=(224, 224), class_mode="categorical"
        )
        test_set = test_datagen.flow_from_directory(
            self.test_path, target_size=(224, 224), class_mode="categorical"
        )

        IMAGE_SIZE = [224, 224]
        vgg = VGG16(input_shape=IMAGE_SIZE + [3], weights="imagenet", include_top=False)

        for layer in vgg.layers:
            layer.trainable = False

        x = Flatten()(vgg.output)

        prediction = Dense(3, activation="softmax")(x)

        model1 = Model(inputs=vgg.input, outputs=prediction)
        model1.compile(
            loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"]
        )
        model1.fit_generator(training_set, validation_data=test_set, epochs=5)

        model1.save("trained_model.h5")
