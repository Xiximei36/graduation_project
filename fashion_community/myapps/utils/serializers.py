from rest_framework import serializers
class BaseSerializer(serializers.ModelSerializer):

    def format_datetime(self, datetime_obj):
        """
        格式化时间为字符串
        :param datetime_obj: 时间对象
        :return: 格式化后的字符串
        """
        if datetime_obj:
            return datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
        return None