#CONVERTIRE IN TENSORFLOW

import os
import numpy as np
import tensorflow as tf
import soundfile as sf

def generate_dataset(input_audio_folder, output_audio_folder, frag_len_seconds=0.5, samplerate=44100):
    """
    Generates the complete dataset from which 
    training, validation, and testing data will be retrieved.
    Write used half-second segments for each data point.
    Returns a TensorFlow Dataset object suitable for use with TensorFlow's data pipeline.
    """
    assert os.path.exists(input_audio_folder), "Input audio folder not found: " + input_audio_folder
    assert os.path.exists(output_audio_folder), "Output audio folder not found: " + output_audio_folder

    # Get audio files in the input folder
    input_files = get_files_in_folder(input_audio_folder, ".wav")
    output_files = get_files_in_folder(output_audio_folder, ".wav")
    assert len(input_files) > 0, "get_files_in_folder yielded zero input files"
    assert len(output_files) > 0, "get_files_in_folder yielded zero output files"

    input_fragments = audio_filelist_to_fragments(input_files, frag_len_seconds, samplerate)
    output_fragments = audio_filelist_to_fragments(output_files, frag_len_seconds, samplerate)

    assert len(input_fragments) > 0, "get_files_in_folder yielded zero inputs"
    assert len(output_fragments) > 0, "get_files_in_folder yielded zero outputs"

    # Make lengths the same
    min_len = min(len(input_fragments), len(output_fragments))
    input_fragments = input_fragments[:min_len]
    output_fragments = output_fragments[:min_len]
    print("generate_dataset:: Loaded frames from audio files:", len(input_fragments))

    # Convert input and output fragments to TensorFlow tensors
    input_tensor = tf.convert_to_tensor(np.array(input_fragments))
    print("input tensor shape:", input_tensor.shape)
    output_tensor = tf.convert_to_tensor(np.array(output_fragments))
    
    dataset = tf.data.Dataset.from_tensor_slices((input_tensor, output_tensor))
    return dataset

def get_files_in_folder(folder, extension='.wav'):
    """
    returns a list of files in the sent folder with the sent extension
    """
    file_list = []
    for file in os.listdir(folder):
        if file.endswith(extension):
            file_list.append(os.path.join(folder, file))
    return file_list

def load_wav_file(filename, want_samplerate):
    """
    Load a WAV file using the soundfile module, resample to 44100 Hz, and return the first channel.
    """
    # Load the WAV file
    data, samplerate = sf.read(filename, dtype='float32')

    # Resample to 44100 Hz
    if samplerate != want_samplerate:
        print("load_wav_file warning: sample rate wrong, resampling from ", samplerate, "to", want_samplerate)
        data = sf.resample(data, target_samplerate=want_samplerate)

    # If the file has more than one channel, only return the first channel
    if len(data.shape) > 1 and data.shape[1] > 1:
        data = data[:, 0]

    # Put each sample in its own array
    # so we have [[sample1], [sample2]]
    data = np.array(data)
    data = data[:, np.newaxis]

    return data

def audio_file_to_fragments(audio_filepath, frag_len_seconds, samplerate):
    """
    load in the sent audio file and chop it into fragments of the sent length
    """
    assert os.path.exists(audio_filepath), "Cannot find audio file " + audio_filepath
    #audio_data, sr = sf.read(audio_filepath)
    
    audio_data = load_wav_file(audio_filepath, samplerate)
    num_samples_per_frag = int(frag_len_seconds * samplerate)
    num_frags = int(np.ceil(len(audio_data) / num_samples_per_frag))

    fragments = []
    for i in range(num_frags):
        frag_start = i * num_samples_per_frag
        frag_end = (i + 1) * num_samples_per_frag
        fragment = audio_data[frag_start:frag_end]
        if len(fragment) != num_samples_per_frag:
            continue 
        fragments.append(fragment)

    return fragments

def audio_filelist_to_fragments(audio_files, frag_len_seconds, samplerate):
    """
    iterates the sent list of audio files
    loads their data, chops to fragments 
    returns a list of all the fragments
    """
    all_fragments = []
    for file in audio_files:
        fragments = audio_file_to_fragments(file, frag_len_seconds, samplerate)
        all_fragments.extend(fragments)
    return all_fragments

def get_train_valid_test_datasets(dataset, splits=[0.8, 0.1, 0.1]):
    assert isinstance(dataset, tf.data.Dataset), "dataset should be a TensorFlow Dataset object, but it is " + type(dataset).__name__
    assert np.isclose(np.sum(splits), 1), "Splits do not add up to one"
    assert int(len(list(dataset)) * np.min(splits)) > 1, "Smallest split yields zero size " + str(splits) + " over " + str(len(list(dataset)))

    dataset_size = len(list(dataset))
    train_size = int(splits[0] * dataset_size)
    val_size = int(splits[1] * dataset_size)
    test_size = int(splits[2] * dataset_size)

    assert train_size > 0, "Trying to create training data but got zero length"
    assert val_size > 0, "Trying to create validation data but got zero length"
    assert test_size > 0, "Trying to create test data but got zero length"

    # Now only use as much of the dataset as we need, in case splits are larger than the dataset
    req_items = np.sum([train_size, val_size, test_size])
    if req_items > dataset_size:
        diff = dataset_size - req_items
        train_size -= diff  # Reduce training size
        print("Cannot get that many items from the dataset: want", req_items, "got", dataset_size, " trimming the training set by", diff)

    if req_items < dataset_size:
        diff = req_items - dataset_size
        train_size -= diff  # Reduce training size
        print("Cannot get that many items from the dataset: want", req_items, "got", dataset_size, " trimming the training set by", diff)

    # Split the dataset
    train_dataset = dataset.take(train_size)
    remaining_dataset = dataset.skip(train_size)
    val_dataset = remaining_dataset.take(val_size)
    test_dataset = remaining_dataset.skip(val_size)

    return train_dataset, val_dataset, test_dataset