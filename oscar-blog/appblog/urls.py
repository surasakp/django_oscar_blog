from django.conf.urls import include, url

from appblog.dashboard.apps import application as blog_dashboard_application


urlpatterns = [
    url(r'', include(blog_dashboard_application.urls))
]
