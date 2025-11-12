from django.urls import path
from menu.views import AcceptCourseView, AddAmountWalletView, AddDepositView, AddEvaluationView, AddPaiementView, AddVehiculeView, CancelCourseView, ConfigurationPaiementView, CoursesDisponiblesView, CreateCourseView, DevenirChauffeurView, EvaluationsChauffeurView, EvaluationsPassagerView, GetDepositView, GetTotalAdminWalletView, GetWalletForAdminView, GetWalletForDriverView, MesCoursesChauffeurView, MesCoursesChauffeurViewTerminee, MesCoursesPassagerView, MesPaiementsView, SignInView, SignupView, PrixCourseAPIView, TerminerCourseView, TransfertWalletView, UpdatePasswordView, UpdateUserInfoView, UploadAvatarView,VehiculeListView,VehiculeDetailView,VehiculeUpdateView,VehiculeDeleteView, WithdrawDepositView, WithdrawWalletView


urlpatterns = [
    path('user/signin/', SignInView.as_view(), name='signin'),
    path('user/signup/', SignupView.as_view(), name='signup'),
    path('user/update/', UpdateUserInfoView.as_view(), name='update-user'),
    path('user/migrate/driver/', DevenirChauffeurView.as_view(), name='update-user'),
    path('user/password/', UpdatePasswordView.as_view(), name='update-password'),
    path('user/avatar/', UploadAvatarView.as_view(), name='update-avatar'),
    path('vehicule/add/', AddVehiculeView.as_view(), name='vehicule-add'),
    path('vehicule/list/', VehiculeListView.as_view(), name='vehicule-list'),
    path('vehicule/', VehiculeDetailView.as_view(), name='vehicule-detail'),
    path('vehicule/<int:id>/update/', VehiculeUpdateView.as_view(), name='vehicule-update'),
    path('vehicule/<int:id>/delete/', VehiculeDeleteView.as_view(), name='vehicule-delete'),
    path('tarification/', PrixCourseAPIView.as_view(), name='tarification-list'),
    path('course/command/', CreateCourseView.as_view(), name='create-course'),
    path('course/<int:pk>/accept/', AcceptCourseView.as_view(), name='accept-course'),
    path('course/<int:pk>/cancel/', CancelCourseView.as_view(), name='cancel-course'),
    path('course/<int:pk>/terminer/', TerminerCourseView.as_view(), name='terminer-course'),
    path('course/passager/', MesCoursesPassagerView.as_view(), name='mes-courses-passager'),
    path('course/disponibles/', CoursesDisponiblesView.as_view(), name='courses-disponibles'),
    path('course/chauffeur/', MesCoursesChauffeurView.as_view(), name='mes-courses-chauffeur'),
    path('course/chauffeur/terminee/', MesCoursesChauffeurViewTerminee.as_view(), name='mes-courses-chauffeur-terminee'),
    path('paiement/add/', AddPaiementView.as_view(), name='add-paiement'),
    path('paiement/mes/', MesPaiementsView.as_view(), name='mes-paiements'),
    path('config/', ConfigurationPaiementView.as_view(), name='config-paiement'),
    path('wallet/add-amount/', AddAmountWalletView.as_view(), name='wallet-add'),
    path('wallet/get-for-admin/', GetWalletForAdminView.as_view(), name='wallet-get-admin'),
    path('wallet/get-total-admin/', GetTotalAdminWalletView.as_view(), name='wallet-total-admin'),
    path('wallet/get-for-driver/', GetWalletForDriverView.as_view(), name='wallet-get-driver'),
    path('wallet/withdraw-cash/', WithdrawWalletView.as_view(), name='wallet-withdraw'),
    path('wallet/transfert/', TransfertWalletView.as_view(), name='wallet-transfert'),
    path('deposit/add/', AddDepositView.as_view(), name='deposit-add'),
    path('deposit/withdraw/', WithdrawDepositView.as_view(), name='deposit-withdraw'),
    path('deposit/get/', GetDepositView.as_view(), name='deposit-get'),
    path('evaluation/add/', AddEvaluationView.as_view(), name='evaluation-add'),
    path('evaluation/chauffeur/<int:chauffeur_id>/', EvaluationsChauffeurView.as_view(), name='evaluation-chauffeur'),
    path('evaluation/passager/', EvaluationsPassagerView.as_view(), name='evaluation-passager'),

]

