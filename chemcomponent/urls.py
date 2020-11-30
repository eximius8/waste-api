from django.urls import path


import chemcomponent.views as comp_views


urlpatterns = [
    path(r'total/', comp_views.comp_statistics, name='total-comps'),
    path(r'', comp_views.ComponentsView.as_view(), name='components'),
    path('<int:pk>/', comp_views.ComponentView.as_view(), name='component'), 
] 
 