from rest_framework import serializers


class VideoUrlValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = dict(value).get(self.field)
        if tmp_val is None:
            return
        elif 'youtube.com' not in tmp_val:
            raise serializers.ValidationError(f"{self.field} поле может содержать только ссылку на youtube.com.")

