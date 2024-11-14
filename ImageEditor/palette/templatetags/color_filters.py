# palette/templatetags/color_filters.py
from django import template

register = template.Library()

@register.filter
def rgb_to_hex(color):
    """Convert an RGB tuple to a hex color string."""
    return "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])
