from django.apps import apps

class ModelHelper:
    @staticmethod
    def update_model_fields(instance, data, fields, foreign_keys=None):
        """
        更新模型实例的字段
        :param instance: 模型实例
        :param data: 更新数据字典
        :param fields: 允许更新的字段列表
        :param foreign_keys: 外键字段列表，默认为None
        """
        foreign_keys = foreign_keys or []
        
        for field in fields:
            if field in data and data[field] is not None:
                if field in foreign_keys:
                    try:
                        # 获取外键字段的关联模型
                        related_model = instance._meta.get_field(field).remote_field.model
                        # 获取外键对象实例
                        if data[field] == '':  # 处理空字符串
                            setattr(instance, field, None)
                        else:
                            foreign_key_instance = related_model.objects.get(id=data.get(field))
                            setattr(instance, field, foreign_key_instance)
                    except Exception as e:
                        print(f"设置外键 {field} 时出现异常: {e}")
                        continue
                else:
                    setattr(instance, field, data.get(field))