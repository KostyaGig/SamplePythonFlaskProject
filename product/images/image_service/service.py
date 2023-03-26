from datetime import datetime, timedelta

import firebase_admin
from firebase_admin import credentials, storage as firebase_storage

cred = credentials.Certificate(
    "/Users/kostiggig/PycharmProjects/SamplePythonFlaskProject/product/images/image_service/firebase_service_account.json")
firebase_admin.initialize_app(cred, {'storageBucket': 'pythonflak-cf106.appspot.com'})
bucket = firebase_storage.bucket()


def upload_image(image):
    blob = bucket.blob("images/" + image.filename)
    blob.upload_from_file(image, content_type=image.content_type)
    exp_time = datetime.utcnow() + timedelta(weeks=7)
    return blob.generate_signed_url(exp_time)
