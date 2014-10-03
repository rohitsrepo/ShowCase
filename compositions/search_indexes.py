import datetime
from haystack import indexes
from .models import Composition

class CompositionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    description = indexes.CharField(model_attr='description')
    painter = indexes.CharField(model_attr='painter')
    tags = indexes.MultiValueField()
    created = indexes.DateTimeField(model_attr='created')
    # We add this for autocomplete.
    content_auto = indexes.EdgeNgramField(model_attr='content')    

    def prepare_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]    

    def get_model(self):
        return Composition
    
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(created__lte=datetime.datetime.now())