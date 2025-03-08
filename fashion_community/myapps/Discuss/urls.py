from django.urls import path
from myapps.Discuss.views import *
urlpatterns = [
    path('frontPage', frontPageView.as_view(), name='前端分页查询'),
    path('frontAll', frontAllView.as_view(), name='前端查询所有'),
    path('frontOne', frontOneView.as_view(), name='前端根据id查询单条'),
    path('queryAll', queryAllView.as_view(), name='后台条件查询'),
    path('selectPage', selectPageView.as_view(), name='后台分页查询'),
    path('selectOne', selectOneView.as_view(), name='后端查询单条'),
    path('add', addView.as_view(), name='新增'),
    path('edit', editView.as_view(), name='编辑'),
    path('deleteById', DelView.as_view(), name='删除')
]
