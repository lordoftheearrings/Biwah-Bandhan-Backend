from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import MatchRequest, ChatRoom, Notification, Message
from biwah.models import UserDatabase

class SendMatchRequestView(APIView):
    """
    Handles sending a match request from one user to another using username as a lookup.
    """
    def post(self, request):
        sender_username = request.data.get('sender_username')  # Get sender username from request data
        receiver_username = request.data.get('receiver_username')  # Get receiver username from request data
        print(sender_username)  
        print(receiver_username)
        # Check if both sender and receiver usernames are provided
        if not sender_username or not receiver_username:
            return Response({"error": "Both sender_username and receiver_username are required."}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        try:
            sender = UserDatabase.objects.get(username=sender_username)
            receiver = UserDatabase.objects.get(username=receiver_username)
        except UserDatabase.DoesNotExist:
            return Response({"error": "Invalid username(s)."}, status=status.HTTP_404_NOT_FOUND)
        
             # Check if a match request already exists and is accepted
        if MatchRequest.objects.filter(sender=sender, receiver=receiver, is_accepted=True).exists():
            return Response({"message": "Match request already accepted."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a match request already exists and is pending
        if MatchRequest.objects.filter(sender=sender, receiver=receiver, is_accepted=False).exists():
            return Response({"message": "Match request already sent."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new match request
        MatchRequest.objects.create(sender=sender, receiver=receiver)

        # Notify the receiver
        Notification.objects.create(
            user=receiver,
            message=f"{sender.username} has sent you a match request."
        )

        return Response({"message": "Match request sent successfully."}, status=status.HTTP_201_CREATED)

class CancelMatchRequestView(APIView):
    """
    Handles canceling a match request using sender_username and receiver_username as lookups.
    """
    def post(self, request):
        sender_username = request.data.get('sender_username')  # Get sender username from request data
        receiver_username = request.data.get('receiver_username')  # Get receiver username from request data
        print(sender_username)
        print(receiver_username)

        # Check if both sender and receiver usernames are provided
        if not sender_username or not receiver_username:
            return Response({"error": "Both sender_username and receiver_username are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            sender = UserDatabase.objects.get(username=sender_username)
            receiver = UserDatabase.objects.get(username=receiver_username)
        except UserDatabase.DoesNotExist:
            return Response({"error": "Invalid username(s)."}, status=status.HTTP_404_NOT_FOUND)

        # Check if a match request exists
        try:
            match_request = MatchRequest.objects.get(sender=sender, receiver=receiver)
        except MatchRequest.DoesNotExist:
            return Response({"error": "Match request not found."}, status=status.HTTP_404_NOT_FOUND)

        # Delete the match request
        match_request.delete()

        # Notify the sender and receiver
        Notification.objects.create(
            user=sender,
            message=f"Your match request to {receiver.username} has been canceled."
        )
        Notification.objects.create(
            user=receiver,
            message=f"{sender.username} has canceled the match request."
        )

        return Response({"message": "Match request canceled successfully."}, status=status.HTTP_200_OK)

class AcceptMatchRequestView(APIView):
    """
    Handles accepting a match request by sender and receiver usernames.
    """
    def post(self, request):
        sender_username = request.data.get('sender')
        receiver_username = request.data.get('receiver')

        try:
            sender = UserDatabase.objects.get(username=sender_username)
            receiver = UserDatabase.objects.get(username=receiver_username)
        except UserDatabase.DoesNotExist:
            return Response({"error": "Sender or receiver not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            match_request = MatchRequest.objects.get(sender=sender, receiver=receiver, is_accepted=False)
        except MatchRequest.DoesNotExist:
            return Response({"error": "Match request not found or already accepted."}, status=status.HTTP_404_NOT_FOUND)

        # Accept the match request
        match_request.is_accepted = True
        match_request.accepted_at = timezone.now()
        match_request.save()

        # Create a chat room
        ChatRoom.objects.create(user_1=sender, user_2=receiver)

        # Notify both users
        Notification.objects.create(
            user=sender,
            message=f"{receiver.username} has accepted your match request!"
        )
        Notification.objects.create(
            user=receiver,
            message="You have successfully accepted the match request."
        )

        return Response({"message": "Match request accepted successfully."}, status=status.HTTP_200_OK)


class DeclineMatchRequestView(APIView):
    """
    Handles declining a match request by sender and receiver usernames.
    """
    def post(self, request):
        sender_username = request.data.get('sender')
        receiver_username = request.data.get('receiver')

        try:
            sender = UserDatabase.objects.get(username=sender_username)
            receiver = UserDatabase.objects.get(username=receiver_username)
        except UserDatabase.DoesNotExist:
            return Response({"error": "Sender or receiver not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            match_request = MatchRequest.objects.get(sender=sender, receiver=receiver, is_accepted=False)
        except MatchRequest.DoesNotExist:
            return Response({"error": "Match request not found or already accepted."}, status=status.HTTP_404_NOT_FOUND)

        # Delete the match request
        match_request.delete()

        # Notify the sender
        Notification.objects.create(
            user=sender,
            message=f"{receiver.username} has declined your match request."
        )

        return Response({"message": "Match request declined successfully."}, status=status.HTTP_200_OK)


class MatchRequestsView(APIView):
    """
    Lists all match requests for the current user, including received, sent, pending, and current matches.
    """
    def get(self, request):
        username = request.query_params.get('username')

        if not username:
            return Response({"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserDatabase.objects.get(username=username)
        except UserDatabase.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Received match requests (pending)
        received_requests = MatchRequest.objects.filter(receiver=user, is_accepted=False)

        # Sent match requests (pending)
        sent_requests = MatchRequest.objects.filter(sender=user, is_accepted=False)

        # Current matches (accepted)
        current_matches = MatchRequest.objects.filter(
            (Q(sender=user) | Q(receiver=user)),
            is_accepted=True
        )

        data = {
            "received_requests": [
                {"id": r.id, "sender": r.sender.username, "sent_at": r.sent_at, "receiver":r.receiver.username}
                for r in received_requests
            ],
            "sent_requests": [
                {"id": r.id, "receiver": r.receiver.username, "is_accepted": r.is_accepted, "sent_at": r.sent_at}
                for r in sent_requests
            ],
            "current_matches": [
                {"id": r.id, "partner": r.receiver.username if r.sender == user else r.sender.username, "sent_at": r.sent_at}
                for r in current_matches
            ],
        }

        return Response(data, status=status.HTTP_200_OK)
    

class CreateChatRoomView(APIView):
    """
    Handles creating a chat room between two users if the match request is accepted.
    """
    def post(self, request):
        user_1_username = request.data.get('user_1_username')
        user_2_username = request.data.get('user_2_username')

        if not user_1_username or not user_2_username:
            return Response({"error": "Both user_1_username and user_2_username are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user_1 = UserDatabase.objects.get(username=user_1_username)
            user_2 = UserDatabase.objects.get(username=user_2_username)
        except UserDatabase.DoesNotExist:
            return Response({"error": "Invalid username(s)."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the match request is accepted
        if not MatchRequest.objects.filter(
            sender=user_1,
            receiver=user_2,
            is_accepted=True
        ).exists() and not MatchRequest.objects.filter(
            sender=user_2,
            receiver=user_1,
            is_accepted=True
        ).exists():
            return Response({"error": "Match request is not accepted."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the chat room
        chat_room = ChatRoom.objects.create(user_1=user_1, user_2=user_2)
        return Response({
            "room_name": chat_room.room_name,
            "created_at": chat_room.created_at
        }, status=status.HTTP_201_CREATED)
    

class FetchChatRoomsView(APIView):
    """
    Handles fetching chat rooms for a user.
    """
    def get(self, request):
        username = request.query_params.get('username')
        
        if not username:
            return Response({"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserDatabase.objects.get(username=username)
        except UserDatabase.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        chat_rooms = ChatRoom.objects.filter(user_1=user) | ChatRoom.objects.filter(user_2=user)
        chat_rooms_data = [
            {
                "room_name": chat_room.room_name,
                "partner": chat_room.user_2.username if chat_room.user_1 == user else chat_room.user_1.username,
                "created_at": chat_room.created_at
            }
            for chat_room in chat_rooms
        ]

        return Response(chat_rooms_data, status=status.HTTP_200_OK) 

'''    
class SendMessageView(APIView):
    """
    Handles sending a message in a chat room.
    """
    def post(self, request):
        room_name = request.data.get('room_name')
        sender_username = request.data.get('sender_username')
        content = request.data.get('content')

        if not room_name or not sender_username or not content: 
            return Response({"error": "room_name, sender_username, and content are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            chat_room = ChatRoom.objects.get(room_name=room_name)
            sender = UserDatabase.objects.get(username=sender_username)
        except (ChatRoom.DoesNotExist, UserDatabase.DoesNotExist):
            return Response({"error": "Invalid room_name or sender_username."}, status=status.HTTP_404_NOT_FOUND)

        # Create the message
        message = Message.objects.create(chat_room=chat_room, sender=sender, content=content)
        return Response({
            "sender": message.sender.username,
            "content": message.content,
            "timestamp": message.timestamp
        }, status=status.HTTP_201_CREATED)
    
'''

class GetMessagesView(APIView):
    """
    Handles retrieving messages from a chat room.
    """
    def get(self, request):
        room_name = request.query_params.get('room_name')

        if not room_name:
            return Response({"error": "room_name is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            chat_room = ChatRoom.objects.get(room_name=room_name)
        except ChatRoom.DoesNotExist:
            return Response({"error": "Invalid room_name."}, status=status.HTTP_404_NOT_FOUND)

        messages = Message.objects.filter(chat_room=chat_room).order_by('timestamp')
        messages_data = [
            {
                "sender": message.sender.username,
                "content": message.content,
                "timestamp": message.timestamp
            }
            for message in messages
        ]
        return Response({"messages_data": messages_data}, status=status.HTTP_200_OK)