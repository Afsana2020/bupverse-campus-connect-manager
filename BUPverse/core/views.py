from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import UserRegistrationForm
from .forms import ProfileForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import UserProfile



@login_required
def general_profile(request):
    return render(request, 'profile_view.html')


#homepage
def index(request):
    return render(request, 'index.html')

def about_us(request):
    return render(request, 'about_us.html')

def contact(request):
    return render(request, 'contact.html')



#custom registration
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            login(request, user)
           
            return redirect('complete_profile')
            
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    return render(request, 'profile.html', {'profile': profile})

@login_required
def profile_edit(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()
            
            user = request.user
                
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        initial_data = {'email': request.user.email}
        form = ProfileForm(instance=profile, initial=initial_data)

    return render(request, 'profile_edit.html', {'form': form})

@login_required
def complete_profile(request):
    try:
        profile = request.user.userprofile
        if profile.is_complete:
            return redirect('profile')
    except UserProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.is_complete = True
            profile.save()
            
           
            user = request.user
            user.save()
                
            messages.success(request, 'Profile completed successfully!')
            return redirect('profile')
    else:
        initial_data = {'email': request.user.email}
        form = ProfileForm(instance=profile, initial=initial_data)

    return render(request, 'complete_profile.html', {'form': form})