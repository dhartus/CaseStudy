import re
from django import forms

class InputForm(forms.Form):
    file = forms.FileField()

class SearchForm(forms.Form):
    store_id = forms.IntegerField(required=False)
    sku = forms.CharField(max_length=50, required=False)
    product_name = forms.CharField(max_length=50,required=False)
    date = forms.DateField(required=False)    

    def clean(self):
        cleaned_data = super().clean()
        if not (cleaned_data.get('store_id') or cleaned_data.get('sku') or cleaned_data.get('product_name') or cleaned_data.get('date')):
            raise forms.ValidationError("Please specify at least one field", code="invalid")

class UpdateForm(forms.Form):
    store_id = forms.IntegerField(required=True)
    sku = forms.CharField(max_length=50, required=True)
    product_name = forms.CharField(max_length=50,required=False)
    price = forms.IntegerField(required=False)
    date = forms.DateField(required=False) 

    def clean(self):
        cleaned_data = super().clean()
        if not (cleaned_data.get('price') or cleaned_data.get('date') or cleaned_data.get('product_name')):
            raise forms.ValidationError("Please specify at least one field", code="invalid")