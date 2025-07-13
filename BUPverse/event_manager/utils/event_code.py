from typing import Dict, List, Tuple, Optional,Set
from datetime import time, date, datetime, timedelta
from django.utils import timezone
from collections import defaultdict
from django.db.models import Avg
from event_manager.models import eventPost, UserBusySlot, UserEventSelection

def time_overlaps(start1: time, end1: time, start2: time, end2: time) -> bool:
    
    def time_to_minutes(t: time) -> int:
        return t.hour * 60 + t.minute
    
    s1, e1 = time_to_minutes(start1), time_to_minutes(end1)
    s2, e2 = time_to_minutes(start2), time_to_minutes(end2)
    
    
    if e1 <= s1: e1 += 1440  
    if e2 <= s2: e2 += 1440
  
    return (
        max(s1, s2) < min(e1, e2) 
        and not (e1 == s2 or e2 == s1)  
    )

class SegmentTree:
    
    def __init__(self, intervals: List[Tuple[time, time]]):
        if not intervals:
            self.n = 0
            self.tree = []
            return
            
        #removing duplicates and sort
        unique_intervals = list(sorted({tuple(sorted(i)) for i in intervals}, key=lambda x: x[0]))
        self.n = len(unique_intervals)
        
        #bulding tree
        self.size = 1
        while self.size < self.n:
            self.size <<= 1
            
        #initializing
        self.tree = [(None, None)] * (2 * self.size)
        
        #leaves
        for i in range(self.n):
            self.tree[self.size + i] = unique_intervals[i]
        
        #internal nodes
        for i in range(self.size - 1, 0, -1):
            left = self.tree[2 * i]
            right = self.tree[2 * i + 1]

            if left[0] is not None and right[0] is not None:
                self.tree[i] = (
                    min(left[0], right[0]),
                    max(left[1], right[1])
                )
            elif left[0] is not None:
                self.tree[i] = left
            elif right[0] is not None:
                self.tree[i] = right
            else:
                self.tree[i] = (None, None)


    def _time_to_minutes(self, t: time) -> int:
        #midnight
        return t.hour * 60 + t.minute

    def _check_overlap(self, range1: Tuple[time, time], range2: Tuple[time, time]) -> bool:
        s1, e1 = self._time_to_minutes(range1[0]), self._time_to_minutes(range1[1])
        s2, e2 = self._time_to_minutes(range2[0]), self._time_to_minutes(range2[1])
        
        if e1 <= s1: e1 += 1440
        if e2 <= s2: e2 += 1440
        
        return max(s1, s2) < min(e1, e2) and not (e1 == s2 or e2 == s1)

    def has_overlap(self, query_start: time, query_end: time) -> bool:
         
        if self.n == 0:
            return False
            
        query = (query_start, query_end)
        
        def _query(node: int, node_left: int, node_right: int) -> bool:
            if node >= 2 * self.size:
                return False
                
            current = self.tree[node]
            if not current or current[0] is None:
                return False
                
            current_min = self._time_to_minutes(current[0])
            current_max = self._time_to_minutes(current[1])
            query_min = self._time_to_minutes(query_start)
            query_max = self._time_to_minutes(query_end)
            
            if current_max <= current_min: current_max += 1440
            if query_max <= query_min: query_max += 1440
            
            if (query_max <= current_min) or (query_min >= current_max):
                return False
                
            if node >= self.size:
                return self._check_overlap(current, query)

            mid = (node_left + node_right) // 2
            return _query(2 * node, node_left, mid) or _query(2 * node + 1, mid + 1, node_right)
        
        return _query(1, 0, self.size - 1)

def knapsack_solve(events: List[Tuple[float, float]], max_hours: float) -> List[eventPost]:
    if not events or max_hours <= 0:
        return []

    n = len(events)
    W = int(max_hours * 60)  
    weight = [int(dur * 60) for dur, _, _ in events]
    value = [int(score * 100) for _, score, _ in events] 


    p = [[0] * (W + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(W + 1):
            if weight[i-1] <= w:
                p[i][w] = max(
                    value[i-1] + p[i-1][w - weight[i-1]],
                    p[i-1][w]
                )
            else:
                p[i][w] = p[i-1][w]

    selected_events = []
    i, w = n, W
    while i > 0 and w > 0:
        if p[i][w] != p[i-1][w]:
            selected_events.append(events[i-1][2]) 
            w -= weight[i-1]
        i -= 1

    return selected_events

class SimpleScheduler:
    
    def __init__(self, user):
        self.user = user
        self.date_trees = self._build_date_trees() 

    def _predict_interest(self, event: eventPost) -> float:
        
        past_engagement = UserEventSelection.objects.filter(
            user_routine__user=self.user,
            event__category=event.category
        ).aggregate(avg_score=Avg('importance_score'))['avg_score'] or 5

        return (past_engagement * 0.4)
    
    def _build_date_trees(self) -> Dict[date, SegmentTree]:
        date_map = defaultdict(list)
        
        #adding fixed busy slots
        today = timezone.now().date()
        for slot in UserBusySlot.objects.filter(user=self.user):
            for days_ahead in range(7): 
                slot_date = today + timedelta(days=days_ahead)
                if slot_date.weekday() == slot.day_of_week:
                    date_map[slot_date].append((slot.start_time, slot.end_time))
        
        #adding events
        for selection in UserEventSelection.objects.filter(
            user_routine__user=self.user
        ).select_related('event'):
            event = selection.event
            date_map[event.date].append((event.start_time, event.end_time))
        
        return {d: SegmentTree(intervals) for d, intervals in date_map.items()}
    
    def check_availability(self, event_date: date, start: time, end: time) -> bool:
        if event_date not in self.date_trees:
            return True
        return not self.date_trees[event_date].has_overlap(start, end)

     
    def get_weekly_recommendations(self, requested_count: int = 5) -> Dict:
        
        today = timezone.now().date()
        weekly_events = []
        
        for day in range(7):
            target_date = today + timedelta(days=day)
            for event in eventPost.objects.filter(
                date=target_date,
                usereventselection__user_routine__user=self.user
            ):
                score = self._predict_interest(event)
                weekly_events.append((event.duration(), score, event))
        
        available_count = len(weekly_events)
        
        result = {
            'available_count': available_count,
            'requested_count': requested_count
        }
        
        if available_count == 0:
            result['status'] = 'not_enough_events'
            result['events'] = []
            return result
            
        if requested_count > available_count:
            result['status'] = 'not_enough_events'
            recommended_events = knapsack_solve(weekly_events, max_hours=available_count)
        else:
            result['status'] = 'success'
            recommended_events = knapsack_solve(weekly_events, max_hours=requested_count)
        
        result['events'] = recommended_events[:requested_count]
        return result
    
#all avaiable conflicts
    def find_conflicts(self, events: List[eventPost]) -> Dict[str, List]:
    
        conflicts = {
            'event_event': [],
            'event_busy': []
        }
        
        # event-event
        for i, e1 in enumerate(events):
            if e1.date in self.date_trees:
                if self.date_trees[e1.date].has_overlap(e1.start_time, e1.end_time):
                    for e2 in events[:i]:
                        if e2.date == e1.date and time_overlaps(
                            e1.start_time, e1.end_time,
                            e2.start_time, e2.end_time
                        ):
                            conflicts['event_event'].append((e1, e2))
        
        # event-busy slot
        for slot in UserBusySlot.objects.filter(user=self.user):
            slot_date = timezone.now().date() + timedelta(
                days=(slot.day_of_week - timezone.now().date().weekday()) % 7
            )
            
            if slot_date in self.date_trees and self.date_trees[slot_date].has_overlap(
                slot.start_time, slot.end_time
            ):
                for event in events:
                    if event.date == slot_date and time_overlaps(
                        event.start_time, event.end_time,
                        slot.start_time, slot.end_time
                    ):
                        conflicts['event_busy'].append((event, slot))
        
        return conflicts
#conflict for an event
    def check_event_conflicts_excluding_self(self, event: eventPost) -> bool:
        if event.date not in self.date_trees:
            return False
        intervals = []
        
        for slot in UserBusySlot.objects.filter(user=self.user):
            slot_date = (timezone.now().date() + 
                        timedelta(days=(slot.day_of_week - timezone.now().date().weekday()) % 7))
            if slot_date == event.date:
                intervals.append((slot.start_time, slot.end_time))
        
        for selection in UserEventSelection.objects.filter(
            user_routine__user=self.user
        ).exclude(event=event).select_related('event'):
            if selection.event.date == event.date:
                intervals.append((selection.event.start_time, selection.event.end_time))

        if intervals:
            temp_tree = SegmentTree(intervals)
            return temp_tree.has_overlap(event.start_time, event.end_time)
        return False
        
    def interval_scheduling(self, events: List[eventPost]) -> Set[int]:
        if not events:
            return set()

        stimes = []
        ftimes = []
        for event in events:
            start = event.start_time.hour * 60 + event.start_time.minute
            end = event.end_time.hour * 60 + event.end_time.minute
            if end <= start:  
                end += 1440
            stimes.append(start)
            ftimes.append(end)

        index = list(range(len(events)))
        index.sort(key=lambda i: ftimes[i])

        maximal_set = set()
        prev_finish_time = 0  
        for i in index:
            if stimes[i] >= prev_finish_time and not self.check_event_conflicts_excluding_self(events[i]):
                maximal_set.add(i)
                prev_finish_time = ftimes[i]

        return maximal_set

    def suggest_optimal_schedule(self, events: List[eventPost]) -> Dict:
        if not events:
            return {
                "optimal_events": [],
                "conflicted_events": [],
                "status": "no_events"
            }

        optimal_indices = self.interval_scheduling(events)
        
        optimal_events = [events[i] for i in optimal_indices]
        conflicted_events = [event for i, event in enumerate(events) if i not in optimal_indices]
        

        optimal_events_ranked = sorted(
            optimal_events,
            key=lambda e: self._predict_interest(e),
            reverse=True
        )
        
        return {
            "optimal_events": optimal_events_ranked,
            "conflicted_events": conflicted_events,
            "status": "success"
        }