import os
from pathlib import Path
from werkzeug.utils import secure_filename

def ensure_folder(path_obj):
    Path(path_obj).mkdir(parents=True, exist_ok=True)

def allowed_file(filename, allowed_set):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_set

def safe_store_name(filename):
    return secure_filename(filename)