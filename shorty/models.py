import re
import string
import random
from django.db import models
from django.core.validators import URLValidator

ALLOWED_CODE = re.compile(r"^[\w-]{3,32}$")

class Link(models.Model):
    long_url = models.URLField(validators=[URLValidator()], max_length=500)
    code = models.SlugField(max_length=32, unique=True, blank=True)
    clicks = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self._generate_code()
        super().save(*args, **kwargs)

    def _generate_code(self, length=6):
        chars = string.ascii_letters + string.digits
        while True:
            code = ''.join(random.choices(chars, k=length))
            if not Link.objects.filter(code=code).exists():
                return code

    def __str__(self):
        return f"{self.code} → {self.long_url}"
