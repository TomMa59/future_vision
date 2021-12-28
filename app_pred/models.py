import os
from flask_sqlalchemy import SQLAlchemy
import logging as lg

from .views import app

# Create database connection object
db = SQLAlchemy(app)

basedir_path = app.config['BASEDIR']

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img_id = db.Column(db.String(200), nullable=False)

    def __init__(self, img_id):
        self.img_id = img_id

def init_db():
    db.drop_all()
    db.create_all()
    img_dir = '{}/app_pred/static/data/input/images/'.format(basedir_path)
    img_list = os.listdir(img_dir)
    for idx in range(len(img_list)):
        db.session.add(Content(img_list[idx]))
    db.session.commit()
    lg.warning('Database initialized!')
