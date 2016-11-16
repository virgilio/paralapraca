from rest_framework import serializers
from paralapraca.models import AnswerNotification
from discussion.serializers import BaseTopicSerializer, BaseCommentSerializer, TopicLikeSerializer, CommentLikeSerializer


class AnswerNotificationSerializer(serializers.ModelSerializer):

    topic = BaseTopicSerializer(read_only=True)
    comment = BaseCommentSerializer(read_only=True)
    topic_like = TopicLikeSerializer(read_only=True)
    comment_like = CommentLikeSerializer(read_only=True)
    activity_url = serializers.SerializerMethodField()
    course_name = serializers.SerializerMethodField()
    course_slug = serializers.SerializerMethodField()

    class Meta:
        model = AnswerNotification
        depth = 1

    def get_activity_url(self, obj):
        course_slug = obj.activity.unit.lesson.course.slug
        lesson_slug = obj.activity.unit.lesson.slug
        unit_num = obj.activity.unit.position + 1
        activity_url = "/course/{}/lesson/{}/#/{}".format(course_slug, lesson_slug, unit_num)
        return activity_url

    def get_course_name(self, obj):
        return obj.activity.unit.lesson.course.name

    def get_course_slug(self, obj):
        return obj.activity.unit.lesson.course.slug
