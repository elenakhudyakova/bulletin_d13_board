from django.urls import path

from board.views import IndexView, AdCreate, AdUpdate, AdDetail, ad_deactivate, SentRepliesView, ReceivedRepliesView, \
    accept_reply, delete_reply, CategoryAdList, UserAdList

urlpatterns = [
    path('', IndexView.as_view(), name='board_index'),
    path('create/', AdCreate.as_view(), name='board_ad_create'),
    path('ad<int:pk>/', AdDetail.as_view(), name='board_ad_detail'),
    path('ad<int:pk>/update/', AdUpdate.as_view(), name='board_ad_update'),
    path('ad<int:pk>/deactivate/', ad_deactivate, name='board_ad_deactivate'),
    path('category<int:category_pk>/', CategoryAdList.as_view(), name='board_ad_list'),
    path('ads/', UserAdList.as_view(), name='board_user_ads'),
    path('sent-replies/', SentRepliesView.as_view(), name='board_sent_replies'),
    path('received-replies/', ReceivedRepliesView.as_view(), name='board_received_replies'),
    path('reply<int:pk>/accept/', accept_reply, name='board_accept_reply'),
    path('reply<int:pk>/delete/', delete_reply, name='board_delete_reply'),
]
