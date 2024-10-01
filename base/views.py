
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.forms import UserCreationForm
from .models import registrationform
from .forms import DocumentForm
from .models import Document, PickleModels
import pandas as pd
import requests
from base.applymodel import apply_model
from django.http import HttpResponse
from numpy import reshape
import numpy as np
import pickle
import os
# Create your views here.
def register(request):
    if request.method=='POST':
        form = registrationform(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            # password1 = form.cleaned_data.get('password1')
            # user = auth.authenticate(username=username,password=password1)
            # auth.login(request, user)
            messages.info(request, f'Hello {username}, you are successfully registered!') 
            return redirect('/login')
            #form = registrationform()
    else:
        form = registrationform()
    return render(request, 'register.html', {'form':form})

def upload(request):
    #username = form.cleaned_data.get('username')
    #qs = Document.objects.get(pk=8)
    #qs = qs.myfile
    #qs = io.StringIO(qs)
    #qs = pd.read_csv(qs)
    #qs = qs.to_html()
    #qs = request.FILES['qs']
    #qs = pd.DataFrame(qs)
    #df = read_frame(qs)
    

    if request.user.is_authenticated: 
        # Is it better to use @login_required ?
        #username = request.user.username
        if request.session.has_key('username'):
            username = request.session['username']

    else:
        #username = ''
        if request.session.has_key('username'):
            username = request.session['username']

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.username = username
            doc.save()
            
            return render(request, 'upload.html', {
               "form": DocumentForm(),
               "uploaded_file_url": doc.myfile.url,
               "username": username,
               #"qs":qs
            })
    else:
        form = DocumentForm()
    return render(request, 'upload.html', {"form": form, "username":username})

def login(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, f"Hello {username}, you are successfully logged in")
            request.session['username'] = username
            #return render(request,"upload.html")
            return redirect('/home')
        else:
            if not User.objects.filter(username=username).exists():
                messages.error(request, "Username Doesn't Exist")
            else:
                messages.info(request, "Incorrect Password", extra_tags="password_incorrect")
            return redirect('/')

    else:  
        return render(request, "login.html")

def logout(request):
    auth.logout(request)
    return redirect('/')

def home(request):
    if request.user.is_authenticated: 
        # Is it better to use @login_required ?
        #username = request.user.username
        if request.session.has_key('username'):
            username = request.session['username']
            data = Document.objects.filter(username=username).values_list('myfile')
            context = {'username': username, 'data': data}
            
            if request.GET.get('document'):
                request.session['document'] = request.GET.get('document')
                return redirect('/dashboard')
            return render(request, 'home.html', context)
    
    else:
        #username = ''
        return render(request, 'home.html')
    
def dashboard(request):
    if request.user.is_authenticated: 
        # Is it better to use @login_required ?
        #username = request.user.username
        if request.session.has_key('username'):
            username = request.session['username']
            document = None
            try:
            
                #request.session['document']
                document = request.session['document']
                data = Document.objects.get(username=username, myfile=document)
                data = data.myfile
                try:
                    data = pd.read_excel(data)
                except:
                    data = pd.read_csv(data)
                data_head = data.head(5)
                data_head = data_head.to_html()
                columns = list(data.columns)
                mods = ['Linear Regression', 'Logistic Regression', 'KNN', 'Random Forest']
                context = {'username': username, 'document': document, 'data_head': data_head, 'columns':columns, 'mods':mods}
                
                if request.GET.getlist('column-x'):
                    request.session['column-x'] = request.GET.getlist('column-x')
                    #print(request.session['column-x'],'bruh')
                    request.session['column-y'] = request.GET.getlist('column-y')
                    request.session['model'] = request.GET.getlist('model')
                    return redirect('/result')

                return render(request, 'dashboard.html', context)
            except:
                return render(request, 'dashboard.html')
            
    else:
        #username = ''
        return render(request, 'dashboard.html')

def result(request):
    
    if request.user.is_authenticated: 
        # Is it better to use @login_required ?
        #username = request.user.username

        if request.session.has_key('username') and request.session.has_key('document'):
            username = request.session['username']
            document = request.session['document']
            if request.session['column-x'] and request.session['column-y'] and request.session['model']:
                print('here')
                columnx = request.session['column-x'] 
                columny = request.session['column-y'] 
                model = request.session['model']
                
                data = Document.objects.get(username=username, myfile=document)
                data = data.myfile
                try:
                    data = pd.read_excel(data)
                except:
                    data = pd.read_csv(data)

                mdl, enc = apply_model(request, data, model[0])
                #lrg = linear_reg(request, data)
                #pk_model = PickleModels(pickle_model=mdl, username=username)
                #pk_model.save()
                pickle.dump(model, open('model.pkl', 'wb'))
                with open(f"media/{request.session['document']}.pkl", "wb") as obj:
                    pickle.dump(model, obj)
                dff = pd.DataFrame(index=[0])

                #print(request.session['df'], 'ad')
                flag = 0
                l1 = request.session['temp_col']

                if request.GET.getlist(columnx[0]):
                    for col in columnx:
                        if request.GET.getlist(col)[0].replace('.', '').replace('-', '').isdigit():
                            request.session[f'{col}'] = float(request.GET.getlist(col)[0])
                            var = float(request.GET.getlist(col)[0])
                            ##print('buraas')
                            dff[col] = var
                            #print('yass')
                            
                        else:
                            request.session[f'{col}'] = str(request.GET.getlist(col)[0])
                            df = pd.DataFrame(index=[0])
                            df[col] = str(request.GET.getlist(col)[0])
                            dum = pd.get_dummies(df.select_dtypes(include = ['object']))
                            dff = pd.concat([dff,dum],axis=1)
                            flag = 1
                    
                    if flag:
                        l2 = list(dff.columns)
                        for cols in l1:
                            print(cols)
                            if cols not in l2:
                                dff[cols] = 0
                        dff = dff[list(l1)]
                    print(dff)
                    if enc:
                        result = mdl.predict(enc.transform(np.array([[request.session[x] for x in columnx]])))
                        context = {'columnx': columnx, 'columny': columny, 'model': model, 'username': username, 'result':result[0]}
                    else:
                        #result = mdl.predict([[request.session[x] for x in columnx]])
                        result = mdl.predict(dff)
                        context = {'columnx': columnx, 'columny': columny, 'model': model, 'username': username, 'result':result[0][0]}
                    return render(request, 'result.html', context)
                else:
                    context = {'columnx': columnx, 'columny': columny, 'model': model, 'username': username}
                    return render(request, 'result.html', context)

    else:
        return render(request, 'result.html')
    
def download_model(request, username):
    file_path = f"media/{request.session['document']}.pkl"
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    # document = request.session['document']
    # response['Content_Disposition'] = f'attachment; filename="{document}.pkl"'
    # return response