from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Homepage
def index_view(request):
    return render(request, 'chat/index.html')

# Chat view
@login_required
def chat_view(request):
    return render(request, 'chat/chat.html')
