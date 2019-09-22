from django.db import models

# Create your models here.

class Event(models.Model):
    REC_ID = models.CharField(max_length=20, default="")
    REPORT_NUM = models.CharField(max_length=20, default="")
    CREATE_TIME = models.DateTimeField('CREATE_TIME')
    DISTRICT_NAME = models.CharField(max_length=20, default="")
    DISTRICT_ID = models.CharField(max_length=20, default="")
    STREET_NAME = models.CharField(max_length=20, default="")
    STREET_ID = models.CharField(max_length=20, default="")
    COMMUNITY_NAME = models.CharField(max_length=20, default="")
    COMMUNITY_ID = models.CharField(max_length=20, default="")
    EVENT_TYPE_NAME = models.CharField(max_length=20, default="")
    EVENT_TYPE_ID = models.CharField(max_length=20, default="")
    MAIN_TYPE_NAME = models.CharField(max_length=20, default="")
    MAIN_TYPE_ID = models.CharField(max_length=20, default="")
    SUB_TYPE_NAME = models.CharField(max_length=20, default="")
    SUB_TYPE_ID = models.CharField(max_length=20, default="")
    DISPOSE_UNIT_NAME = models.CharField(max_length=20, default="")
    DISPOSE_UNIT_ID = models.CharField(max_length=20, default="")
    EVENT_SRC_NAME = models.CharField(max_length=20, default="")
    EVENT_SRC_ID = models.CharField(max_length=20, default="")
    OPERATE_NUM = models.CharField(max_length=20, default="")
    OVERTIME_ARCHIVE_NUM = models.CharField(max_length=20, default="")
    INTIME_TO_ARCHIVE_NUM = models.CharField(max_length=20, default="")
    INTIME_ARCHIVE_NUM = models.CharField(max_length=20, default="")
    EVENT_PROPERTY_ID = models.CharField(max_length=20, default="")
    EVENT_PROPERTY_NAME = models.CharField(max_length=20, default="")
    OCCUR_PLACE = models.CharField(max_length=20, default="")

class User(models.Model):
    user_name = models.CharField(max_length=20, default="sadness")
    password = models.CharField(max_length=20, default="happiness")