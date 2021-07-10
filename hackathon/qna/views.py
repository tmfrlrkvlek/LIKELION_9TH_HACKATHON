from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
import json
# Create your views here.
def qna(request, book_id) :
    book = Book.objects.get(id = book_id)
    qnas = Qna.objects.filter(room = book.room)
    return render(request, 'qna.html', {'book':book, 'qnas': qnas})

def registerQna(request, room_id):
    if request.method == 'POST':
        qna = Qna()
        room = Room.objects.get(id = request.POST['room_id'])
        qna.room = room
        qna.title = request.POST['questionTitle']
        writer = Profile.objects.get(user = request.user)
        qna.writer = writer
        qna.content = request.POST['content']
        if(request.FILES.getlist('files')): qna.isfile = True
        qna.chapter = request.POST['chapter']
        qna.page = request.POST['page']
        qna.qnum = request.POST['qnum']
        qna.save()
        idx = 1
        for item in request.FILES.getlist('files'):
            file = File()
            file.profile = writer
            file.qna = qna
            file.order = idx
            file.filename = item
            file.save()
            idx += 1
        return redirect('/qna/detail/'+str(qna.id))
    else:
        room = Room.objects.get(id = room_id)
        return render(request, 'registerQna.html', {'room_id':room_id, 'book':room.book})

def detail(request, qna_id):
    qna = Qna.objects.get(id=qna_id)
    comments = Comment.objects.filter(qna = qna, parent = 0)
    replydict = {}
    for comment in comments:
        replylist = []
        replies = Comment.objects.filter(parent = comment.id)
        for reply in replies:
            replylist.append(reply)
        replydict[str(comment.id)] = replylist
    book = Book.objects.get(id = qna.room.book.id)
    profile = Profile.objects.get(user=qna.writer.user)
    if(qna.isfile):
        files = File.objects.filter(qna = qna, profile = profile)
    else: 
        files = None
    return render(request, 'detail.html', {'qna': qna, "book": book, "files":files, "comments":comments, "replydict":replydict.items()})

def detail_back(request, qna_id):
    qna = Qna.objects.get(id=qna_id)
    comments = Comment.objects.filter(qna = qna, parent = 0)
    replydict = {}
    for comment in comments:
        replylist = []
        replies = Comment.objects.filter(parent = comment.id)
        for reply in replies:
            replylist.append(reply)
        replydict[str(comment.id)] = replylist
    book = Book.objects.get(id = qna.room.book.id)
    profile = Profile.objects.get(user=request.user)
    if(qna.isfile):
        files = File.objects.filter(qna = qna, profile = profile)
    else: 
        files = None
    return render(request, 'detail_back.html', {'qna': qna, "book": book, "files":files, "comments":comments, "replydict":replydict.items()})

def comment(request):
    obj = json.loads(request.body)
    comment = Comment.objects.create(
        qna = Qna.objects.get(id=int(obj.get('qna_id'))),
        writer = Profile.objects.get(user=request.user),
        content = obj.get('comment'),
        parent = obj.get('parent')
    )
    comment.save()
    context = {
        'writer' : comment.writer.nickname,
        'content' : comment.content,
        'pubdate' : comment.pubdate,
    }
    return JsonResponse(context)

def selected(request, comment_id):
    cmt = Comment.objects.get(id=int(comment_id))
    cmt.selected = True
    cmt.save()
    qna = Qna.objects.get(id=cmt.qna.id)
    qna.selected = True
    qna.save()
    comments = Comment.objects.filter(qna = qna, parent = 0)
    replydict = {}
    for comment in comments:
        replylist = []
        replies = Comment.objects.filter(parent = comment.id)
        for reply in replies:
            replylist.append(reply)
        replydict[str(comment.id)] = replylist
    book = Book.objects.get(id = qna.room.book.id)
    profile = Profile.objects.get(user=request.user)
    if(qna.isfile):
        files = File.objects.filter(qna = qna, profile = profile)
    else: 
        files = None
    return render(request, 'detail.html', {'qna': qna, "book": book, "files":files, "comments":comments, "replydict":replydict.items()})