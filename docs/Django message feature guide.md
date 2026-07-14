# Building a Real-Time Django Inbox with Server-Sent Events (SSE)

Welcome to this comprehensive guide! In this tutorial, you will build a fully functional, real-time messaging inbox in Django. We will use **Server-Sent Events (SSE)** to push real-time unread message counts to the browser, and **Bootstrap 5** alongside **Django Crispy Forms** for a polished, professional user interface.

---

## Table of Contents
1. [Prerequisites & Setup](#1-prerequisites--setup)
2. [Database Design: The Message Model](#2-database-design-the-message-model)
3. [Building the Form (Crispy Forms)](#3-building-the-form-crispy-forms)
4. [Creating the Views (Standard & Async)](#4-creating-the-views-standard--async)
5. [Configuring URLs](#5-configuring-urls)
6. [Designing the Templates (Bootstrap 5)](#6-designing-the-templates-bootstrap-5)
7. [Testing the Application](#7-testing-the-application)

---

## 1. Prerequisites & Setup

Before we write code, ensure you have the required packages installed in your Django environment. We need Django, Crispy Forms, and the Bootstrap 5 template pack (we've been using these all along in the djang_start example repository)

**Install the packages:**
```bash
pip install django django-crispy-forms crispy-bootstrap5
```

**Update `settings.py`:**
Add the new apps to your `INSTALLED_APPS` and configure Crispy Forms to use Bootstrap 5.

```python
# settings.py
INSTALLED_APPS = [
    # ... your default django apps
    'crispy_forms',
    'crispy_bootstrap5',
    # The app we are building - DO NOT name this 'messages' as this will conflict with django!
    'user_messages', 
]

# Crispy Forms Configuration
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
```

---

## 2. Database Design: The Message Model

We need a model that tracks the sender, recipient, and the read/archive status of the message.

Create this in `user_messages/models.py`:

```python
from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    subject = models.CharField(max_length=255)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # State tracking
    is_read = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False) 

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.subject} (From: {self.sender.username})"
```
> ⚠️ **Don't forget:** Run `python manage.py makemigrations` and `python manage.py migrate` after creating your model.

---

## 3. Building the Form (Crispy Forms)

Django Crispy Forms allows us to define how a form renders directly in Python. We will use `FormHelper` to style our compose message form beautifully with Bootstrap classes.

Create `user_messages/forms.py`:

```python
from django import forms
from .models import Message
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class ComposeMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'body']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        # Add a custom bootstrap primary button via python
        self.helper.add_input(Submit('submit', 'Send Message', css_class='btn btn-primary mt-3'))
```

---

## 4. Creating the Views (Standard & Async)

We need views to display the inbox, send messages, read messages, and our special **Async SSE view** for the real-time badge.

In `user_messages/views.py`:

```python
import asyncio
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse
from asgiref.sync import sync_to_async
from .models import Message
from .forms import ComposeMessageForm

# --- STANDARD VIEWS ---

@login_required
def inbox_view(request):
    messages = Message.objects.filter(recipient=request.user, is_archived=False)
    return render(request, 'user_messages/inbox.html', {'messages': messages})

@login_required
def compose_view(request):
    if request.method == 'POST':
        form = ComposeMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('inbox')
    else:
        form = ComposeMessageForm()
    
    return render(request, 'user_messages/compose.html', {'form': form})

@login_required
def read_message_view(request, message_id):
    message = get_object_or_404(Message, id=message_id, recipient=request.user)
    
    # Mark as read when opened
    if not message.is_read:
        message.is_read = True
        message.save()
        
    return render(request, 'user_messages/read.html', {'message': message})


# --- REAL-TIME SSE VIEW ---

async def sse_unread_count(request):
    """
    Streams the unread message count to the browser in real-time.
    """
    user = request.user
    if not user.is_authenticated:
        return StreamingHttpResponse("Unauthorized", status=401)

    async def event_stream():
        last_count = -1
        while True:
            # We must wrap ORM calls in sync_to_async in an async generator
            @sync_to_async
            def get_unread_count():
                return Message.objects.filter(
                    recipient=user, 
                    is_read=False, 
                    is_archived=False
                ).count()

            current_count = await get_unread_count()

            # Only push data if the count changes
            if current_count != last_count:
                yield f"data: {current_count}\n\n"
                last_count = current_count

            # Wait 3 seconds before checking again (Polling the DB asynchronously)
            await asyncio.sleep(3)

    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response['Cache-Control'] = 'no-cache'
    return response
```

---

## 5. Configuring URLs

Map our views to URLs. 

In `user_messages/urls.py`:
```python
from django.urls import path
from . import views

urlpatterns = [
    path('inbox/', views.inbox_view, name='inbox'),
    path('compose/', views.compose_view, name='compose'),
    path('message/<int:message_id>/', views.read_message_view, name='read_message'),
    
    # The SSE Endpoint
    path('sse/unread-count/', views.sse_unread_count, name='sse_unread_count'),
]
```

---

## 6. Designing the Templates (Bootstrap 5)

We need three templates: a base template (which contains the navbar and our real-time JavaScript), an inbox view, and a compose view.

Create a folder structure: `user_messages/templates/user_messages/`

### A. Update The Base Template (`base.html`)
Add the **EventSource API** script for SSE to the bottom of your base.html so it loads on every page:


NOTE: ADD THIS JUST BEFORE THE CLOSING `</body>` tag
```html

<script>
    document.addEventListener("DOMContentLoaded", function() {
        // 1. Connect to the SSE endpoint
        const eventSource = new EventSource("{% url 'sse_unread_count' %}");
        const badge = document.getElementById('inbox-badge');

        // 2. Listen for incoming messages from the server
        eventSource.onmessage = function(event) {
            const count = parseInt(event.data, 10);
            
            // 3. Update the UI
            badge.innerText = count;
            if (count > 0) {
                badge.style.display = 'inline-block';
            } else {
                badge.style.display = 'none'; // Hide if 0 unread messages
            }
        };

        // Handle connection errors gracefully
        eventSource.onerror = function(err) {
            console.error("SSE Connection dropped. Browser will auto-reconnect.");
        };
    });
</script>

```

### B. The Inbox Template (`inbox.html`)

```html
{% extends 'base.html' %}

{% block content %}
<div class="card shadow-sm">
    <div class="card-header bg-white border-bottom d-flex justify-content-between align-items-center">
        <h4 class="mb-0">My Inbox</h4>
        <a href="{% url 'compose' %}" class="btn btn-sm btn-outline-primary">New Message</a>
    </div>
    <div class="list-group list-group-flush">
        {% for message in messages %}
            <a href="{% url 'read_message' message.id %}" 
               class="list-group-item list-group-item-action {% if not message.is_read %}list-group-item-light fw-bold{% endif %}">
                <div class="d-flex w-100 justify-content-between">
                    <h5 class="mb-1">{{ message.subject }}</h5>
                    <small class="text-muted">{{ message.timestamp|timesince }} ago</small>
                </div>
                <p class="mb-1 text-muted">From: {{ message.sender.username }}</p>
            </a>
        {% empty %}
            <div class="p-4 text-center text-muted">
                Your inbox is empty.
            </div>
        {% endfor %}
    </div>
</div>
{% endblock %}
```

### C. The Compose Template (`compose.html`)
Using Crispy Forms makes rendering complex forms trivial!

```html
{% extends 'base.html' %}
{% load crispy_forms_tags %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8">
        <div class="card shadow-sm">
            <div class="card-header bg-white border-bottom">
                <h4 class="mb-0">Compose Message</h4>
            </div>
            <div class="card-body">
                <!-- Crispy Forms handles all the styling, inputs, and errors -->
                {% crispy form %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### D. The Read Message Template (`read.html`)

```html
{% extends 'base.html' %}

{% block content %}
<div class="card shadow-sm">
    <div class="card-body">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="card-title mb-0">{{ message.subject }}</h2>
            <a href="{% url 'inbox' %}" class="btn btn-outline-secondary btn-sm">&larr; Back to Inbox</a>
        </div>
        
        <h6 class="card-subtitle mb-3 text-muted">
            <strong>From:</strong> {{ message.sender.username }} <br>
            <strong>Sent:</strong> {{ message.timestamp|date:"F j, Y, g:i a" }}
        </h6>
        
        <hr>
        
        <div class="card-text mt-3" style="white-space: pre-wrap;">{{ message.body }}</div>
    </div>
</div>
{% endblock %}
```

---

##  7. Testing the Application

1. Open two different browsers (or one normal window and one Incognito window).
2. Log into User A in window 1, and User B in window 2.
3. Keep User B's screen on any page of the site.
4. Have User A send a message to User B.
5. **Watch the magic:** Without refreshing the page, User B's notification badge in the navbar will instantly light up red with a "1" in it! When they click into the message to read it, the badge will disappear.

###  Done!
You just implemented real-time, asynchronous push updates in Django without configuring Redis, WebSockets, or third-party JavaScript libraries. SSE relies on plain HTTP and the browser's native capabilities!
