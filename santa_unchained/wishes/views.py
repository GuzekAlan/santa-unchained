from django.shortcuts import render
from django.urls import reverse

from django.views.generic import TemplateView, DetailView, CreateView
from santa_unchained.wishes.models import WishList
from santa_unchained.wishes.forms import WishListWithAddressAndItemsForm

# Create your views here.


class WishListSuccessView(TemplateView):
    model = WishList
    template_name = "wishes/wishlist_success.html"


class WishListDetailView(DetailView):
    model = WishList
    template_name = "wishes/wishlist_detail.html"


class WishListsFormView(CreateView):
    model = WishList
    form_class = WishListWithAddressAndItemsForm

    def get_success_url(self) -> str:
        return reverse("wishes:success", kwargs={"slug": self.object.slug})
