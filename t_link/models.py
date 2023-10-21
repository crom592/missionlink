from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class CommonInfo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation Time')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Modification Time')

    class Meta:
        abstract = True


class Task(CommonInfo):
    code = models.CharField(max_length=50, unique=True, verbose_name='Task Code')
    name = models.CharField(max_length=255, verbose_name='Task Name')
    description = models.TextField(verbose_name='Task Description')  # 추가된 필드

    def __str__(self):
        return self.name


class Profile(CommonInfo):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=12, choices=[('short_term', 'Short Term Missionary'), ('long_term', 'General Missionary')], verbose_name='Type')
    introduction = models.TextField(verbose_name='Introduction')
    tasks = models.ManyToManyField(Task, verbose_name='Tasks')
    availability = models.DateField(verbose_name='Availability')
    personality = models.CharField(max_length=255, verbose_name='Personality')
    experience = models.TextField(verbose_name='Experience')
    education = models.TextField(null=True, blank=True, verbose_name='Education')
    matched_with = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    verified = models.BooleanField(default=False, verbose_name='Verification Status')
    language = models.CharField(max_length=50, null=True, blank=True, verbose_name='Language')


class JobPosting(CommonInfo):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, verbose_name='Type')  # Type 길이를 확장
    title = models.CharField(max_length=255, verbose_name='Title')  # 새로운 필드
    description = models.TextField(verbose_name='Description')
    country = models.CharField(max_length=255, verbose_name='Country')
    language = models.CharField(max_length=50, verbose_name='Language')  # 새로운 필드
    tasks = models.ManyToManyField(Task, verbose_name='Tasks')
    start_date = models.DateField(null=True, blank=True, verbose_name='Start Date')
    end_date = models.DateField(null=True, blank=True, verbose_name='End Date')
    status = models.CharField(max_length=20, choices=[('open', 'Open'), ('closed', 'Closed')], default='open', verbose_name='Status')
    image = models.URLField(null=True, blank=True, verbose_name='Image URL')  # 새로운 필드
    latitude = models.FloatField(null=True, blank=True, verbose_name='Latitude')  # 새로운 필드
    longitude = models.FloatField(null=True, blank=True, verbose_name='Longitude')  # 새로운 필드
    zoom = models.IntegerField(null=True, blank=True, verbose_name='Zoom Level')  # 새로운 필드


class Match(CommonInfo):
    missionary = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="missionary_matches")
    short_term_missionary = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="short_term_matches")
    matched_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('in_progress', 'In Progress'), ('completed', 'Completed')], default='in_progress', verbose_name='Status')

    def __str__(self):
        return f"{self.missionary.user.username} matched with {self.short_term_missionary.user.username}"


class ChatRoom(CommonInfo):
    participants = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)
    last_message = models.DateTimeField(default=timezone.now)


class Message(CommonInfo):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name='Message Content')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Sent Time')
    is_read = models.BooleanField(default=False, verbose_name='읽음 여부')