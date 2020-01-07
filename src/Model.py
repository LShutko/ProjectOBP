import matplotlib.pyplot as plt
import pickle

from keras.models import Sequential
from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import Conv2D, AveragePooling2D, MaxPooling2D
from keras.layers.core import Activation, Flatten, Dense
from keras.optimizers import Adam


class Model(object):

    def __init__(self, settings, n_classes):
        self.settings = settings
        self.n_classes = n_classes

    def run(self, images, labels):
        x, y = images, labels

        # Initialize Keras model
        cnn = self.define_model()

        # Write cnn structure to table
        self.write_model(cnn)

        # Train the CNN!
        trained_cnn, history = self.train_nn(cnn, x, y)

        # Create training history visualization
        self.export_plots(history)

        # Create export of model
        pickle.dump(trained_cnn, open(self.settings['output_directory']+'cnn_model.pkl', 'wb'))

        return

    def train_nn(self, model, x, y):

        # Define the loss function
        model.compile(loss="binary_crossentropy",
                      optimizer=Adam(lr=self.settings['learning_rate'],
                                     decay=self.settings['learning_rate'] / self.settings['epochs']),
                      metrics=["accuracy"])

        # Fit the data
        print(f'Training model')
        history = model.fit(x=x,
                            y=y,
                            batch_size=self.settings['batch_size'],
                            validation_split=self.settings['validation_size'],
                            epochs=self.settings['epochs'],
                            verbose=self.settings['verbose'])

        return model, history

    def define_model(self):
        print(f'Defining the Model according to Hyperparams')
        model = Sequential()

        input_shape = (self.settings['height'], self.settings['width'], self.settings['depth'])

        model.add(Conv2D(32, (3, 3), padding="same", input_shape=input_shape))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=-1))

        model.add(MaxPooling2D(pool_size=(3, 3), padding="same", strides=(2, 2)))

        model.add(Conv2D(64, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=-1))

        model.add(MaxPooling2D(pool_size=(3, 3), padding="same", strides=(2, 2)))

        model.add(Conv2D(128, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=-1))

        model.add(MaxPooling2D(pool_size=(3, 3), padding="same", strides=(2, 2)))

        model.add(Conv2D(256, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=-1))

        model.add(Conv2D(256, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=-1))

        model.add(MaxPooling2D(pool_size=(3, 3), padding="same", strides=(2, 2)))

        model.add(Conv2D(512, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=-1))

        model.add(Conv2D(512, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=-1))

        model.add(MaxPooling2D(pool_size=(3, 3), padding="same", strides=(2, 2)))

        model.add(AveragePooling2D(pool_size=(1, 1), padding='valid'))

        model.add(Flatten())

        model.add(Dense(self.n_classes))
        model.add(Activation("softmax"))

        return model

    def write_model(self, model):

        with open(self.settings['output_directory'] + 'report.txt', 'w') as fh:
            # Pass the file handle in as a lambda function to make it callable
            model.summary(print_fn=lambda x: fh.write(x + '\n'))

        return

    def export_plots(self, history):

        # Plot training & validation accuracy values
        plt.plot(history.history['acc'])
        plt.plot(history.history['val_acc'])
        plt.title('Model accuracy')
        plt.ylabel('Accuracy')
        plt.xlabel('Epoch')
        plt.legend(['Train', 'Test'], loc='upper left')
        plt.savefig('output/fig1.png')
        plt.clf()

        # Plot training & validation loss values
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('Model loss')
        plt.ylabel('Loss')
        plt.xlabel('Epoch')
        plt.legend(['Train', 'Test'], loc='upper left')
        plt.savefig('output/fig2.png')
        plt.close()

        return
