from django.conf import settings
from rest_framework import serializers
from .models import Tweet

#Seleciona-se no Settings a quantidade de caracteres que o formulário deverá ter.
# Foi salvo no varárvel MAX_TWEET_LENGTH com 280 caracteres, como o Twitter original
MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH

#Este Serializer ainda está em desenvolvimento. É voltado para os botos de Likes e Deslikes
TWEET_ACTION_OPTIONS = settings.TWEET_ACTION_OPTIONS

class TweetActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)

    def validate_action(self, value):
        value = value.lower().strip() # "Like " -> "like"
        if not value in TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not a valid action for tweets")
        return value


# Este Serializer está dedicado *as informacöes do firmulário
class TweetCreateSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    
    # A primeira classe é sempre Meta. Ira absorver as informacoes do Modelo Tweet
    # Nos campos Id, Content e Likes
    class Meta:
        model = Tweet
        fields = ['id', 'content', 'likes']
    
    def get_likes(self, obj):
        return obj.likes.count()
    
    # condicao para que o Twitter nao tenha mais que 280 caracteres
    def validate_content(self, value):
        if len(value) > MAX_TWEET_LENGTH:
            raise serializers.ValidationError("Your tweet has more than 280 characteres")
        return value


# Este Serializer está voltado para o Retweet. A funcao ainda está em desenvolvimento
class TweetSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    parent = TweetCreateSerializer(read_only=True)
    class Meta:
        model = Tweet
        fields = ['id', 'content', 'likes', 'is_retweet', "parent"]

    def get_likes(self, obj):
        return obj.likes.count()