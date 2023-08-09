import os
import pandas as pd
import tensorflow as tf
class MyDataLoader:
    def __init__(self, path_input, path_output, path_knobs):
        self.path_input_audio, self.path_output_audio, self.knobs_labels = self.extract_input_target(path_input,
                                                                                                     path_output,
                                                                                                     path_knobs)
        self.dataset = self.get_dataset(self.path_input_audio, self.path_output_audio, self.knobs_labels)
        self.train_ds, self.val_ds = self.prepare_for_training(self.dataset)

    def extract_input_target(self, path_in, path_out, path_knobs):
        path_input_audio = path_in
        path_output_audio = path_out
        assert os.path.exists(path_input_audio), "Audio folder  not found. Looked for " + path_input_audio
        assert os.path.exists(path_output_audio), "Audio folder  not found. Looked for " + path_output_audio
        assert os.path.exists(path_knobs), "Audio folder  not found. Looked for " + path_knobs

        path_output_audio = sorted(self.get_files_in_folder(path_output_audio, ".wav"))
        path_input_audio = sorted(self.get_files_in_folder(path_input_audio, ".wav"))
        len_out = len(path_output_audio)
        len_in = len(path_input_audio)
        len_tot = len_out / len_in
        path_input_audio = path_input_audio * int(len_tot)
        data_knobs = pd.read_csv(path_knobs)
        data_knobs = data_knobs.drop(columns=['path'])
        data_knobs = data_knobs.iloc[:, :4]
        data_knobs = data_knobs.values
        data_knobs = [item for item in data_knobs for _ in range(60)]
        return path_input_audio, path_output_audio, data_knobs

    def get_dataset(self, input_path, output_path, knob_labels):
        input_path = tf.data.Dataset.from_tensor_slices(input_path)
        output_path = tf.data.Dataset.from_tensor_slices(output_path)
        knob_labels = tf.data.Dataset.from_tensor_slices(knob_labels)
        return tf.data.Dataset.zip((input_path, output_path, knob_labels))

    def generate_full_dataset(self, file_path, label_audio_path, knob_labels):

        audio_input = tf.io.read_file(file_path)
        audio_input = tf.audio.decode_wav(audio_input, desired_channels=1)[0]  # Extract the audio data

        audio_output = tf.io.read_file(label_audio_path)
        audio_output = tf.audio.decode_wav(audio_output)[0]  # Extract the audio data

        # Ensure output_audio has the same length as input_audio
        audio_output = tf.cond(tf.shape(audio_output)[0] >= tf.shape(audio_input)[0],
                               lambda: audio_output[:tf.shape(audio_input)[0]],
                               lambda: tf.pad(audio_output,
                                              [[0, tf.shape(audio_input)[0] - tf.shape(audio_output)[0]], [0, 0]]))

        return audio_input, audio_output, knob_labels

    def get_files_in_folder(self, folder, extension='.wav'):
        """
        returns a list of files in the sent folder with the sent extension
        """
        file_list = []
        for file in os.listdir(folder):
            if file.endswith(extension):
                file_list.append(os.path.join(folder, file))
        return file_list

    def prepare_for_training(self, ds, batch_size=512, shuffle_buffer_size=1024):

        dataset = ds.map(lambda x, y, z: self.generate_full_dataset(x, y, z))
        dataset = dataset.shuffle(shuffle_buffer_size)
        dataset = dataset.map(lambda x, y, z: (self.map_knob_to_audio_fragment(x, z), y))
        train_ds = dataset.map(lambda x, y: self.split_train(x, y))
        val_ds = dataset.map(lambda x, y: self.split_val(x, y))
        train_ds = train_ds.batch(batch_size)
        val_ds = val_ds.batch(batch_size)
        train_ds = train_ds.prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
        val_ds = val_ds.prefetch(buffer_size=tf.data.experimental.AUTOTUNE)

        return train_ds, val_ds

    def split_train(self, input_audio, output_audio):
        train_ratio = 80  # proporzione per il set di addestramento
        input_audio = tf.reshape(input_audio, [-1, 4])  # flatten the audio_fragment
        output_audio = tf.reshape(output_audio, [-1, 1])  # flatten the audio_fragment
        num_examples = tf.shape(input_audio)[0]
        len_audio = int(num_examples * train_ratio / 100)  # Convert to 80 from 0.8

        input_audio = input_audio[:len_audio]
        output_audio = output_audio[:len_audio]
        input_audio = tf.reshape(input_audio, (len_audio, 4))
        output_audio = tf.reshape(output_audio, (len_audio, 1))
        return input_audio, output_audio

    def split_test(self, input_audio, output_audio):
        train_ratio = 80
        test_ratio = 10  # proporzione per il set di test
        input_audio = tf.reshape(input_audio, [-1, 4])  # flatten the audio_fragment
        output_audio = tf.reshape(output_audio, [-1, 1])  # flatten the audio_fragment
        num_examples = tf.shape(input_audio)[0]
        len_audio = int(num_examples * train_ratio / 100)  # Convert to 80 from 0.8
        test_len = int(num_examples * test_ratio / 100) + len_audio

        input_audio = input_audio[len_audio:test_len]
        output_audio = output_audio[len_audio:test_len]
        input_audio = tf.reshape(input_audio, (test_len - len_audio, 4))
        output_audio = tf.reshape(output_audio, (test_len - len_audio, 1))
        return input_audio, output_audio

    def split_val(self, input_audio, output_audio):
        train_ratio = 80
        val_ratio = 10  # proporzione per il set di val
        test_ratio = 10  # proporzione per il set di test
        input_audio = tf.reshape(input_audio, [-1, 4])  # flatten the audio_fragment
        output_audio = tf.reshape(output_audio, [-1, 1])  # flatten the audio_fragment
        num_examples = tf.shape(input_audio)[0]
        len_audio = int(num_examples * train_ratio / 100)  # Convert to 80 from 0.8

        test_len = int(num_examples * test_ratio / 100) + len_audio

        input_audio = input_audio[test_len:num_examples]
        output_audio = output_audio[test_len:num_examples]
        input_audio = tf.reshape(input_audio, (num_examples - test_len, 4))
        output_audio = tf.reshape(output_audio, (num_examples - test_len, 1))
        return input_audio, output_audio

    def map_knob_to_audio_fragment(self, audio_fragment, knob_labels):
        shape_fragments = tf.shape(audio_fragment)
        shape_label = tf.shape(knob_labels)
        knob_labels = tf.cast(knob_labels, tf.float32)
        audio_fragment = tf.reshape(audio_fragment, [-1, 1])  # flatten the audio_fragment
        knob_labels = tf.reshape(knob_labels, [-1, 1])
        knob_labels = tf.repeat(knob_labels, tf.shape(audio_fragment)[0], axis=1)
        knob_labels = tf.transpose(knob_labels)
        combined_tensor = tf.concat([audio_fragment, knob_labels], axis=-1)
        combined_tensor = tf.reshape(combined_tensor, (22050, 4))
        return combined_tensor