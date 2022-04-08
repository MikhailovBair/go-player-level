import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import layers


def get_tensor(df, features, sequence_len):
    def resize_to_length(m, length):
        if len(m) > length:
            return m[:length]
        n_nules = length - len(m)
        return list([0] * n_nules) + list(m)

    arr = []
    for feature in features:
        arr.append([np.array(y) for y in df[feature].apply(lambda x: resize_to_length(x, sequence_len))])
    arr = np.array(arr)
    arr = arr.swapaxes(0, 1)
    arr = arr.swapaxes(1, 2)
    return tf.convert_to_tensor(arr, np.float32)


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
            self.model = self.__create_rnn(128, (sequence_len, len(features)))
        else:
            self.model = model

    def fit(self, df, target, val_X, val_y, epochs=10, batch_size=256):
        val_data = None
        if val_X is not None:
            val_X = get_tensor(val_X, self.features, self.sequence_len)
            val_y = tf.convert_to_tensor(val_y, np.float32)
            val_data = (val_X, val_y)
        X = get_tensor(df, self.features, self.sequence_len)
        self.model.fit(X, tf.convert_to_tensor(target, np.float32), validation_data = val_data, epochs=epochs,
                       batch_size=batch_size)

    def predict(self, df):
        X = get_tensor(df, self.features, self.sequence_len)
        return np.array([y[0] for y in self.model.predict(X)])


class RnnKerasClassifierRunner:
    __DEFAULT_FEATURES = ['score', 'winrate', 'utility', 'stddev', 'selfplay', 'dist_from_prev', 'winrate_sqr', 'score_sqr', 'dist_more_5']

    def cnt_ranks(self):
        return self.max_rank - self.min_rank + 1

    def __create_rnn(self, hidden_units, input_shape):
        model = keras.Sequential()
        model.add(tf.keras.layers.Masking(mask_value=0.,
                                          input_shape=input_shape))
        model.add(layers.BatchNormalization())
        model.add(layers.Dense(units=12, activation="linear"))
        model.add(layers.Dense(32, activation='relu'))
        model.add(layers.Bidirectional(layers.LSTM(hidden_units)))  # , dropout = 0.15, reccurent_dropout = 0.15)))
        model.add(layers.Dense(units=self.cnt_ranks(), activation="linear"))
        model.add(layers.Activation('softmax'))
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics='accuracy')
        return model

    def __init__(self, min_rank, max_rank, model=None, sequence_len=150, features=__DEFAULT_FEATURES):
        self.features = features
        self.sequence_len = sequence_len
        self.min_rank = min_rank
        self.max_rank = max_rank
        if model is None:
            self.model = self.__create_rnn(128, (sequence_len, len(features)))
        else:
            self.model = model

    def fit(self, df, target, val_X, val_y, epochs=10, batch_size=256):
        val_data = None
        if val_X is not None:
            val_y = keras.utils.to_categorical(tf.convert_to_tensor(np.array(val_y - self.min_rank, dtype="int32"),
                                                                    np.int32), num_classes=self.cnt_ranks())
            val_X = get_tensor(val_X, self.features, self.sequence_len)
            val_data = (val_X, val_y)
        X = get_tensor(df, self.features, self.sequence_len)
        y = keras.utils.to_categorical(tf.convert_to_tensor(np.array(target - self.min_rank, dtype="int32"), np.int32),
                                       num_classes=self.cnt_ranks())
        self.model.fit(X, y, validation_data=val_data, epochs=epochs, batch_size=batch_size)

    def get_probs(self, df):
        X = get_tensor(df, self.features, self.sequence_len)
        return self.model.predict(X)

    def predict(self, df):
        y = self.get_probs(df)
        return np.array([np.sum(x * np.arange(self.min_rank, self.max_rank + 1)) for x in y], dtype="int32")
