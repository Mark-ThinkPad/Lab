from django.test import TestCase
# from Motion.EmotionAnalysis.API import API
from LabProject import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
os.environ.update({'DJANGO_SETTINGS_MODULE': 'LabProject.settings'})


# Create your tests here.
# path = settings.MEDIA_ROOT
# print(type(path), path)
path = default_storage.save('../media/csv/test.txt', ContentFile(b'new content'))
print(path, type(path))
f = default_storage.open(path)
print(type(f))
pa = f.name
print(pa, type(pa))
default_storage.delete(pa)
print(default_storage.exists(pa))