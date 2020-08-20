"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# urlpattern사용법
# 사용자가 요청하는 객체(room,review,list...)의 view.py에 함수를 만든다.
# 장고에서 url 작동방법
# /rooms로 시작하는 모든 url들은 rooms의 파일로 가게 하고
# /user로 시작하는 모든 url들을 users의 파일로 가게 한다.
# 그러나 아무것으로도 시작하지 않는 제일 처음 페이지 home, login,log-out일 경우
# core에서 관리한다.
# url pattern은 필수이다.
urlpatterns = [
    path("", include("core.urls", namespace="core")),
    path("rooms/", include("rooms.urls", namespace="rooms")),
    path("users/", include("users.urls", namespace="users")),
    path("admin/", admin.site.urls),
]


# view를 가진 path를 return하는 static
""" static-url을 폴더에 연결하기 """
# uploads폴더에 있는 자료들을 외부에서 접근할 수 있게끔 할려면 Settings.py에서 MEDIA_ROOT,MEDIA_URL을 이용하여
# 장고에게 urlpattern을 알려주면 외부에서 local에 저장된 자료들을 접근할 수 있다.
# 따라서 static파일이나 업르드된 파일들을 내 컴의 서버에 사용하지 말자. -> 아마존 저장소 이용

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
