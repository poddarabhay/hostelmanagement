from django import forms
from django.core.exceptions import ValidationError
from django.core import validators
from django.contrib.auth.models import User
from .models import Hostel,Hostels,Student
from django.forms import ModelForm
from django.db.models import Max, IntegerField
from django.contrib.auth.forms import UserCreationForm

class StudentLoginForm(forms.Form):
    usn= forms.CharField(label='USN', max_length=10, validators=[validators.RegexValidator('1[s|S][i|I][0-9][0-9][a-z|A-Z][a-z|A-Z][0-9][0-9][0-9]')], widget=forms.TextInput(attrs={'class':'form-control form-control-danger','placeholder':'USN'}))
    password=forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control form-control-danger','placeholder':'Password'}))
        

class studentForm(ModelForm):
    class Meta:
        model=Student
        fields=["usn","fname","lname","gender","bill","billcategory","hostel","priority"]
        initial={'priority': 1}
        widgets={
            'usn':forms.TextInput(attrs={'class':'form-control','placeholder':'USN'}),
            'lname':forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
            'fname':forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'gender':forms.Select(attrs={'class':'form-control'}),
            'bill':forms.TextInput(attrs={'class':'form-control','placeholder':'Bill Number'}),
            'billcategory':forms.Select(attrs={'class':'form-control'}),
            'hostel':forms.Select(attrs={'class':'form-control'}),
            'priority':forms.HiddenInput(),
        }
    def setPriority(self):
        ob=Student.objects.filter(hostel=self.cleaned_data['hostel'],billcategory=self.cleaned_data['billcategory'])
        if ob.count()>0:
            pri=ob.aggregate(Max('priority',output_field=IntegerField()))['priority__max']+1
        else:
            pri=1
        self.priority=pri

class createHostelForm(ModelForm):
    class Meta:
        model=Hostels
        fields=["hname","year","gender"]
        widgets={
            'hname':forms.TextInput(attrs={'class':'form-control has-danger','placeholder':'Hostel Name'}),
            'year':forms.Select(attrs={'class':'form-control','placeholder':'Year'}),
            'size':forms.HiddenInput(),
            'gender':forms.Select(attrs={'class':'form-control'}),
            'asize':forms.HiddenInput()
        }

class createFloorForm(forms.Form):
    Floor=forms.IntegerField(label='Floor', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Floor Number'}))
    res3= forms.CharField(label='Three resident rooms', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Three resident rooms'}))
    res2= forms.CharField(label='Two resident rooms', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Two resident rooms'}))
    res1= forms.CharField(label='One resident rooms', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'One resident rooms'}))

class chooseRoomForm(forms.Form):
    room=forms.ModelChoiceField(label='Room Number', widget=forms.Select(attrs={'class':'form-control'}),queryset=Hostel.objects.all())
    def roomBlock(self,hostel,billcategory):
        self.fields['room'].queryset = hostel.hosteldetails.filter(size=billcategory,status=3)

class studentSignUp(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','password1', 'password2', )
        validators={
            'username':validators.RegexValidator('1[s|S][i|I][0-9][0-9][a-z|A-Z][a-z|A-Z][0-9][0-9][0-9]'),
        }
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control form-control-danger','placeholder':'USN'}),
            'password1':forms.PasswordInput(attrs={'class':'form-control form-control-danger','placeholder':'Password'}),
            'password2':forms.PasswordInput(attrs={'class':'form-control form-control-danger','placeholder':'Enter your Password Again'}),
        }
    def clean_username(self):
        username=self.cleaned_data['username']
        if Student.objects.filter(usn=username).count()==0:
            raise ValidationError("Bill Not Paid")
        return username
