VIDEO LINK: https://drive.google.com/file/d/1gVc5IoTqrvq-2g_9hDVBxWN2eA4oeawm/view?usp=sharing

I would split up my problem into the following decomposition. I chose this order becuase it makes the most sense to be followed in a linear fashion for the building for my project logically. Everything is something that needs to be done before moving onto the next. 

1. Prototype rough UI
The first step to the project has to be deciding how to represent visually in a UI sense each destination’s open hours, visit duration per destination, any fixed reservation, daily start and end times, and starting / ending location. This can be iterated with AI. 

2. Define shortest trip 
Next, I need to actually decide what “shortest trip” means for the algorithm. I'm thinking right now that the initial goal will be to minimize the number of days needed and then then minimize the travel time among schedules using the same number of days. This is doable with AI also. 

3. Build a checker for one day’s schedule
Next, I will use AI to help write a function that checks whether a given order of destinations fits into one day. For example, if I enter museum → restaurant → park, it will follow that exact order and calculate when I would arrive at and leave each place. It will account for travel time and waiting before a place opens, and check whether I can finish each visit before closing, meet reservations, and finish the day on time. This step does not choose the best order yet, it just checks whether one proposed order works. I can specify this clearly to AI and test it with small examples where I will calculate the correct answer myself. This will be my initial prototype.

4. Find the best order for a single day
Next, I will build code using AI that compares possible visiting orders for a small set of destinations. It will use the reject invalid orders and compare all possible routes internall.For the first verwitsion, I will limit the number of destinations so that checking every possible order is within reasonable runtime, as my mentor reccommended. I can work with AI to implement this and then also for the testing against examples h known answers. 

5. Extend the planner across multiple days
Once the single-day version works, I will add the ability to divide destinations across days while respecting opening hours and reservations tied to particular days. The program will compare daily groupings and visiting orders to find the shortest feasible trip within the supported input size. This is the most complicated part so I'll develop it through small iterations with AI. The first few days I will work with a few destinations, then more varied constraints. I'll also make the program report when no feasible itinerary exists. I chose this next because multi-day planning depends on the single-day checker and route comparison already working.

6. Build the full UI and test complete trips
Finally, I will refine and create the whole UI for entering destinations and viewing a day-by-day itinerary. I will use AI to help implement the interface and refine unclear inputs or error messages. I will then test complete example trips and check that the displayed itinerary matches the algorithm’s calculations. 

7. Refine and add
Figure out things to add, change, remove for the whole prototype in general. Work with AI to implement it all. 


Questions for  mentor:

- I'm also worried about runtime efficenicy of this problem. Should I place a limit on the website itself for how many destinations to hit? 
- How do I figure out what might be too many destinations / cause the most inefficeny?
- Should I add a UI of a map between stuff or just list out with words the itinarary and display time in between each, and then also display time overall. 
- Are there any parts of this scope you think I should refine or add or cut before I start?