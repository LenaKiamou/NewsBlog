from django import forms
from .models import Article, Category

class NewArticle(forms.ModelForm):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Title', 'class': 'form-control mb-3'}))
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder':'Body', 'class': 'form-control z-depth-1 mb-3', 'rows': 15}))
    category = forms.ModelChoiceField(
        queryset= Category.objects.all(), 
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-control mb-3'})
        )
    class Meta:
        model = Article
        fields = ['title' ,'content', 'category']

 