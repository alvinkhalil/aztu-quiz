from django.urls import path
from django.urls.conf import include
from pages import views

app_name  = "pages"
urlpatterns = [
    path('',views.index, name = "index"),
    path('register/',views.register_user, name = "register"),
    path('logout/',views.logout_user,name = "logout"),
    path('addquiz/',views.add_quiz,name = "addquiz"),
    path('quiz/',views.quiz, name='quiz'),
    path('myquestions/',views.my_questions, name = "my_questions"),
    path('delete/<int:id>',views.delete_quiz, name ="deletequiz"),
    path('update/<int:id>',views.update_quiz, name ="updatequiz"),
    path("myresults/",views.results, name  = "myresults"),
    path("myresults/delete/<int:id>",views.deleteresult, name  = "deleteresult")



    
]
