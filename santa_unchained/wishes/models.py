from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.utils.translation import gettext_lazy as _

# Create your models here.


class WishListStatuses(models.TextChoices):
    NEW = "NEW", _("NEW")
    ACCEPTED = "ACCEPTED", _("Accepted")
    REJECTED = "REJECTED", _("Rejected")
    READY_FOR_SHIPPING = "READY_FOR_SHIPPING", _("Ready for shipping")
    DELIVERED = "DELIVERED", _("Delivered")


class Address(models.Model):
    street = models.CharField(verbose_name="Steet", max_length=100)
    post_code = models.CharField(verbose_name="Postal Code", max_length=6)
    city = models.CharField(verbose_name="City", max_length=100)
    country = models.CharField(verbose_name="Country", max_length=100)
    lng = models.DecimalField(verbose_name="Longitude",
                              max_digits=9, decimal_places=6, default=0)
    lat = models.DecimalField(verbose_name="Latitude",
                              max_digits=9, decimal_places=6, default=0)


class WishList(models.Model):
    name = models.CharField(verbose_name="Name", max_length=50)
    email = models.EmailField(verbose_name="E-mail", max_length=100)
    content = models.TextField(verbose_name="Content", max_length=1000)
    status = models.CharField(verbose_name="Status", max_length=100, choices=WishListStatuses.choices,
                              default=WishListStatuses.NEW)
    slug = AutoSlugField(populate_from="name")
    address = models.ForeignKey(
        Address, verbose_name="Address", on_delete=models.CASCADE)


class WishListItem(models.Model):
    wish_list = models.ForeignKey(
        WishList, verbose_name="Wish List", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Name", max_length=100)
    approved = models.BooleanField(verbose_name="Approved", default=False)


class NewWishListManager(models.Manager):
    """Manager which filters only NEW wish lists"""

    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(status=WishListStatuses.NEW)


class WishListNew(WishList):
    objects = NewWishListManager()

    class Meta:
        proxy = True
        verbose_name = _("new wish list")
        verbose_name_plural = _("new wish lists")
