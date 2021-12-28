This Flask API, which can be launched with python app.py or using a Docker makes
predictions on different images for autonomous vehicles.

A sample of 20 images from the CityScape Dataset is present. These images where
never seen by the model (neither in training or in validation set).

The model is present in .h5 format in the static folder. It has been developed
using a Feature Pyramid Network, with efficient-net b3 backbone.

The model has been completely retrained, with image-net coeffcients as a starting
point.

A loss made from the Dice Coefficient metric has been used, with training on an
augmented dataset of 20825 images/masks and input shape of 512x512.

8 labels have been considered, ranging from sky to vehicles or circulation signs.

The result page of the API displays the image to be predicted, the predicted
mask and an overlap of these two images.

Final metrics are a pixel-per-pixel accuracy of 91,97% and IoU of 71,37%.
