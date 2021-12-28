import random

from .models import Content

def display_content():
    contents = Content.query.all()
    id = []
    for i in range(len(contents)):
        id.append(contents[i].img_id)
    return id
