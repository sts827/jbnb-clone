from django.urls import path
from rooms import views as room_views

# urlpattern사용법
# 사용자가 요청하는 객체(room,review,list...)의 view.py에 함수를 만든다.
# 장고에서 url 작동방법
# /rooms로 시작하는 모든 url들은 rooms의 파일로 가게 하고
# /user로 시작하는 모든 url들을 users의 파일로 가게 한다.
# 그러나 아무것으로도 시작하지 않는 제일 처음 페이지 home, login,log-out일 경우
# core에서 관리한다.
# path("")는 /을 의미한다.<- 첫 페이지
app_name = "core"
# django에는 class based view라는 기능이 있다.=>HomeView
# class based view는 오직 한가지 기능만 할 수 있고 특화되있다.
urlpatterns = [path("", room_views.HomiView.as_view(), name="home")]

