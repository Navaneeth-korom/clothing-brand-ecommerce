from rest_framework.decorators import api_view
from .serializers import ChatMessageSerializer
from .services import generate_reply
from rest_framework.response import Response
from rest_framework import status
from .exceptions import ChatbotServiceError
from django.shortcuts import render
from django.contrib.auth.decorators import login_required



@api_view(["POST"])
def get_message(request):
    serializer = ChatMessageSerializer(data= request.data)
    if serializer.is_valid():
        message = serializer.validated_data["message"]
        try:
            reply = generate_reply(message)
            return Response({"reply": reply})
        except ChatbotServiceError as e:
            return Response({
                "error":e.message,
            }, status=e.status_code)
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )
    
@login_required
def chat_page(request):
    return render(request, "chatbot/chat.html")