import asyncio

from asgiref.sync import sync_to_async
from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ComposeMessageForm
from .models import Message

# --- STANDARD VIEWS ---


@login_required
def inbox_view(request):
    messages = Message.objects.filter(recipient=request.user, is_archived=False)
    return render(request, "user_messages/inbox.html", {"messages": messages})


@login_required
def compose_view(request):
    if request.method == "POST":
        form = ComposeMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect("inbox")
    else:
        form = ComposeMessageForm()

    return render(request, "user_messages/compose.html", {"form": form})


@login_required
def read_message_view(request, message_id):
    message = get_object_or_404(Message, id=message_id, recipient=request.user)

    # Mark as read when opened
    if not message.is_read:
        message.is_read = True
        message.save()

    return render(request, "user_messages/read.html", {"message": message})


# --- REAL-TIME SSE VIEW ---


async def sse_unread_count(request):
    """
    Streams the unread message count to the browser in real-time.
    """
    user = await request.auser()
    if not user.is_authenticated:
        return StreamingHttpResponse("Unauthorized", status=401)

    async def event_stream():
        last_count = -1
        while True:
            # We must wrap ORM calls in sync_to_async in an async generator
            @sync_to_async
            def get_unread_count():
                return Message.objects.filter(
                    recipient=user, is_read=False, is_archived=False
                ).count()

            current_count = await get_unread_count()

            # Only push data if the count changes
            if current_count != last_count:
                yield f"data: {current_count}\n\n"
                last_count = current_count

            # Wait 3 seconds before checking again (Polling the DB asynchronously)
            await asyncio.sleep(3)

    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response["Cache-Control"] = "no-cache"
    return response
