from django import forms
from django.db.transaction import atomic
from santa_unchained.wishes.models import WishList, WishListItem, Address


class WishListWithAddressAndItemsForm(forms.ModelForm):
    street = forms.CharField(max_length=100, label='Street and number')
    post_code = forms.CharField(max_length=10, label='Post code')
    city = forms.CharField(max_length=100, label='City')
    country = forms.CharField(max_length=100, label='Country')
    items = forms.Textarea()

    class Meta:
        model = WishList
        fields = ["name", "email", "content", "items"]

    def clean(self):
        cleaned_data = super().clean()
        items_names = cleaned_data.get("items", "").split("\n")
        items_names = [item_name.strip() for item_name in items_names]
        cleaned_data["items"] = items_names
        return cleaned_data

    @atomic
    def create_address_and_items(self, wish_list: WishList) -> WishList:
        """
        Create a wish list instance.

        Also, create related address and wish list items based on the payload
        of the form.
        """
        address_data = {
            "street": self.cleaned_data["street"],
            "post_code": self.cleaned_data["post_code"],
            "city": self.cleaned_data["city"],
            "country": self.cleaned_data["country"],
        }
        address = Address.objects.create(**address_data)
        wish_list.address = address
        wish_list.save()
        items = [
            WishListItem(name=name, wish_list=wish_list)
            for name in self.cleaned_data["items"]
        ]
        WishListItem.objects.bulk_create(items)
        return wish_list

    def save(self, commit=True):
        wish_list = super().save(commit=False)
        return self.create_address_and_items(wish_list)
