from django.urls import path
from todo_app import views



#todolara erişmke için todos/ pattern eklencek
#sonra ise istediğimiz todoya erişmke için /<int:pk>/ patterni  oluşturlcak
urlpatterns = [
    path('todos/', views.TodoAPIView.as_view()),
    path('todos/<int:pk>/', views.TodoAPIView.as_view()),
]
