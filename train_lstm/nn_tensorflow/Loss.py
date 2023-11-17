import tensorflow as tf
class ESRLoss(tf.keras.losses.Loss):
    def __init__(self, epsilon=0.00001):
        super(ESRLoss, self).__init__()
        self.epsilon = epsilon

    def call(self, target, output):
        # Compute the squared error between target and output
        loss = tf.pow(tf.add(target, -output), 2)
        loss = tf.reduce_mean(loss)

        # Calculate the energy of the target
        energy = tf.reduce_mean(tf.pow(target, 2)) + self.epsilon

        # Compute the final ESR loss
        loss = tf.divide(loss, energy)
        return loss


# Function to calculate ESR metric
def esr_metric(target, output):
    loss = tf.pow(tf.add(target, -output), 2)
    loss = tf.reduce_mean(loss)
    energy = tf.reduce_mean(tf.pow(target, 2)) + 0.00001
    loss = tf.divide(loss, energy)
    return loss

class PreEmph(tf.keras.layers.Layer):
    def __init__(self, filter_cfs, low_pass=False):
        super(PreEmph, self).__init__()
        self.epsilon = 0.00001
        self.zPad = len(filter_cfs) - 1

        self.conv_filter = tf.keras.layers.Conv1D(1, kernel_size=2, use_bias=False)
        self.conv_filter.build(input_shape=(None, None, 1))
        self.conv_filter.set_weights([tf.constant([filter_cfs], dtype=tf.float32)])

        self.low_pass = low_pass
        if self.low_pass:
            self.lp_filter = tf.keras.layers.Conv1D(1, kernel_size=2, use_bias=False)
            self.lp_filter.build(input_shape=(None, None, 1))
            self.lp_filter.set_weights([tf.constant([[[0.85, 1]]], dtype=tf.float32)])

    def call(self, inputs):
        output, target = inputs

        # Zero pad the input/target so the filtered signal is the same length
        output = tf.concat([tf.zeros((self.zPad, tf.shape(output)[1], 1)), output], axis=0)
        target = tf.concat([tf.zeros((self.zPad, tf.shape(target)[1], 1)), target], axis=0)

        # Apply pre-emph filter
        output = self.conv_filter(output)
        target = self.conv_filter(target)

        if self.low_pass:
            output = self.lp_filter(output)
            target = self.lp_filter(target)

        return tf.transpose(output, perm=[2, 0, 1]), tf.transpose(target, perm=[2, 0, 1])


class DCLoss(tf.keras.losses.Loss):
    def __init__(self, epsilon=0.00001):
        super(DCLoss, self).__init__()
        self.epsilon = epsilon

    def call(self, target

             , output):
        # Calculate the mean of target and output along the batch dimension
        mean_target = tf.reduce_mean(target, axis=0)
        mean_output = tf.reduce_mean(output, axis=0)

        # Compute the squared error between the mean of target and output
        loss = tf.pow(tf.add(mean_target, -mean_output), 2)
        loss = tf.reduce_mean(loss)

        # Calculate the energy of the target
        energy = tf.reduce_mean(tf.pow(target, 2)) + self.epsilon

        # Compute the final DC loss
        loss = tf.divide(loss, energy)
        return loss


# Function to calculate DC metric
def dc_metric(target, output):
    mean_target = tf.reduce_mean(target, axis=0)
    mean_output = tf.reduce_mean(output, axis=0)
    loss = tf.pow(tf.add(mean_target, -mean_output), 2)
    loss = tf.reduce_mean(loss)
    energy = tf.reduce_mean(tf.pow(target, 2)) + 0.00001
    loss = tf.divide(loss, energy)
    return loss


class CombinedLoss(tf.keras.losses.Loss):
    def __init__(self, dc_weight=1.0, esr_weight=1.0, filters_cfs=None):
        super(CombinedLoss, self).__init__()
        self.dc_weight = dc_weight
        self.esr_weight = esr_weight
        self.dc_loss = DCLoss()
        self.esr_loss = ESRLoss()
        self.filters_cfs = filters_cfs
        if filters_cfs:
            self.pre_emph_layer = PreEmph(filters_cfs)
    
    def call(self, target, output):
        if self.filters_cfs:
            output, target = self.pre_emph_layer([output, target])
        
        loss_dc = self.dc_loss(target, output)
        loss_esr = self.esr_loss(target, output)

        combined_loss = self.dc_weight * loss_dc + self.esr_weight * loss_esr
        return combined_loss