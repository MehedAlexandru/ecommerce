from django import forms
from .models import Category

# CATEGORY_CHOICES = [
#     ("fashion", "Fashion"),
#     ("toys", "Toys"),
#     ("electronics", "Electronics"),
#     ("home", "Home"),
#     ("sports", "Sports"),
#     ("collectibles", "Collectibles"),
#     ("cars", "Cars"),
#     ("other", "Other"),
# ]


class NewListingForm(forms.Form):
    title = forms.CharField(label="Title", max_length=64, widget=forms.TextInput(attrs={'class': 'form-control my-2'}))
    description = forms.CharField(label="Description", widget=forms.Textarea(attrs={'class': 'form-control my-2'}))
    starting_bid = forms.IntegerField(label="Starting Bid", min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control my-2'}))
    image_url = forms.URLField(label="Image URL", required=False, widget=forms.URLInput(attrs={'class': 'form-control my-2'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), initial="other", required=False, widget=forms.Select(attrs={'class': 'form-control my-2'}))
    def __init__(self, *args, **kwargs):
        super(NewListingForm, self).__init__(*args, **kwargs)
        self.fields['category'].initial = Category.objects.get(categories='other')
    # category = forms.ChoiceField(label="Category", choices=CATEGORY_CHOICES, initial="other", required=False, widget=forms.Select(attrs={'class': 'form-control my-2'}))