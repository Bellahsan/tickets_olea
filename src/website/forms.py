from django import forms
from .models import *
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'role', 'linkedin_url',]  # Incluez linkedin_url ici
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', )  # Add fields you want to include

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class TicketForm(forms.ModelForm):
      class Meta:
        model = Ticket
        fields = ['type_ticket', 'title', 'description', 'attachments', 'status', 'traite_par']

      def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type_ticket'].queryset = TypeTicket.objects.all()
        # You can customize fields here if necessary
        
        
class TypeTicketForm(forms.ModelForm):
    class Meta:
        model = TypeTicket  # Corrected to link to TypeTicket model
        fields = ['libelle', 'code']  # Fields to be included in the form
        widgets = {
            'libelle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le libellé du type de ticket'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le code du type de ticket'
            }),
        }
        labels = {
            'libelle': 'Libellé',
            'code': 'Code',
        }


class ContactForm(forms.Form):
    motif = forms.ChoiceField(choices=[('question', 'Question'), ('feedback', 'Feedback')], label='Motif')
    name = forms.CharField(max_length=100, label='Nom & Prénom(s)')
    company = forms.CharField(max_length=100, label='Société')
    email = forms.EmailField(label='E-mail')
    phone = forms.CharField(max_length=20, label='Téléphone')
    message = forms.CharField(widget=forms.Textarea, label='Message')