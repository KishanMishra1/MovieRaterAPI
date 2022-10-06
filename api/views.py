from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.decorators import action
from .models import Movie,Rating
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from .serializers import MovieSerializer,RatingSerializer,UserSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class MovieViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    '''@action(detail=True,methods=['POST'])
    def rate_movie(self,request,pk=None):
        response={'message':'ITS WORKING !'}
        return Response(response,status=status.HTTP_200_OK)'''

    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        if 'stars' in request.data:
            movie=Movie.objects.get(id=pk)
            star=request.data['stars']
            user=request.user


            try:
                rating=Rating.objects.get(user=user.id,movie=movie.id)
                rating.stars=star
                rating.save()
                serializer=RatingSerializer(rating,many=False)
                response = {'message': 'Rating Updated !','result':serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                rating=Rating.objects.create(user=user, movie=movie,stars=star)
                serializer = RatingSerializer(rating, many=False)
                response = {'message': 'Rating Created !', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)


        else:
            response={'message':'YOU NEED TO PROVIDE STARS !'}
            return Response(response,status=status.HTTP_400_BAD_REQUEST)



class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        response = {'message': 'YOU CANT UPDATE RATING LIKE THAT !'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = {'message': 'YOU CANT CREATE RATING LIKE THAT !'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)