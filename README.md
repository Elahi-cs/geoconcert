# GeoConcert
#### Video Demo: https://youtu.be/V6O0rtt73wM
#### Description:
GeoConcert is a web app that allows you to find concerts for your favorite artists on a world map.

## Warning: Work in Progress
Because of a recent update to the (Spotify Developer Terms)[https://developer.spotify.com/terms/], developers need to manually add users before they can authenticate with an app until Spotify has reviewed the application. If you want to use this application before then, send me an email and include your Spotify associated email address.

## About

[GeoConcert](https://geoconcert.herokuapp.com/) asks Spotify for your favorite artists and then asks about those artists to the TicketMaster database.
Then, it takes that information and renders it in a Google Map so you can see where your favorite artists are playing, anywhere in the world!

## Features:

* Select one of your favorite artists to see when and where they will play on a Google Map!
* You can filter the artists by the dates you are interested in.
* You can select only one, a few, or even all of your favorite artists!

## Planned Features:

These are the features that are waiting to be developed at some point in the future:

* Search for artist concerts using a search bar.
* Hide/toggle artist markers in the map.

## Design Choices
* **Real app**: GeoConcert was born out of a real-life problem: I was planning to travel with my girlfriend and we wanted to attend some of our favorite artists' concerts if we could.
We decided to check which artists would play close to where we wanted to go at the time of our hypothetic stay. We found the process of gathering information and thinking of artists that could be playing then and there to be really tedious.
It was for that situation that I thought of developing GeoConcert, an app that would allow us to skip the hurdles of navigating through artists tour dates and individually checking where each tour was.
So, from the beginning, GeoConcert was concieved as a real app that could solve a real world problem (albeit not a very important one). Most of the design choices were made with that problem in mind.

* **Easy to use**: Having looked at some other projects and web applications, I decided that another thing I wanted GeoConcert to be is easy to use for the user. I decided that the app must be able to be used without reading any instructions, and that the process, UI, and UX should be intuitive enough that the user wouldn't need a guide. Let me know how I did!

* **API usage**: I was inspired to use the Spotify API by another project, [Divide for Spotify](https://github.com/TiceWise/SpotifyDivide). After seeing what that API could and couldn't do, I knew I needed at least another service that could find the concert information, which ended up being the TicketMaster API because it was comprehensive and well documented. Lastly, I decided to use the Google Maps API because I found it to be the best option to handle maps and custom markers.

* **User choices**: The initial thought was to let the app do everything, just log in and see your top artists on a map. After some tinkering I decided that the user should have some agency on which artists they see and when.

* **Flask blueprints**: I knew from the beginning I was going to use Flask to build the app. But after researching its documentation, I decided another thing: I would use Flask's blueprint system instead of having all the app's logic in a single app.py file. Blueprints are a way to encapsulate functionalities as a collection of independent components. This improves code reuse and makes it easier to extend an application's functionality. I made this choice in case I wanted to keep working on this project for longer than was originally planned.

## File descriptions
* `config.py` has most of the app's configuration; where to find the environment variables needed for the various API calls, and whether to activate the app in development mode or production mode.
* `setup.py` contains the instructions to install the app as a package.
* `wsgi.py` exists so Heroku is able to properly load the app.
* `tests/` includes some early testing logic, but the coverage isn't nearly as it should be and I want to work on this at some point.
* `geoconcert/` contains all of the app's logic:
    - `static/` is where all static files are, that is, all files that won't be changed by the application's code.
    - `templates/` stores all the HTML and some JavaScript needed to render and make the different pages work.
    - `__init__.py` is the file that joins all the app's blueprints and creates an app from them. This is called an **application factory**.
    - `auth.py` handles all the authentication logic and behavior, that is, an user's Spotify acess token (log in), the ability to delete all stored information (log out) as well as logic to ensure a user is logged in before they can access the application.
    - `maps.py` handles the main application logic, which is the API call pipeline (Spotify to TicketMaster to Google Maps).

## Privacy and Data
The only data GeoConcert uses is provided by your Spotify account, namely your username and top artists. This data will not be stored for more than a day and can be immediately cleared by logging out. Your information will not be stored, sold to, nor shared with Third Parties in any way.
