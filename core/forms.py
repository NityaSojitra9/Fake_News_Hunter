from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class ArticleURLForm(forms.Form):
    url = forms.URLField(
        label='Article URL',
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter the URL of the article to analyze'
        })
    )
    file = forms.FileField(
        label='Or upload a file',
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.txt,.pdf'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        url = cleaned_data.get('url')
        file = cleaned_data.get('file')
        
        if not url and not file:
            raise forms.ValidationError("Please provide either a URL or upload a file.")
        
        if url and file:
            raise forms.ValidationError("Please provide either a URL or upload a file, not both.")
        
        return cleaned_data

class UserRegistrationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]
    
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        required=True,
        initial='user',
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='Select your role: User for regular access, Admin for administrative privileges'
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'role', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'bio', 'profile_picture']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        } 