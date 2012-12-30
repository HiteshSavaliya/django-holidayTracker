from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('holiTrack.views',
    # Examples:
    url(r'^employee/$', 'home', name='home'),
    url(r'^employee/(?P<emp_id>\d+)/$', 'details', name='details'),
    # url(r'^holidayTracker/', include('holidayTracker.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

urlpatterns += patterns ('', url(r'^admin/', include(admin.site.urls)),)
