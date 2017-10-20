import requests
import datetime
import shelve
import ast



#this class uses open weather map to retrieve info

class WeatherUpdate(object):

    def __init__(self,apiKey):

        self._apiKey = apiKey
        self._citiesAsked = {}
        self._temperature = None
        self._mainWeather = None
        self._mainWeatherDesc = None
        self._time = 0
        self._location = None




    def getTemperature(self,location):

        self.timeToUpdate(location)
        self._location = location

        return self._temperature

    def getWeatherStatus(self,location):

        self.timeToUpdate(location)
        self._location = location

        return self._mainWeather

    def getWeatherStatusDetail(self,location):

        self.timeToUpdate(location)
        self._location = location

        return self._mainWeatherDesc


    def timeToUpdate(self,location):

        currenthour = datetime.datetime.now().hour
        hoursBetweenLastUpdate = currenthour - self._time
        cityPrevAsked = location in self._citiesAsked

        if self._location != location: #if the user has asked for a different city
            if cityPrevAsked: #if we have the cities details previously stored in our citiesAsked dictionary
                print("has been asked")
                if currenthour - self._citiesAsked[location][1] < 3: #it is not time to update

                    self.updateFields(location) #already have the fresh info for that city so no need to re send a request
                else:
                    self._time = currenthour #it is time to update so we update or time because that will be the time we most recently updated
                    self.processFreshRequest(location)


            else: #we know it hasnt been previously asked so now we update
                print("we havent seen this before")
                self._time = currenthour
                self.processFreshRequest(location)

        elif hoursBetweenLastUpdate >=3: #we have been asked the same location so we just need to check if it is time to update, if it isnt we do nothing
            print("needs update")
            self._time = currenthour
            self.processFreshRequest(location)

        else: #we have been asked the same city and we dont need to re update as its within the time frame

            print("this is already our current one so nothing needs to happen")





    def updateFields(self,location):

        #if we already have the city stored and dont want to have to re send a request

        city = self._citiesAsked[location][0]

        self._mainWeather = city["weather"][0]["main"]
        self._mainWeatherDesc = city["weather"][0]["description"]
        self._temperature =  "%.2f" % (city["main"]["temp_max"] - 273.15)
        self._location  = location





    def processFreshRequest(self,location):

        print("updating")
        request = requests.get('https://api.openweathermap.org/data/2.5/weather?q=%s&APPID=%s'% (location,self._apiKey))
        dictionary = ast.literal_eval(request.text)

        time = self._time
        self._citiesAsked[location]=[dictionary,time]



        self._mainWeather = dictionary["weather"][0]["main"]
        self._mainWeatherDesc = dictionary["weather"][0]["description"]
        self._temperature =  "%.2f" % (dictionary["main"]["temp_max"] - 273.15)

        self._location  = location


if __name__ == '__main__':

    w = WeatherUpdate("API KEY")
    print(w.getWeatherStatus("Cork"))
    print(w.getWeatherStatusDetail("Cork"))
    print(w.getWeatherStatus("Dublin"))
    print(w.getWeatherStatus("Cork"))
    print(w.getTemperature("Israel"))
    print(w.getWeatherStatusDetail("Dublin"))
