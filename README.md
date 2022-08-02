# globant-weather-api

This project is an API where you can set a country and a city and get the current weather in that location, also you will get the forecast weather for the next five days with intervals of three hours. This API connects to a third-party api that belongs to OpenWeatherMap. It will get all the neccesary information about the weather and forecast and will parse it so you can get a human-readable json response.

## Usage

* Clone the repository inside a directory of your preference.
* Inside the directory you cloned the repository, activate the local environment ("source ./local_python_environment/bin/activate").
* Once the local environment is activated install the dependencies that are found in 'requirements.txt' ("pip install -r requirements.txt").
* When finished installing the dependencies go inside the directory "weather_project".
* Run the django server ("python manage.py runserver").
* Now open yout browser or software where you call an endpoint to use the url containing the parameters needed to call the API. (http://127.0.0.1:8000/weather/?city=<city>&country=<twoDigitCountryCode>).
  
## Testing
  
* To run the tests go inside the directory "weather_project". 
* Inside the directory run the command ("python3 manage.py test").
* Tests status will show up in terminal.
