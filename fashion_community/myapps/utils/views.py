from rest_framework import generics
from django.db import connection
from django.db.models import Q

class BaseQueryView(generics.GenericAPIView):
    """
    通用查询视图基类
    """
    
    def get_custom_fields(self):
        """
        获取自定义字段定义
        子类重写此方法来定义需要添加的自定义字段
        return: {
            'field_name': {
                'sql': 'SQL查询语句，使用 %s 作为参数占位符',
                'params': lambda obj: [obj.id]  # 返回参数列表的函数
            }
        }
        """
        return {}

    def get_sort_mappings(self):
        """
        获取排序规则映射
        子类重写此方法来定义排序规则
        return: {
            'sort_key': 'order_by_field'
        }
        """
        return {}

    def get_custom_conditions(self, request_data):
        """
        获取自定义查询条件
        子类重写此方法来定义额外的查询条件
        return: Q对象或None
        """
        return None

    def execute_custom_sql(self, sql, params=None):
        """
        执行自定义SQL查询
        """
        with connection.cursor() as cursor:
            cursor.execute(sql, params or ())
            result = cursor.fetchone()
            return result[0] if result else 0

    def process_queryset(self, queryset, request_data):
        """
        处理查询集，添加自定义字段和排序
        """
        # 处理自定义查询条件
        custom_conditions = self.get_custom_conditions(request_data)
        if custom_conditions:
            queryset = queryset.filter(custom_conditions)

        # 处理排序
        sort_by = request_data.get('sortBy')
        sort_mappings = self.get_sort_mappings()
        if sort_by and sort_by in sort_mappings:
            queryset = queryset.order_by(sort_mappings[sort_by])

        return queryset

    def process_serializer_data(self, data, instance):
        """
        处理序列化数据，添加自定义字段
        """
        custom_fields = self.get_custom_fields()
        for field_name, config in custom_fields.items():
            params = config['params'](instance) if callable(config['params']) else config['params']
            data[field_name] = self.execute_custom_sql(config['sql'], params)
        return data 