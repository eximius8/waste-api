from rest_framework import serializers
from litsource.models import LiteratureSource


class LitSourceSerializer(serializers.ModelSerializer):

    class Meta:

        model = LiteratureSource        
        fields =  ('id', 'name', 'source_type', 'latexpart', 'human_name', 'source_url', )