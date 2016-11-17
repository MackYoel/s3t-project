from django import template

register=template.Library()

@register.filter
def is_hidden(field):
	widget = field.field.widget
	class__ = widget.__class__
	return class__.__name__ == 'HiddenInput'