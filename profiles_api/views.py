#from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status #list of HTTP status code, like 200, 400, 404 ect
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
#from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated

from profiles_api import serializers #What data to expect when making post put and patch request
from profiles_api import models
from profiles_api import permissions

# Create your views here.
class HelloApiView(APIView):
    """Test API View"""
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Return a list of APIView features """
        an_apiview = [
                'Uses HTTP methods as function(get, post, put, delete, patch)',
                'It is similar to a traditional Django View',
                'Gives you the most control over your application logic',
                'It is mapped manually ti URLs'
                ]
        return Response({
            'message':'Hello!',
            'an_apiview': an_apiview
            })

    def post(self, request):
        """Create a hello message with a name"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message':message})
        else:
            return Response(
                    serializer.errors,
                    status = status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Handle updating an object"""
        return Response({'method':'PUT'})

    def patch(self, request, pk=None):
        """Handle a partial update of an object"""
        return Response({'method':'PATCH'})

    def delete(self, request, pk=None):
        """Delete an object"""
        return Response({'method':'DELETE'})


class HelloViewSet(viewsets.ViewSet):
    """Test API Viewset"""
    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """Return a hello message"""
        a_viewset = [
            'Uses action (list, create, retrieve, update, partial_update, destory)',
            'Automatically maps to URLs using Routers',
            'Provides more funcionality with less code',
        ]
        return Response({'message': 'Hello!', 'a_viewset': a_viewset})

    def create(self, request):
        """Create a hello message with a name"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message':message})
        else:
            return Response(
                    serializer.errors,
                    status = status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Retrieve an specific object by its ID"""
        return Response({'message': "Retrieved Data HTTP_method 'GET'"})

    def update(self, request, pk=None):
        """Update an object"""
        return Response({'message': "Updated HTTP_method 'PUT'"})

    def partial_update(self, request, pk=None):
        """Partially Update an object"""
        return Response({'message': "Partially Updated Updated HTTP_method 'PATCH'"})

    def destroy(self, request, pk=None):
        """Delete an object"""
        return Response({'message': "Deleted HTTP_Method 'DELETE'"})

class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating, creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()

    #Add authentication and permissions for updating user profile
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)

    #Search feature with filters
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()

    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)
    """
    permission_classes = (
            permissions.UpdateOwnStatus,
            IsAuthenticatedOrReadOnly
        )
    """

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)
