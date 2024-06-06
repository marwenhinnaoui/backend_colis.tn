from django.urls import re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    re_path('signup', views.signup),
    re_path('login', views.login),
    re_path('ajouter_admin', views.ajouterAdmin),
    re_path('delete/(?P<userId>\d+)$', views.deleteUser),
    re_path('accepte_user/(?P<userId>\d+)$', views.acceptUser),
    re_path('blocage_utilisateur/(?P<userId>\d+)$', views.blocage_utilisateur),
    re_path('deblocage_utilisateur/(?P<userId>\d+)$', views.deblocage_utilisateur),
    re_path('update/(?P<user_id>\d+)$', views.update_user),
    re_path('modifier_profile/(?P<user_id>\d+)$', views.modifier_profile),
    re_path('update_admin/(?P<admin_id>\d+)$', views.update_admin),
    re_path('delete_admin/(?P<admin_id>\d+)$', views.delete_admin),
    re_path('logout', views.logout),
    re_path('cree_colis', views.cree_colis),
    re_path('cree_reclamation', views.cree_reclamation),
    re_path('get_all_users', views.get_all_users),
    re_path('get_all_admins/(?P<admin_id>\d+)', views.get_all_admins),
    re_path('get_all_reclamations', views.get_all_reclamations),
    re_path('get_reclamation/(?P<reclamant_id>\d+)', views.get_reclamations),
    re_path('get_colis/(?P<client_id>\d+)$', views.get_colis_by_client_id),
    re_path('get_colis_by_transporteur_id/(?P<transporteur_id>\d+)$', views.get_colis_by_transporteur_id),
    re_path('delete_colis/(?P<colis_id>\d+)$', views.delete_colis),
    re_path('upload/', views.upload_images),
    re_path('update_colis_status/(?P<colis_id>\d+)$', views.update_colis_status),
    re_path(r'^create-transporteur-calendrier$', views.create_transporteur_calendrier),
    re_path(r'^transporteur-calendriers/(?P<transporteur_id>\d+)/$', views.get_transporteur_calendriers),
    re_path(r'^users/(?P<user_id>\d+)$', views.get_user_by_id),
    re_path('get_colis_compare/(?P<transporteur_id>\d+)$', views.get_colis_compare),
    re_path('update_reclamation/(?P<reclamation_id>\d+)$', views.update_reclamation),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
