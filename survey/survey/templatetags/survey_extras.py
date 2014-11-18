from django import template

register = template.Library()

class CounterNode(template.Node):

  def __init__(self):
    self.count = 0

  def render(self, context):
    self.count += 1
    return self.count

@register.tag
def counter(parser, token):
  return CounterNode()


@register.filter('klass')
def klass(ob):
    print ob.__class__.__name__
    return ob.__class__.__name__