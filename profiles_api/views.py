from django.http import JsonResponse, HttpResponse, QueryDict
from django.views.generic import CreateView
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings
from profiles_api import serializers, models
from rest_framework.response import Response
from rest_framework import status, viewsets

import text2emotion as te

from rest_framework.views import APIView

from rest_framework.decorators import authentication_classes, permission_classes

from profiles_api.models import TodayNote
from profiles_api.serializers import TodayNoteSerializer
from django.utils.timezone import datetime


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class NoteListForUser(APIView):
    serializer_class = serializers.TodayNoteSerializer
    permission_classes = (
        IsAuthenticated,
    )
    authentications_classes = (TokenAuthentication,)

    def get(self, request):
        queryset = models.TodayNote.objects.all().filter(user_profile=self.request.user)
        data = list(queryset.values())
        if len(data) > 0:
            return Response({'data': data}, status.HTTP_200_OK)
        return Response({'data': 'No etries'}, status.HTTP_404_NOT_FOUND)


class CreateNoteForDay(APIView):
    """Create a note for the particular day with specific user id"""

    serializer_class = serializers.TodayNoteSerializer
    permission_classes = (
        IsAuthenticated,
    )
    authentications_classes = (TokenAuthentication,)

    def get(self, request):
        date = datetime.today().strftime('%Y-%m-%d')
        default_val = date
        date = request.GET.get('date', default_val)
        try:

            queryset = models.TodayNote.objects.get(user_profile=self.request.user, created_on=date)
            serializer = self.serializer_class(queryset)
            print(serializer.data)
            return Response({'message': serializer.data}, status.HTTP_200_OK)
        except:
            return Response({'message': 'Not created yet'}, status.HTTP_404_NOT_FOUND)

    def post(self, request):
        """Creates or update a new note with userid"""
        default_val = datetime.today().strftime('%Y-%m-%d')
        date = request.data.get('date', default_val)
        data = QueryDict.dict(self.request.data)
        try:
            note = models.TodayNote.objects.get(user_profile=self.request.user,
                                                created_on=date)
            serializer = self.serializer_class(data=note)
            note.written_data = data.get('written_data')
            emotions_data = te.get_emotion(note.written_data)
            print(emotions_data)
            note.save()
            return Response({'message': 'Updated successfully', 'emotions': emotions_data}, status.HTTP_200_OK)
        except Exception:
            emotions_data = te.get_emotion(data.get('written_data'))
            print(emotions_data)
            serializer = self.serializer_class(data={'user_profile': self.request.user.id,
                                                     'written_data': data.get('written_data'),
                                                     'created_on': date,
                                                     'emotions': str(emotions_data)})
            if serializer.is_valid():
                serializer.save(user_profile=self.request.user)
                return Response({'message': serializer.data, 'emotions': emotions_data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([])
@authentication_classes([])
class CreateUserProfile(APIView):
    serializer_class = serializers.UserProfileSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': serializer.data}, status.HTTP_201_CREATED)
        return Response({'message': serializer.errors}, status.HTTP_400_BAD_REQUEST)
