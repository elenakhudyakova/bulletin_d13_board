from django.contrib import admin
from django.urls import path, re_path, include
from MMORPG_messages.views import UserView, UserUpdate, PostList, CommentListFiltered
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import never_cache

from ckeditor_uploader import views as ckeditor_views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),

    path('user/', UserView.as_view()),
    path('user/edit/<int:pk>/', UserUpdate.as_view(), name='user_edit'),

    path('', PostList.as_view(), name='post_list'),
    path('post/', include('MMORPG_messages.urls')),
    path('post/search/', CommentListFiltered.as_view(), name='comment_search'),

    # path('ckeditor/', include('ckeditor_uploader.urls')),

    re_path(r'^upload/', ckeditor_views.upload, name='ckeditor_upload'),
    re_path(r'^browse/', ckeditor_views.browse, name='ckeditor_browse'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

