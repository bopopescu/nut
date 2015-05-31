from django.dispatch import Signal

notify = Signal(providing_args=[
    'recipient', 'actor', 'verb', 'action_object', 'target', 'description',
    'timestamp'
])

# push_notify = Signal(providing_args=[
#     'verb', 'rid', 'platform', 'content_type', 'production'
# ])

__author__ = 'edison'
