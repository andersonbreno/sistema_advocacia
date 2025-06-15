from django.forms.widgets import ClearableFileInput, DateInput
from datetime import datetime

class ImageInput(ClearableFileInput):
    template_name = "widgets/foto_widget.html"

class DatePickerInput(DateInput):
    input_type = 'date'
    
    def __init__(self, attrs=None, format=None):
        super().__init__(attrs=attrs, format=format or '%Y-%m-%d')
    
    def format_value(self, value):
        if value is None:
            return ''
            
        # Se já for um objeto date/datetime
        if hasattr(value, 'strftime'):
            return value.strftime(self.format)
            
        # Se for string, tenta converter para date
        if isinstance(value, str):
            try:
                # Tenta formatos comuns de data
                for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y'):
                    try:
                        date_obj = datetime.strptime(value, fmt).date()
                        return date_obj.strftime(self.format)
                    except ValueError:
                        continue
            except (TypeError, ValueError):
                pass
                
        return value

