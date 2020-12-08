from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
import phonenumbers

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
        self.fields['username'].label = 'Nickname'
        self.fields['password'].label = 'Password'
        self.fields['password'].help_text = 'Enter password'
        self.fields['password_check'].label = 'Confirm password'
        self.fields['password_check'].help_text = 'Write your password once again please'
        self.fields['first_name'].label = 'First name'
        self.fields['first_name'].help_text = 'Enter your first name'
        self.fields['last_name'].label = 'Last name'
        self.fields['last_name'].help_text = 'Enter yout last name'
        self.fields['email'].label = 'Email'
        self.fields['email'].help_text = 'Enter your email address'

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
        self.fields['username'].label = 'Your Nickname'
        self.fields['username'].help_text = 'Enter your nickname'
        self.fields['password'].label = 'Your Password'
        self.fields['password'].help_text = 'Enter your password'

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
    last_name = forms.CharField()
    phone = forms.CharField()
    buying_type = forms.ChoiceField(widget=forms.Select(), choices=([("self", "User pickup"),("delivery", "Delivery")]))
    date = forms.DateField(widget=forms.SelectDateWidget(), initial=timezone.now())
    address = forms.CharField()
    comments = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'
        self.fields['phone'].label = 'Phone number'
        self.fields['phone'].help_text = 'Enter your phone number'
        self.fields['buying_type'].label = 'Buying type'
        self.fields['buying_type'].help_text = 'Choose the buying type'
        self.fields['address'].label = 'Address'
        self.fields['address'].help_text = 'Enter address of delievery'
        self.fields['comments'].label = 'Additional info'
        self.fields['date'].label = 'Date of delivery'
        self.fields['date'].help_text = 'Choose the date of delivery'

    def clean(self):
        date = self.cleaned_data['date']
        if date < timezone.now().date():
            raise forms.ValidationError('Incorrect date!')
        phone = self.cleaned_data['phone']
        try:
            parsed = phonenumbers.parse(phone)
        except phonenumbers.NumberParseException as e:
            raise forms.ValidationError('Incorrect phone number!')

