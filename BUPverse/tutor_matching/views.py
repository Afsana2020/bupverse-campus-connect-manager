from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import nextDoorPost
from .forms import nextDoorPostForm
from core.utils.geo_utils import geocode_with_ors


#nextdoor profile
@login_required
def nextDoor_profile(request):
    try:
        post = request.user.nextdoorpost
    except nextDoorPost.DoesNotExist:
        post = None

    return render(request, 'nextDoor_profile.html', {
        'user': request.user,
        'post': post
    })


#post list view

def nextDoor_homepage(request):
    posts = nextDoorPost.objects.all()
    return render(request, 'nextDoor_homepage.html', {'posts': posts})

@login_required
def nextDoor_tutor_post_list(request):
    posts = nextDoorPost.objects.filter(user_type='looking_tutions').exclude(user=request.user)
    return render(request, 'nextDoor_tutor_post_list.html', {'posts': posts})

@login_required
def nextDoor_student_post_list(request):
    posts = nextDoorPost.objects.filter(user_type='looking_tutor').exclude(user=request.user)
    return render(request, 'nextDoor_student_post_list.html', {'posts': posts})





#view post details
def nextDoor_post_details(request, post_id):
    post = get_object_or_404(nextDoorPost, id=post_id)
    return render(request, 'nextDoor_post_details.html', {'post': post})



#post 
@login_required
def nextDoor_post_create(request):

    if hasattr(request.user, 'nextdoorpost'):
        return redirect('nextDoor_post_edit', post_id=request.user.nextdoorpost.id)

    if request.method == "POST":
        form = nextDoorPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            if post.location:
                lat, lon = geocode_with_ors(post.location)
                if lat and lon:
                    post.latitude = lat
                    post.longitude = lon
            post.user = request.user  
            post.save()
            return redirect('nextDoor_profile')
    else:
        form = nextDoorPostForm()

    return render(request, 'nextDoor_post_form.html', {'form': form})

# edit tutor post
@login_required
def nextDoor_post_edit(request, post_id):
    post = get_object_or_404(nextDoorPost, pk=post_id)

    if request.method == "POST":
        form = nextDoorPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            if post.location:
                lat, lon = geocode_with_ors(post.location)
                if lat and lon:
                    post.latitude = lat
                    post.longitude = lon
            post.user = request.user  
            post.save()
            return redirect('nextDoor_profile')
    else:
        form = nextDoorPostForm(instance=post)

    return render(request, 'nextDoor_post_form.html', {'form': form})

#delete tutor post
@login_required
def nextDoor_delete(request, post_id):
   
    post = get_object_or_404(nextDoorPost, pk=post_id)

    if request.method == "POST":
        post.delete()
        return redirect('nextDoor_profile')

    return render(request, 'nextDoor_post_confirm_delete.html', {'post': post})



# similarity

from .utils.graph_matcher import choose_method
@login_required
def nextDoor_matched_posts(request, post_id):
    user_post = get_object_or_404(nextDoorPost, id=post_id)
    
    matches = choose_method(user_post, top_n=10) 
    context = {
        'user_post': user_post,
        'matches': matches, 
    }
    return render(request, 'nextDoor_matched_posts.html', context)
