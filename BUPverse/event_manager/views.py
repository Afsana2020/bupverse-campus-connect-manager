from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.core.cache import cache
from .models import eventPost, UserEventSelection, UserRoutine,UserBusySlot,Recom
from event_manager.utils.event_code import SimpleScheduler
from .forms import EventPostForm, UserBusySlotForm,RecomForm


# event post

def event_homepage(request):
    posts = eventPost.objects.all()
    return render(request, 'event_homepage.html', {'posts': posts})

@login_required
def my_events(request):
    post = eventPost.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_events.html', {'post': post})

def event_manage(request):
    return render(request, 'event_manage.html')


def event_post_list(request):

    events = eventPost.objects.filter(date__gte=timezone.now().date()).order_by('date', 'start_time')
    
    if request.user.is_authenticated:
        already_added_events = eventPost.objects.filter(
            date__gte=timezone.now().date(),
            usereventselection__user_routine__user=request.user
        ).distinct()
        
  
        available_events = events.exclude(
            id__in=already_added_events.values_list('id', flat=True)
        )
        scheduler = SimpleScheduler(user=request.user)
        schedule_result = scheduler.suggest_optimal_schedule(available_events)
        
        conflicted_events = schedule_result.get('conflicted_events', [])
        conflicted_event_ids = [e.id for e in conflicted_events]
        
        other_available = available_events.exclude(id__in=[e.id for e in schedule_result['optimal_events']])
        other_non_conflicting = other_available.exclude(id__in=conflicted_event_ids)
        other_conflicting = other_available.filter(id__in=conflicted_event_ids)
        
        context = {
            'already_added_events': already_added_events,
            'optimal_events': schedule_result['optimal_events'],
            'other_non_conflicting': other_non_conflicting,
            'other_conflicting': other_conflicting,
            'is_authenticated': True,
        }
    else:
        context = {
            'events': events,
            'is_authenticated': False,
        }
    
    return render(request, 'event_post_list.html', context)

def event_details(request, event_id):
    event = get_object_or_404(eventPost, id=event_id)
    
    user_events = []
    if request.user.is_authenticated:
        user_events = eventPost.objects.filter(
            usereventselection__user_routine__user=request.user
        )

    return render(request, 'event_details.html', {
        'event': event,
        'user_events': user_events 
    })



@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventPostForm(request.POST, request.FILES, user=request.user) 
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "Event created successfully!") 
            return redirect('my_events')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label}: {error}")
    else:
        form = EventPostForm(user=request.user)  

    return render(request, 'event_form.html', {'form': form})

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(eventPost, id=event_id, user=request.user)
    
    if request.method == 'POST':
        form = EventPostForm(request.POST, request.FILES, instance=event, user=request.user)
        if form.is_valid():
            event = form.save()
            
            
            UserEventSelection.objects.filter(event=event).update(has_conflict=False)
            
           
            attendees = UserEventSelection.objects.filter(event=event).select_related('user_routine__user')
            for attendee in attendees:
                scheduler = SimpleScheduler(attendee.user_routine.user)
                if not scheduler.check_availability(event.date, event.start_time, event.end_time):
                    attendee.has_conflict = True
                    attendee.save()
            
            messages.success(request, "Event updated successfully!")
            return redirect('my_events')
        else:
           
            for field, errors in form.errors.items():
                if field == '__all__':
                    for error in errors:
                        messages.error(request, f"Error: {error}")
                else:
                    field_label = form.fields[field].label if field in form.fields else field
                    for error in errors:
                        messages.error(request, f"{field_label}: {error}")
    
    return render(request, 'event_form.html', {
        'form': EventPostForm(instance=event, user=request.user),
        'event': event
    })


@login_required
def delete_event(request, event_id):
    post = get_object_or_404(eventPost, id=event_id, user=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('my_events')
    return render(request, 'event_post_confirm_delete.html', {'post': post})


#event Management

@login_required
def events_to_attend(request):

    events = eventPost.objects.all()
    routine_selections = UserEventSelection.objects.filter(
        user_routine__user=request.user
    ).select_related('event')
    scheduler = SimpleScheduler(request.user)
    conflict_flags = {}
    routine_events = []
    for selection in routine_selections:
        event = selection.event
        has_conflict = scheduler.check_event_conflicts_excluding_self(event)
        routine_events.append({
            'id': event.id,
            'event_title': event.event_title,  
            'date': event.date,
            'start_time': event.start_time,
            'end_time': event.end_time,
            'poster':event.poster,
            'has_conflict': has_conflict,
            'importance_score': selection.importance_score
        })
        if has_conflict:
            conflict_flags[event.id] = True
    
    return render(request, 'events_to_attend.html', {
        'events': events,
        'routine_events': routine_events,
        'has_conflicts': bool(conflict_flags)
    })


@login_required
def add_busy_slot(request):
    if request.method == 'POST':
        form = UserBusySlotForm(request.POST, user=request.user)
        if form.is_valid():
            scheduler = SimpleScheduler(request.user)

            day_of_week = form.cleaned_data['day_of_week']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
        
            today = timezone.now().date()
            target_date = today + timedelta(days=(day_of_week - today.weekday()) % 7)
        
            if not scheduler.check_availability(target_date, start_time, end_time):
                messages.error(request, "This time slot conflicts with existing commitments")
                return render(request, 'busy_slot_form.html', {
                    'form': form,
                    'form_title': 'Add Busy Time Slot'
                })
            
            busy_slot = form.save(commit=False)
            busy_slot.user = request.user
            busy_slot.save()
            messages.success(request, f"Added busy slot: {busy_slot.task_name}")
            return redirect('view_routine')
    else:
        form = UserBusySlotForm(user=request.user)
    
    return render(request, 'busy_slot_form.html', {
        'form': form,
        'form_title': 'Add Busy Time Slot'
    })


@login_required
def edit_busy_slot(request, slot_id):
    slot = get_object_or_404(UserBusySlot, id=slot_id, user=request.user)
    
    if request.method == 'POST':
        form = UserBusySlotForm(request.POST, instance=slot, user=request.user)
        if form.is_valid():
          
            scheduler = SimpleScheduler(request.user)
            
            day_of_week = form.cleaned_data['day_of_week']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
           
            today = timezone.now().date()
            target_date = today + timedelta(days=(day_of_week - today.weekday()) % 7)
            
            if not scheduler.check_availability(target_date, start_time, end_time):
              
                messages.error(request, "This time slot conflicts with existing commitments")
                return render(request, 'busy_slot_form.html', {
                    'form': form,
                    'form_title': 'Edit Busy Time Slot'
                })

            form.save()
            messages.success(request, "Time slot updated successfully")
            return redirect('view_routine')
    else:
        form = UserBusySlotForm(instance=slot, user=request.user)
    
    return render(request, 'busy_slot_form.html', {
        'form': form,
        'form_title': 'Edit Busy Time Slot'
    })

@login_required
def delete_busy_slot(request, slot_id):
    slot = get_object_or_404(UserBusySlot, id=slot_id, user=request.user)
    
    if request.method == 'POST':
        slot.delete()
        messages.success(request, "Time slot deleted successfully")
        return redirect('view_routine')
    
    return render(request, 'busy_confirm_delete.html', {
        'object': slot,
        'object_type': 'time slot'
    })

@login_required
def view_routine(request):
    
    today = timezone.localtime(timezone.now()).date()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    
    days = []
    conflict_flags = {}

    scheduler = SimpleScheduler(request.user)
    
    for i in range(7):
        current_date = week_start + timedelta(days=i)
        days.append({
            'name': current_date.strftime('%A'),
            'value': i,
            'date': current_date,
            'is_today': current_date == today,
            'date_display': current_date.strftime("%b %d"),
            'full_date_display': current_date.strftime("%A, %B %d, %Y")
        })


    for day in days:
        day['slots'] = UserBusySlot.objects.filter(
            user=request.user,
            day_of_week=day['value']
        ).order_by('start_time')
 
        day['events'] = []
        selections = UserEventSelection.objects.filter(
            user_routine__user=request.user,
            event__date=day['date']
        ).select_related('event').order_by('event__start_time')
        
        for selection in selections:
            event = selection.event
            has_conflict = scheduler.check_event_conflicts_excluding_self(event)
            
            day['events'].append({
                'event': event,
                'importance_score': selection.importance_score,
                'has_conflict': has_conflict
            })
            
            if has_conflict:
                conflict_flags[event.id] = True

    return render(request, 'view_routine.html', {
        'days': days,
        'current_week': today.strftime("%U"),
        'current_year': today.year,
        'week_start_date': week_start,
        'week_end_date': week_end,
        'today': today,
        'has_conflicts': bool(conflict_flags)
    })



@login_required
def fix_conflict(request):
    scheduler = SimpleScheduler(request.user)
    conflicts = []

    user_events = [
        event_sel.event 
        for event_sel in UserEventSelection.objects.filter(
            user_routine__user=request.user
        ).select_related('event')
    ]
    
    all_conflicts = scheduler.find_conflicts(user_events)
    
    for e1, e2 in all_conflicts['event_event']:
        conflicts.append({
            'type': 'event_event',
            'items': [
                {
                    'type': 'event',
                    'id': e1.id,
                    'title': e1.event_title,
                    'time': f"{e1.start_time.strftime('%H:%M')}-{e1.end_time.strftime('%H:%M')}",
                    'date': e1.date
                },
                {
                    'type': 'event',
                    'id': e2.id,
                    'title': e2.event_title,
                    'time': f"{e2.start_time.strftime('%H:%M')}-{e2.end_time.strftime('%H:%M')}",
                    'date': e2.date
                }
            ]
        })
    
    for event, slot in all_conflicts['event_busy']:
        slot_date = timezone.now().date() + timedelta(
            days=(slot.day_of_week - timezone.now().date().weekday()) % 7
        )
        conflicts.append({
            'type': 'event_busy',
            'items': [
                {
                    'type': 'event',
                    'id': event.id,
                    'title': event.event_title,
                    'time': f"{event.start_time.strftime('%H:%M')}-{event.end_time.strftime('%H:%M')}",
                    'date': event.date
                },
                {
                    'type': 'busy_slot',
                    'id': slot.id,
                    'title': slot.task_name,
                    'time': f"{slot.start_time.strftime('%H:%M')}-{slot.end_time.strftime('%H:%M')}",
                    'date': slot_date
                }
            ]
        })
    
    return render(request, 'fix_conflict.html', {
        'conflicts': conflicts,
        'has_conflicts': bool(conflicts)
    })
@login_required
def update_routine(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        action = request.POST.get('action')
        
        if event_id and action in ['add', 'remove']:
            event = get_object_or_404(eventPost, id=event_id)
            routine, _ = UserRoutine.objects.get_or_create(user=request.user)
            
            if action == 'add':
                importance_score = request.POST.get('importance_score', 5)
                try:
                    importance_score = int(importance_score)
                    importance_score = max(1, min(10, importance_score))
                except (ValueError, TypeError):
                    importance_score = 5

                scheduler = SimpleScheduler(request.user)
                if scheduler.date_trees.get(event.date, None) and \
                   scheduler.date_trees[event.date].has_overlap(event.start_time, event.end_time):
                    messages.error(request, "Time conflict detected with existing commitments")
                    return redirect(request.META.get('HTTP_REFERER', 'events_to_attend'))

                UserEventSelection.objects.get_or_create(
                    user_routine=routine,
                    event=event,
                    defaults={'importance_score': importance_score}
                )

                cache.delete(f'user_{request.user.id}_interest_predictions')
                messages.success(request, f"Added '{event.event_title}' to your routine")

            elif action == 'remove':
                UserEventSelection.objects.filter(
                    user_routine=routine,
                    event=event
                ).delete()

                cache.delete(f'user_{request.user.id}_interest_predictions')
                messages.success(request, f"Removed '{event.event_title}'")

        return redirect(request.META.get('HTTP_REFERER', 'events_to_attend'))
    return redirect('events_to_attend')




@login_required
def event_recom(request):
    try:
        requested_count = int(request.GET.get('count'))
    except (TypeError, ValueError):
        try:
            requested_count = int(request.user.recommendations.latest('created_at').choose)
        except Recom.DoesNotExist:
            requested_count = 3 

    scheduler = SimpleScheduler(request.user)
    result = scheduler.get_weekly_recommendations(requested_count)

    total_recommended_hours = sum(event.duration() for event in result['events']) if result['events'] else 0

    return render(request, 'event_recom.html', {
        'events': result['events'],
        'available_count': result['available_count'],
        'selected_count': result['requested_count'],
        'show_warning': result['status'] == 'not_enough_events',
        'requested_count': requested_count,
        'total_recommended_hours': total_recommended_hours
    })

@login_required
def choose_number(request):
    if request.method == 'POST':
        form = RecomForm(request.POST)
        if form.is_valid():
            Recom.objects.update_or_create(
                user=request.user,
                defaults={'choose': form.cleaned_data['choose']}
            )
            return redirect('event_recom')
    else:
        try:
            initial = {'choose': request.user.recommendations.latest('created_at').choose}
        except Recom.DoesNotExist:
            initial = {'choose': '3'}

        form = RecomForm(initial=initial)

    return render(request, 'choose_number.html', {'form': form})