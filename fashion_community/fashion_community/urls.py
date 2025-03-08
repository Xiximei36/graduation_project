from django.urls import path, include
from django.conf.urls.static import static
from myapps.Common.views import *

urlpatterns = [
    path('login', LoginView.as_view(), name='登录'),
    path('register', RegisterView.as_view(), name='注册'),
    path('updateUser', UpdateView.as_view(), name='更新信息'),
    path('file/imgUpload', UploadView.as_view(), name='上传'),
    path('admin/', include('myapps.Admin.urls')),
    path('cart/', include('myapps.Cart.urls')),
    path('category/', include('myapps.Category.urls')),
    path('comment/', include('myapps.Comment.urls')),
    path('discuss/', include('myapps.Discuss.urls')),
    path('forum/', include('myapps.Forum.urls')),
    path('goods/', include('myapps.Goods.urls')),
    path('orders/', include('myapps.Orders.urls')),
    path('orderItem/', include('myapps.OrderItem.urls')),
    path('outfit/', include('myapps.Outfit.urls')),
    path('stars/', include('myapps.Stars.urls')),
    path('user/', include('myapps.User.urls')),
    path('review/', include('myapps.Review.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
