from django.shortcuts import render, redirect, get_object_or_404
from .models import roomPost
from .forms import roomPostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from core.utils.geo_utils import geocode_with_ors,get_real_distance_km
from django.http import HttpResponseForbidden
from django.db import IntegrityError

@login_required
def room_profile(request):
    try:
        post = request.user.roompost
    except roomPost.DoesNotExist:
        post = None

    return render(request, 'room_profile.html', {
        'user': request.user,
        'post': post
    })

def room_homepage(request):
    posts = roomPost.objects.all()
    return render(request, 'room_homepage.html', {'posts': posts})

def roommate_post_list(request):
    posts = roomPost.objects.filter(user_type='looking_house')
    if request.user.is_authenticated:
        posts = posts.exclude(user=request.user)
    return render(request, 'roommate_post_list.html', {'posts': posts})

def house_post_list(request):
    posts = roomPost.objects.filter(user_type='looking_roommate')
    if request.user.is_authenticated:
        posts = posts.exclude(user=request.user)
    return render(request, 'house_post_list.html', {'posts': posts})

def room_post_details(request, post_id):
    post = get_object_or_404(roomPost, id=post_id)
    return render(request, 'room_post_details.html', {'post': post})

@login_required
def room_post_create(request):
    if roomPost.objects.filter(user=request.user).exists():
        return redirect('room_post_edit', post_id=request.user.roompost.id)

    if request.method == "POST":
        form = roomPostForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                post = form.save(commit=False)
                post.user = request.user
                
                if post.area:
                    lat, lon = geocode_with_ors(post.area) 
                    if lat and lon:
                        post.latitude = lat
                        post.longitude = lon
                        post.dist_from_bup = get_real_distance_km(
                            (post.latitude, post.longitude),  
                            (23.8395916, 90.3573579)
                        )
                
                post.save()
                return redirect('room_profile')
                
            except IntegrityError:
                form.add_error(None, "You already have a post. Redirecting to edit")
                return redirect('room_post_edit', post_id=request.user.roompost.id)
    else:
        form = roomPostForm()

    return render(request, 'room_post_form.html', {'form': form})

# edit 
@login_required
def room_post_edit(request, post_id):
    post = get_object_or_404(roomPost, pk=post_id)
    
    if post.user != request.user:
        return HttpResponseForbidden("You don't have permission to edit this post.")

    if request.method == "POST":
        form = roomPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            
            if 'area' in form.changed_data and post.area:
                lat, lon = geocode_with_ors(post.area)
                if lat and lon:
                    post.latitude = lat
                    post.longitude = lon
                    post.dist_from_bup = get_real_distance_km(
                        (post.latitude, post.longitude),  
                        (23.839640, 90.357430))
            
            try:
                post.save()
                return redirect('room_profile')
            except IntegrityError:
                form.add_error(None, "Error saving your post. Please try again.")
    else:
        form = roomPostForm(instance=post)

    return render(request, 'room_post_form.html', {'form': form})

#delete tutor post
@login_required
def room_delete(request, post_id):
   
    post = get_object_or_404(roomPost, pk=post_id)

    if request.method == "POST":
        post.delete()
        return redirect('room_profile')

    return render(request, 'room_post_confirm_delete.html', {'post': post})



#similarity
from .utils.room_matcher import dijkstra_roommate_matching
@login_required
def room_matched_posts(request, post_id):
    user_post = get_object_or_404(roomPost, id=post_id)
    
    matches = dijkstra_roommate_matching(user_post, top_n=10) 

    context = {
        'user_post': user_post,
        'matches': matches, 
    }
    return render(request, 'room_matched_posts.html', context)
