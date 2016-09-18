from django.conf.urls import include, url
from django.contrib import admin
from .views import view_invoice, charge_card

urlpatterns = [
    # Examples:
    # url(r'^$', 'payable.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^invoice/(?P<pk>\d*)/$', view_invoice, name='view-invoice'),
    url(r'^charge$', charge_card, name='charge-card'),
]
