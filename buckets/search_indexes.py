import datetime
from haystack import indexes
from .models import Bucket


class BucketIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    owner = indexes.CharField(model_attr='owner')
    pub_date = indexes.DateTimeField(model_attr='created')

    def get_model(self):
        return Bucket

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()