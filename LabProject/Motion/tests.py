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
# with open('../media/csv/try20.csv', mode='r') as f:
#     path = default_storage.save('../media/csv/test.csv', f)
#     print(path, type(path))
#     ft = default_storage.open(path)
#     print(type(ft), type(f))
#     pa = ft.name
#     print(pa, type(pa))
#     st = API()
#     sts = st.getFile(ft)
#     print(sts)
# default_storage.delete(pa)
# print(default_storage.exists(pa))
print(settings.BASE_DIR)
print(settings.BASE_DIR.replace('LabProject', '') + 'cache')
