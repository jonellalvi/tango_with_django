from django.conf.urls import patterns, url
from rango import views
# importing views accesses view in view.py


# to create mappings, use a tuple
# tuple MUST be called urlpatterns
# it contains a series of calls to the django.conf.url() function
# each call handles a unique mapping.
# only one URL mapping here.
# first parameter is ^$ which matches to an empty string.
# Any URL from the user matching this pattern means the view views.index()
# would be invoked by Django.
# the view would be passed a HttpRequest object as a parameter with
# information about the user's request to the server
# optional parameter to url() name, using 'index' as the value
# http://www.tangowithdjango.com/book/chapters/setup.html  section 3.5
urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^about/', views.about, name='about'),
        url(r'^add_category/$', views.add_category, name='add_category'),
        url(r'^category/(?P<category_name_url>\w+)/add_page/$', views.add_page, name='add_page'),
        url(r'^category/(?P<category_name_url>\w+)/$', views.category, name='category'),
        )
