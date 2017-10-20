from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^blogs/$', views.BlogListView.as_view(), name='blogs'),
    url(r'^blogger/(?P<pk>\d+)$', views.BlogListbyAuthorView.as_view(), name='blogs-by-author'),
    url(r'^blog/(?P<pk>\d+)$', views.BlogDetailView.as_view(), name='blog-detail'),
    url(r'^bloggers/$', views.BloggerListView.as_view(), name='bloggers'),
    url(r'^blog/(?P<pk>\d+)/comment/$', views.BlogCommentCreate.as_view(), name='blog_comment'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^blog/(?P<pk>\d+)/edit/$', views.blog_edit, name='blog_edit'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),

]
