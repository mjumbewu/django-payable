from django.urls import path
from django.contrib import admin
from .views import view_invoice, charge_card, send_invoice

urlpatterns = [
    # Examples:
    # url(r'^$', 'payable.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    path('admin/', admin.site.urls),

    path('invoice/<int:pk>/', view_invoice, name='view-invoice'),
    path('invoice/<int:pk>/send', send_invoice, name='send-invoice'),
    path('charge', charge_card, name='charge-card'),
]
