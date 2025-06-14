from rest_framework import serializers
from comments.models import Comment
from accounts.api.serializers import SimpleAccountSerializer

class ProjectCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user_id', 'project_id', 'comment', 'created_date']


class CommentReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user_id', 'project_id', 'parent_id', 'comment', 'created_date']

class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    user = SimpleAccountSerializer(source='user_id', read_only=True) 

    class Meta:
        model = Comment
        fields = ['id', 'user_id', 'project_id', 'parent_id', 'comment', 'created_date', 'replies','user']

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []