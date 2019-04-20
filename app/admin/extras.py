import os
import random
import bleach
from markdown import markdown
ALLOWED_file_EXTENSIONS = set(['md', 'MD', 'word', 'txt', 'py', 'java', 'c', 'c++', 'xlsx'])
ALLOWED_photo_EXTENSIONS = set(['png', 'jpg', 'xls', 'JPG', 'PNG', 'gif', 'GIF','jpeg'])
imageUpload:True


def random_str(randomlength=5):
    _str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    for i in range(randomlength):
        _str += chars[random.randint(0, length)]
    return _str


def allowed_photo(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_photo_EXTENSIONS


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_file_EXTENSIONS

def format_datetime(self, request, obj, fieldname, *args, **kwargs):
    return getattr(obj, fieldname).strftime("%Y-%m-%d %H:%M")


def markitup(text):
    """
    把Markdown转换为HTML
    """

    # 删除与段落相关的标签，只留下格式化字符的标签
    # allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
    #                 'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
    #                 'h1', 'h2', 'h3', 'p', 'img']
    return bleach.linkify(markdown(text, ['extra'], output_format='html5'))
    # return bleach.linkify(bleach.clean(
    #     # markdown默认不识别三个反引号的code-block，需开启扩展
    #     markdown(text, ['extra'], output_format='html5'),
    #     tags=allowed_tags, strip=True))



