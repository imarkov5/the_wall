from django.urls import path
from . import views
urlpatterns = [
    path('', views.wall),
    path('logout', views.logout),
    path('post_message', views.post_message),
    path('post_comment/<int:mess_id>', views.post_comment),
    path('delete/<int:mess_id>', views.delete_message),
    path('edit/<int:mess_id>', views.edit_message),
    path('like/<int:mess_id>', views.like),
    path('edit_profile', views.edit_profile),
    path('unlike/<int:mess_id>', views.unlike)
]