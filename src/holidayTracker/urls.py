from django.conf.urls import patterns, include, url


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^employee/', include('holiTrack.urls')),
    url(r'^admin/', include(admin.site.urls)),
#    url(r'^admin/password_reset/$', 'django.contrib.auth.views.password_reset', name='admin_password_reset'),
#    (r'^admin/password_reset/done/$', 'django.contrib.auth.views.password_reset_done'),
#    (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
#    (r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
    )
