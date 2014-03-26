from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'home.views.index', name='home'),
    url(r'^student-record$', 'home.views.student_record', name='student-record'),
    url(r'^course-selection$', 'home.views.course_selection', name='course-selection'),
    url(r'^course-details$', 'home.views.course_details', name='course-details'),
)
