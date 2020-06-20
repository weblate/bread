from django.utils.html import mark_safe

from .required import *  # noqa

# custom unicode symbols
HTML_TRUE = mark_safe("&#x2714;")  # ✔
HTML_FALSE = mark_safe("&#x2716;")  # ✖
HTML_NONE = mark_safe('<div class="center">&empty;</div>')  # ∅
