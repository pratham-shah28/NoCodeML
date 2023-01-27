from django.shortcuts import render
from .forms import DocumentForm
# Create your views here.


def upload(request):
    if request.user.is_authenticated: 
        # Is it better to use @login_required ?
        username = request.user.username
    else:
        username = ''
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save()
            return render(request, 'upload.html', {
               "form": DocumentForm(),
               "uploaded_file_url": doc.myfile.url,
               "username": username,
            })
    else:
        form = DocumentForm()
    return render(request, 'upload.html', {"form": form})
