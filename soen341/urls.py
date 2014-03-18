from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'home.views.index', name='home'),
    url(r'^student-record$', 'home.views.student_record', name='student-record'),
    url(r'^course-selection$', 'home.views.course_selection', name='course-selection'),
    url(r'^login$', 'home.login.login_view', name='login'),
    url(r'^do-login$', 'home.login.do_login', name='do login'),
    url(r'^do-logout$', 'home.login.do_logout', name='do logout'),
    url(r'^do-register$', 'home.login.do_register', name='do register'),
    
)
