from django import template

register = template.Library()


@register.simple_tag
def get_object_field_name_verbose(object, fieldnm):
    return object._meta.get_field(fieldnm).verbose_name


@register.filter
def is_string(val):
    try:
        float(val)
    except ValueError:
        return isinstance(val, str)


@register.simple_tag
def get_object_value_name_verbose(object, valuenm):
    get_foo_display = getattr(object, f"get_{valuenm}_display")
    return get_foo_display()
