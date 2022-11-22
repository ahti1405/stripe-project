from django.urls import path

from .views import SuccessView, CancelView, ItemDetailView, SessionIdAPIView, HtmlPageAPIView

urlpatterns = [
    path('<int:pk>/', ItemDetailView.as_view(), name='item_detail'),
    path('success/', SuccessView.as_view(), name='success'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('buy/<int:pk>/', SessionIdAPIView.as_view(), name='session_id'),
    path('item/<int:pk>/', HtmlPageAPIView.as_view(), name='html_page'),
]
