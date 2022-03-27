from django.contrib import admin
from .models import *

admin.site.register(Author)
admin.site.register(Reader)
admin.site.register(Article)
admin.site.register(Category)
