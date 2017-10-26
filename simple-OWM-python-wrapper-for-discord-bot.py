import requests
import datetime
import shelve
import ast



#this class uses open weather maps API

class WeatherUpdate(object):

    def __init__(self,apiKey):

        self._apiKey = apiKey
        self._citiesAsked = {}
        self._time = 0
        self._windSpeed = None
        self._humidity = None
        self._temperature = None
        self._mainWeather = None
        self._mainWeatherDesc = None
        self._location = None




    def getTemperature(self,location):

        self.timeToUpdate(location)

        return location + ": " + self._temperature + " degrees celcius"

    def getWeatherStatus(self,location):

        self.timeToUpdate(location)

        return location + ": " + self._mainWeather

    def getWeatherStatusDetail(self,location):

        self.timeToUpdate(location)

        return location + ": " + self._mainWeatherDesc

    def getWindSpeed(self,location):
        self.timeToUpdate(location)

        return location + ": " + str(self._windSpeed)+" km/ph"

    def getHumidity(self,location):

        return location + ": " + str(self._humidity)+"%"


    def timeToUpdate(self,location):
        currenthour = datetime.datetime.now().hour
        hoursBetweenLastUpdate = currenthour - self._time
        cityPrevAsked = location in self._citiesAsked

        if self._location == location: #if the user has asked for the same city
            if hoursBetweenLastUpdate >=3: #we have been asked the same location so we just need to check if it is time to update, if it isnt we do nothing
                print("needs update")
                self._time = currenthour
                self.processFreshRequest(location)

        elif cityPrevAsked: #if we have the cities details previously stored in our citiesAsked dictionary but isnt our current city
            print("has been asked")
            if currenthour - self._citiesAsked[location][1] < 3: #it is not time to update

                city = self._citiesAsked[location][0]
                self.updateFields(city,location) #already have the fresh info for that city so no need to re send a request
            else:
                print("its time to update?")
                self._time = currenthour #it is time to update so we update or time because that will be the time we most recently updated
                self.processFreshRequest(location)

        else: #we know it hasnt been previously asked so now we update
            print("we havent seen this before")
            self._time = currenthour
            self.processFreshRequest(location)







    def updateFields(self,dictionary,location):

        #if we already have the city stored and dont want to have to re send a request
        self._mainWeather = dictionary["weather"][0]["main"]
        self._mainWeatherDesc = dictionary["weather"][0]["description"]
        self._temperature =  "%.2f" % (dictionary["main"]["temp_max"] - 273.15) #KELVIN TO CELCIUS
        self._humidity = dictionary["main"]["humidity"]
        self._windSpeed = "%.2f" % (dictionary["wind"]["speed"] *3.6) #MPS -> KMPH
        self._location  = location





    def processFreshRequest(self,location):

        print("updating")
        request = requests.get('https://api.openweathermap.org/data/2.5/weather?q=%s&type=accurate&APPID=%s'% (location,self._apiKey))

        if request.status_code==200:

            dictionary = ast.literal_eval(request.text)

            time = self._time
            self._citiesAsked[location]=[dictionary,time]
            self.updateFields(dictionary,location)

        else:
            raise AttributeError("Invalid country/city (name/substring)") #AttributeError as we cannot update our fields with incorrect location data, as we get an Error 404

if __name__ == '__main__':

    w = WeatherUpdate("API KEY")
    print(w.getWeatherStatus("Cork"))
    print(w.getWeatherStatusDetail("Cork"))
    print(w.getWeatherStatus("Dublin"))
    print(w.getWeatherStatus("Cork"))
    print(w.getTemperature("Israel"))
    print(w.getWeatherStatusDetail("Dublin"))
