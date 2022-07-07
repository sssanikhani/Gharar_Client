import random
import sys
import threading
import time

import redis

import requests
from rest_framework.response import Response
from rest_framework.views import APIView

from host.service import get_message
from host.utils import send_presence


class RegisterInterface(APIView):
    def post(self, request):
        nonce = 0
        username = request.data.get('username')
        redis_cli = redis.Redis()
        redis_cli.set(f"gharar_username_{sys.argv[-1]}", username)
        res = requests.post(f'http://localhost:8080/register?nonce={nonce}', data={'username': username, 'port': sys.argv[-1]})
        return Response(res.content, status=res.status_code)


class UnregisterInterface(APIView):
    def post(self, request):
        username = request.data.get('username')
        nonce = request.GET.get('nonce')
        res = requests.post(f'http://localhost:8080/unregister?nonce={nonce}', data={'username': username, 'port': sys.argv[-1]})
        return Response(res.content, status=res.status_code)


class SendMessageInterface(APIView):
    def post(self, request):
        username = request.data.get('username'),
        to = request.data.get('to')
        message = request.data.get('message')
        nonce = request.GET.get('nonce')
        res = requests.post(
            f'http://localhost:8080/message?nonce={nonce}',
            data={'username': username, 'port': sys.argv[-1], 'to': to, 'message': message}
        )
        return Response(res.content, status=res.status_code)


class OKView(APIView):
    def post(self, request):
        nonce = request.GET.get('nonce')
        print(f"OK from server. nonce: {request.GET.get('nonce')}")
        if nonce == '0':
            th = threading.Thread(target=send_presence)
            th.start()
        return Response()


class NOKView(APIView):
    def post(self, request):
        print(f"NOK from server. nonce: {request.GET.get('nonce')} reason: {request.data.get('reason')}")
        return Response()


class MessageView(APIView):
    def post(self, request):
        get_message(
            request.data.get('from'),
            request.data.get('message'),
            request.GET.get('nonce')
        )
        time.sleep(20)
        return Response()
