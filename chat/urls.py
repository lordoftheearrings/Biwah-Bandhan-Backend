from django.urls import path
from .views import (
    SendMatchRequestView,
    CancelMatchRequestView,
    AcceptMatchRequestView, 
    DeclineMatchRequestView,
    MatchRequestsView,
    CreateChatRoomView,
    FetchChatRoomsView,
    #SendMessageView,
    GetMessagesView,
)

urlpatterns = [
    path('send_match_request/', SendMatchRequestView.as_view(), name='send_match_request'),
    path('cancel_match_request/', CancelMatchRequestView.as_view(), name='send_match_request'),
    path('accept_match_request/', AcceptMatchRequestView.as_view(), name='accept_match_request'),
    path('decline_match_request/', DeclineMatchRequestView.as_view(), name='decline_match_request'),
    path('list_match_requests/', MatchRequestsView.as_view(), name='list_match_requests'),
    path('create-chat-room/', CreateChatRoomView.as_view(), name='create-chat-room'),
    path('fetch-chat-rooms/', FetchChatRoomsView.as_view(), name='fetch-chat-rooms'),
    #path('send-message/', SendMessageView.as_view(), name='send-message'),
    path('get-messages/', GetMessagesView.as_view(), name='get-messages'),
    
]
