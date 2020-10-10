DEBUG = True

ALLOWED_HOSTS = ["*"]

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
MEDIA_URL = "media/"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "zdpytpol1_shareimages",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "localhost",
        "PORT": 5432,
    }
}
