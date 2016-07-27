from flask.views import View
from flask.templating import render_template



class BaseView(View):

    def get_template_name(self):
        raise NotImplementedError()

    def render_template(self, context):
        return render_template(self.get_template_name(), **context)


class ListView(BaseView):

    def get_objects(self):
# TODO: get list from models
        pass

    # def get_template_name(self):
    #     raise NotImplementedError()

    # def render_template(self, context):
    #     return render_template(self.get_template_name(), **context)

    def dispatch_request(self):
        context = {'objects': self.get_objects()}

        return self.render_template(context)


class FormView(BaseView):


    pass