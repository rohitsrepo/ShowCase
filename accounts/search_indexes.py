import datetime
from haystack import indexes
from .models import User

class UserIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    first_name = indexes.CharField(model_attr='first_name')
    last_name = indexes.CharField(model_attr='last_name')
    email = indexes.CharField(model_attr='email')
    about = indexes.CharField(model_attr='about')
    date_joined = indexes.DateTimeField(model_attr='date_joined')
    # We add this for autocomplete.
    content_auto = indexes.EdgeNgramField(model_attr='content')    

    def get_model(self):
        return User
    
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(date_joined__lte=datetime.datetime.now())