import re
from django.db.models import Q

def match_camel_case(name):
    pattern = r'^[a-z]+([A-Z][a-z]*)*$'
    return re.match(pattern, name) is not None

def to_underscore(name: str) -> str:
    """驼峰转下划线"""
    if '_' not in name:
        name = re.sub(r'([a-z])([A-Z])', r'\1_\2', name)
    else:
        raise ValueError(f'{name}字符中包含下划线，无法转换')
    return name.lower()

class QueryHelper:
    # 添加关联字段映射
    RELATED_FIELD_MAPPING = {
        'forumTitle': {'fk': 'fid', 'related_field': 'title'},
        'goodsName': {'fk': 'gid', 'related_field': 'name'},
        'ordersNo': {'fk': 'oid', 'related_field': 'no'},
        'outfitName': {'fk': 'oid', 'related_field': 'name'},
        'categoryName': {'fk': 'cid', 'related_field': 'name'},
    }

    @staticmethod
    def build_query_conditions(request_data, field_list, fuzzy_fields=None):
        """
        构建查询条件
        :param request_data: 请求数据
        :param field_list: 需要查询的字段列表
        :param fuzzy_fields: 需要模糊查询的字段列表
        :return: 查询条件 Q 对象
        """
        q = Q()
        q.connector = 'AND'
        fuzzy_fields = fuzzy_fields or []
        for field in field_list:
            value = request_data.get(field)
            # 处理空字符串，将其视为 None
            if value == '':
                value = None
            if value is not None:
                if field in fuzzy_fields:
                    if match_camel_case(field):
                        # 检查是否存在映射关系
                        field_mapping = QueryHelper.RELATED_FIELD_MAPPING.get(field)
                        if field_mapping:
                            # 构建关联查询条件
                            lookup = f"{field_mapping['fk']}__{field_mapping['related_field']}__icontains"
                            q.children.append((lookup, value))
                        else:
                            # 如果没有映射关系，使用默认的转换方式
                            field_name = to_underscore(field)
                            q.children.append((f"{field_name}__icontains", value))
                    else:
                        q.children.append((f"{field}__icontains", value))
                else:
                    q.children.append((field, value))
        return q

    @staticmethod
    def exclude_null_foreign_keys(queryset, foreign_key_fields):
        """
        过滤掉没有对应外键的记录
        :param queryset: 查询集
        :param foreign_key_fields: 外键字段名称列表
        :return: 过滤后的查询集
        """
        for foreign_key_field in foreign_key_fields:
            queryset = queryset.exclude(**{f"{foreign_key_field}__isnull": True})
        return queryset
