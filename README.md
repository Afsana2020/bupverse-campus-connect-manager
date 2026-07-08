
# A Web Platform for Sharing Services and Connectivity among Students
BUPVerse is a Django-based web application that combines multiple student-focused services in one platform. It integrates real-time recommendation systems and scheduling algorithms using core data structures and advanced DSA algorithms, along with deep learning NLP architecture (all-MiniLM-L6-v2 Bi-Encoder) for semantic preference matching. The goal is to simplify campus life for students at the Bangladesh University of Professionals (BUP).

The system includes three main modules:

- NextDoor Tutor

- Roommate Finder

- Event Hub

These modules are implemented using Sentence-Transformers (the all-MiniLM-L6-v2 Bi-Encoder AI model), PyTorch Vector Mathematics, Segment Trees, Interval Scheduling, and 0/1 Knapsack to ensure optimal performance, low latency, and deep personalization.

## Features: 

### Main Homepage:
   
![homepage](https://github.com/user-attachments/assets/267495db-0fd4-4b90-b5c7-796f889adf8c)


The homepage of BUPVerse provides a clean and intuitive user interface. It acts as a navigation hub for the entire system. Users can easily access modules like NextDoor Tutor, Roommate Finder, and Event Hub from here.

### Login:

![login](https://github.com/user-attachments/assets/d89eabb5-31a6-4595-8263-64437421ecd4)


###  Registration:

![reg](https://github.com/user-attachments/assets/63d08148-dc72-4a8d-b04a-b1f9744f709a)



### NextDoor Tutor:
The NextDoor Tutor module connects students and tutors using an advanced Semantic AI Matchmaking Architecture. Instead of relying on strict keyword matching, the module utilizes the deep learning all-MiniLM-L6-v2 Sentence-Transformer model to convert raw user profiles (subjects, budget, medium, and class level) into high-dimensional vector embeddings.

To prevent server lag, candidate profiles are evaluated using PyTorch Batch Matrix Multiplication (util.pytorch_cos_sim) to calculate semantic similarity scores instantly. This is combined with an exponential decay location scoring algorithm (via OpenRouteService API) using a 70% AI with 30% Geographic Proximity hybrid formula to fetch the Top-K best matches in milliseconds.

- NextDoor Homepage

![thome](https://github.com/user-attachments/assets/529e8ba7-b378-4f26-8492-6c8b593e324e)


- Matching:

![tmatch](https://github.com/user-attachments/assets/d50fa24e-76df-4deb-8a13-ecccf71adfed)

![tmatchres](https://github.com/user-attachments/assets/c13e268b-e5ff-4a7b-a290-793522e1f3ab)




### Roommate Finder:

The Roommate Finder module helps students find highly compatible room pairings by analyzing human lifestyle context. The module dynamically translates user database rows (rent expectations, food preferences, clean/noisy habits, and location) into clean, natural-language text strings, which are then passed into the cached all-MiniLM-L6-v2 model.

By calculating the mathematical cosine angle between the user's vector and all pool candidates simultaneously, the AI grasps "soft preferences" (e.g., matching "quiet environment" with "peaceful room"). A local LRU cache prevents redundant model computations, rendering highly personalized roommate rankings with maximum runtime efficiency.

- Roommate FinderHomepage:

![roomH](https://github.com/user-attachments/assets/481e1683-2535-4d7b-9013-5d0ffe497a72)


- Matching

![roompost](https://github.com/user-attachments/assets/ca2f4d91-4fda-4042-a42b-90b35e8e0526)

![roommatch](https://github.com/user-attachments/assets/9c03dce4-23c0-4bba-b80c-f3d8158d2a9f)




### Campus events:

The Event Hub centralizes event info across BUP clubs and departments, helping students discover and manage events efficiently. It uses a Segment Tree to quickly detect schedule conflicts and a greedy Interval Scheduling algorithm to suggest non-overlapping events. For personalized planning, a 0/1 Knapsack algorithm recommends the most valuable set of events based on user availability and event priority, maximizing utility while avoiding clashes.

- Campus Events Homepage
  
![eventshome](https://github.com/user-attachments/assets/f0001f8f-4b4c-44a4-ac05-65f0e6fd63bd)


- Conflict free event list

![list](https://github.com/user-attachments/assets/c91912e4-20c6-4fe4-abc1-2300efd77e33)


If the user is logged in, the list displays a personalized list of events—highlighting conflict-free ones and clearly indicating any scheduling conflicts.


- Event manager:

![manage](https://github.com/user-attachments/assets/406d6ea4-3360-4d57-99ab-cd6e0dab31d8)

- Events in your routine:

  ![urevent](https://github.com/user-attachments/assets/eb33a984-8799-4229-aa82-911fdc9feb24)



The Event Manager allows users to manage events they’ve created or plan to attend, featuring a smart time allocator and regular routines management.

- Smart time allocator:

![eventrecom](https://github.com/user-attachments/assets/4315e291-2f9a-4a81-b118-0fe7734cfa84)


![weekly recom](https://github.com/user-attachments/assets/51796122-6255-4dbd-9cb0-128dbd9b274a)


The smart time allocator schedules the maximum number of events based on their importance scores and the available time in a given week

- Routine management:

![routine](https://github.com/user-attachments/assets/dafe63ef-01d9-4e3d-974b-358d596b1863)


Routine management handles regular tasks by blocking busy time slots and schedules events while resolving conflicts with these routines.

- Fixing the conflict:

![conlfic](https://github.com/user-attachments/assets/0e1afff2-4ccd-4192-8f13-fbe249019fd2)

![con solve](https://github.com/user-attachments/assets/cee0f5e5-25ca-4d9f-8bf4-a074506dc4da)

Notify users about sudden event time changes to inform them of any conflicts with their existing schedule and help them resolve these conflicts easily.

## Tool Used: 
- AI & Machine Learning: Sentence-Transformers (all-MiniLM-L6-v2), PyTorch Vector Math
  
- Backend: Django (Python)

- Frontend: HTML, CSS, JavaScript, Bootstrap

- Database: SQLite

- APIs: OpenRouteService, Nominatim (for geolocation)

## Local Setup:
Please follow **read.txt** file.


## Contact:
Email: afsanahena24@gmail.com

LinkedIn: https://www.linkedin.com/in/afsana-hena/
