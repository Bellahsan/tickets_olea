from django.shortcuts import render, redirect,get_object_or_404
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse,HttpResponse,HttpResponseNotAllowed
from django.urls import reverse
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import TemplateView
from django.core.cache import cache
from django.contrib import admin
from django.core.paginator import Paginator
from django.db.models import Q,Count
from shared.enum import StatutTicket
from django.core.exceptions import ObjectDoesNotExist
import uuid
from .forms import *
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import *
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_http_methods
from django.http import FileResponse,HttpResponseRedirect
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.utils.dateparse import parse_date
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden
import random









def redirecttohome(request):
    return redirect('/')


def clear_cache(request):
     cache.clear()
     return redirect('/')


@staff_member_required
def index(request):
    context = admin.site.each_context(request)
    return render(request, 'website/index.html', context)


#################################################################################################
#################################################################################################
#################################################################################################
def generate_unique_ticket_code():
    last_ticket = Ticket.objects.all().last()
    if last_ticket:
        last_id = last_ticket.id
    else:
        last_id = 0
    code = f'TICKET{200 + last_id + 1}'
    print(f'@@ code : {code}')
    return code


def generate_unique_typeticket_id():
    last_typeticket = TypeTicket.objects.all().last()
    if last_typeticket:
        last_id = last_typeticket.id
    else:
        last_id = 0
    id = f'TYPETICKET{200 + last_id + 1}'
    print(f'@@ id : {id}')
    return id


def tickets_page(request):
    typetickets = TypeTicket.objects.all()
    users = CustomUser.objects.all()
    tickets = Ticket.objects.all()
    statuses=StatutTicket
    return render(request, 'website/tickets.html', {'typetickets': typetickets, 'users': users ,'statuses' : statuses, 'tickets':tickets})
#################################################################################
###################################################################################
##################################################################################
###########   Typestickets     ############




######################################################################################
#####################################################################################
######################################################################################
#######################################################################################
# class UsersView(PermissionRequiredMixin, TemplateView):
#     permission_required = "webiste.can_view_users","can_view_website",
#     template_name = 'website/users.html'
#     model = User

#     def get(self, request, *args, **kwargs):
#         context_original = self.get_context_data(**kwargs)
#         users = User.objects.all()
#         context_perso = {
#             'users': users
#         }
#         context = {**context_original, **context_perso}
#         return self.render_to_response(context)

#     def get_context_data(self, **kwargs):
#         return {
#             **super().get_context_data(**kwargs),
#             **admin.site.each_context(self.request),
#             "opts": self.model._meta,
#         }





class TypesTicketsView(PermissionRequiredMixin, TemplateView):
    permission_required = "webiste.can_view_typeticket"
    template_name = 'website/types.html'
    model = TypeTicket

    def get(self, request, *args, **kwargs):
        context_original = self.get_context_data(**kwargs)
        types = TypeTicket.objects.all()
        context_perso = {
            'types': types
        }
        context = {**context_original, **context_perso}
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            **admin.site.each_context(self.request),
            "opts": self.model._meta,
        }


def types_tickets_datatable(request):
    # Default parameters for pagination
    items_per_page = 10
    page_number = request.GET.get('page')
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', items_per_page))
    sort_column_index = int(request.GET.get('order[0][column]'))
    sort_direction = request.GET.get('order[0][dir]')
   
    search_libelle = request.GET.get('libelle', '')
    search_code = request.GET.get('code', '')

    queryset = TypeTicket.objects.all()
    
    # Filter based on search parameters

    if search_libelle:
        queryset = queryset.filter(libelle__icontains=search_libelle)
    if search_code:
        queryset = queryset.filter(code__icontains=search_code)
                
    
 
    

    sort_columns = {
        0: 'libelle',
        1: 'code',

    }
    sort_column = sort_columns.get(sort_column_index, 'id')

    # Apply sorting
    if sort_direction == 'desc':
        sort_column = '-' + sort_column  # Descending sorting

    queryset = queryset.order_by(sort_column)

    # Paginate the queryset
    paginator = Paginator(queryset, length)
    page_obj = paginator.get_page(page_number)

    # Prepare data for the datatable
    data = []
    for typeticket in page_obj:
        
        update_url = reverse('popup_update_typeticket', args=[typeticket.id])
        delete_url = reverse('delete_typeticket', args=[typeticket.id])

        
        

        
        actions_html = (
        f'<a href="{update_url}" class="typeticket-update-link" style="color:blue;" >Update</a>'
        f'<a href="{delete_url}" class="typeticket-delete-link"  style="color:red;">Delete</a>')

                  

       
        data.append({
            "id": typeticket.id,
            "libelle": typeticket.libelle,
            "code": typeticket.code,
            "actions": actions_html,
            
        })

    return JsonResponse({
        "data": data,
        "recordsTotal": queryset.count(),
        "recordsFiltered": paginator.count,
        "draw": int(request.GET.get('draw', 1)),
    })
    
    
    
def add_typeticket(request):
    if request.method == 'POST':
        libelle = request.POST.get('libelle')
        code = request.POST.get('code')
        

        

        # # Generate a unique ticket code
        # id = generate_unique_typeticket_id()

        # Create and save the ticket
        typeticket = TypeTicket(
            libelle=libelle,
            code=code,
            
        )
        typeticket.save()

        # Return success response
        response = {
            'statut': 1,
            'message': "TypeTicket créé avec succès!",
            'data': {
                'typeticket_id': typeticket.id
            }
        }
    else:
        response = {
            'statut': 0,
            'message': "Methode non autorisée !",
            'data': {}
        }

    return JsonResponse(response)

    
    
    




    
    #####################################################################################################"
def popup_update_typeticket(request, typeticket_id):
    # Retrieve the ticket or raise a 404 error if not found
    typeticket = TypeTicket.objects.get(id=typeticket_id)
    # Prepare the context dictionary
    context = {
        'typeticket': typeticket,
    }
    
    # Render the template with the context
    return render(request, 'website/Modals/types/modal_update_typeticket.html', context)
        
def update_typeticket(request, typeticket_id):
    
    
    if request.method == 'POST':
        typeticket = TypeTicket.objects.get(id=typeticket_id)

        # Mise à jour des champs du ticket avec les données POST
        
        typeticket.libelle = request.POST.get('libelle')
        typeticket.code = request.POST.get('code')
        

        # Enregistrer les modifications
        typeticket.save()

        # Préparer la réponse en cas de succès
        response = {
            'statut': 1,
            'message': "Modification du typeticket effectuée avec succès !",
            'data': {}
        }
        
        # Retourner la réponse JSON
    return JsonResponse(response)







def delete_typeticket(request, typeticket_id):
    if request.method == 'POST':
        typeticket = get_object_or_404(TypeTicket, pk=typeticket_id)
        typeticket.delete()
        response = {
            'statut': 1,
            'message': "Suppression du typeticket effectuée avec succès !",
            'data': {}
        }
        return JsonResponse(response)

    return JsonResponse({
        'statut': 0,
        'message': "Méthode non autorisée. Utilisez POST pour supprimer.",
        'data': {}
    })

# def delete_typeticket(request, typeticket_id):
#     if request.method == 'POST':
#         typeticket = get_object_or_404(TypeTicket, pk=typeticket_id)
#         typeticket.delete()
#         return redirect('')  # Redirect to a success page or another URL after deletion
#     else:
#         return HttpResponseNotAllowed(['POST'])  # Handle other methods if needed
    

#####################################################################################################################""""""
#####################################################################################################################""""""
#####################################################################################################################""""""
#####################################################################################################################""""""
#####################################################################################################################""""""
#####################################################################################################################""""""
#####################################################################################################################""""""
#####################################################################################################################""""""
#####################################################################################################################""""""
#####################################################################################################################""""""
#####################################################################################################################""""""
#####################################################################################################################""""""
#####################################################################################################################""""""
#####################################################################################################################""""""
#####################################################################################################################""""""
#####################################################################################################################""""""
#####################################################################################################################""""""
##########################################   TICKETS   ##################################################################

class TicketsView(PermissionRequiredMixin, TemplateView):
    permission_required = "website.can_view_tickets"

    template_name = 'website/tickets_new.html'
    model = Ticket

    def get(self, request, *args, **kwargs):
        context_original = self.get_context_data(**kwargs)
        tickets = Ticket.objects.all()
        typetickets = TypeTicket.objects.all()
        users = CustomUser.objects.all()
        tickets = Ticket.objects.all()
        statuses=StatutTicket
        context_perso = {
            'tickets': tickets,
            'typetickets':typetickets,
            'statuses':statuses,
            'users':users,
            
            
            
        }
        context = {**context_original, **context_perso}
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            **admin.site.each_context(self.request),
            "opts": self.model._meta,
        }

# def render_to_pdf(request):
#     # Load and render your HTML template with context variables
#     html_string = render_to_string('website/exemple_attestation.html', {'context_variable': 'value'})
    
#     # Convert HTML string to PDF
#     pdf_file = HTML(string=html_string).write_pdf()
    
#     # Return the PDF as a response
#     response = HttpResponse(pdf_file, content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="document.pdf"'
#     return response
    
       

def tickets_datatable(request,status=None):
    # Default parameters for pagination
    items_per_page = 10
    page_number = request.GET.get('page')
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', items_per_page))
    sort_column_index = int(request.GET.get('order[0][column]'))
    sort_direction = request.GET.get('order[0][dir]')
    
        # Retrieve filter parameters

    created_by = request.GET.get('created_by', '')
    search_title = request.GET.get('title', '')
    search_type = request.GET.get('type', '')
    search_status = request.GET.get('status', '')
    date_from = request.GET.get('date_from', None)
    date_to = request.GET.get('date_to', None)
    if status:
         queryset_resolved = Ticket.objects.filter(status=status)
    else:
        queryset = Ticket.objects.all()
    
    # Filter based on search parameters
    # Apply filters
    if status:  # Apply status filter if it's provided
         queryset = queryset_resolved.filter(status=status)
    if created_by:
        queryset = queryset.filter(created_by__username=created_by)
    if search_title:
        queryset = queryset.filter(title__icontains=search_title)
    if search_type:
        queryset = queryset.filter(type_ticket__libelle__icontains=search_type)
    if search_status:
        queryset = queryset.filter(status__icontains=search_status)
    if date_from:
        queryset = queryset.filter(created_at__gte=parse_date(date_from))
    if date_to:
        queryset = queryset.filter(created_at__lte=parse_date(date_to))
        

    sort_columns = {
        0: 'code',
        1: 'type_ticket__libelle',
        2: 'created_by__username',
        3: 'status',
        4: 'title',
        5: 'description',
        6: 'attachments',
        7: 'traite_par',
    }
    sort_column = sort_columns.get(sort_column_index, 'id')

    # Apply sorting
    if sort_direction == 'desc':
        sort_column = '-' + sort_column  # Descending sorting

    queryset = queryset.order_by(sort_column)

    # Paginate the queryset
    paginator = Paginator(queryset, length)
    page_obj = paginator.get_page(page_number)

    # Prepare data for the datatable
    data = []
    for ticket in page_obj:
        
        detail_url = reverse('details_ticket', args=[ticket.id])
        update_url = reverse('popup_update_ticket', args=[ticket.id])
        delete_url = reverse('delete_ticket', args=[ticket.id])

        
        

        
        actions_html = (
        f'<a href="{detail_url}" class="ticket-details-link" style="color:green;">Details</a> '
        f'<a href="{update_url}" class="ticket-update-link" style="color:blue;" data-ticket-id="{{ ticket.id }}" >Update</a>'
        f'<a href="{delete_url}" id="ticket-delete-link" class="badge badge-danger" style="color:red;">Delete</a>')
        
                  

       
        data.append({
            "id": ticket.id,
            "code": ticket.code,
            "type_ticket": ticket.type_ticket.libelle if ticket.type_ticket else "",
            "created_by": ticket.created_by.username if ticket.created_by else "",
            "status": ticket.status,
            "title": ticket.title,
            "description": ticket.description,
            "attachments": ticket.attachments.url if ticket.attachments else "",  # Convertir en URL
            "traite_par": ticket.traite_par.username if ticket.traite_par else "",
            "actions": actions_html, 
            
        })
        # if status:
        #     return JsonResponse({
        #  "data": data,
        #  "recordsTotal": queryset_resolved.count(),
        #  "recordsFiltered": paginator.count,
        #  "draw": int(request.GET.get('draw', 1)),
        #  }) 
        # else:   
            
    return JsonResponse({
                "data": data,
                "recordsTotal": queryset.count(),
                "recordsFiltered": paginator.count,
                "draw": int(request.GET.get('draw', 1)),
                    })       
#######################################""
def details_ticket(request, ticket_id):
    
        ticket = Ticket.objects.get(id=ticket_id)
        return render(request, 'website/Modals/tickets/modal_read_ticket.html', {'ticket': ticket})
    
    
    
    

def popup_update_ticket(request, ticket_id):

    # Retrieve the ticket or raise a 404 error if not found
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    # Retrieve all necessary data
    typetickets = TypeTicket.objects.all()
    users = CustomUser.objects.all()
    statuses = StatutTicket.choices  # List of tuples for choices
    
    # Prepare the context dictionary
    context = {
        'ticket': ticket,
        'typetickets': typetickets,
        'users': users,
        'statuses': statuses
    }
    
    # Render the template with the context
    return render(request, 'website/Modals/tickets/modal_update_ticket.html', context)
        
def update_ticket(request, ticket_id):
    
    
    if request.method == 'POST':
        ticket = Ticket.objects.get(id=ticket_id)

        # Mise à jour des champs du ticket avec les données POST
        ticket.type_ticket_id = request.POST.get('type_ticket')
        ticket.title = request.POST.get('title')
        ticket.description = request.POST.get('description')
        ticket.status = request.POST.get('status')
        ticket.traite_par_id = request.POST.get('traite_par')

        # Enregistrer les modifications
        ticket.save()

        # Préparer la réponse en cas de succès
        response = {
            'statut': 1,
            'message': "Modification du ticket effectuée avec succès !",
            'data': {}
        }
        
    

    # Retourner la réponse JSON
    return JsonResponse(response)


   
###################################################################################################################""

def delete_ticket(request, ticket_id):
    if request.method == 'POST':
        ticket = get_object_or_404(Ticket, pk=ticket_id)
        ticket.delete()
        response = {
            'statut': 1,
            'message': "Suppression du ticket effectuée avec succès !",
            'data': {}
        }
        return JsonResponse(response)

    return JsonResponse({
        'statut': 0,
        'message': "Méthode non autorisée. Utilisez POST pour supprimer.",
        'data': {}
    })






def add_ticket(request):
    if request.method == 'POST':
        typeticket_id = request.POST.get('typeticket')
        title = request.POST.get('title')
        description = request.POST.get('description')
        attachments = request.FILES.get('attachments')
        status = request.POST.get('status')
        traite_par_id = request.POST.get('traite_par')

        # Retrieve objects using get_object_or_404 to handle missing objects
        typeticket = get_object_or_404(TypeTicket, id=typeticket_id)
        traite_par = CustomUser.objects.get(id=traite_par_id) if traite_par_id else None

        # Generate a unique ticket code
        code = generate_unique_ticket_code()

        # Create and save the ticket
        ticket = Ticket(
            created_by=request.user,
            code=code,
            type_ticket=typeticket,
            title=title,
            description=description,
            attachments=attachments,
            traite_par=traite_par,
            status=status,
        )
        ticket.save()

        # Return success response
        response = {
            'statut': 1,
            'message': "Ticket créé avec succès!",
            'data': {
                'ticket_id': ticket.id
            }
        }
    else:
        response = {
            'statut': 0,
            'message': "Methode non autorisée !",
            'data': {}
        }
    
    return JsonResponse(response)









    





def contact(request):
    return render(request, 'website/contact.html')


def about_us(request):
  
        # Récupérer tous les rôles disponibles
    roles = [role[0] for role in RoleUtilisateur.choices]
    users_by_role = {role: CustomUser.objects.filter(role=role) for role in roles}
    return render(request, 'website/about_us.html',{'users_by_role': users_by_role})

def statistics(request):
    
    status = None
    
    number_of_tickets = Ticket.objects.count()  # Récupère le nombre total de tickets
    users = CustomUser.objects.order_by('-date_joined')[:8]
    number_of_users = CustomUser.objects.count()  # Récupère le nombre total de tickets
    number_of_typetickets=TypeTicket.objects.count()  # Récupère le nombre total de typetickets
    resolved_tickets = Ticket.objects.filter(status='RESOLU').count()
    percentage_resolved_tickets = (resolved_tickets / number_of_tickets * 100) if number_of_tickets > 0 else 0
    #tickets_resolved = Ticket.objects.filter(status='RESOLU')
 
    context = {
        
        'number_of_tickets': number_of_tickets,
        'users': users,
        'number_of_users': number_of_users,
        'number_of_typetickets': number_of_typetickets,
        'percentage_resolved_tickets': percentage_resolved_tickets,
        #'tickets_resolved': tickets_resolved,
 

        
    }
    return render(request, 'website/Dashboard&Statistics.html',context)


# def tickets_by_type_view(request):
#     # Aggregate the number of tickets per TypeTicket
#     queryset = Ticket.objects.values('type_ticket__libelle').annotate(ticket_count=Count('type_ticket'))

#     labels = []
#     data = []

#     for entry in queryset:
#         labels.append(entry['type_ticket__libelle'])
#         data.append(entry['ticket_count'])

#     return JsonResponse(data={
#         'labels': labels,
#         'data': data,
#     })

# Function to generate random colors
def generate_random_colors(num_colors):
    colors = []
    for _ in range(num_colors):
        color = "rgba({}, {}, {}, 0.6)".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        colors.append(color)
    return colors
def chart_view(request):
    # Get ticket counts by type

    queryset = TypeTicket.objects.annotate(ticket_count=Count('tickets')).values('libelle', 'ticket_count')

    total_tickets = Ticket.objects.count()  # Get the total number of tickets

    labels = []
    data = []
    
    # Prepare labels and percentages
    for entry in queryset:
        labels.append(entry['libelle'])
        percentage = (entry['ticket_count'] / total_tickets) * 100 if total_tickets > 0 else 0
        data.append(round(percentage, 2))
    
    # Generate a list of colors dynamically
    colors = generate_random_colors(len(labels))
    
    # Return the data and the colors as JSON
    return JsonResponse({
        'labels': labels,
        'data': data,
        'colors': colors,  # Send the colors to the frontend
    })


   
    
    
    
def send_email(request):
    if request.method == "POST":
        motif = request.POST.get('motif', '')
        name = request.POST.get('name', '')
        company = request.POST.get('company', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')

        # Simple validation to check if essential fields are present
        if not all([motif, name, company, email, phone, message]):
            return render(request, 'website/contact.html', {'error': 'All fields are required.'})

        subject = f"New Contact Form Submission: {motif}"
        message_body = f"Name: {name}\nCompany: {company}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message}"

        send_mail(
            subject,
            message_body,
            email,  # From email
            ['azizfadhlaoui2k23@gmail.com'],  # To email
            fail_silently=False,
        )

        return render(request, 'website/contact.html', {'success': True})

    return render(request, 'website/contact.html')