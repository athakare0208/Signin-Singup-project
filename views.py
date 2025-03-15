from django.contrib import messages
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout 
from django.http import HttpResponse
from django.shortcuts import render, redirect 
from .models import Note, Signup 
from django.contrib.auth.models import User 
from datetime import datetime 
import re 

# Create your views here.
# ------------------------------------------------------------------------------------------

def about(request):
    return render (request,'about.html')

# ------------------------------------------------------------------------------------------

def index(request):
    return render (request,'index.html') 

# ------------------------------------------------------------------------------------------

def contact(request):
    return render (request,'contact.html')

# ------------------------------------------------------------------------------------------

def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')  
        user = authenticate(request, username=username, password=password) 
        if user is not None:
            login(request, user) 
            return redirect('user_profile')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})   
        
    return render(request, 'login.html')  

# ------------------------------------------------------------------------------------------

def adminlogin(request):
    # Check if user is already logged in
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('adminhome')
        else:
            logout(request)  # Logout if not superuser
    
    if request.method == "POST":
        username = request.POST.get("username") #Get and Post are the most common HTTP request used to send data between the client(browser) and server. 
        password = request.POST.get("pass")  
        
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser: 
            login(request, user)
            return redirect('adminhome')  
        else:
            return render(request, 'adminlogin.html', 
                {'error': 'Invalid admin credentials'})
    
    return render(request, 'adminlogin.html')

# -------------------------------------------------------------------------------------------

def signup1(request):
    error = None
    if request.method == 'POST':
        un = request.POST.get('username')
        fullname = request.POST.get('fullname')
        email = request.POST.get('emailid')  
        p1 = request.POST.get('password1')
        p2 = request.POST.get('password2')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender') 
        
        if not re.search(r'[@$!%*?&./-_ ^:;><=()#]', p1) or not re.search(r'[@$!%*?&./-_ ^:;><=()#]', p2):
            return render(request, 'signup.html', {'error': 'Atleast one special character in your password.'})  


        # Check if username already exists 
        if User.objects.filter(username=un).exists():
            error = "Username already exists. Please choose a different username." 
            return render(request, 'signup.html', {'error': error})   
            
        # Check if passwords match
        if p1 != p2:    
            error = "Your password and confirm password do not match!"
            return render(request, 'signup.html', {'error': error}) 
            
        try:
            # Create user 
            myuser = User.objects.create_user(username=un, email=email, password=p1)
            myuser.first_name = fullname 
            myuser.set_password(p1)  # Hash the password before saving
            myuser.save()
            
            # Create signup profile
            Signup.objects.create(
                user=myuser,
                dob=dob,
                gender=gender,
                role='User' 
            )
            
            return redirect('login')  
        except Exception as e:
             return render(request, 'signup.html', {'error': f"An error occurred: {str(e)}"}) 
            
    return render(request, 'signup.html')

# ------------------------------------------------------------------------------------------------

def adminhome(request):
    if not request.user.is_authenticated:
        return redirect('adminlogin')  
    if not request.user.is_superuser:
        logout(request)  # Force logout if not superuser 
        return redirect('login') 
        
    pn = Note.objects.filter(status='pending').count()
    an = Note.objects.filter(status='accepted').count() 
    rn = Note.objects.filter(status='rejected').count()  
    alln = Note.objects.filter().count()
    d = {"pn": pn, "an": an, "rn": rn, "alln": alln}   
    return render(request, 'adminhome.html', d)  

# ------------------------------------------------------------------------------------------

def Logout(request):
    logout(request) 
    return redirect('login')  

# ------------------------------------------------------------------------------------------

def  Profile(request): 
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        signup = Signup.objects.get(user=request.user)
    except Signup.DoesNotExist:
        signup = None
    
    return render(request, 'profile.html', {'signup': signup})

# ------------------------------------------------------------------------------------------

def changepassword(request):
    if not request.user.is_authenticated:
        return redirect('login') 
        
    if request.method == 'POST': 
        user = request.user
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')  
        
        if not user.check_password(old_password):
            return render(request, 'changepassword.html', {'error': 'Old password is incorrect'})
       
        if new_password1 != new_password2:
            return render(request, 'changepassword.html', {'error': 'New passwords do not match'})
        
        user.set_password(new_password1)
        user.save()
        
        login(request, user)
        return redirect('user_profile') 
        
    return render(request, 'changepassword.html') 

# ------------------------------------------------------------------------------------------

def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        signup = Signup.objects.get(user=request.user)
    except Signup.DoesNotExist:
        signup = None
        
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')   
        contact = request.POST.get('contact')
        branch = request.POST.get('branch')
        dateofbirth = request.POST.get('dob')
        gender = request.POST.get('gender')

        # Update user information 
        user = request.user 
        user.first_name = first_name 
        user.last_name = last_name   
        user.email = email
        user.save() 
        
        # Update or create signup information  
        # signup = Signup.objects.get(user=request.user)
        if signup:
            signup.contact = contact
            signup.branch = branch
            signup.dob = dateofbirth 
            signup.gender = gender
            signup.save()
        else:
            signup = Signup.objects.create(
                user=request.user, 
                contact=contact,
                branch=branch,
                role='User',
                dob=dateofbirth,
                gender=gender
            )
        
        return redirect('user_profile')
    # signup = Signup.objects.get(user=request.user)
    return render(request, 'edit_profile.html', {'signup': signup}) 

# ------------------------------------------------------------------------------------------

def upload_note(request):
    if not request.user.is_authenticated:
        return redirect('login')

    error = ''
    if request.method == 'POST':
        branch = request.POST.get('branch')
        subject = request.POST.get('subject')
        notefile = request.FILES.get('notesfile')      
        file_type = request.POST.get('filetype')  
        des = request.POST.get('description') 
        
        if not notefile:
            error = 'yes'
            return render(request, 'uploadnote.html', {'error': error, 'message': 'Please select a file to upload'})
        
        try:
            Note.objects.create(
                user=request.user,
                uploadingdate=datetime.now(),     
                branch=branch,
                subject=subject,
                description=des,
                notefile=notefile,
                filetype=file_type,
                status='pending',
            )
            error = 'no'
        except Exception as a: 
            error = 'yes'
            print(str(a))   

    return render(request, 'uploadnote.html', {'error': error})

# ------------------------------------------------------------------------------------------

def view_mynotes(request): 
    if not request.user.is_authenticated:
        return redirect('login')
    
    notes = Note.objects.filter(user=request.user)     
    return render(request, 'view_mynotes.html', {'notes': notes})   

# ------------------------------------------------------------------------------------------

def delete_mynote(request, pid):
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        note = Note.objects.get(id=pid, user=request.user)
        note.delete()
    except Note.DoesNotExist: 
        pass
    return redirect('view_mynotes')

# ------------------------------------------------------------------------------------------

def viewuser(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    users = Signup.objects.exclude(user=request.user)
    
    # Get the first note's ID for each user
    first_notes = {}
    for signup in users:
        first_note = Note.objects.filter(user=signup.user).first()
        if first_note:
            first_notes[signup.user.id] = first_note.id
    
    return render(request, 'viewuser.html', {
        'users': users,
        'first_notes': first_notes  
    })

# ------------------------------------------------------------------------------------------

def delete_user(request, user_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        user = User.objects.get(id=user_id)
        # Delete the associated Signup object first
        Signup.objects.filter(user=user).delete()
        # Then delete the user
        user.delete()
        return redirect('view_user')
    except User.DoesNotExist:
        return redirect('view_user') 

# ------------------------------------------------------------------------------------------

def pending(request):
    if not request.user.is_authenticated:
        return redirect('adminlogin')  
    notes = Note.objects.filter(status='pending')
    return render(request, 'pending_notes.html', {'notes': notes}) 

# ------------------------------------------------------------------------------------------

def accepted(request):
    if not request.user.is_authenticated:
        return redirect('adminlogin')
    notes = Note.objects.filter(status='Accept')
    print(f"Accepted Notes: {list(notes.values('id', 'subject', 'status'))}")  
    return render(request, 'accepted.html', {'notes': notes})

# ------------------------------------------------------------------------------------------

def rejected(request):
    if not request.user.is_authenticated: 
        return redirect('adminlogin')
    notes = Note.objects.filter(status='Reject')
    return render(request, 'rejected.html', {'notes': notes})

# ------------------------------------------------------------------------------------------ 

def all_notes(request):
    if not request.user.is_authenticated:
        return redirect('adminlogin')
    notes = Note.objects.all()
    print(f"Total Notes: {notes.count()}")
    print("Note Details:")
    for note in notes:
        print(f"ID: {note.id}, Subject: {note.subject}, Status: {note.status}, User: {note.user.username}") 
    return render(request, 'all_notes.html', {'notes': notes})

# ------------------------------------------------------------------------------------------

def asign_status(request, pid):
    if not request.user.is_authenticated:
        return redirect('adminlogin') 
    note = Note.objects.get(id=pid)
    if request.method == "POST":
        status = request.POST.get("status")  
        note.status = status
        note.save()
        return redirect('all_notes')
    return render(request, 'asign_status.html', {'note': note}) 