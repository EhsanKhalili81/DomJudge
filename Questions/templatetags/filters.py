from django import template
import jdatetime

register = template.Library()


@register.filter
def to_jalali(gregorian_date):
    # Convert the date using jdatetime
    return jdatetime.datetime.fromgregorian(datetime=gregorian_date).strftime('%Y/%m/%d')
