from django.db import models
from rest_framework import serializers
from myapps.utils.serializers import BaseSerializer
from myapps.Goods.models import Goods
from myapps.User.models import User

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    gid = models.ForeignKey(Goods, on_delete=models.CASCADE, db_constraint=False)
    uid = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False)
    content = models.CharField(max_length=200, null=True, verbose_name="评论内容")
    create_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name="评论时间")
    class Meta:
        db_table = "review"

class ReviewSerializer(BaseSerializer):
    createTime = serializers.SerializerMethodField()
    def get_createTime(self, obj):
        return self.format_datetime(obj.create_time)

    gid = serializers.SerializerMethodField()

    def get_gid(self, obj):
        return obj.gid_id if hasattr(obj, 'gid_id') else None

    uid = serializers.SerializerMethodField()

    def get_uid(self, obj):
        return obj.uid_id if hasattr(obj, 'uid_id') else None

    goodsName = serializers.SerializerMethodField()

    def get_goodsName(self, obj):
        try:
            if hasattr(obj, 'gid') and obj.gid is not None:
                return obj.gid.name
        except (Goods.DoesNotExist, AttributeError):
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
        model = Review
        fields = [
            'id',
            'gid',
            'uid',
            'content',
            'createTime',
            'goodsName',
            'realname',
            'userImage',
        ]
