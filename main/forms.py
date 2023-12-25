from django import forms
from models import TeaProduct, TeaCategory
from django.core.exceptions import ValidationError

class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=TeaCategory.objects.all, empty_label = 'Choose category')
    forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():    # self.fields - django dict
            field.widget.attrs['class'] = 'form_control'

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name', '')
        description = cleaned_data.get('description', '')

        for field_value, field_name in [(name, 'name'), (description, 'description')]:
            value = field_value.lower()
            for word in self.forbidden_words:
                if word in value:
                    raise ValidationError(f"Forbidden word '{word}' is not allowed in the {field_name}.")

    class Meta:
        model = TeaProduct
        fields = ['name', 'description', 'ingredients', 'flavour', 'aroma', 'preparation', 'preview', 'price', 'category']