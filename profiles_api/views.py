from copy import error
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from profiles_api import serializers
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from profiles_api import models
from profiles_api import permissions

class HelloApiView(APIView):
    """Test API View"""
    serializer_class = serializers.HelloSerializer
    put_serializer_class = serializers.HelloPutSerializer
    
    products = ['tv', 'laptop', 'car']
    
    
    
    def get(self, request, pk=None, format=None):
        """Returns a list of APIView features"""
        
        an_apiview = [
            'Uses HTTP methods as function(get,post, patch,put, delete',
            'Is similar to a traditinal Django View',
            'Gives you to most control over you applğication logic',
            'Is mapped manually to URLs'
        ]
        return Response({'message': 'Hello!', 'products': self.products})
    
    def post(self, request):
        """create a hello message with our name"""
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            email = serializer.validated_data.get('email')
            message = f'Hello {name}'
            return Response({'message': message, 'email': email})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST 
            )
    def put(self, request, pk=None):
        """Handle updating an object"""
        put_serializer = self.put_serializer_class(data=request.data)
        if put_serializer.is_valid():
            product = put_serializer.validated_data.get('product')
            self.products = self.products.append(product)
            
            return Response({'new_product': product})
        else:
            return Response(
                put_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST 
            )
        
    def patch(self, request, pk=None):
        """Handle a partial update of an object"""  
        return Response({'method': 'PATCH'})
    def delete(self, request, pk=None):
        deleted_products = self.products.pop(pk)
        products = self.products
        
        """Delete an object"""
        return Response({'method': 'DELETE', 'deleted_products': deleted_products, 'products': products})




class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""
    serializer_class = serializers.HelloSerializer
    def list(self, request):
        """return a helo message"""
        a_viewset= [
            'Uses actions ( list, create, retrive, update, partial_update',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code',
        ]
        return Response({'message':'Hello!', 'a_viewset': a_viewset})
    def create(self, request):
        """Create a new hello message"""
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
    def retrieve(self, request, pk=None):
        """Handle getting a object by its ID"""
        return Response({'http_method': 'GET'})
    def update(self, request, pk=None):
        """Handle updating an object"""
        return Response({'http_method': 'PUT'})
    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""
        return Response({'http_method': 'PATCH'})
    def destroy(self, request, pk=None):
        """Handle removing an object"""
        return Response({'http_method': 'DELETE'})
    
class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.UpdateOwnProfile, )






