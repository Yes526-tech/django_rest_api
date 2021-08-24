from rest_framework import serializers

#todları transfer etmek için yeni bir serializer oluşturlcak

class TodoSerializer(serializers.Serializer):
    """todo serializer"""

    id = serializers.IntegerField()
    text = serializers.CharField()
    created_at = serializers.CharField()
    is_complete = serializers.BooleanField()


