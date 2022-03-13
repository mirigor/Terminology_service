from django.contrib import admin
from django.urls import path

from app.views import ReferenceBookAPI, ReferenceBookElementsCurrentVersionAPI, ActualReferenceBookAPI, \
    ReferenceBookElementsSpecificVersionAPI, ValidationReferenceBookElementsCurrentVersionAPI, \
    ValidationReferenceBookElementsSpecificVersionAPI

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/reference_book/<str:created_at>/', ActualReferenceBookAPI.as_view()),
    path('api/reference_book/', ReferenceBookAPI.as_view()),

    path('api/<str:name>/<str:version>/elements/', ReferenceBookElementsSpecificVersionAPI.as_view()),
    path('api/<str:name>/elements/', ReferenceBookElementsCurrentVersionAPI.as_view()),

    path('api/element_validation/<str:name>/<str:version>/<str:value>/elements/', ValidationReferenceBookElementsSpecificVersionAPI.as_view()),
    path('api/element_validation/<str:name>/<str:value>/elements/', ValidationReferenceBookElementsCurrentVersionAPI.as_view()),

]
