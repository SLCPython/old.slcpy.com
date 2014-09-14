#encoding: utf-8
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # ----------------------- Home
    url(r'^$', 'slcpy.views.home.main_view', name='home'),

    # ----------------------- profile
    url(r'^login$', 'profiles.views.home.login_view', name='login'),    
    url(r'^register$', 'profiles.views.home.register_view', name='register'),          
    url(r'^profiles/', include('profiles.urls', namespace='profiles')),
    # TODO:  url(r'^logout$', 'profiles.views.home.logout_view', name='logout'),        

    # ----------------------- API urls
    #url(r'^api/', include(tagged_post.urls)),

    # ----------------------- 3rd party urls
    url(r'^search/', include('haystack.urls', namespace='search')),

    # ----------------------- admin urls
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
