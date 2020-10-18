from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from rest_framework import routers 

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views

# local
from waste.views import WasteDetailView
import chemcomponent.views as comp_views
import componentprop.views as prop_views

router = routers.DefaultRouter()                      
router.register(r'components', comp_views.ComponenterView, 'component')
router.register(r'categoryprops', prop_views.CategoryPropView, 'categoryprop')
router.register(r'valueprops', prop_views.ValuePropView, 'valueprop')

urlpatterns = [
    path('django-admin/', admin.site.urls),

    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),

    path('search/', search_views.search, name='search'),

    path('waste/<int:pk>/', WasteDetailView.as_view(), name='waste-detail'),
    path('api/', include(router.urls))  

]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
