from django.urls import path
from .views import *
from . import views


urlpatterns = [
    path('index/', index, name='index'),

    # path('typetickets/',typetickets_page, name='typetickets_page'),




 
    path('contact/', views.contact, name='contact'), 
    path('about_us/', views.about_us, name='about_us'),
    path('Dashboard&Statistics/', views.statistics, name='statistics'),



    # path('users/', UsersView.as_view(), name='users'),

    path('contact/send-email/', views.send_email, name='send_email'),


    


    
    path('types/', TypesTicketsView.as_view(), name='types'),
    path('typetickets_datatable/',types_tickets_datatable, name='types_tickets_datatable'),
    
    path('typeticket/<int:typeticket_id>/popup/', popup_update_typeticket, name='popup_update_typeticket'),
    path('typeticket/<int:typeticket_id>/update/', update_typeticket, name='update_typeticket'),
    
    path('typetickets/<int:typeticket_id>/delete/', views.delete_typeticket, name='delete_typeticket'),
    path('modal_add_ticket/', add_ticket, name='add_ticket'),



    path('chart/', views.chart_view, name='chart_view'),

    # path('tickets_by_type/', tickets_by_type_view, name='tickets_by_type'),

    
# path('pdf/', render_to_pdf, name='render_to_pdf'),
    
    
    path('tickets/', TicketsView.as_view(), name='tickets_page'),
    path('tickets_datatable/', views.tickets_datatable, name='tickets_datatable'),
    path('tickets_datatable/<str:status>/', views.tickets_datatable, name='tickets_datatable_with_status'),
    path('tickets_datatable/', views.tickets_datatable, name='tickets_datatable'),
    path('modal_add_typeticket/', add_typeticket, name='add_typeticket'),
    path('detail_ticket/<int:ticket_id>/', views.details_ticket, name='details_ticket'),
    
    path('ticket/<int:ticket_id>/popup/', popup_update_ticket, name='popup_update_ticket'),
    path('ticket/<int:ticket_id>/update/', update_ticket, name='update_ticket'),
    
    path('tickets/<int:ticket_id>/delete/', views.delete_ticket, name='delete_ticket'),


    
]