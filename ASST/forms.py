import os
from .ip2 import face_detect
from .image_decoder import save_screenshot
from fractions import Fraction
import pyrebase
from crispy_forms.helper import FormHelper
from django import forms
from ASST.config import *
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User



# class forgotpassForm(forms.Form):
#     email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={
#         'placeholder': ('enter your email here'), 'class': ' form-control form-control-sm', 'text-color': 'white'
#     }), required=True)


class signInForm(forms.Form):

    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={
        'placeholder': ('enter your email here'), 'for': 'exampleInputEmail1', 'class': ' form-floating mb-3', 'text-color': 'white'
    }), required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-floating mb-3', 'placeholder': ('enter password here'), }))


class signUpForm(forms.Form):

    email = forms.EmailField(label='E-mail \n', required=True, widget=forms.EmailInput(attrs={
        'placeholder': ("enter society's email here"), 'class': 'mb-3 form-control '
    }))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'mb-3 form-control '}))
    sname = forms.CharField(label='society_name \n',  widget=forms.TextInput(attrs={
        'placeholder': ('enter Society name here'), 'class': 'mb-3 form-control '
    }))
    nroom = forms.IntegerField(label='number of rooms \n', widget=forms.NumberInput(attrs={
        'placeholder': ('enter number of rooms here'), 'class': 'mb-3 form-control'
    }))
    address = forms.CharField(label='Society Address', widget=forms.TextInput(attrs={
        'placeholder': ('enter address here'), 'class': 'mb-3 form-control'
    }))

    # class Meta:
    #     model = User
    #     fields = ['email', 'password', 'sname', 'nroom', 'address']


class visitcreateForm(forms.Form):
    fname = forms.CharField(label='First Name',  widget=forms.TextInput(attrs={
        'placeholder': ('enter first name here'), 'class': 'mb-3 form-control', 'style': 'width: 50 %'
    }))
    contact1 = forms.IntegerField(label='Primary Contact Number', widget=forms.NumberInput(attrs={
        'placeholder': ('enter contact number here'), 'class': 'mb-3 form-control', 'style': 'width: 50 %'
    }))
    contact2 = forms.IntegerField(label='Secondary Contact Number', widget=forms.NumberInput(attrs={
        'placeholder': ('enter contact number here'), 'class': 'mb-3 form-control ', 'style': 'width: 50 %'
    }))
    occupation = forms.CharField(label='Occupation',  widget=forms.TextInput(attrs={'placeholder': (
        'enter occupation here'), 'class': 'mb-3 form-control', 'style': 'width: 50 %'}))

    adhar = forms.RegexField(regex="^[2-9]{1}[0-9]{3}\\s[0-9]{4}\\s[0-9]{4}$")
    image_data = forms.CharField(widget=forms.HiddenInput())

    def clean_image_data(self):

        print(type(self.cleaned_data))
        image_string = self.cleaned_data.get('image_data')
        image_list = image_string.strip().split(' ')
        for image in image_list:
            if image:
                print('in form')

                filename = save_screenshot('temp', image)
                if face_detect(filename) < 1:
                    print('error')
                    raise forms.ValidationError('No face Detected in an image')
                    break
                elif face_detect(filename) > 1:
                    print('error')
                    raise forms.ValidationError(
                        'More than one face Detected in an image')
                    break
                os.remove(filename)
            else:
                print('no image')
        return image_list

    def clean_adhar(self):
        print(self.society)
        adhar_string = self.cleaned_data.get('adhar')
        users = database.child(self.society).child('users').get()
        print(users.val())
        available_adhars = []
        if users.val():
            for user in users.each():
                available_adhars.append(str(user.val()['adhar']))
            if adhar_string in available_adhars:
                raise forms.ValidationError('adhar number already present')
        return adhar_string

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = "visitcreateForm"
        self.helper.form_method = 'post'
        self.society = kwargs.pop('society')

        super(visitcreateForm, self).__init__(*args, **kwargs)


class usercreateForm(forms.Form):
    fname = forms.CharField(label='First Name',  widget=forms.TextInput(attrs={
        'placeholder': ('enter first name here'), 'class': 'mb-3 form-control', 'style': 'width: 50 %'
    }))
    contact1 = forms.IntegerField(label='Primary Contact Number', widget=forms.NumberInput(attrs={
        'placeholder': ('enter contact number here'), 'class': 'mb-3 form-control', 'style': 'width: 50 %'
    }))
    contact2 = forms.IntegerField(label='Secondary Contact Number', widget=forms.NumberInput(attrs={
        'placeholder': ('enter contact number here'), 'class': 'mb-3 form-control', 'style': 'width: 50 %'
    }))

    adhar = forms.RegexField(regex="^[2-9]{1}[0-9]{3}\\s[0-9]{4}\\s[0-9]{4}$")
    image_data = forms.CharField(widget=forms.HiddenInput())

    def clean_image_data(self):

        print(type(self.cleaned_data))
        image_string = self.cleaned_data.get('image_data')
        image_list = image_string.strip().split(' ')
        for image in image_list:
            if image:
                print('image detected')
                print(image[0:10])
                filename = save_screenshot('temp', image)
                print(face_detect(filename))
                if face_detect(filename) < 1:
                    raise forms.ValidationError('No face Detected in an image')
                elif face_detect(filename) > 1:
                    raise forms.ValidationError(
                        'More than one face Detected in an image')
                os.remove(filename)
            else:
                print('no image')
        return image_list

    def clean_adhar(self):
        print(self.society)
        adhar_string = self.cleaned_data.get('adhar')
        users = database.child(self.society).child('users').get()
        print(users.val())
        available_adhars = []
        if users.val():
            for user in users.each():
                available_adhars.append(str(user.val()['adhar']))
            if adhar_string in available_adhars:
                raise forms.ValidationError('adhar number already present')
        return adhar_string

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = "usercreateForm"
        self.helper.form_method = 'post'
        self.society = kwargs.pop('society')

        super(usercreateForm, self).__init__(*args, **kwargs)


class admincreateForm(forms.Form):

    email = forms.EmailField(label='E-mail \n', required=True, widget=forms.EmailInput(attrs={
        'placeholder': ("enter society's email here"), 'class': 'form-control mb-3'
    }))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': ('enter password'), 'class': 'form-control mb-3'}))

    roomnum = forms.IntegerField(label='Room Number', widget=forms.NumberInput(attrs={
        'placeholder': ('enter room number here'), 'class': 'form-control mb-3', 'style': 'width: 50 %'
    }))


class watchmancreateForm(forms.Form):

    fname = forms.CharField(label='First Name',  widget=forms.TextInput(attrs={
        'placeholder': ('enter first name here'), 'class': 'mb-3 form-control', 'style': 'width: 50 %'
    }))

    email = forms.EmailField(label='E-mail \n', required=True, widget=forms.EmailInput(attrs={
        'placeholder': ("enter society's email here"), 'class': 'form-control mb-3'
    }))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': ('enter password'), 'class': 'form-control mb-3'}))


class reasonForm(forms.Form):
    reason = forms.CharField(label='Reason',  widget=forms.TextInput(attrs={
        'placeholder': ('enter reason to reject here'), 'class': 'mb-3 form-control', 'style': 'width: 50 %'
    }))


class DateForm(forms.Form):
    date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
