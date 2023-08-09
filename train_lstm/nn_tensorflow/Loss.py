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
    def __init__(self, dc_weight=1.0, esr_weight=1.0):
        super(CombinedLoss, self).__init__()
        self.dc_weight = dc_weight
        self.esr_weight = esr_weight
        self.dc_loss = DCLoss()
        self.esr_loss = ESRLoss()

    def call(self, target, output):
        loss_dc = self.dc_loss(target, output)
        loss_esr = self.esr_loss(target, output)

        # Combina le due loss usando i pesi specificati
        combined_loss = self.dc_weight * loss_dc + self.esr_weight * loss_esr
        return combined_loss