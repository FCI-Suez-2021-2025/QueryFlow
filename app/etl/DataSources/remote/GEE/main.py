from GoogleEarthAPIDataCollector import GoogleEarthAPIDataCollector


data_collector = GoogleEarthAPIDataCollector('ee-mohamedmagdy721')
end_date = "2024-11-22"
start_date = "2024-06-14"

latitude = 30.0065457
longitude = 27.5157469
data = data_collector.collect(start_date,end_date,longitude,latitude,1000)
print(data)