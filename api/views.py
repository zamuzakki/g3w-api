from core.api.base.views import G3WAPIView, Response
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import APIException

from core.models import Group as ProjectGroup
from qps_timeseries.models import QpsTimeseriesProject
from .permissions import (
    GetProjectPermission,
    GetUserPermission,
    GetCreateGroupPermission
)


class QpsTimeseriesGetProjectApiView(G3WAPIView):
    """
    API for get information about PS Timeseries Project
    """

    permission_classes = (
        GetProjectPermission,
    )

    def get(self, request, *args, **kwargs):
        try:
            qps_ts_project = QpsTimeseriesProject.objects.get(project__title=kwargs['project_name'])
        except ObjectDoesNotExist:
            raise APIException('QpsTimeseriesProject object not found in DB')

        results = {
            "id": qps_ts_project.id,
            "name": kwargs['project_name'],
        }

        return Response(results)


class GetUser(G3WAPIView):
    """
    API for getting user information
    """

    permission_classes = (
        GetUserPermission,
    )

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])

        result = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }

        return Response(result)


class GetOrCreateGroup(G3WAPIView):
    """
    API for getting or creating group
    """

    permission_classes = (
        GetCreateGroupPermission,
    )

    def post(self, request, *args, **kwargs):
        data = request.data
        group, _ = Group.objects.get_or_create(name=data['group_name'])

        result = {
            "id": group.id,
            "name": group.name
        }

        return Response(result)


class GetProjectGroup(G3WAPIView):
    """
    API for getting Project Group
    """

    permission_classes = (
        GetCreateGroupPermission,
    )

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(ProjectGroup, name=kwargs['group_name'])

        result = {
            "id": group.id,
            "name": group.name,
            "title": group.title,
            "slug": group.slug,
        }

        return Response(result)
