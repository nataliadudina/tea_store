from django import forms
from .models import TeaProduct, TeaCategory, Version
from django.core.exceptions import ValidationError


# Mixin class to add common styles to form fields
class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Iterate over form fields and add CSS class to each one
        for field_name, field in self.fields.items():  # self.fields - django dict
            if field_name != 'is_active':
                field.widget.attrs['class'] = 'form-control'


# Form for creating and updating TeaProduct instances
class ProductForm(StyleFormMixin, forms.ModelForm):
    # Customizing the category field to include all TeaCategory instances
    category = forms.ModelChoiceField(queryset=TeaCategory.objects.all(), empty_label='Choose category')

    # Overriding the clean method to perform custom validation
    def clean(self):
        cleaned_data = super().clean()
        forbidden_words = ['cure', 'prescription', 'miracle', 'magical', 'guaranteed', 'addictive', 'dangerous',
                           'exclusive', 'forbidden']

        # Checking for forbidden words in 'name' and 'description' fields
        for field_name in ['name', 'description']:
            value = cleaned_data.get(field_name, '').lower()
            if any(word in value for word in forbidden_words):
                raise ValidationError(f"Forbidden word '{value}' is not allowed in the {field_name}.")

    class Meta:
        model = TeaProduct
        fields = ['name', 'description', 'ingredients', 'flavour', 'aroma', 'preparation', 'preview', 'price',
                  'category']

        # Customizing the 'description' field to use a Textarea widget
        widgets = {
            'description': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }


# Form for creating and updating Version instances
class VersionForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Version
        fields = ['product', 'version_number', 'version_name', 'text', 'is_active']

        # Customizing the 'text' field to use a Textarea widget
        widgets = {
            'text': forms.Textarea(attrs={'cols': 50, 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Making the 'is_active' field optional
        self.fields['is_active'].required = False

    # Overriding the clean_is_active method to perform custom validation
    def clean_is_active(self):
        is_active = self.cleaned_data.get('is_active')
        product = self.cleaned_data.get('product')

        # Checking that only one version is active per product
        if is_active and Version.objects.filter(product=product, is_active=True).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('Only one active version allowed.')

        return is_active
