### mysql setting
import os, json
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent

secret_file = os.path.join(BASE_DIR, 'secrets.json') # secrets.json 파일 위치를 명시

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': 'chunghaha',
		'USER': 'admin',
		'PASSWORD': get_secret("DB_PASSWORD"),
		'HOST': get_secret("DB_HOST"),
		'PORT': '3306',
		'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
            'use_unicode': True,
        },  
	},
	'chunghaha' : {
     	'ENGINE': 'django.db.backends.mysql',
		'NAME': 'chunghaha',
		'USER': 'admin',
		'PASSWORD': get_secret("DB_PASSWORD"),
		'HOST': get_secret("DB_HOST"),
		'PORT': '3306',
		'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
            'use_unicode': True,
        },
	},
 	'chunghaha-dev': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'chunghaha_image_post',
        'USER': 'root',
        'PASSWORD': get_secret("DB_PASSWORD"),
        'HOST': get_secret("DB_HOST"),
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
            'use_unicode': True,
        },
    },
}