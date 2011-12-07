from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^gin/message','gin.gin_backend.views.message'),
    (r'^gin/handlers','gin.gin_backend.views.message'),
    (r'^gin/gips','gin.gin_backend.views.message'),
    (r'^gin/groups','gin.gin_backend.views.message'),
    (r'^gin/main','gin.gin_backend.views.index'),
    (r'^gin/', 'gin.gin_backend.views.message'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
