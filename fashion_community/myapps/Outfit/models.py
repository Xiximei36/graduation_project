from django.db import models
from rest_framework import serializers
from myapps.utils.serializers import BaseSerializer
from myapps.User.models import User

class Outfit(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.CharField(max_length=200, null=True, verbose_name="图片")
    type = models.CharField(max_length=200, null=True, verbose_name="类型")
    season = models.CharField(max_length=200, null=True, verbose_name="季节")
    name = models.CharField(max_length=200, null=True, verbose_name="名称")
    content = models.CharField(max_length=200, null=True, verbose_name="内容")
    uid = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False)
    num = models.IntegerField(null=True, verbose_name="浏览量")
    status = models.CharField(max_length=200, null=True, verbose_name="状态")
    create_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name="发布时间")
    class Meta:
        db_table = "outfit"

class OutfitSerializer(BaseSerializer):
    createTime = serializers.SerializerMethodField()
    def get_createTime(self, obj):
        return self.format_datetime(obj.create_time)

    uid = serializers.SerializerMethodField()

    def get_uid(self, obj):
        return obj.uid_id if hasattr(obj, 'uid_id') else None

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
        model = Outfit
        fields = [
            'id',
            'image',
            'type',
            'season',
            'name',
            'content',
            'uid',
            'num',
            'status',
            'createTime',
            'realname',
            'userImage',
        ]
