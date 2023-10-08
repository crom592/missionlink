from django.contrib.auth.models import User
from django.db import models

class Task(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name='직무 코드')  # 고유한 직무 코드
    name = models.CharField(max_length=255, verbose_name='직무 이름')

    def __str__(self):
        return self.name
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=12, choices=[('short_term', '단기 선교사'), ('long_term', '일반 선교사')], verbose_name='유형')
    introduction = models.TextField(verbose_name='소개')
    tasks = models.ManyToManyField(Task, verbose_name='할 수 있는 일')
    availability = models.DateField(verbose_name='가능 기간')
    personality = models.CharField(max_length=255, verbose_name='성격')
    experience = models.TextField(verbose_name='경험')
    education = models.TextField(null=True, blank=True, verbose_name='교육')

class JobPosting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=12, choices=[('seeking', '단기 선교 가고 싶어요'), ('offering', '단기 선교사 찾아요')], verbose_name='유형')
    description = models.TextField(verbose_name='설명')
    # 다른 필드들을 여기에 추가 가능
    
class ChatRoom(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_user2')

class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name='메시지 내용')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='보낸 시간')

