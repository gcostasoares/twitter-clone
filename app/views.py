import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme

from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .forms import TweetForm
from .models import Tweet
from .serializers import (TweetSerializer, TweetActionSerializer, TweetCreateSerializer,
)

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.
# Primeiro View relaciona-se com a pagina inicial do projeto. Furutamente será implantado um sistema de Login na página inicial
# No momento, somente há a necessidade no usuário estar logado
def home_view(request, *args, **kwargs):
    username = None
    # Necessário a autentificacao no usuário. No momento, somente é possível logar através da página de administracao
    # No futuro, será implatada uma página onde o cliente poderá fazer login
    if request.user.is_authenticated:
        username = request.user.username
    # Rendererizacao da páginca home com Status 200
    return render(request, "pages/home.html", context={"username": username}, status=200)

# Este view busca o API gerado pelo formulário da mensagem do formulário preenchido na página incial
@api_view(['POST']) 
@permission_classes([IsAuthenticated])
# Uso do Django Rest Framework. O código estava muito grande e confuso.
# Com o uso do framework, basta identificar o tipo de de informacao que está sendo absorvida do formulário
# No caso, o formulário é do tipo POST, e só pode ser executada a acao se o usuário estiver logado
def tweet_create_view(request, *args, **kwargs):
    serializer = TweetCreateSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    # Caso o usuário nao esteja logado, o Status 400 é usado para indicar um erro
    return Response({}, status=400)

# Um outro API do tipo GET, para buscar as informacoes geradas pelos formulários
@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    # Salva-se a mensagem filtrada em uma variável qs
    qs = Tweet.objects.filter(id=tweet_id)
    # Caso o filtro nao exista, o Status 404 de erro é enviada ao cliente
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data, status=200)

# Uma terceira view para deletar os Tweets
@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    # repete-se o mesmo processo de filtragem do tweet, mas agora buscango os tweet do usuário requerido
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message": ""}, status=401)
    obj = qs.first()
    # Com ajuda do comando delete do Django, pode-se salvat o tweet filtrado em uma variável e exclui-lo
    obj.delete()
    return Response({"message": "Tweet has been removed"}, status=200)

# Esta View ainda está em desenvolvimento. Deverá ser dedicada a um sistema de Likes e Dislikes
#!!!
#!!!
#!!!

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request, *args, **kwargs):
    serializer = TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get("id")
        action = data.get("action")
        content = data.get("content")
        qs = Tweet.objects.filter(id=tweet_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action == "like":
            obj.likes.add(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "unlike":
            obj.likes.remove(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "retweet":
            new_tweet = Tweet.objects.create(
                    user=request.user, 
                    parent=obj,
                    content=content,
                    )
            serializer = TweetSerializer(new_tweet)
            return Response(serializer.data, status=201)
    return Response({}, status=200)


# Esta View é dedicada a buscar todas mesagens existentes. Nota-se que ao invés de
# usar o método filter como das views anteriores, Django oferece também o método all
@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    serializer = TweetSerializer(qs, many=True)
    return Response(serializer.data, status=200)

