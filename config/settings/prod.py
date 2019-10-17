from .base import *

DEBUG = False

TEMPLATES[0]["OPTIONS"]["loaders"] = [  # noqa F405
    (
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    )
]

TEMPLATES[0]["APP_DIRS"] = False

INSTALLED_APPS += [
    "gunicorn", "whitenoise.runserver_nostatic"
]

STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
)  # whitenoise
# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

MIDDLEWARE.insert(1, "django.middleware.gzip.GZipMiddleware")
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

MIDDLEWARE = (
    []
    + MIDDLEWARE
    + [
        "htmlmin.middleware.HtmlMinifyMiddleware",
        "htmlmin.middleware.MarkRequestMiddleware",
    ]
)
HTML_MINIFY = True

# ------------------------- Feedback ---------------------------------------------------------

FEEDBACK_MAIL = {
    "mail": env("MAIL"),
    "password": env("MAIL_PASSWORD"),
    "to": env("TO_MAIL"),
}


# ------------------------- Sentry Shit ---------------------------------------------------------

# sentry_sdk.init(
#     dsn="https://a86b628039394e4c89bea5b5b6835a8f@sentry.io/1299999",
#     integrations=[DjangoIntegration(), CeleryIntegration()],
#     send_default_pii=True,
#     request_bodies="medium",
#     with_locals=True,
#     server_name=env("SENTRY_SERVERNAME"),
# )

# ------------------------------------------- SECURITY -----------------------------------
# SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
# SESSION_COOKIE_SECURE = True  # need this for security, though can break smth
# SESSION_COOKIE_HTTPONLY = False  # seems like we can uncomment it and use django auth
