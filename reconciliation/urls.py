from django.urls import path
from .views import FileUploadView, ReconciliationReportView

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file_upload'),
    path('report/', ReconciliationReportView.as_view(), name='file_upload'),
]