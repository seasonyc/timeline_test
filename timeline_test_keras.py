import keras
from keras.layers.core import Dense
from keras.models import Sequential
import tensorflow as tf
from tensorflow.python.client import timeline
import numpy as np
import keras.backend as K
import timeline_stat

x = np.random.randn(10000, 2)
y = (x[:, 0] * x[:, 1]) > 0 # xor

sess = K.get_session()
run_options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
run_metadata = tf.RunMetadata()
model = Sequential()
model.add(Dense(units=64, activation='relu', input_dim=2))
model.add(Dense(units=2, activation='softmax'))
model.compile(loss='categorical_crossentropy',
              optimizer='sgd',
              options=run_options,
              run_metadata=run_metadata)
model.fit(x, keras.utils.to_categorical(y), epochs=1, batch_size=64)

print(sess.run(tf.contrib.memory_stats.MaxBytesInUse()))
# current usage
print(sess.run(tf.contrib.memory_stats.BytesInUse()))

trace = timeline.Timeline(step_stats=run_metadata.step_stats)
json_file_name = 'timeline.keras.json'
with open(json_file_name, 'w') as f:
    f.write(trace.generate_chrome_trace_format(show_memory=True))

print('timeline memory total: ' + str(timeline_stat.stat_timeline_memory(json_file_name)))

