from django.urls import path
from kahoot import views

urlpatterns = [
    path('', views.home_view, name='home-view'),
    path('detail/<int:pk>', views.detail_view, name='detail-view')

]
