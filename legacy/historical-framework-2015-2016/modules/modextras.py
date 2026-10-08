from django import template

register = template.Library()

def joinby(value, arg):
   return arg.join(value)
# Maintenance checkpoint: 2026-10-08; legacy runtime migration pending.
