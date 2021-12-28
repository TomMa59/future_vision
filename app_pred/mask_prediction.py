import os
import time
import glob
import cv2
from PIL import Image
import numpy as np
import tensorflow as tf
import keras
from tensorflow.python.keras import backend as K
import segmentation_models as sm
sm.set_framework('tf.keras')
sm.framework()

file = open("app_pred/img_id.txt", "r")
img_id = file.read()

def addColors(gg):
        im = np.zeros([gg.shape[0], gg.shape[1],3], dtype=np.uint8)

        for i in range(gg.shape[0]):

             for u in range(gg.shape[1]):
                if gg[i,u]==7:
                        im[i,u]= np.array([0, 0, 255])
                if gg[i,u]==6:
                        im[i,u]= np.array([255, 0, 0])
                if gg[i,u]==5:
                        im[i,u]= np.array([0, 204, 204])
                if gg[i,u]==4:
                        im[i,u]= np.array([0, 255, 0])
                if gg[i,u]==3:
                        im[i,u]= np.array([255, 0, 127])
                if gg[i,u]==2:
                        im[i,u]= np.array([255, 151, 0])
                if gg[i,u]==1:
                        im[i,u]= np.array([153, 153, 0])
                if gg[i,u]==0:
                        im[i,u]= np.array([0, 0, 0])
        return im

def display_mask_on_img(img_path, model):
    _image = cv2.imread(img_path)
    res = cv2.resize(_image, (512, 512), interpolation = cv2.INTER_AREA)
    s=model.predict(np.expand_dims(res, axis = 0))
    check = np.zeros((512, 512), dtype=np.uint8)
    for i in range(0, len(s[0])):
        check[i]= np.argmax(s[0][i], axis = 1)
    mask= addColors(check)
    mask = cv2.resize(mask, (2048, 1024), interpolation = cv2.INTER_AREA)
    mask = Image.fromarray(mask)
    mask.save('app_pred/static/data/output/predicted_mask.png')
    mask.putalpha(120)
    img = Image.open(img_path)
    img.paste(mask, (0, 0), mask)
    return img


def calcul(env_file_name):

    img_dir = 'app_pred/static/data/input/images/'
    img_list = sorted(glob.glob(os.path.join(img_dir + env_file_name)))

    def dice_coef_loss(y_true, y_pred):
        intersection = K.sum(K.abs(y_true * y_pred), axis=-1)
        return 1-((2. * intersection + 1) / (K.sum(K.square(y_true),-1) + K.sum(K.square(y_pred),-1) + 1))

    BACKBONE = 'efficientnetb3'

    tf.keras.backend.clear_session()
    tf.compat.v1.reset_default_graph()
    tf.keras.backend.set_image_data_format('channels_last')

    model_fpn = sm.FPN(BACKBONE, classes=8, input_shape=(512, 512, 3), activation='softmax',
                                  pyramid_block_filters=256, pyramid_aggregation='sum', pyramid_dropout=0.1)
    model_fpn.load_weights('app_pred/static/data/model/sm_fpn_hp_aug_512.h5')
    model_fpn.compile(loss=dice_coef_loss, optimizer='nadam',
                        metrics=["acc", sm.metrics.iou_score])
    mask_on_img = display_mask_on_img(img_list[0], model_fpn)
    mask_on_img.save('app_pred/static/data/output/predicted_mask_on_image.png')
    init_img = cv2.imread(img_list[0])
    init_img = cv2.cvtColor(init_img, cv2.COLOR_BGR2RGB)
    init_img = Image.fromarray(init_img)
    init_img.save('app_pred/static/data/output/init_image.png')

calcul(img_id)
