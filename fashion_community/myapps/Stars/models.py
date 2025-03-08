from django.db import models
from rest_framework import serializers
from myapps.utils.serializers import BaseSerializer
from myapps.Forum.models import Forum
from myapps.User.models import User

class Stars(models.Model):
    id = models.AutoField(primary_key=True)
    fid = models.ForeignKey(Forum, on_delete=models.CASCADE, db_constraint=False)
    uid = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False)
    create_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name="收藏时间")
    class Meta:
        db_table = "stars"

class StarsSerializer(BaseSerializer):
    createTime = serializers.SerializerMethodField()
    def get_createTime(self, obj):
        return self.format_datetime(obj.create_time)

    fid = serializers.SerializerMethodField()

    def get_fid(self, obj):
        return obj.fid_id if hasattr(obj, 'fid_id') else None

    uid = serializers.SerializerMethodField()

    def get_uid(self, obj):
        return obj.uid_id if hasattr(obj, 'uid_id') else None

    forumTitle = serializers.SerializerMethodField()

    def get_forumTitle(self, obj):
        try:
            if hasattr(obj, 'fid') and obj.fid is not None:
                return obj.fid.title
        except (Forum.DoesNotExist, AttributeError):
            return None
        return None

    realname = serializers.SerializerMethodField()

    def get_realname(self, obj):
        try:
            if hasattr(obj, 'uid') and obj.uid is not None:
                return obj.uid.realname
        except (User.DoesNotExist, AttributeError):
            return None
        return None

    class Meta:
        model = Stars
        fields = [
            'id',
            'fid',
            'uid',
            'createTime',
            'forumTitle',
            'realname',
        ]
