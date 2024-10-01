from django import forms
from .models import News


class NewsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            
            if field_name != 'is_published':
                field.widget.attrs["class"] = "form-control mb-3"

    class Meta:
        model = News
        fields = ["image", "title", "body", "is_published"]
