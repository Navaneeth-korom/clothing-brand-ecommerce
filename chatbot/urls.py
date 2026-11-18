from django.urls import path
from . import views
urlpatterns = [
    path("assistant", views.chat_page, name="chat_page"),
    path("api/message/", views.get_message, name="get_response")
]