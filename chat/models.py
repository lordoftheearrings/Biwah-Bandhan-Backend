import uuid
from django.db import models
from biwah.models import UserDatabase

# MatchRequest Model
class MatchRequest(models.Model):
    sender = models.ForeignKey(UserDatabase, related_name="sent_requests", on_delete=models.CASCADE)
    receiver = models.ForeignKey(UserDatabase, related_name="received_requests", on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)  # Whether the match request is accepted or not
    sent_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)  # Only filled when accepted

    def __str__(self):
        return f"{self.sender.username} to {self.receiver.username} - Accepted: {self.is_accepted}"


# ChatRoom Model
class ChatRoom(models.Model):
    user_1 = models.ForeignKey(UserDatabase, related_name='chat_user_1', on_delete=models.CASCADE)
    user_2 = models.ForeignKey(UserDatabase, related_name='chat_user_2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    room_name = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # UUID for unique chat room name

    # Ensure that the chat room is created only if the match request is accepted
    def save(self, *args, **kwargs):
        # Check if the match request is accepted between these two users
        match_request = MatchRequest.objects.filter(
            sender=self.user_1,
            receiver=self.user_2,
            is_accepted=True
        ).first()
        
        # If the match request is accepted, allow the chat room to be created
        if not match_request:
            raise ValueError("Chat room cannot be created until the match request is accepted.")
        
        super(ChatRoom, self).save(*args, **kwargs)

    def __str__(self):
        return f"Chat between {self.user_1.username} and {self.user_2.username} (Room ID: {self.room_name})"


# Message Model
class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(UserDatabase, related_name='messages_sent', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"


# Call Model (Optional)
class Call(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    caller = models.ForeignKey(UserDatabase, related_name='caller', on_delete=models.CASCADE)
    receiver = models.ForeignKey(UserDatabase, related_name='receiver', on_delete=models.CASCADE)
    call_start = models.DateTimeField(auto_now_add=True)
    call_end = models.DateTimeField(null=True, blank=True)
    status = models.CharField(choices=[('Ongoing', 'Ongoing'), ('Completed', 'Completed')], default='Ongoing', max_length=10)

    def __str__(self):
        return f"Call from {self.caller.username} to {self.receiver.username} - Status: {self.status}"


# Notification Model
class Notification(models.Model):
    user = models.ForeignKey(UserDatabase, related_name='notifications', on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)  # Mark if the notification is read
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - Read: {self.is_read}"
