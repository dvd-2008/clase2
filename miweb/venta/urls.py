from django.urls import path, include
from . import views

urlpatterns = [
    path('venta/', include([
        path('', views.menu_principal, name='menu_principal'), 
        path('q_cliente/', views.consulta_cliente, name='lista_clientes'),
        path('c_cliente/', views.crear_cliente, name='crear_cliente'),
        path('u_cliente/', views.actualizar_cliente, name='actualizar_cliente'),
        path('d_cliente/', views.borrar_cliente, name='borrar_cliente'),

        path('q_producto/', views.consulta_producto, name='lista_producto'),
        path('c_producto/', views.crear_producto, name='crear_producto'),
        path('u_producto/', views.actualizar_producto, name='actualizar_producto'),
        path('d_producto/', views.borrar_producto, name='borrar_producto'),
    ])),
]
