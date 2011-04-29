# Create your views here.
from django.shortcuts import render_to_response, HttpResponse, HttpResponseRedirect, RequestContext
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.contrib.auth.models import User
from home.models import *
from home.forms import *

# Home Page

def home(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")
        
    # Get User
    user = User.objects.get(username = request.user.username)
    
    # Get User Credits 
    credits = user.get_profile().total_credits();
    
    # Get User Points
    points = user.get_profile().total_points();
    
    # Get User referral hash
    
    referral_hash = user.get_profile().referral_hash
    
    variables = RequestContext(request,{"credits":credits, "points":points, "referral_hash":referral_hash})
    return render_to_response("home.html",variables)


# Signup Page

def index(request):
    #signupform = SignupForm()
    if request.method == "POST":
        signupform = SignupForm(request.POST)
        if signupform.is_valid():
            cd = signupform.cleaned_data
            
            # POST DATA
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            sexe = request.POST['sexe']
            
            # Add new user
            new_user = User(username = username, email = email)
            new_user.set_password(password)
            new_user.save()
            
            # Add user profile
            refhash = hashlib.sha1(new_user.username).hexdigest()[:6]
            user_profile = UserScores(user = new_user, sexe = sexe, referral_hash = refhash)
            user_profile.save()
            
            # Give user 450 credits
            new_credit = Credit(user = new_user, credits = 450, action = "Inscription")
            new_credit.save()
            
            return   HttpResponseRedirect("/login")
    else:
        signupform = SignupForm()
    variables = RequestContext(request,{"signupform":signupform})
    return render_to_response("index.html",variables)
    

# Login Page

def login(request):
    error = ""
    if request.user.is_authenticated():
        return HttpResponseRedirect("/home")
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login_auth(request, user)
            return HttpResponseRedirect("/home")
        else:
            error = "Connexion non valide"
    signinform = SigninForm()
    variables = RequestContext(request,{"signinform":signinform, "error":error})
    return render_to_response("login.html", variables)
    
# Logout Page

def logout(request):
    logout_auth(request)
    return HttpResponseRedirect("/login")
    