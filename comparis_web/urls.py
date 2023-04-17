from django.urls import path, include
from comparis_web import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('logout_view', views.logout_view, name='logout_view'),
    path('signup', views.signup, name='signup'),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path("properties_views", views.properties_views, name="properties_views"),
    path("detail_view/<int:id>/", views.detail_view, name="detail_view"),
]