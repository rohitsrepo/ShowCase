import datetime
from haystack import indexes
from .models import Composition


class CompositionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    uploader = indexes.CharField(model_attr='uploader')
    pub_date = indexes.DateTimeField(model_attr='created')

    def get_model(self):
        return Composition

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()