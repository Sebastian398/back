from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf.urls.static import static
from .views import (SensorViewSet, ProgramacionRiegoViewSet, 
                    RegisterView, AccesoValidateView, 
                    CustomLoginView, UserDetailView, 
                    UserDetailView1, ProgramacionRiegoAdminViewSet, 
                    ActivarCuentaView, RegistroRiegoViewSet, 
                    LecturasHumedadList, EstadisticasHumedadSemanal, 
                    CultivoViewSet, LogoutView, 
                    InfoFincaView, InfoFincaEditarView, 
                    UserUpdateView, CustomPasswordResetView, 
                    CustomPasswordResetConfirmView,
                    UpdateAvatarView)
from rest_framework_simplejwt.views import TokenRefreshView


# Router para viewsets de sensores y programacion_riego
router = DefaultRouter()
router.register(r'sensores', SensorViewSet, basename='sensor')
router.register(r'programacion_riego', ProgramacionRiegoViewSet, basename='programacion_riego')
router.register(r'programacion_riego_admin', ProgramacionRiegoAdminViewSet, basename='programacionriegoadmin')
router.register(r'registro_riego', RegistroRiegoViewSet, basename='registro_riego')
router.register(r'cultivos', CultivoViewSet, basename='cultivo')

class ApiRootView(APIView):
    def get(self, request, format=None):
        return Response({
            'register': request.build_absolute_uri('register/'),
            'login': request.build_absolute_uri('login/'),
            'token_refresh': request.build_absolute_uri('token/refresh/'),
            'sensores': request.build_absolute_uri('sensores/'),
            'datos': request.build_absolute_uri('usuario-actual/'),
            'datos1': request.build_absolute_uri('usuario-actual1/'),
            'programacion_riego': request.build_absolute_uri('programacion_riego/'),
            'programacion_riego_admin': request.build_absolute_uri('programacion_riego_admin/'),
            'registro_riego': request.build_absolute_uri('registro_riego/'),
            'lecturas_humedad': request.build_absolute_uri('lecturas_humedad/'),
            'estadisticas_humedad_semanal': request.build_absolute_uri('estadisticas_humedad_semanal/'),
            'cultivos': request.build_absolute_uri('cultivos/'),
            'infoFinca':request.build_absolute_uri('infoFinca/'),
            'info_finca_editar':request.build_absolute_uri('info_finca/editar/'),
            'usuario-actual-editar': request.build_absolute_uri('usuario-actual/editar/'),
            'password_reset': request.build_absolute_uri('password_reset/'),
            'password_reset_confirm': request.build_absolute_uri('password_reset/confirm/'),

        })


urlpatterns = [
    path('', ApiRootView.as_view(), name='api-root'),          
    path('register/', RegisterView.as_view(), name='register'), 
    path('login/', CustomLoginView.as_view(), name='login'),          
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
    path('api/acceso-validate/', AccesoValidateView.as_view(), name='acceso-validate'),
    path('usuario-actual/', UserDetailView.as_view(), name='usuario-actual'),
    path('usuario-actual1/', UserDetailView1.as_view(), name='usuario-actual1'),
    path('activar-cuenta/<uuid:token>/', ActivarCuentaView.as_view(), name='activar-cuenta'),
    path('lecturas_humedad/', LecturasHumedadList.as_view(), name='lecturas-humedad'),
    path('estadisticas_humedad_semanal/', EstadisticasHumedadSemanal.as_view(), name='estadisticas-humedad-semanal'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('infoFinca/', InfoFincaView.as_view(), name='infoFinca'),
    path('info_finca/editar/', InfoFincaEditarView.as_view(), name='info_finca_editar'),
    path('usuario-actual/editar/', UserUpdateView.as_view(), name='usuario-actual-editar'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('update-avatar/', UpdateAvatarView.as_view(), name='update-avatar'),
    path('update-avatar/', UpdateAvatarView.as_view(), name='update-avatar'),
    path('', include(router.urls)),                              
]

