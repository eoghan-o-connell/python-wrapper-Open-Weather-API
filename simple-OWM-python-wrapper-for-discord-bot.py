import requests
from time import time
import ast



#this class uses open weather maps API

class WeatherUpdate(object):

    def __init__(self,apiKey):

        self._apiKey = apiKey
        self._citiesAsked = {}
        self._timeStamp = None
        self._location = None



    def getTemperature(self,location):
        """
            Returns the locations temperature in degrees celcius
        """

        return location + ": " + str(self.retrieveInformation(location,"temp")) + " degrees celcius"



    def getWeatherStatus(self,location):
        """
            Returns basic info about the locations current weather. ie misty,
            windy, sunny etc.
        """

        self.timeToUpdate(location)

        return location + ": " + str(self.retrieveInformation(location,"mainWeather"))



    def getWeatherStatusDetail(self,location):
        """
            Returns the locations current weather with a little more detail. ie
            light winnds, heavy rain etc.
        """

        return location + ": " + str(self.retrieveInformation(location,"mainWeatherDesc"))



    def getWindSpeed(self,location):
        """
            Returns the locations wind speed in KMPH.
        """

        return location + ": " + str(self.retrieveInformation(location,"windspeed")) +" km/ph"



    def getHumidity(self,location):
        """
            Returns the locations humidity in a percentile format.
        """

        return location + ": " + str(self.retrieveInformation(location,"humidity")) +"%"



    def getCloudCoverage(self,location):
        """
            Returns the locations cloud coverage in percentile format.
        """


        return location + ": " + str(self.retrieveInformation(location,"coverage")) +"%"




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

        except KeyError: #dont have city

            self.processFreshRequest(location) #dont have it so we send for city



    def retrieveInformation(self,location,weatherType):
        """
            This method updates our objects fields with fresh information that
            was requested for.
            This information may already be stored or may be freshly retrieved from
            the open weather api.
        """

        self.timeToUpdate(location)

        dictionary = self._citiesAsked[location][0]

        if weatherType=="mainWeather":
            return dictionary["weather"][0]["main"]

        elif weatherType=="mainWeatherDesc":
            return dictionary["weather"][0]["description"]

        elif weatherType=="temp":
            return "%.2f" % (dictionary["main"]["temp_max"] - 273.15) #KELVIN TO CELCIUS

        elif weatherType=="humidity":
            return dictionary["main"]["humidity"]

        elif weatherType=="windspeed":
            return "%.2f" % (dictionary["wind"]["speed"] *3.6) #MPS -> KMPH

        elif weatherType=="coverage":

            return "%.2f" % (dictionary["clouds"]["all"]) #%



    def processFreshRequest(self,location):

        """
            This method asks the openweathermap api for fresh weather information
            for a given location and then updates our stored city dictionary and
            asks for the objects fields to be updated accordingly.
        """

        request = requests.get('https://api.openweathermap.org/data/2.5/weather?q=%s&type=accurate&APPID=%s'% (location,self._apiKey))

        if request.status_code==200:

            dictionary = ast.literal_eval(request.text)

            self._citiesAsked[location] = [dictionary,int(time())]

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
