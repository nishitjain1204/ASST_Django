import os
from django.shortcuts import render, redirect, HttpResponse

from django.contrib import auth
from django.contrib import messages
from .forms import signInForm, signUpForm, visitcreateForm, admincreateForm, usercreateForm, watchmancreateForm, reasonForm
from collections import OrderedDict
from .image_decoder import save_screenshot
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from ASST.config import *
from datetime import date
import pandas as pd
from csv import DictWriter
import numpy as np
from ASST.notificationpush import notificationsend
import openpyxl
from wsgiref.util import FileWrapper







def pending_visitors(request):

    if check_user_authenticity(request.session['session_id']) == True and request.session['position'] == 'admin':
        form = reasonForm(request.POST)
        pending_visitors = database.child(
            request.session['society_name']).child('visitors').child('Non_validated').child('pending').child(request.session['roomnum']).get()
        pending_visitors_list = []
        print(pending_visitors.val())

        if pending_visitors.val():
            for user in pending_visitors.each():
                user_dict = user.val()
                print(user.val())
                user_dict['key'] = user.key()
                pending_visitors_list.append(user_dict)
        return render(request, "pending_visitors.html", {'users': pending_visitors_list, 'form': form})
    else:
        return redirect('/')
    print("========", request.GET)
    return render(request, "pending_visitors.html")


def welcome(request):
    try:
        if isSignedIn(request) == True:
            return(redirect('/postsignin'))
    except:
        pass
    return render(request, "welcome.html")


def isSignedIn(request):
    if check_user_authenticity(request.session['session_id']) == True:
        return True
    else:
        return False


def panel(request):
    if 'session_id' in request.session and request.session['position'] == 'secretary' and check_user_authenticity(request.session['session_id']) == True:
        existing_email = request.session['email']
        society_name = request.session['society_name']
        pending_users = database.child(
            society_name).child('pending_users').get()
        pending_users_list = []
        print(pending_users.val())

        if pending_users.val():
            for user in pending_users.each():
                user_dict = user.val()
                user_dict['key'] = user.key()
                pending_users_list.append(user_dict)
        return render(request, "panel.html", {'users': pending_users_list})

    return render(request, "panel.html")


def shift(request):
    if check_user_authenticity(request.session['session_id']) == True:
        society_name = request.session['society_name']
        print("yes panel baby", society_name)
        pending_users = database.child(
            society_name).child('pending_users').get()
        pending_users_list = []

        if pending_users.val():
            for user in pending_users.each():
                pending_users_list.append(user)
        for a in pending_users_list:
            adhar = (a.val()['adhar'])
            contact1 = (a.val()['contact1'])
            contact2 = (a.val()['contact2'])
            fname = (a.val()['fname'])
            image = (a.val()['image'])
            roomnum = (a.val()['roomnum'])
            data = {"adhar": adhar,
                    "contact1": contact1, "contact2": contact2, "fname": fname, "image": image, "roomnum": roomnum}
            database.child(society_name).child('shifted_users').push(data)
            break

    return render(request, "panel.html")


def adminusers(request):
    # and request.session['position']=='secretary'
    if check_user_authenticity(request.session['session_id']) == True:
        roomnum = request.session['roomnum']
        print(roomnum)
        existing_email = request.session['email']
        society_name = request.session['society_name']
        registered_users = database.child(society_name).child('users').get()
        registered_users_list = []
        print(registered_users.val())
        if registered_users.val():
            for user in registered_users.each():
                registered_users_list.append(user)
        return render(request, "adminusers.html", {'users': registered_users_list, 'roomnum': roomnum})


def createuser(request):
    if check_user_authenticity(request.session['session_id']) == True and request.session['position'] == 'admin':
        form = usercreateForm(society=request.session['society_name'])
        if request.method == 'POST':
            print('data posted')
            form = usercreateForm(
                request.POST, society=request.session['society_name'])
            if form.is_valid():
                print('form valid')

                # print(sname.val())
                fname = form.cleaned_data['fname']
                contact1 = form.cleaned_data['contact1']
                contact2 = form.cleaned_data['contact2']
                adhar = form.cleaned_data['adhar']
                image_data = form.cleaned_data['image_data']
                print('image list received')
                i = 0

                society_name = request.session['society_name']
                print(society_name)
                image_url_list = []
                # uploading images to firebase storage
                for image in image_data:
                    print('data received') if image else None
                    # print(image)
                    filename = str(adhar)+str(datetime.now())+str(i)
                    foldername = str(adhar)
                    foldername = ''.join(e for e in foldername if e.isalnum())
                    foldername = foldername
                    image_name = save_screenshot(filename, image)
                    image_url = image_uploader(
                        society_name, foldername, image_name)
                    image_url_list.append(image_url)
                    os.remove(image_name)
                    i += 1

                data = {
                    "fname": fname,
                    "contact1": str(contact1),
                    "contact2": str(contact2),
                    "roomnum": request.session['roomnum'],
                    "adhar": str(adhar),
                    'image': (image_url_list)

                }

                pushed_user = database.child(
                    society_name).child('pending_users').push(data)
                print(pushed_user)

                return render(request, "output.html")
            else:
                print('form invalid')
                print(form.errors)
                if 'image_data' in form.errors:
                    print(type(form.errors.as_data()))
                    img_error = ''.join(form.errors.as_data()['image_data'][0])
                    if img_error == 'This field is required.'.strip():
                        img_error = 'Please click image'
                    return render(request, 'createuser.html', {"form": form, "img_error": img_error})
    else:
        return redirect('/')

    return render(request, 'createuser.html', {"form": form})


def admins(request):
    if check_user_authenticity(request.session['session_id']) == True and request.session['position'] == 'admin':
        roomnum = request.session['roomnum']
        admindata = database.child(request.session['society_name']).child(
            'admin').child(roomnum).get()
        print(admindata.val())
        return redirect('/')


def image_uploader(society_name, foldername, name):
    print(society_name+'/' + foldername+'/'+name)
    storage.child(society_name+'/' + foldername+'/'+name).put(name)
    return storage.child(society_name+'/' + foldername+'/'+name).get_url('None')


def visitorvalidation(request, key, decision):

    token = database.child(
        request.session['society_name']).child('details').child(
        'watchmanfcmtoken').get().val()
    print(token)
    reg_ids = []
    reg_ids.append(token)

    user = database.child(request.session['society_name']).child('visitors').child(
        'Non_validated').child('pending').child(request.session['roomnum']).child(key).get().val()

    if int(decision) == 1:
        print("visitor accepted")

        database.child(request.session['society_name']).child('visitors').child(
            'Non_validated').child('adminvalidated').push(user)
        database.child(request.session['society_name']).child('visitors').child(
            'Non_validated').child('pending').child(request.session['roomnum']).child(key).remove()

        body = "the visitor "+user['name']+' was accepted'
        click_action = '/watchmanpanel'

    elif int(decision) == 0:
        database.child(request.session['society_name']).child('visitors').child(
            'Non_validated').child('pending').child(request.session['roomnum']).child(key).remove()
        body = "the visitor"+user['name'] + \
            'was rejected\n'+'reason : '+request.GET['reason']
        click_action = '/watchmanpanel'

    notificationsend(reg_ids, 'Visitor accepted', body, click_action)

    return redirect('/pending_visitors')


def secretaryvalidation(request, key, decision):
    if int(decision) == 1:
        print('accepted')
        user = database.child(request.session['society_name']).child(
            'pending_users').child(key).get().val()
        print(user)
        roomnum = user['roomnum']
        database.child(request.session['society_name']).child(
            'users').push(user)
        myadmin = database.child((request.session['society_name'])).child(
            'Admins').child(roomnum).get()
        print(myadmin.val())
        if myadmin.val()['registered_users'] == 0:
            database.child(request.session['society_name']).child('Admins').child(
                roomnum).set({"user_list": [key], 'registered_users': 1})
        else:
            user_list = database.child(request.session['society_name']).child(
                'Admins').child(roomnum).child('user_list').get().val()
            user_list.append(key)
            number_of_users = myadmin.val()['registered_users']+1
            database.child(request.session['society_name']).child('Admins').child(roomnum).set(
                {"user_list": user_list, 'registered_users': number_of_users})

        database.child(request.session['society_name']).child(
            'pending_users').child(key).remove()
        print('user pushed to db')
        messages.info(
            request, f'Member Accepted')
    elif int(decision) == 0:
        user = database.child(request.session['society_name']).child(
            'pending_users').child(key).get().val()
        print('rejected')
        files = storage.child(request.session['society_name']).child(
            ''.join(e for e in user['adhar'] if e.isalnum())).list_files()
        if files:
            for file in files:
                name = file.name.strip().split('/')
                if name[1] == str(''.join(e for e in user['adhar'] if e.isalnum())).strip():
                    storage.delete(file.name)
        database.child(request.session['society_name']).child(
            'pending_users').child(key).remove()
        messages.info(
            request, f'Member Rejected')

    return redirect('/panel')


def signin(request):
    try:
        if isSignedIn(request) == True:
            return(redirect('/postsignin'))
    except:
        pass
    if request.method == 'POST':
        form = signInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = authe.sign_in_with_email_and_password(email, password)
                session_id = user['idToken']
                print(check_user_authenticity(session_id))
                if user and check_user_authenticity(session_id) == True:
                    print('user signed in')
                session_id = user['idToken']
                # print(session_id)

                request.session['session_id'] = str(session_id)
                request.session['email'] = str(email)
                existing_email = request.session['email']
            except Exception as e:
                print(e)
                messages.info(
                    request, f'Please check your email or password')
                return redirect('signin')
                # return render(request, "signin.html", {'form': form})

            sname = database.child('Secretary_mapping').get()
            for key in sname.each():
                if (key.val()['email'] == existing_email):
                    request.session['society_name'] = key.val()['sname']
                    society_name = key.val()['sname']
                    print(society_name)
                    if 'isSecretary' in key.val():
                        print(key.val()['isSecretary'])
                        if key.val()['isSecretary'] == True:
                            request.session['position'] = 'secretary'
                            return redirect('/postsignin')
                    if 'iswatchman' in key.val():
                        if key.val()['iswatchman'] == True:
                            request.session['position'] = 'watchman'
                            return redirect('/postsignin')
                    else:
                        request.session['position'] = 'admin'
                        request.session['roomnum'] = key.val()['roomnum']
                        print('user is an admin')
                        return redirect('/postsignin')
                    break

    form = signInForm()
    return render(request, "signin.html", {"form": form})


def logout(request):
    if 'roomnum' in request.session and 'FCMToken' in request.session:
        myadmin = database.child((request.session['society_name'])).child(
            'Admins').child(request.session['roomnum']).child('signedinDevices').get()
        devices_list = myadmin.val()
        if request.session['FCMToken'] in devices_list:
            devices_list.remove(request.session['FCMToken'])
        database.child((request.session['society_name'])).child('Admins').child(
            request.session['roomnum']).child('signedinDevices').set(devices_list)

    auth.logout(request)
    return redirect('/')
    # return render(request, "signin.html", {"form": signInForm()})


def secretarysignup(request):
    form = signUpForm()
    if request.method == 'POST':
        form = signUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            nroom = form.cleaned_data['nroom']
            sname = form.cleaned_data['sname']
            address = form.cleaned_data['address']
            messages.success(request, f'Account created for Society {sname}!')
            try:
                user = authe.create_user_with_email_and_password(
                    email, password)

            except:
                print('error')
                message = "unable to create account, try again"
                return redirect('/')
            uid = user['localId']

            data = {"nroom": nroom, "address": address, "email": email}
            database.child(sname).child('details').set(data)

            data = {"email": email, "sname": sname, "isSecretary": True}
            database.child('Secretary_mapping').push(data)

            return redirect('/')

    return render(request, "signup.html", {"form": form})


def output(request):
    return render(request, "output.html")


def forgotpass(request):
    return render(request, "forgotpass.html")


def postsignin(request):

    print('society name : ', request.session['society_name'])
    if request.session['position'] == 'secretary':

        # wb = openpyxl.load_workbook('spreadsheet.xlsx')
        # sheet = wb.active
        # sheet.column_dimensions['A'].width = 100
        # sheet.column_dimensions['A'].height = 100

        # wb.save('spreadsheet.xlsx')

        # df = pd.DataFrame.from_dict(excel))
        # print(df)
        # df.to_excel('players.xlsx')
        print('user is a secretary')
        return render(request, "secretarypostsignin.html", {'n': request.session['society_name']})
    elif request.session['position'] == 'admin':
        print('user is admin')
        roomnum = request.session['roomnum']
        users_logged = database.child(request.session['society_name']).child(
            'Admins').child(roomnum).get()
        return render(request, "adminpostsignin.html", {'roomnum': roomnum})

    elif request.session['position'] == 'watchman':
        print('user is watchman')
        # users_logged = database.child(request.session['society_name']).child(
        #     'Admins').child(roomnum).get()
        return redirect('/watchmanpanel')


def visitcreate(request):
    if check_user_authenticity(request.session['session_id']) == True and request.session['position'] == 'secretary':
        print('email in request')

        form = visitcreateForm(society=request.session['society_name'])
        if request.method == 'POST':
            print('data posted')
            form = visitcreateForm(
                request.POST, society=request.session['society_name'])
            if form.is_valid():
                print('form valid')

                # print(sname.val())
                fname = form.cleaned_data['fname']
                contact1 = form.cleaned_data['contact1']
                contact2 = form.cleaned_data['contact2']
                occupation = form.cleaned_data['occupation']
                adhar = form.cleaned_data['adhar']
                image_data = form.cleaned_data['image_data']
                print('image list received')
                i = 0

                society_name = request.session['society_name']
                print(society_name)

                # uploading images to firebase storage
                for image in image_data:
                    filename = str(adhar)+str(datetime.now())+str(i)
                    foldername = str(adhar)
                    foldername = ''.join(e for e in foldername if e.isalnum())
                    image_name = save_screenshot(filename, image)
                    image_url = image_uploader(
                        society_name, foldername, image_name)
                    os.remove(image_name)
                    i += 1

                # data upload to firebase rt db
                data = {
                    "fname": fname,
                    "contact1": str(contact1),
                    "contact2": str(contact2),
                    "occupation": occupation,
                    "adhar": str(adhar),
                    'image': (image_url),
                    'isresident': False

                }
                print(image_url)
                database.child(society_name).child('users').push(data)
                print('form is valid')
                return render(request, "output.html")
            else:
                print('form invalid')
                print(form.errors)
                if 'image_data' in form.errors:
                    print(type(form.errors.as_data()))
                    img_error = ''.join(form.errors.as_data()['image_data'][0])
                    if img_error == 'This field is required.'.strip():
                        img_error = 'Please click image'
                    print(img_error)
                    return render(request, 'visitcreate.html', {"form": form, "img_error": img_error})
    else:
        return redirect('/')

    return render(request, 'visitcreate.html', {"form": form})


def admincreate(request):
    if check_user_authenticity(request.session['session_id']) == True and request.session['position'] == 'secretary':
        print('email in request')

        form = admincreateForm()
        if request.method == 'POST':
            print('data posted')
            form = admincreateForm(request.POST)
            if form.is_valid():
                print('form valid')

                # print(sname.val())
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                roomnum = form.cleaned_data['roomnum']
                society_name = request.session['society_name']
                print(society_name)
                try:
                    user = authe.create_user_with_email_and_password(
                        email, password)
                except:
                    print('error')
                    message = "unable to create account, try again"
                    return redirect('/admincreate')
                data = {'registered_users': 0}
                database.child(society_name).child(
                    'Admins').child(str(roomnum)).set(data)
                print('registration Successful')
                data = {"email": email,
                        "sname": society_name, 'roomnum': roomnum}
                database.child('Secretary_mapping').push(data)
                messages.success(
                    request, f'Admin account created successfully!')

                return redirect('/')
            else:
                print('form invalid')
                print(form.errors)

    else:
        return redirect('/')

    return render(request, 'admincreate.html', {"form": form})


@ csrf_exempt
def fcmtoken_save(request):
    if request.POST.get("token"):
        token = request.POST.get("token")
        print(token)
        if request.session['position'] == 'admin':
            roomnum = request.session['roomnum']
            myadmin = database.child((request.session['society_name'])).child(
                'Admins').child(roomnum).child('signedinDevices').get()

            if str(myadmin.val()) == 'None':
                print('No admin devices signed in :', str(myadmin.val()))
                database.child(request.session['society_name']).child(
                    'Admins').child(roomnum).child('signedinDevices').set([token])
            else:
                print('devices found signedin')
                if token not in myadmin.val():
                    print('devices found signedin')
                    devices_list = myadmin.val()
                    devices_list.append(token)
                    database.child(request.session['society_name']).child('Admins').child(
                        roomnum).child('signedinDevices').set(devices_list)

        request.session['FCMToken'] = request.POST.get("token")
        return HttpResponse(request.POST.get("token"))


@ csrf_exempt
def fcmtoken_save_watchman(request):
    if request.POST.get("token"):
        token = request.POST.get("token")
        print(token)
        if request.session['position'] == 'watchman':
            society = request.session['society_name']
            database.child(society).child('details').child(
                'watchmanfcmtoken').set(str(token))

        request.session['FCMToken'] = request.POST.get("token")
        return HttpResponse(request.POST.get("token"))


class ServiceWorkerView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'firebase-messaging-sw.js', content_type="application/javascript")


def watchmancreate(request):
    if check_user_authenticity(request.session['session_id']) == True and request.session['position'] == 'secretary':
        form = watchmancreateForm()
        if request.method == 'POST':
            print('data posted')
            form = watchmancreateForm(request.POST)
            if form.is_valid():
                print('form valid')

                # print(sname.val())
                name = form.cleaned_data['fname']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                society_name = request.session['society_name']
                print(society_name)
                try:
                    user = authe.create_user_with_email_and_password(
                        email, password)
                except:
                    print('error')
                    message = "unable to create account, try again"
                    return redirect('/watchmancreate')
                print('registration Successful')
                data = {"name": name, "email": email,
                        "sname": society_name, 'iswatchman': True}
                database.child('Secretary_mapping').push(data)
                return redirect('/')
            else:
                print('form invalid')
                print(form.errors)

    else:
        return redirect('/')

    return render(request, 'watchmancreate.html', {"form": form})


def watchmanpanel(request):

    if check_user_authenticity(request.session['session_id']) == True and request.session['position'] == 'watchman':
        adminvalidatedusers = database.child(request.session['society_name']).child(
            'visitors').child('Non_validated').child('adminvalidated').get()

        adminvalidatedusers_list = []
        print(adminvalidatedusers.val())

        if adminvalidatedusers.val():
            for user in adminvalidatedusers.each():
                user_dict = user.val()
                print(user.val())
                user_dict['key'] = user.key()
                adminvalidatedusers_list.append(user_dict)
        return render(request, "watchmanpanel.html", {'users': adminvalidatedusers_list})
    else:
        return redirect('/')
    return render(request, 'watchmanpanel.html')


def watchmanvalidate(request, key, decision):

    if check_user_authenticity(request.session['session_id']) == True and request.session['position'] == 'watchman':
        if int(decision) == 1:

            adminvalidatedacccepteduser = database.child(request.session['society_name']).child(
                'visitors').child('Non_validated').child('adminvalidated').child(key).get().val()
            roomnum = adminvalidatedacccepteduser['roomnum']
            print(roomnum)
            database.child(request.session['society_name']).child('Entry_Logs').child(
                str(date.today())).push(adminvalidatedacccepteduser)
            database.child(request.session['society_name']).child('visitors').child(
                'Non_validated').child('adminvalidated').child(key).remove()
            reg_ids = database.child(request.session['society_name']).child(
                'Admins').child(roomnum).child('signedinDevices').get().val()

            body = "the visitor " + \
                adminvalidatedacccepteduser['name']+' was let in'
            click_action = '/watchmanpanel'
            notificationsend(reg_ids, 'Visitor accepted', body, click_action)

        elif int(decision) == 0:
            adminvalidatedacccepteduser = database.child(request.session['society_name']).child(
                'visitors').child('Non_validated').child('adminvalidated').child(key).get().val()
            roomnum = adminvalidatedacccepteduser['roomnum']
            database.child(request.session['society_name']).child('visitors').child(
                'Non_validated').child('adminvalidated').child(key).remove()
            reg_ids = database.child(request.session['society_name']).child(
                'Admins').child(roomnum).child('signedinDevices').get().val()
            body = "the visitor " + \
                adminvalidatedacccepteduser['name']+' left before u responded'
            click_action = '/watchmanpanel'
            notificationsend(reg_ids, 'Visitor accepted', body, click_action)
    return redirect('/watchmanpanel')


def report(request):
    print('date:')
    print(request.GET)
    return render(request, "report.html")


@csrf_exempt
def get_excel_sheet(request):
    print('in get excel sheet')
    print(request.GET)

    if request.GET['date'] != '':
        date_from_request = request.GET['date']
        excel = database.child(request.session['society_name']).child(
            'Entry_Logs').child(date_from_request).get()
        if excel.val() != 'None':
            print(excel.val())
            excel_2 = []
            print(excel.val())
            if excel.val():
                for user in excel.each():
                    user_dict = user.val()
                    print(user_dict)
                    user_dict['image'] = '=IMAGE("' + \
                        str(user_dict['image'])+'",4,100,100)'
                    print("--------", user_dict['image'])
                    excel_2.append(user_dict)
                    print(excel_2)

                with open('spreadsheet.csv', 'w') as outfile:
                    writer = DictWriter(
                        outfile, ('image', 'name', 'reason', 'time', 'roomnum'))
                    writer.writeheader()
                    writer.writerows(excel_2)

                df_new = pd.read_csv('spreadsheet.csv')
                GFG = pd.ExcelWriter('spreadsheet.xlsx')
                df_new.to_excel(GFG, index=False)

                GFG.save()
                content = open('spreadsheet.xlsx', "rb")
                print(content)
                response = HttpResponse(
                    content, content_type='application/ms-excel')
                print('response', response)
                response['Content-Length'] = os.path.getsize(
                    'spreadsheet.xlsx')
                response['Content-Disposition'] = 'attachment; filename=%s' % 'spreadsheet.xlsx'

                return response
            else:
                return(redirect('/report'))
        else:
            messages.info(
                request, f'No report available for selected date')
            return(redirect('/report'))
    else:
        messages.info(
            request, f'Please select a date first.')
        return redirect('/report')
