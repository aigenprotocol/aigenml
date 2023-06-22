import os
import re
import unicodedata

from flask import flash
from werkzeug.utils import secure_filename

from .globals import globals as g
from server.config import MODEL_ALLOWED_EXTENSIONS, IMAGE_ALLOWED_EXTENSIONS


def allowed_file(filename, file_type):
    if file_type == 'model_file':
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in MODEL_ALLOWED_EXTENSIONS
    else:
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in IMAGE_ALLOWED_EXTENSIONS


def save_files(request):
    model_file_status = save_file(request, 'model_file')
    if model_file_status['status'] == "success":
        return {"status": "success", "message": "Model File uploaded",
                "model_file_path": model_file_status['file_path']}
    else:
        return {"status": "failure", "message": "Issue In uploading Files"}


def save_file(request, file_type):
    # check if the post request has the file part
    #  Save Logo File , Model File , banner File
    if file_type not in request.files:
        flash('No file part')
        print('No file part')
        return {"status": "failure", "message": "No file found"}
    file = request.files[file_type]
    # If the user does not select a file, the browser submits an empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        print("No selected file")
        return {"status": "failure", "message": "No file found"}

    if file and allowed_file(file.filename, file_type):
        filename = secure_filename(file.filename)
        file.save(os.path.join(g.app.config['UPLOAD_FOLDER'], filename))
        print(os.path.join(g.app.config['UPLOAD_FOLDER'], filename))
        return {"status": "success", "message": "Model File uploaded",
                "file_path": os.path.join(g.app.config['UPLOAD_FOLDER'], filename)}
    else:
        print("Unsupported type")
        return {"status": "failure", "message": "Unsupported file type"}


def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')
