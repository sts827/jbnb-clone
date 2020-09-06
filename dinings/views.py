from django.views.generic import ListView, DetailView, View, FormView
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from django.contrib import messages
from . import models

# Create your views here.


class DiningListView(ListView):
    """ HomeView Definition """

    model = models.Dining
    paginate_by = 12
    paginate_orphans = 3
    ordering = "-created"
    context_object_name = "dinings"

    # model = models.Food
    # context_object_name = "foods"
    # qs = models.Food.objects.filter(**filter_args).order_by("-created")

    # paginator = Paginator(qs, 10, orphans=5)
    # page = request.GET.get("page", 1)
    # foods = paginator.get_page(page)

    # def get(self, request, *args, **kwargs):
    #     return render(request, "foods/food_list.html", {"foods": foods})


class DiningDetail(DetailView):

    """ Room_detail Definition """

    model = models.Dining


class SearchView(View):

    """ Search View Defintion :: search-box에서 room을 찾는다."""

    def get(self, request):
        address = request.GET.get("address")
        if address:
            form = forms.SearchForm(request.GET)

            if form.is_valid():

                name = form.cleaned_data.get("name")
                menu = form.cleand_data.get("address")
                price = form.cleaned_data.get("price")
                description = form.cleaned_data.get("description")
                # QuerySet=> qs
                qs = models.Room.objects.filter(**filter_args).order_by("-created")

                paginator = Paginator(qs, 10, orphans=5)
                page = request.GET.get("page", 1)
                rooms = paginator.get_page(page)

                # render는 html에 내용을 담아 표시하는것(rendering)
                return render(
                    request, "rooms/search.html", {"form": form, "rooms": rooms}
                )

        else:
            # 여기서 form안에 값을 집어넣지 않고 search할 경우 error가 발생 -> unbound Form 에러라고 함
            form = forms.SearchForm()

        return render(request, "rooms/search.html", {"form": form})

