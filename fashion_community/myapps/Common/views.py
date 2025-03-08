import json
from datetime import datetime
from django.http import JsonResponse
from django.views import View
from rest_framework_jwt.settings import api_settings
from fashion_community import settings
from myapps.Admin.models import Admin, AdminSerializer
from myapps.User.models import User, UserSerializer
from myapps.utils.response import ResponseHandler
from myapps.utils.model import ModelHelper
def custom_jwt_payload_handler(user, user_type):
    """
    自定义JWT payload
    :param user: 用户对象
    :param user_type: 用户类型 01-管理员 02-普通用户
    """
    if user_type == '01':
        # 管理员登录
        return {
            'user_id': user.pk,
            'username': user.username,
            # JWT令牌有效期为5天
            'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA, 
            'user_type': user_type
        }
    else:
        # 用户登录
        return {
            'user_id': user.pk,
            'phone': user.phone,
            'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA,
            'user_type': user_type
        }

# 登录
class LoginView(View):

    def post(self, request):
        json_str = request.body
        json_dict = json.loads(json_str)
        user_type = json_dict.get("type")

        if user_type == '01':
            admin = Admin.objects.filter(username=json_dict.get("phone"))
            if not admin:
                return ResponseHandler.error(msg='账号不存在！')
            if admin.count() > 1:
                return ResponseHandler.error(msg='数据库异常！')
            if json_dict.get("password") != admin.first().password:
                return ResponseHandler.error(msg='密码错误！')
            
            # 使用自定义的payload处理器
            payload = custom_jwt_payload_handler(admin.first(), user_type)
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            token = jwt_encode_handler(payload)
            
            user_data = AdminSerializer(admin.first()).data
            user_data['token'] = token
            return ResponseHandler.success(data=user_data, msg='登录成功！')

        if user_type == '02':
            user = User.objects.filter(phone=json_dict.get("phone"))
            if not user:
                return ResponseHandler.error(msg='账号不存在！')
            if user.count() > 1:
                return ResponseHandler.error(msg='数据库异常！')
            if json_dict.get("password") != user.first().password:
                return ResponseHandler.error(msg='密码错误！')
            
            # 使用自定义的payload处理器
            payload = custom_jwt_payload_handler(user.first(), user_type)
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            token = jwt_encode_handler(payload)
            
            user_data = UserSerializer(user.first()).data
            user_data['token'] = token
            return ResponseHandler.success(data=user_data, msg='登录成功！')

# 注册
class RegisterView(View):

    def post(self, request):
        json_data = request.body.decode("utf-8")
        try:
            dic = json.loads(json_data)
        except Exception as e:
            return ResponseHandler.error(msg='参数有误')
        serializer_obj = UserSerializer(data=dic)
        user = User.objects.filter(phone=dic.get("phone"))  # 使用phone检查
        if user:
            return ResponseHandler.error(msg='手机号已存在，请检查')
        if not serializer_obj.is_valid():
            return ResponseHandler.error(msg=serializer_obj.errors)
        new_user = User.objects.create(**serializer_obj.validated_data)

        # 生成 token
        payload = custom_jwt_payload_handler(new_user, '02')  # 注册的都是普通用户，使用02
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        token = jwt_encode_handler(payload)

        user_data = UserSerializer(new_user).data
        user_data['token'] = token
        return ResponseHandler.success(data=user_data, msg='注册成功')

# 更新信息
class UpdateView(View):

    def post(self, request):
        json_str = request.body
        json_dict = json.loads(json_str)
        if 'id' not in json_dict:
            return ResponseHandler.error(msg='id不能为空')
        
        user_type = json_dict.get("type")
        
        try:
            if user_type == '01':
                # 管理员更新
                obj = Admin.objects.get(id=json_dict['id'])
                # 检查用户名唯一性
                if Admin.objects.filter(username=json_dict.get('username')).exclude(id=json_dict['id']).exists():
                    return ResponseHandler.error(msg='用户名已存在，请检查')
                
                serializer_obj = AdminSerializer(data=json_dict)
                if not serializer_obj.is_valid():
                    return ResponseHandler.error(msg=serializer_obj.errors)
                
                # 使用 ModelHelper 更新字段
                ModelHelper.update_model_fields(
                    instance=obj,
                    data=json_dict,
                    fields=['password', 'username'],  # 管理员可更新的字段列表
                    foreign_keys=[]  # 管理员没有外键字段
                )
                obj.save()
                
                # 重新生成token
                payload = custom_jwt_payload_handler(obj, user_type)
                jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                token = jwt_encode_handler(payload)
                
                # 将token添加到返回数据中
                user_data = AdminSerializer(obj).data
                user_data['token'] = token
                return ResponseHandler.success(data=user_data, msg='更新成功')
            
            elif user_type == '02':
                # 用户更新
                obj = User.objects.get(id=json_dict['id'])
                # 检查手机号唯一性
                if User.objects.filter(phone=json_dict.get('phone')).exclude(id=json_dict['id']).exists():
                    return ResponseHandler.error(msg='手机号已存在，请检查')
                
                serializer_obj = UserSerializer(data=json_dict)
                if not serializer_obj.is_valid():
                    return ResponseHandler.error(msg=serializer_obj.errors)
                
                # 使用 ModelHelper 更新字段
                ModelHelper.update_model_fields(
                    instance=obj,
                    data=json_dict,
                    fields=['phone', 'password', 'image', 'realname', 'sex', 'age', 'address'],  # 用户可更新的字段列表
                    foreign_keys=[]  # 用户没有外键字段
                )
                obj.save()
                
                # 重新生成token
                payload = custom_jwt_payload_handler(obj, user_type)
                jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                token = jwt_encode_handler(payload)
                
                # 将token添加到返回数据中
                user_data = UserSerializer(obj).data
                user_data['token'] = token
                return ResponseHandler.success(data=user_data, msg='更新成功')
            
            else:
                return ResponseHandler.error(msg='无效的用户类型')
                
        except (Admin.DoesNotExist, User.DoesNotExist):
            return ResponseHandler.error(msg='数据不存在')
        except Exception as e:
            print(f"更新时出现异常: {e}")
            return ResponseHandler.error(msg='更新失败')

# 上传图片
class UploadView(View):

    def post(self, request):
        file = request.FILES.get('file')
        if file:
            file_name = file.name
            suffixName = file_name[file_name.rfind("."):]
            new_file_name = datetime.now().strftime('%Y%m%d%H%M%S') + suffixName
            file_path = str(settings.MEDIA_ROOT) + "\\" + new_file_name
            print("file_path=", file_path)
            try:
                with open(file_path, 'wb') as f:
                    for chunk in file.chunks():
                        f.write(chunk)
                return ResponseHandler.success(data='/api/upload/'+new_file_name, msg='上传成功')
            except Exception as e:
                print("出现如下异常%s" % e)
                return ResponseHandler.error(msg="上传错误，请检查")
