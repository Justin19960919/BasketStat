# BasketStat


## About The Project
<!-- project screen shot -->
[![Product Name Screen Shot][product-screenshot]](https://example.com)

This project was built with the intention of creating a webapp that serves the purpose of recording basketball scores, which include
player scores, and team scores on the court, which provides a real-time analysis and calculation of team/ player statistics to help 
a local basketball team grow. The idea was that local basketball teams don't have the time and resources to hire an analytics team
to help with analyzing player combinations and track performance. Most team adjustments weren't data driven, and teams miss the 
opportunity to grow. The website also serves as a platform to integrate Posts, player management, score-tracking, and analysis all 
in one place.


### Built With

This section should list any major frameworks that you built your project using. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.
* Django
* Python 
* JavaScript
* PostGreSql
* Javascript
* Jquery
* Css


### Prerequisites
To use the django framework:
```
pip install Django
```
Other dependencies include:
- django-crispy-forms
- PILLOW


### How to run the app

1. Clone the repo
   ```
   git clone https://github.com/Justin19960919/BasketStat.git
   ```
2. Activate virtual environment
   ```
   source env/bin/activate
   ```
   
3. Make migrations to populate db
   ```python
   python manage.py makemigrations
   python manage.py migrate
   ```

4. Run server
   ```
   python manage.py runserver
   ```

5. Visit local host
   Go to http://localhost:8000/


## Features
An user is a whole basketball team, different teams can't access each others information.
- Landing Page
   ###### Landing page to introduce users to the features, and point to registering for an user

- Register/ Login / Logout
   - User needs to register in order to user the app
   - Upon register success, we create profile in the backend


- Profile
   - User can modify Profile, including change user profile picture
   - change information , e.g. Email


- Posts
   - B.c. a whole team shares an account, they can post about their feelings or thoughts
   regarding the game or practice.


- Games
   - CRUD functionality 
   - Keep track of all the games the team has played.


- Game Details
   - Details of the game (display information about the game when creating)
   - Access to player statistics in that game


- Record in game
   - Record the game in real time, upon creation of the game
   - Moves include scoring, rebounds, steals, assists, fouls .. etc
   - Automatic logging of play by play records when recording in the backend


- Comments
   - Comment about the game (what can be done better ..)


- Statistics
   - Automatic calculation of player and team statistics, and high level statistics including efg% (effective field goal pecentage), TS% (true shooting percentage ..etc)
   - Visualization using chart.js


- Players
   - Create / Delete players to the team
   - Once a player is created, upon creation of a game, the user is asked which players are to play in the game.


