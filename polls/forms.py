from django import forms
from django.utils import timezone
from django.contrib.auth.models import User

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_check = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'password_check',
            'first_name',
            'last_name',
            'email',
        ]
    def __init__(self,*args,**kwargs):
        super(RegistrationForm,self).__init__(*args,**kwargs)
        self.fields['username'].label = 'Your nickname'
        self.fields['password'].label = 'Password'
        self.fields['password'].help_text = 'Enter your new password'
        self.fields['password_check'].label = 'Confirm your new password'
        self.fields['password_check'].help_text = 'Write once again your password'
        self.fields['first_name'].label = 'Your first name'
        self.fields['last_name'].label = 'Your last name'
        self.fields['email'].label = 'Your email'
        self.fields['email'].help_text = 'Enter your correct email address'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        email = self.cleaned_data['email']
        password_check = self.cleaned_data['password_check']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("User with this name already exists")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("User with this email already exists")
        if password != password_check:
            raise forms.ValidationError("Password and Password check are not similar.Try again")

class LogingForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self,*args,**kwargs):
        super(LogingForm,self).__init__(*args,**kwargs)
        self.fields['username'].label = 'Your nickname'
        self.fields['password'].label = 'Password'
        self.fields['password'].help_text = 'Enter your new password'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Incorrect nickname or password.Try again")
        user = User.objects.get(username=username)
        if user and not user.check_password(password):
            raise forms.ValidationError('Incorrect password!')

class OrderForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField(required=False)
    phone = forms.CharField()
    buying_type = forms.ChoiceField(widget=forms.Select(), choices=([("self", "User pickup"),("delivery", "Delivery")]))
    date = forms.DateField(widget=forms.SelectDateWidget(), initial=timezone.now())
    address = forms.CharField(required=False)
    comments = forms.CharField(widget=forms.Textarea, required=False)
    
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'
        self.fields['phone'].label = 'Your phone'
        self.fields['buying_type'].label = 'Buying type'
        self.fields['address'].label = 'Your address'
        self.fields['comments'].label = 'Your addictional comments'
        self.fields['date'].label = 'Date of delivery'

    def clean(self):
        date = self.cleaned_data['date']
        if date < timezone.now().date():
            raise forms.ValidationError('Incorrect date!')

