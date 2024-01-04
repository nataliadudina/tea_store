from django import forms
from .models import TeaProduct, TeaCategory, Version
from django.core.exceptions import ValidationError


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():  # self.fields - django dict
            if field_name != 'is_active':
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    category = forms.ModelChoiceField(queryset=TeaCategory.objects.all(), empty_label='Choose category')

    def clean(self):
        cleaned_data = super().clean()
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']

        for field_name in ['name', 'description']:
            value = cleaned_data.get(field_name, '').lower()
            if any(word in value for word in forbidden_words):
                raise ValidationError(f"Forbidden word '{value}' is not allowed in the {field_name}.")

    class Meta:
        model = TeaProduct
        fields = ['name', 'description', 'ingredients', 'flavour', 'aroma', 'preparation', 'preview', 'price',
                  'category']
        widgets = {
            'description': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }


class VersionForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Version
        fields = ['product', 'version_number', 'version_name', 'text', 'is_active']
        widgets = {
            'text': forms.Textarea(attrs={'cols': 50, 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_active'].required = False

    def clean_is_active(self):
        is_active = self.cleaned_data.get('is_active')
        product = self.cleaned_data.get('product')

        # Check that only one version is active
        if is_active and Version.objects.filter(product=product, is_active=True).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('Only one active version allowed.')

        return is_active
