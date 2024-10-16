from pathlib import Path
import os
from django.core.exceptions import ImproperlyConfigured

def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        raise ImproperlyConfigured(f"The {var_name} environment variable is not set.")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

#Load our environental variables
from dotenv import load_dotenv
load_dotenv()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-gu^p^izz+f#(u76ptf)16^%pv&t*tarvwjx*j6hs!t-(aez08c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# ALLOWED_HOSTS = ['antukinecom-production.up.railway.app', 'https://antukinecom-production.up.railway.app']
# CSRF_TRUSTED_ORIGINS =  ['antukinecom-production.up.railway.app', 'https://antukinecom-production.up.railway.app']

ALLOWED_HOSTS = ['antukinecom-production-3e63.up.railway.app', 'antukinecom.onrender.com', 'localhost', '127.0.0.1', 'localhost', 'dc4f-136-158-65-170.ngrok-free.app']

# CSRF_TRUSTED_ORIGINS = [os.environ.get('ALLOWED_HOST')]
CSRF_TRUSTED_ORIGINS = [
    'http://antukinecom-production-3e63.up.railway.app',
    'https://antukinecom-production-3e63.up.railway.app',
    'https://antukinecom.onrender.com',
    'https://dc4f-136-158-65-170.ngrok-free.app'
]



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store',
    'cart',
    'payment',
    'whitenoise.runserver_nostatic',
    'paypal.standard.ipn',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'ecom.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecom.wsgi.application'



# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway',
        'USER': 'postgres',
        #password pag localhost
        # 'PASSWORD': os.environ.get('DB_PASSWORD_YO'),
        #password pag online db
        'PASSWORD': os.environ['DB_PASSWORD_YO'],
        'HOST': 'junction.proxy.rlwy.net',
        'PORT': '46361',
    }
} 

# DATABASES = { 
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ.get('DB_NAME', 'railway'),  # Defaults to 'railway' if not set
#         'USER': os.environ.get('DB_USER', 'postgres'),  # Defaults to 'postgres' if not set
#         'PASSWORD': os.environ.get('DB_PASSWORD_YO'),   # Fetches from environment variables
#         'HOST': os.environ.get('DB_HOST', 'junction.proxy.rlwy.net'),  # Defaults to Railway host
#         'PORT': os.environ.get('DB_PORT', '46361'),  # Defaults to Railway port
#     }
# }




# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = ['static/']

#white noise static stuff
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#add paypal setting
#set sandbox to true
PAYPAL_TEST = True
PAYPAL_RECEIVER_EMAIL = 'group5business@gmail.com'