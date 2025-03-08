from django.db import models
from rest_framework import serializers
from myapps.utils.serializers import BaseSerializer
from myapps.Outfit.models import Outfit
from myapps.User.models import User

class Discuss(models.Model):
    id = models.AutoField(primary_key=True)
    oid = models.ForeignKey(Outfit, on_delete=models.CASCADE, db_constraint=False)
    uid = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False)
    content = models.CharField(max_length=200, null=True, verbose_name="评论内容")
    reply = models.CharField(max_length=200, null=True, verbose_name="回复内容")
    create_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name="评论时间")
    class Meta:
        db_table = "discuss"

class DiscussSerializer(BaseSerializer):
    createTime = serializers.SerializerMethodField()
    def get_createTime(self, obj):
        return self.format_datetime(obj.create_time)

    oid = serializers.SerializerMethodField()

    def get_oid(self, obj):
        return obj.oid_id if hasattr(obj, 'oid_id') else None

    uid = serializers.SerializerMethodField()

    def get_uid(self, obj):
        return obj.uid_id if hasattr(obj, 'uid_id') else None

    outfitName = serializers.SerializerMethodField()

    def get_outfitName(self, obj):
        try:
            if hasattr(obj, 'oid') and obj.oid is not None:
                return obj.oid.name
        except (Outfit.DoesNotExist, AttributeError):
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

    userImage = serializers.SerializerMethodField()

    def get_userImage(self, obj):
        try:
            if hasattr(obj, 'uid') and obj.uid is not None:
                return obj.uid.image
        except (User.DoesNotExist, AttributeError):
            return None
        return None

    class Meta:
        model = Discuss
        fields = [
            'id',
            'oid',
            'uid',
            'content',
            'reply',
            'createTime',
            'outfitName',
            'realname',
            'userImage',
        ]
