from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm, EvaluationRequestForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import EvaluationRequest

# Create your views here.

# Task 1 - Develop a secure web form that allows customers to register in the application.
def user_signup(request):
    if request.method == "POST":
        fm = SignUpForm(request.POST)
        if fm.is_valid():
            fm.save()
            print("Data successfully saved")
            messages.success(request, "Congratulations, your account has been successfully created")
    else:
        fm = SignUpForm()
        print("Get the form data")
    return render(request, 'UserApp/signup.html', {"forms": fm})

# Task 2 - Develop a secure login feature.
def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/profile/')
    else:
        if request.method == 'POST':
            fm = AuthenticationForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    print("I am logged in")
                    messages.success(request, "Successfully logged in")
                    return HttpResponseRedirect('/profile/')
                else:
                    print("You are fake")
                    messages.error(request, f"Wrong credentials for {uname}")
        else:
            fm = AuthenticationForm()
        return render(request, "UserApp/login.html", {"forms": fm})

# Task 4 - Implement a “Request Evaluation” web page only accessible to logged in users.
@login_required(login_url='/login/')
def request_evaluation(request):
    if request.method == "POST":
        fm = EvaluationRequestForm(request.POST, request.FILES)
        if fm.is_valid():
            instance = fm.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, "Your evaluation request has been submitted successfully")
    else:
        fm = EvaluationRequestForm()
    return render(request, 'UserApp/request_evaluation.html', {"forms": fm})

# Task 6 - Implement a page that displays a list of evaluation requests (visible to an administrator role).
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def evaluation_requests_list(request):
    requests = EvaluationRequest.objects.all()
    return render(request, 'UserApp/evaluation_requests_list.html', {"requests": requests})



@login_required(login_url='/login/')  # Make sure the user is logged in to access this view
def user_profile(request):
    if request.user.is_authenticated:
        return render(request, 'UserApp/Home.html', {"name": request.user.username})
    else:
        return HttpResponseRedirect('/login/')
    

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')  # Redirect to the login page after logging out