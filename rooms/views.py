import os
from django.http import Http404
from django.views.generic import ListView, DetailView, View, UpdateView, FormView
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from users import mixins as user_mixins
from . import models, forms

# from django.shortcuts import render, redirect
# from django.core.paginator import Paginator, EmptyPage

# 프로그래밍이 아닌 구성을 갖추도록 세팅하는 클래스.
# <HomeView는 rooms_list를 보여주기 위한 클래스>
# 만약 class based view에서 무언가 추가할 기능들이 있다면, get_context_dat()를 통해서
# context에 변수를 담아 template에 렌더링하면 된다.
class HomiView(ListView):

    """ HomeView Definition """

    # 오직 model을 정의함으로써 자동적으로 HomeView 클래스에서 model에 있는 List를 보여줄수 있다.
    model = models.Room
    paginate_by = 12
    paginate_orphans = 3
    ordering = "-created"
    context_object_name = "rooms"


# Abstraction
class RoomDetail(DetailView):

    """ Room_detail Definition """

    model = models.Room


def get_find_room(request):
    # title = request.GET("category")
    category = request.GET.get("room_category")  # 수정이 필요함 :None
    print(category)
    return render(request, "rooms/room_list.html", {"category": category})


def map_view(request):
    ## 추후 context에 map_data를 삽입합시다.

    return render(request, "maps/map_view.html")


class SearchView(View):

    """ Search View Defintion :: search-box에서 room을 찾는다."""

    def get(self, request):
        country = request.GET.get("country")
        if country:
            form = forms.SearchForm(request.GET)
            if form.is_valid():
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilities"] = facility

                # QuerySet=> qs
                qs = models.Room.objects.filter(**filter_args).order_by("-created")

                paginator = Paginator(qs, 10, orphans=5)
                page = request.GET.get("page", 1)
                rooms = paginator.get_page(page)

                # render는 html에 내용을 담아 표시하는것(rendering)
                return render(
                    request, "maps/search.html", {"form": form, "rooms": rooms}
                )

        else:
            # 여기서 form안에 값을 집어넣지 않고 search할 경우 error가 발생 -> unbound Form 에러라고 함
            form = forms.SearchForm()

        return render(request, "rooms/search.html", {"form": form})


class EditRoomView(user_mixins.LoggedInOnlyView, UpdateView):

    model = models.Room
    template_name = "rooms/room_edit.html"
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    )

    def get_object(self, queryset=None):
        # room객체를 찾아서 보여주는 메소드
        room = super().get_object(queryset=queryset)
        # print(room.host.pk, self.request.user.pk)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


class RoomPhotosView(user_mixins.LoggedInOnlyView, DetailView):

    model = models.Room
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


# class RoomMapView(DetailView):
#     model = models.Room
#     template_name = "rooms/map_view.html"

#     def get_address(self, queryset=None):
#         address = super().get_object(queryset=queryset)
#         if address in None:
#             raise Http404()
#         return room


class RoomPhotosView(user_mixins.LoggedInOnlyView, DetailView):

    model = models.Room
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


@login_required
def delete_photo(request, room_pk, photo_pk):
    user = request.user
    try:
        room = models.Room.objects.get(pk=room_pk)
        if room.host.pk != user.pk:
            messages.error(request, "Cant delete that photo")
        else:
            models.Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, "Photo Deleted")
        return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))
    except models.Room.DoesNotExist:
        return redirect(reverse("core:home"))


class EditPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = models.Photo
    template_name = "rooms/photo_edit.html"
    pk_url_kwarg = "photo_pk"
    success_message = "Photo Updated"
    fields = ("caption",)

    def get_success_url(self):
        room_pk = self.kwargs.get("room_pk")
        return reverse("rooms:photos", kwargs={"pk": room_pk})


class AddPhotoView(user_mixins.LoggedInOnlyView, FormView):

    template_name = "rooms/photo_create.html"
    form_class = forms.CreatePhotoForm

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        form.save(pk)
        messages.success(self.request, "Photo Uploaded")
        return redirect(reverse("rooms:photos", kwargs={"pk": pk}))


class CreateRoomView(user_mixins.LoggedInOnlyView, FormView):

    form_class = forms.CreateRoomForm
    template_name = "rooms/room_create.html"

    def form_valid(self, form):
        room = form.save()
        room.host = self.request.user
        room.save()
        form.save_m2m()
        messages.success(self.request, "Room Uploaded")
        return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))


# url에 의해서 사용자에게 보여주는 view.py
# 여기서 어떻게 보여질지 정해짐
# 매번 요청을 보내면 Django는 python object로 반환시켜준다.

# render 함수는 httpResponse안에 html을 담아서 보내줄수 있다. 따라서 template을 담아서 rendering 시킨다.
# view에서 template을 rendering시에 template위치를 django에게 알려줘야 한다.
# config settings.py 에서 template-> DIRS=[os.path.join(BASE_DIR,"templates")]
# context는 변수를 담어 template에 보내줄수도 있다.

# context를 통해서 변수를 보내줄 수 있고 해당html에서 logic을 구현할 수 있다.
# => {{변수명}}
# logic if문 => {% if true:%} ~~~ {% else  ~~%} ~~ {% endif %}
# all_rooms.html은 template 폴더 내 파일이름과 똑같아야 한다.

# 위에있는 RoomDetail클래스와 똑같이 작동된다. 다만 코드가 많을뿐..
# [manual code]
# def room_detail(request, pk):
#     # primary key인 rooms의 id로 접근하여 해당 room을 보여지기 위한 room_detail
#     try:
#         room = models.Room.objects.get(pk=pk)
#         return render(request, "rooms/detail.html", {"room": room})
#     except models.Room.DoesNotExist:
#         # return redirect(reverse("core:home"))
#         raise Http404()


# def all_rooms(request):
#     page = request.GET.get("page", 1)
#     room_list = models.Room.objects.all()
#     paginator = Paginator(room_list, 10, orphans=5)  # (object, number of rooms)

#     try:
#         rooms = paginator.page(int(page))  # get_page와 page의 기능 document참고
#         return render(request, "rooms/home.html", {"page": rooms})
#     except EmptyPage:
#         return redirect("/")


# version 1: manualy-paginator
# def all_rooms():
# int를 해주는 이유는 query가 str타입이고 1은 숫자이기 때문.. "page"="1"이 되버린다.
# page = int(request.GET.get("page", 1))
# page = int(page or 1)
# page_size = 10
# limit = page_size * page
# offset = limit - page_size
# all_rooms = models.Room.objects.all()[offset:limit]
# ->쿼리셋을 생성하는것 뿐.. 여기서 print()나 어떠한Action을 할 경우 서버가 터질수도..조심해야함
# page_count = ceil(models.Room.objects.count() / page_size)
# return render(
#     request,
#     "rooms/home.html",
#     context={
#         "rooms": all_rooms,
#         "page": page,
#         "page_count": page_count,
#         "page_range": range(1, page_count + 1),
#     },)
