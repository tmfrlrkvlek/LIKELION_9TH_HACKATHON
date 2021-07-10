from django.shortcuts import render
from qna.models import *
# from qna.views import qna
import requests
import json

# Create your views here.
def index(request):
    return render(request, 'index.html')

def search(request):
    ver = int(request.POST['ver'])
    key = request.POST.get('key', '')
    if ver == 0:
        books = Book.objects.filter(isbn__icontains = key)
    elif ver == 1:
        books = Book.objects.filter(title__icontains = key)
    else :
        books = Book.objects.filter(author__icontains = key)
    return render(request, 'search.html', {'books':books, 'ver':ver, 'key':key})

def registerBook(request):
    if request.method == 'GET':
        isbn = request.GET.get('isbn', '')
        return render(request, 'registerBook.html', {'isbn':isbn})
    else:
        isbn = request.POST['isbn']
        if(len(isbn)==0):
            return render(request, 'registerBook.html', {'error_msg' : "ISBN을 입력해주세요"})
        if Book.objects.filter(isbn__icontains = isbn).exists():
            return render(request, 'registerBook.html', {'error_msg' : "이미 존재하는 책은 등록할 수 없습니다."})
        headers = {'Authorization': 'KakaoAK kakaoappkey'}
        response = requests.get("https://dapi.kakao.com/v3/search/book?target=isbn&query="+isbn, headers = headers)
        result = json.loads(response.text)['documents']
        if not len(result) :
            return render(request, 'registerBook.html', {'error_msg' : "잘못된 ISBN입니다."})
        else :
            result = result[0]
            book = Book()
            book.isbn = result['isbn'].replace(' ', ' / ')
            book.title = result['title']
            book.author = result['authors'][0]
            book.publisher = result['publisher']
            book.imageUrl = result['thumbnail']
            book.save()
            room = Room()
            room.book = book
            room.save()
            return qna(request, book.id)


def qna(request, book_id) :
    chapter = int(request.GET.get('chapter', '-1'))
    page = int(request.GET.get('page', '-1'))
    book = Book.objects.get(id = book_id)
    qnas = Qna.objects.filter(room = book.room)
    chapters = []
    for qna in qnas :
        if qna.chapter not in chapters :
            chapters.append(qna.chapter)
    if chapter != -1 :
        qnas = qnas.filter(chapter = chapter)
    if page != -1 :
        qnas = qnas.filter(page = page)
        return render(request, 'qna.html', {'book':book, 'qnas': qnas, 'chapters':chapters, 'cur_chapter':chapter, 'cur_page':page})
    else :
        return render(request, 'qna.html', {'book':book, 'qnas': qnas, 'chapters':chapters, 'cur_chapter':chapter})
    
    
