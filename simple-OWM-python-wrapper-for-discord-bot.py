import requests
from time import time
import ast



#this class uses open weather maps API

class WeatherUpdate(object):

    def __init__(self,apiKey):

        self._apiKey = apiKey
        self._citiesAsked = {}
        self._timeStamp =0
        self._windSpeed = None
        self._humidity = None
        self._temperature = None
        self._mainWeather = None
        self._mainWeatherDesc = None
        self._cloudCoverage = None
        self._location = None


    def getTemperature(self,location):
        """
            Returns the locations temperature in degrees celcius
        """

        self.timeToUpdate(location)

        return location + ": " + self._temperature + " degrees celcius"

    def getWeatherStatus(self,location):
        """
            Returns basic info about the locations current weather. ie misty,
            windy, sunny etc.
        """

        self.timeToUpdate(location)

        return location + ": " + self._mainWeather

    def getWeatherStatusDetail(self,location):
        """
            Returns the locations current weather with a little more detail. ie
            light winnds, heavy rain etc.
        """

        self.timeToUpdate(location)

        return location + ": " + self._mainWeatherDesc

    def getWindSpeed(self,location):
        """
            Returns the locations wind speed in KMPH.
        """

        self.timeToUpdate(location)

        return location + ": " + str(self._windSpeed)+" km/ph"

    def getHumidity(self,location):
        """
            Returns the locations humidity in a percentile format.
        """

        self.timeToUpdate(location)
        return location + ": " + str(self._humidity)+"%"

    def getCloudCoverage(self,location):
        """
            Returns the locations cloud coverage in percentile format.
        """

        self.timeToUpdate(location)

        return location + ": " + str(self._cloudCoverage)+"%"


    def timeToUpdate(self,location):
        """
            This method checks if we need to send a request for fresh weather stats
            for a particular location.
            This method prevents unneeded requests from being sent if we have valid data
            for a previously asked location that is currently stored in memory.
        """
        timeStampNow = int(time()) #unix timestamp

        self._timeStamp = timeStampNow #updating our time for the next request

        try:
            locationInfo = self._citiesAsked[location]
            city = locationInfo[0]
            lastUpdateTimeForCity = locationInfo[1]
            

            if ((timeStampNow - int(lastUpdateTimeForCity))/60) >= 30:
                self.processFreshRequest(location) #stale data, send for new data for the same city stored

            elif self._location!=location: #we have it ready already
                self.updateFields(city,location) #just update with our stored info

        except KeyError: #dont have city
            self.processFreshRequest(location) #dont have it so we send for city


    def updateFields(self,dictionary,location):
        """
            This method updates our objects fields with fresh information that
            was requested for.
            This information may already be stored or may be freshly retrieved from
            the open weather api.
        """

        #if we already have the city stored and dont want to have to re send a request
        self._mainWeather = dictionary["weather"][0]["main"]
        self._mainWeatherDesc = dictionary["weather"][0]["description"]
        self._temperature =  "%.2f" % (dictionary["main"]["temp_max"] - 273.15) #KELVIN TO CELCIUS
        self._humidity = dictionary["main"]["humidity"]
        self._windSpeed = "%.2f" % (dictionary["wind"]["speed"] *3.6) #MPS -> KMPH
        self._cloudCoverage ="%.2f" % (dictionary["clouds"]["all"]) #%
        self._location  = location





    def processFreshRequest(self,location):

        """
            This method asks the openweathermap api for fresh weather information
            for a given location and then updates our stored city dictionary and
            asks for the objects fields to be updated accordingly.
        """

        request = requests.get('https://api.openweathermap.org/data/2.5/weather?q=%s&type=accurate&APPID=%s'% (location,self._apiKey))

        if request.status_code==200:

            dictionary = ast.literal_eval(request.text)

            time = self._timeStamp
            self._citiesAsked[location]=[dictionary,time]
            self.updateFields(dictionary,location)

        else:
            raise ValueError("Invalid country/city (name/substring)")

if __name__ == '__main__':

    w = WeatherUpdate("6b366290283f7986ea062f324197a64c")
    print(w.getWeatherStatus("Cork"))
    print(w.getWeatherStatusDetail("Cork"))
    print(w.getWeatherStatus("Dublin"))
    print(w.getWeatherStatus("Cork"))
    print(w.getTemperature("Israel"))
    print(w.getWeatherStatusDetail("Dublin"))
