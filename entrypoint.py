from django.contrib.auth import get_user_model
from django.db import IntegrityError

try:
    get_user_model().objects.create_superuser("admin", "admin@example.com", "h98yt54y5rd")
except IntegrityError:
    pass
