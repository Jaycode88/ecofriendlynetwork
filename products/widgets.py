from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _


class CustomClearableFileInput(ClearableFileInput):
    """
    Custom widget for clearable file inputs, for image uploads.
    Extends Django's ClearableFileInput to customize its appearance
    and behavior.
    """

    # Label for the checkbox used to clear the file if already set.
    clear_checkbox_label = _('remove')

    # Text to display when there is an existing file (image).
    initial_text = _('Current Image')

    # Text to display for the input itself, kept blank for custom styling.
    input_text = _('')

    # Template used to render this widget. Points to a custom HTML template.
    template_name = 'products/custom_widget_templates/custom_clearable_file_input.html'
    
