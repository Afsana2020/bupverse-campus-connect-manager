
# A Web Platform for Sharing Services and Connectivity among Students
BUPVerse is a Django-based web application that combines multiple student-focused services in one platform. It integrates real-time recommendation systems and scheduling algorithms using core data structures and algorithms (DSA). The goal is to simplify campus life for students at the Bangladesh University of Professionals (BUP).

The system includes three main modules:

- NextDoor Tutor

- Roommate Finder

- Event Hub

These modules are implemented using Dijkstra’s Algorithm, Segment Tree, Interval Scheduling, and 0/1 Knapsack to ensure optimal performance and personalization.

## Features: 

### 1) Homepage:
   
![homepage](https://github.com/user-attachments/assets/267495db-0fd4-4b90-b5c7-796f889adf8c)


The homepage of BUPVerse provides a clean and intuitive user interface. It acts as a navigation hub for the entire system. Users can easily access modules like NextDoor Tutor, Roommate Finder, and Event Hub from here.

### 2) Login:

![login](https://github.com/user-attachments/assets/d89eabb5-31a6-4595-8263-64437421ecd4)


### 3) Registration:

![reg](https://github.com/user-attachments/assets/63d08148-dc72-4a8d-b04a-b1f9744f709a)



### 4) NextDoor Tutor:
The NextDoor Tutor module connects students and tutors using a graph-based system where each post is a node. A customized Dijkstra’s Algorithm calculates compatibility scores based on subject match, budget, gender preference, and location (via OpenRouteService and Nominatim). A max-heap retrieves the top-K best matches efficiently, with real-time updates as users post or edit, enabling dynamic, personalized recommendations.


- Homepage

![thome](https://github.com/user-attachments/assets/529e8ba7-b378-4f26-8492-6c8b593e324e)


- Matching:

![tmatch](https://github.com/user-attachments/assets/d50fa24e-76df-4deb-8a13-ecccf71adfed)

![tmatchres](https://github.com/user-attachments/assets/c13e268b-e5ff-4a7b-a290-793522e1f3ab)




### 5) Roommate Finder:

The Roommate Finder module helps students find compatible roommates using a graph-based model. Each user is a node, and matches are scored with a customized Dijkstra’s Algorithm. Key factors include location (high weight), rent and gender (medium), and food preferences (low). A max-heap retrieves the top-K matches, delivering personalized, real-time roommate suggestions.

- Homepage:

![roomH](https://github.com/user-attachments/assets/481e1683-2535-4d7b-9013-5d0ffe497a72)


- Matching

![roompost](https://github.com/user-attachments/assets/ca2f4d91-4fda-4042-a42b-90b35e8e0526)

![roommatch](https://github.com/user-attachments/assets/9c03dce4-23c0-4bba-b80c-f3d8158d2a9f)




### 6) Campus events:

The Event Hub centralizes event info across BUP clubs and departments, helping students discover and manage events efficiently. It uses a segment tree to quickly detect schedule conflicts and a greedy interval scheduling algorithm to suggest non-overlapping events. For personalized planning, a 0/1 Knapsack algorithm recommends the most valuable set of events based on user availability and event priority, maximizing utility while avoiding clashes.

- Homepage
- 
![eventshome](https://github.com/user-attachments/assets/f0001f8f-4b4c-44a4-ac05-65f0e6fd63bd)


- Conflict free event list

![list](https://github.com/user-attachments/assets/c91912e4-20c6-4fe4-abc1-2300efd77e33)


If the user is logged in, the list displays a personalized list of events—highlighting conflict-free ones and clearly indicating any scheduling conflicts.


- Event manager

![manage](https://github.com/user-attachments/assets/406d6ea4-3360-4d57-99ab-cd6e0dab31d8)


The Event Manager allows users to manage events they’ve created or plan to attend, featuring a smart time allocator and regular routines management.

- Smart time allocator

![eventrecom](https://github.com/user-attachments/assets/4315e291-2f9a-4a81-b118-0fe7734cfa84)


![weekly recom](https://github.com/user-attachments/assets/51796122-6255-4dbd-9cb0-128dbd9b274a)


The smart time allocator schedules the maximum number of events based on their importance scores and the available time in a given week

- Routine management

![routine](https://github.com/user-attachments/assets/dafe63ef-01d9-4e3d-974b-358d596b1863)


Routine management handles regular tasks by blocking busy time slots and schedules events while resolving conflicts with these routines.

- Fixing conflict

![conlfic](https://github.com/user-attachments/assets/0e1afff2-4ccd-4192-8f13-fbe249019fd2)

![con solve](https://github.com/user-attachments/assets/cee0f5e5-25ca-4d9f-8bf4-a074506dc4da)

Notify users about sudden event time changes to inform them of any conflicts with their existing schedule and help them resolve these conflicts easily.

## Tool Used: 
- Backend: Django (Python)

- Frontend: HTML, CSS, JavaScript, Bootstrap

- Database: SQLite

- APIs: OpenRouteService, Nominatim (for geolocation)


## Contact:
Email: afsanahena24@gmail.com

LinkedIn: https://www.linkedin.com/in/afsana-hena/
