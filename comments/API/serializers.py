from rest_framework import serializers
from comments.models import Comment

class ProjectCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user_id', 'project_id', 'comment', 'created_date']


class CommentReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user_id', 'project_id', 'parent_id', 'comment', 'created_date']
