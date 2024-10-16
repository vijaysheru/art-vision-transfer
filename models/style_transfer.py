import tensorflow as tf
import numpy as np

# Load and preprocess images
def load_img(path_to_img, max_dim=256):  # Added max_dim parameter for flexibility
    img = tf.io.read_file(path_to_img)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)

    shape = tf.cast(tf.shape(img)[:-1], tf.float32)
    long_dim = max(shape)
    scale = max_dim / long_dim
    new_shape = tf.cast(shape * scale, tf.int32)

    img = tf.image.resize(img, new_shape)
    img = img[tf.newaxis, :]
    return img

# Content loss function
def content_loss(base_content, target):
    return tf.reduce_mean(tf.square(base_content - target))

# Style loss function
def style_loss(base_style, gram_target):
    gram_style = gram_matrix(base_style)
    return tf.reduce_mean(tf.square(gram_style - gram_target))

# Gram matrix calculation
def gram_matrix(input_tensor):
    result = tf.linalg.einsum('bijc,bijd->bcd', input_tensor, input_tensor)
    input_shape = tf.shape(input_tensor)
    num_locations = tf.cast(input_shape[1] * input_shape[2], tf.float32)
    return result / num_locations

# VGG19 model for feature extraction
def vgg_layers(layer_names):
    vgg = tf.keras.applications.VGG19(include_top=False, weights='imagenet')
    vgg.trainable = False
    outputs = [vgg.get_layer(name).output for name in layer_names]
    model = tf.keras.Model([vgg.input], outputs)
    return model

# Style transfer function
def style_transfer(content_path, style_path, num_iterations=100):  # Reduced iterations
    content_image = load_img(content_path)
    style_image = load_img(style_path)

    content_layers = ['block5_conv2']
    style_layers = ['block1_conv1', 'block2_conv1', 'block3_conv1', 'block4_conv1', 'block5_conv1']

    vgg = vgg_layers(style_layers + content_layers)

    style_features = vgg(style_image)
    content_features = vgg(content_image)

    style_weight = 1e-2
    content_weight = 1e4

    style_outputs = style_features[:len(style_layers)]
    content_outputs = content_features[len(style_layers):]

    style_targets = [gram_matrix(style_output) for style_output in style_outputs]

    image = tf.Variable(content_image)

    optimizer = tf.optimizers.Adam(learning_rate=0.02, beta_1=0.99, epsilon=1e-1)

    @tf.function()
    def train_step(image):
        with tf.GradientTape() as tape:
            outputs = vgg(image)
            style_output_features = outputs[:len(style_layers)]
            content_output_features = outputs[len(style_layers):]

            style_score = 0
            content_score = 0

            for target, output in zip(style_targets, style_output_features):
                style_score += style_weight * style_loss(output, target)

            for target, output in zip(content_outputs, content_output_features):
                content_score += content_weight * content_loss(output, target)

            total_loss = style_score + content_score

        grad = tape.gradient(total_loss, image)
        optimizer.apply_gradients([(grad, image)])
        image.assign(tf.clip_by_value(image, clip_value_min=0.0, clip_value_max=1.0))

    for i in range(num_iterations):
        train_step(image)
        if i % 10 == 0:  # Reduced logging frequency
            print(f"Iteration {i}")

    return image.numpy()
