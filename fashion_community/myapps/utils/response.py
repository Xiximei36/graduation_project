from django.http import JsonResponse

class ResponseHandler:
    @staticmethod
    def success(data=None, msg="操作成功"):
        return JsonResponse({
            'code': 200,
            'msg': msg,
            'data': data
        })

    @staticmethod
    def success_with_page(list_data, total, msg="操作成功"):
        return JsonResponse({
            'code': 200,
            'msg': msg,
            'data': {
                'list': list_data,
                'total': total
            }
        })

    @staticmethod
    def error(msg="操作失败", code=1):
        return JsonResponse({
            'code': code,
            'msg': msg
        }) 