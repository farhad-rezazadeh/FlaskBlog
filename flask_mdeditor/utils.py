import os
import uuid

from flask import url_for


def get_url(endpoint_or_url):
    if endpoint_or_url.startswith(("https://", "http://", "/")):
        return endpoint_or_url
    else:
        return url_for(endpoint_or_url)


def random_filename(old_filename):
    ext = os.path.splitext(old_filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename
