from braces.views import AjaxResponseMixin, JSONRequestResponseMixin

from django.contrib.auth.forms import AuthenticationForm

from django.views.generic import FormView
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from rest_framework import permissions
from rest_framework.parsers import FileUploadParser
from rest_framework import views

from apps.core.models import GKUser
from apps.api.serializers.user import UserSerializer
from apps.api.permissions import Admin_And_Editor_Only

from django.utils.log import getLogger

log = getLogger('django')


class UserAjaxAuthView(JSONRequestResponseMixin,FormView):
    form_class = AuthenticationForm

    def form_invalid(self, form):
        self.render_json_response({'error':1}, status=401)

    def form_valid(self, form):
        user = form.get_user()
        token = Token.objects.get_or_create(user=user)
        self.render_json_response({
            'token': token,
            'username': user.nick,
        }, status=200)



class UserViewSet(viewsets.ModelViewSet):
    queryset = GKUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)



    @list_route(permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def active(self, request):
        recent_users = GKUser.objects.filter(is_active=GKUser.active)
        # recent_users = GKUser.objects.filter(is_admin=True)
        page = self.paginate_queryset(recent_users)
        serializer = self.get_pagination_serializer(page)
        return Response(serializer.data)

    @list_route(permission_classes=[Admin_And_Editor_Only])
    def writers(self,request):
        writer = GKUser.objects.filter(is_active__gte=2)
        serializer = self.get_serializer(writer, many=True)
        return Response(serializer.data)


class AvatarUpload(views.APIView):
    parser_classes = (FileUploadParser,)

    def put(self, request, filename, format=None):
        file_obj = request.data['file']
        log.info(file_obj)
        return Response(status=204)



__author__ = 'edison7500'
