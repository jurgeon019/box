from rest_framework import serializers 
from ..models import * 


class ParentCommentSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = []
        model = PostComment


class CommentSerializer(serializers.ModelSerializer):
    parent = ParentCommentSerializer()
    class Meta:
        exclude = []
        model = PostComment


class PostSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    comments = CommentSerializer(many=True)
    # image = serializers.ReadOnlyField()
    views_count = serializers.ReadOnlyField()
    my_absolute_url = serializers.SerializerMethodField() # define a SerializerMethodField        

    def get_my_absolute_url(self, obj):
        return obj.get_absolute_url() # return the absolute url of the object

    class Meta:
        exclude = [

        ]
        model = Post
    


