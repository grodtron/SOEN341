from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'home.views.index', name='home'),
    url(r'^student-record$', 'home.views.student_record', name='student-record'),

    url(r'^course-selection$', 'home.views.course_selection', name='course-selection'),
    url(r'^course-selection/([A-Z]{4})$', 'home.views.course_selection', name='course-selection'),

    url(r'^course-details/([A-Z]{4}[0-9]{3})$', 'home.views.course_details', name='course-details'),

    url(r'^login$', 'home.login.login_view', name='login'),
    url(r'^do-login$', 'home.login.do_login', name='do login'),
    url(r'^do-logout$', 'home.login.do_logout', name='do logout'),
    url(r'^do-register$', 'home.login.do_register', name='do register'),
    url(r'^edit-student-record$', 'home.views.edit_student_record' , name='edit-student-record'),

    url(r'^shopping-cart$', 'home.shopping_cart.shopping_cart', name='shopping cart'),
    url(r'^shopping-cart/do-add$', 'home.shopping_cart.add', name='shopping cart add'),
    url(r'^shopping-cart/do-remove$', 'home.shopping_cart.remove', name='shopping cart remove'),
    url(r'^shopping-cart/get-cart$', 'home.shopping_cart.get_cart', name='get complete shopping cart')
)
