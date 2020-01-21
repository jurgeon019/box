from rest_framework import serializers 
from box.blog.models import * 


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
    class Meta:
        exclude = []
        model = Post
    

