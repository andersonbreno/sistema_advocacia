from django.forms.widgets import ClearableFileInput
from django.forms.widgets import DateInput

class ImageInput(ClearableFileInput):
    template_name = "widgets/foto_widget.html"

class DatePickerInput(DateInput):
    input_type = 'date'

    def format_value(self, value):
        if value is None:
            return ''
        # Formata a data no padrão ISO esperado pelo input type=date
        return value.strftime('%Y-%m-%d')
