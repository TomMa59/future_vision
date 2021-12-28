from flask import Flask, render_template, request, url_for, session, redirect
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.core import Workspace
import subprocess
import time
import os

app = Flask(__name__)

app.config.from_object('config')

basedir_path = app.config['BASEDIR']

from .utils import display_content
from .models import Content

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', img_ids=display_content())

@app.route('/transition/', methods=['GET', 'POST'])
def transition():
        return render_template('transition.html', img_id_to_display=request.form['img_id_to_display'])

@app.route('/result/', methods=['GET', 'POST'])
def result():
    if request.method == 'GET':
        return render_template('result.html')

    img_id_to_display = request.form.get('img_id_to_display')
    file = open("app_pred/img_id.txt", "w")
    file.write(img_id_to_display)
    file.close()
    subprocess.Popen(['python app_pred/mask_prediction.py'], stdout = subprocess.PIPE, close_fds=True, shell=True).wait()
    return 'done'

if __name__ == "__main__":
    app.run()
