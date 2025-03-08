from django.http import HttpResponse, JsonResponse
from django.utils.deprecation import MiddlewareMixin
from jwt import ExpiredSignatureError, InvalidTokenError, PyJWTError
from rest_framework_jwt.settings import api_settings

class JwtAuthenticationMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 白名单路径，直接放行
        white_list = ["/login", "/register", "/file/imgUpload"]
        
        # 静态资源后缀
        static_files = ['.jpg', '.jpeg', '.png', '.gif', '.ico', '.css', '.js']
        
        path = request.path
        
        # 如果路径在白名单中，直接放行
        if path in white_list:
            return None
            
        # 如果是静态资源，直接放行
        if any(path.lower().endswith(ext) for ext in static_files) or path.startswith('/upload/'):
            return None
            
        # 如果路径包含 'front'，不需要验证 token
        if 'front' in path.lower():
            return None
            
        print("进行token验证")
        # 获取 Token 的多种可能形式
        token = request.headers.get('Token')
        print("Token:", token)
        
        if not token:
            return JsonResponse({'code': -1, 'msg': '未提供Token！'})
            
        try:
            jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
            jwt_decode_handler(token)
        except ExpiredSignatureError:
            return JsonResponse({'code': -1, 'msg': 'Token过期，请重新登录！'})
        except InvalidTokenError:
            return JsonResponse({'code': -1, 'msg': 'Token验证失败！'})
        except PyJWTError:
            return JsonResponse({'code': -1, 'msg': 'Token验证异常！'})