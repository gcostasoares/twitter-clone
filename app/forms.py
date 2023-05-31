# Django oferece a ferramenta forms.py para fazer formularios

from django import forms
from .models import Tweet

MAX_TWEET_LENGTH = 280 # o máximo de caracteres do tweet

# importar o modelo do conteúdo 
class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']
    
    # funcao que valida o conteúdo do texto escrito no formuário
    def clean_content(self):
        # o comando self.cleaned_data "pega" o conteúdo e salva em uma variável que será submetida à validacao
        content = self.cleaned_data.get("content")
        if len(content) > MAX_TWEET_LENGTH: # caso seja grande demais, o tweet nao é validado
            raise forms.ValidationError("Your tweet has more than 280 characteres")
        return content