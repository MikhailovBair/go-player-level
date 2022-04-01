import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


class RnnKerasRunner:
    __DEFAULT_FEATURES = ['score', 'winrate', 'utility', 'stddev', 'selfplay', 'dist_from_prev', 'winrate_sqr', 'score_sqr', 'dist_more_5']

    def __create_rnn(self, hidden_units, input_shape):
        model = keras.Sequential()
        # model.add(layers.Embedding(input_dim=6, output_dim=6))
        model.add(tf.keras.layers.Masking(mask_value=0.,
                                          input_shape=input_shape))
        model.add(layers.BatchNormalization())
        model.add(layers.Dense(units=12, activation="linear"))
        model.add(layers.Dense(32, activation='relu'))
        model.add(layers.Bidirectional(layers.LSTM(hidden_units)))  # , dropout = 0.15, reccurent_dropout = 0.15)))
        model.add(layers.LeakyReLU())
        model.add(layers.Dense(units=1, activation="linear"))
        model.compile(loss='mean_squared_error', optimizer='adam', metrics="mean_absolute_error")
        return model

    def __init__(self, model = None, sequence_len=150, features=__DEFAULT_FEATURES):
        self.features = features
        self.sequence_len = sequence_len
        if model is None:
            self.model = self.__create_rnn(64, (sequence_len, len(features)))
        else:
            self.model = model

    def __get_tensor(self, df):

        def resize_to_length(m, length):
            if len(m) > length:
                return m[:length]
            n_nules = length - len(m)
            return list([0] * n_nules) + list(m)

        arr = []
        for feature in self.features:
            arr.append([np.array(y) for y in df[feature].apply(lambda x : resize_to_length(x, self.sequence_len))])
        arr = np.array(arr)
        arr = arr.swapaxes(0, 1)
        arr = arr.swapaxes(1, 2)
        return tf.convert_to_tensor(arr, np.float32)

    def fit(self, df, target, epochs=10, batch_size=256):
        X = self.__get_tensor(df)
        self.model.fit(X, tf.convert_to_tensor(target, np.float32), epochs=epochs, batch_size = batch_size)

    def predict(self, df):
        X = self.__get_tensor(df)
        return self.model.predict(X)
