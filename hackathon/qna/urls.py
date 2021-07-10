from django.urls import path
from django.conf.urls import url
from .views import *
from search.views import qna

urlpatterns = [
    path('<int:book_id>', qna, name="qna"),
    path('registerqna/<int:room_id>', registerQna, name="registerQna"),
    path('detail/<int:qna_id>', detail, name="detail"),
    path('detail_back/<int:qna_id>', detail_back, name="detail_back"),
    path('comment', comment, name="comment"),
    path('selected/<int:comment_id>', selected, name="selected"),
]
