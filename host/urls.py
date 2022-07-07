from django.urls import path

from host.views import MessageView, NOKView, OKView, SendMessageInterface, RegisterInterface, UnregisterInterface

urlpatterns = [
    path('ok', OKView.as_view(), name='ok'),
    path('nok', NOKView.as_view(), name='nok'),
    path('message', MessageView.as_view(), name='message'),

    # Interfaces
    path('send_message', SendMessageInterface.as_view(), name='message_interface'),
    path('register', RegisterInterface.as_view(), name='register_interface'),
    path('unregister', UnregisterInterface.as_view(), name='unregister_interface')
]