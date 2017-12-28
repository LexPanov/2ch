### Соглашение о кодировании:
##### Получение постов
Для получения списка постов необходимо получить таблицу Post с помощью
``` python
from app import db
posts = db.session.query(Post).order_by(db.text('id desc'))
```
##### Добавление поста
Для добавления поста в базу данных необходимо выполнить следующее, где ```author, subject, body, owner``` - текстовые атрибуты поста, ```img``` — имя файла-картинки поста которая лежит в папках ```static/img``` и ```static/thumb```

``` python
from app import db
from app.models.user_models import Post
from datetime import datetime

post = Post(date=datetime.now().strftime("%d/%m/%y %a %H:%M:%S"),
            author=author,
            subject=subject,
            body=body,
            owner=owner,
            img=filename
            )
db.session.add(post)
db.session.commit()
```
##### Вложения
Для корректного сохранения изображений необходимо провести валидацию с помощью ```PIL``` и сохранить две версии изображения в папки ```static/img``` и ```static/thumb```
``` python
from app.models.user_models import PostForm

import os
from PIL import Image, ImageFile
from time import time
from hashlib import md5

MAX_IMAGE_SIZE = 1000, 1000
MAX_THUMB_SIZE = 220, 220
MAX_AVATAR_SIZE = 400, 400

form = PostForm()

data = form.file.data.read()
hash = md5(data).hexdigest()
filename = '{0}-{1}-{2}.jpg'.format(id, int(time()), hash)
path = os.path.join("app/static/img", filename)
thumb_path = os.path.join("app/static/thumb", filename)
image_parser = ImageFile.Parser()
try:
    image_parser.feed(data)
    image = image_parser.close()
except IOError:
    filename = ''
    raise
thumb = image.copy()
image.thumbnail(MAX_IMAGE_SIZE, Image.ANTIALIAS)
thumb.thumbnail(MAX_THUMB_SIZE, Image.ANTIALIAS)
if image.mode != 'RGB':
    image = image.convert('RGB')
    thumb = thumb.convert('RGB')
image.save(path)
thumb.save(thumb_path)
```
##### Удаление
Для корректного удаления постов необходимо удалить вложенные изображения, если они присутствуют и удалить пост с указанным ```id```

``` python
from app import db
from app.models.user_models import Post
import os

post = db.session.query(Post).filter_by(id=id).one()
if post.img:
    filename = post.img
    path = os.path.join("app/static/img", filename)
    thumb_path = os.path.join("app/static/thumb", filename)
    os.remove(path)
    os.remove(thumb_path)
db.session.delete(post)
db.session.commit()
```