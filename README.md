# mealPal
COMS W4111 Course Project
Name: Lin Shi, Yanqing Dai

+ The PostgreSQL account: yd2369   
+ The URL of your web application: http://35.185.238.36:8111


#### Parts implemented: 
* All users have a food profile and 2 lists Eaten and To Eat within. Users can add restaurants to these lists using our web-app.
* The web-app will suggest some users that share some common interest. We only show users that have at least 1 same Eaten or To Eat restaurant with the user. We also only show the users located in the same city if there is at least 1 other user that’s in the same city.
* Users can then click yes to show interest and no for not interested. (We used 2 buttons instead of swiping.)
* If 2 users are mutually interested into each other, they are matched by our system.
* Once matched, the user can send a request to the other user, suggesting a date to have a meal together and leaving one’s contact information.

#### Parts not implemented:
* We didn’t use Yelp API for searching restaurant. Instead, we populated our Restaurants Table by some static data. The reason is that implementing Yelp API takes long time and it doesn’t necessarily relate strong to SQL database access. We decided to put more effort to designing and interacting with our database.
* We didn’t implement the swiping activity. Instead, we used 2 button to provide the same function. We believe that wouldn’t sacrifice our app’s interaction with our database too much and it’s easier to implement.

#### There are no new features that were not included in the proposal.

#### Two interesting pages and the reason why they are interesting:
* Food profile page: The food profile page lists all the restaurants’ ID and names. Users can add eaten restaurants by entering restaurant’s ID, score and review. They can also add marked restaurants. After user entered the restaurant’s information, the database will be updated. The database will first check whether the restaurant’s ID(rid) the user enters is in the database. If not, the page will reload and let the user to enter again. For scores, if the score is not in the range of 1-5 or the review is empty, the page will reload and let the user to enter again.

  This page is interesting because it interacts with 3 different tables and users thus can see all the restaurants and record the ones they have been and mark the ones that they want to go to.
* Swipe page: The swipe page will suggest some users that share some common interests such as they are in the same city and they have been to or marked one same restaurant before. It will show all of that user’s information: such as his/her name, gender, date of birth, location, eaten restaurants, and marked restaurants. User can press yes button to show interest in this user and no otherwise. User can press send request button to send a request including contact info and date to eat if they both show interest to each other. On the bottom of the page, user can press back to profile to direct back. Once users input yes, the database will be updated and record that user is interested in this person. 

  This page is interesting because it interacts with 6 different tables to provide an interactive interface for user to interact with each other. And the interaction with our database includes checking if a tuple exists, filtering some data and combining information from different table together.
