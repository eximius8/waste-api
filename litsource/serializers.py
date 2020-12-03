from rest_framework import serializers
from litsource.models import LiteratureSource


class LitSourceSerializer(serializers.ModelSerializer):

    class Meta:

        model = LiteratureSource
        read_only_fields = ('human_name', 'source_url')
        fields =  ('human_name', 'source_url')