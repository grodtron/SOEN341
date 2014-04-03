from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'home.views.index', name='home'),
    url(r'^student-record$', 'home.views.student_record', name='student-record'),


    url(r'^course-selection$', 'home.views.course_selection', name='course-selection'),
    url(r'^course-selection/([A-Z]{1,4}[0-9]{0,3})$', 'home.views.course_selection', name='course-selection'),

    url(r'^course-details/([A-Z]{4}[0-9]{3})$', 'home.views.course_details', name='course-details'),

    url(r'^login$', 'home.login.login_view', name='login'),
    url(r'^do-login$', 'home.login.do_login', name='do login'),
    url(r'^do-logout$', 'home.login.do_logout', name='do logout'),
    url(r'^do-register$', 'home.login.do_register', name='do register'),
    url(r'^edit-student-record$', 'home.views.edit_student_record' , name='edit-student-record'),

    url(r'^shopping-cart$', 'home.shopping_cart.shopping_cart', name='shopping cart'),
    url(r'^shopping-cart/do-add$', 'home.shopping_cart.add', name='shopping cart add'),
    url(r'^shopping-cart/do-remove$', 'home.shopping_cart.remove', name='shopping cart remove'),
    url(r'^shopping-cart/get-cart$', 'home.shopping_cart.get_cart', name='get complete shopping cart'),

    url(r'^register/get-courses$','home.course_registration.get_registered_courses', name='get registered courses'),
    url(r'^register/get-course/([0-9]+)$','home.course_registration.get_course_section', name='get registered courses'),
    url(r'^register/do-add$','home.course_registration.register_for_course', name='get registered courses'),
    url(r'^register/do-remove$','home.course_registration.remove', name='remove course'),
)
handler404 = 'mysite.views.my_custom_404_view'
handler500 = 'mysite.views.my_custom_error_view'
