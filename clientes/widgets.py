from django.forms.widgets import ClearableFileInput


class ImageInput(ClearableFileInput):
    template_name = "widgets/foto_widget.html"
