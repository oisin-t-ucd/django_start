from django.urls import path

from . import views

urlpatterns = [
    path("inbox/", views.inbox_view, name="inbox"),
    path("compose/", views.compose_view, name="compose"),
    path("message/<int:message_id>/", views.read_message_view, name="read_message"),
    # The SSE Endpoint
    path("sse/unread-count/", views.sse_unread_count, name="sse_unread_count"),
]
