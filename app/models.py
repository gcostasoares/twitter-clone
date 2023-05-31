import random
from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

# Esse modelo está em desenvolvimento e será dedicado a buscar as informacoes de Likes e Deslikes
class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

# Este modelo é dedicado a gerar informacoes para o serializer, buscado os campos que serao
# Usados como informacao para o banco de dados. 
class Tweet(models.Model):
    # campo do Tweet 'pai'
    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
    # campo que registra o usuário. Caso deletado, o modo casacada é acionado para apagar todas as informacoes relacionadas ao usuário
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # em desenvolvimento
    likes = models.ManyToManyField(User, related_name='tweet_user', blank=True, through=TweetLike)
    # o campo de conteudo, usando um TextField para buscar o string digitado
    content = models.TextField(blank=True, null=True)
    # campos em desenvolvimento
    image = models.FileField(upload_to='images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    # a classe meta primeiramente organizando os IDs dos tweets de forma decrescente
    class Meta:
        ordering = ['-id']
    
    # esta tag gerencia a tweets pais
    @property
    def is_retweet(self):
        return self.parent != None
   