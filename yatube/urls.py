from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.contrib.flatpages import views
from django.conf.urls.static import static


from django.conf.urls import handler404, handler500

urlpatterns = [
    path('', include('posts.urls')),
    path('about/', include('django.contrib.flatpages.urls')),
    path('auth/', include('Users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('god/admin/', admin.site.urls),

]

urlpatterns += [
    path('about-author/',
         views.flatpage,
         {'url': '/about-author/'},
         name='about'
         ),
    path('about-spec/', views.flatpage, {'url': '/about-spec/'}, name='terms'),
]

handler404 = "posts.views.page_not_found"  # noqa
handler500 = "posts.views.server_error"  # noqa

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT
                          )
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT
                          )
    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
