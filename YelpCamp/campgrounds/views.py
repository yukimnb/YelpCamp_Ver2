from accounts.models import CustomUser
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from utils.mapbox_api import get_forward_geocoding

from .models import Campground, Review


class Index(generic.TemplateView):
    template_name = "campgrounds/index.html"


class ListCampground(generic.ListView):
    model = Campground
    template_name = "campgrounds/list.html"
    context_object_name = "campgrounds"
    campgrounds = Campground.objects.all().order_by("id")

    def get_queryset(self):
        return self.campgrounds

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["campgrounds_json"] = []
        for campground in list(self.campgrounds.values()):
            campground["properties"] = {
                "title": campground["title"],
            }
            context["campgrounds_json"].append(campground)
        return context


class DetailCampground(generic.DetailView):
    model = Campground
    template_name = "campgrounds/detail.html"
    context_object_name = "campground"
    pk_url_kwarg = "id"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if Review.objects.filter(campground=self.kwargs["id"]).exists():
            context["reviews"] = Review.objects.select_related("reviewer").filter(campground=self.kwargs["id"])
        else:
            context["reviews"] = None
        context["author"] = CustomUser.objects.get(id=Campground.objects.get(id=self.kwargs["id"]).author_id)
        return context


class CreateCampground(LoginRequiredMixin, generic.CreateView):
    model = Campground
    template_name = "campgrounds/create.html"
    fields = ["title", "price", "location", "description", "image1", "image2", "image3", "author"]
    success_url = reverse_lazy("campgrounds:list")

    def form_valid(self, form):
        campground = form.save(commit=False)
        campground.geometry = get_forward_geocoding(campground.location)
        campground.save()
        messages.success(self.request, "キャンプ場を作成しました")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "キャンプ場の作成に失敗しました")
        return super().form_invalid(form)


class EditCampground(LoginRequiredMixin, generic.UpdateView):
    model = Campground
    template_name = "campgrounds/edit.html"
    pk_url_kwarg = "id"
    fields = ["title", "price", "location", "description", "image1", "image2", "image3"]

    def get_success_url(self):
        return reverse_lazy("campgrounds:detail", kwargs={"id": self.kwargs["id"]})

    def form_valid(self, form):
        messages.success(self.request, "キャンプ場を更新しました")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "キャンプ場の更新に失敗しました")
        return super().form_invalid(form)


class DeleteCampground(LoginRequiredMixin, generic.DeleteView):
    model = Campground
    template_name = "campgrounds/delete.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("campgrounds:list")

    def form_valid(self, form):
        messages.success(self.request, "キャンプ場を削除しました")
        return super().form_valid(form)


class CreateReview(LoginRequiredMixin, generic.CreateView):
    model = Review
    template_name = "reviews/create_review.html"
    pk_url_kwarg = "id"
    fields = ["comment", "rating", "campground", "reviewer"]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["campground"] = Campground.objects.get(id=self.kwargs["id"])
        return context

    def get_success_url(self):
        return reverse_lazy("campgrounds:detail", kwargs={"id": self.kwargs["id"]})

    def form_valid(self, form):
        messages.success(self.request, "レビューを作成しました")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "レビューの作成に失敗しました")
        return super().form_invalid(form)


class DeleteReview(LoginRequiredMixin, generic.DeleteView):
    model = Review
    pk_url_kwarg = "review_id"

    def get_success_url(self):
        return reverse_lazy("campgrounds:detail", kwargs={"id": self.kwargs["id"]})

    def form_valid(self, form):
        messages.success(self.request, "レビューを削除しました")
        return super().form_valid(form)
