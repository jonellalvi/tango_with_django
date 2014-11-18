from django.conf import settings
from django.conf.urls import patterns, include, url


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tango_with_django.views.home', name='home'),
    # url(r'^tango_with_django/', include('tango_with_django.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    #this mapping looks for url strings that match the pattern ^rango/.
    # when a match is made the remainder of the url string is passed onto
    # and handled by rango.urls, done by include() in django.conf.urls.
    # domain is stripped out, remainder of the url string (rango/) passed
    # on to the application rango. Rango tries to match the empty string,
    # (and does) which dispatches the index() view we created.
    # http://www.tangowithdjango.com/book/chapters/setup.html
    url(r'^rango/', include('rango.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}),
    )
