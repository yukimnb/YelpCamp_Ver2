from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic

from .models import Campground, Review


class ListCampground(generic.ListView):
    model = Campground
    template_name = "list.html"
    context_object_name = "campgrounds"

    def get_queryset(self):
        return Campground.objects.all().order_by("id")


class DetailCampground(generic.DetailView):
    model = Campground
    template_name = "detail.html"
    context_object_name = "campground"
    pk_url_kwarg = "id"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["reviews"] = Review.objects.filter(campground=self.kwargs["id"])
        return context


class CreateCampground(generic.CreateView):
    model = Campground
    template_name = "create.html"
    fields = ["title", "price", "location", "description", "image"]
    success_url = reverse_lazy("campgrounds:list")

    def form_valid(self, form):
        messages.success(self.request, "キャンプ場を作成しました")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "キャンプ場の作成に失敗しました")
        return super().form_invalid(form)


class EditCampground(generic.UpdateView):
    model = Campground
    template_name = "edit.html"
    pk_url_kwarg = "id"
    fields = ["title", "price", "location", "description", "image"]

    def get_success_url(self):
        return reverse_lazy("campgrounds:detail", kwargs={"id": self.kwargs["id"]})

    def form_valid(self, form):
        messages.success(self.request, "キャンプ場を更新しました")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "キャンプ場の更新に失敗しました")
        return super().form_invalid(form)


class DeleteCampground(generic.DeleteView):
    model = Campground
    template_name = "delete.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("campgrounds:list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "キャンプ場を削除しました")
        return super().delete(request, *args, **kwargs)


class CreateReview(generic.CreateView):
    model = Review
    template_name = "create_review.html"
    pk_url_kwarg = "id"
    fields = ["campground", "comment", "rating"]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["campground"] = Campground.objects.get(id=self.kwargs["id"])
        return context

    def get_success_url(self):
        return reverse_lazy("campgrounds:detail", kwargs={"id": self.kwargs["id"]})

    def form_valid(self, form):
        messages.success(self.request, "コメントを作成しました")
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form)
        messages.error(self.request, "コメントの作成に失敗しました")
        return super().form_invalid(form)


class DeleteReview(generic.DeleteView):
    model = Review
    pk_url_kwarg = "review_id"

    def get_success_url(self):
        return reverse_lazy("campgrounds:detail", kwargs={"id": self.kwargs["id"]})

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "コメントを削除しました")
        return super().delete(request, *args, **kwargs)
