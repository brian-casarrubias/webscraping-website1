import requests
from bs4 import BeautifulSoup
import re
import json


title_regex = re.compile(r'''
    <p>
    ([a-zA-Z0-9<>"=\s:]+)
   
   
''', re.VERBOSE)
month_year_regex = re.compile(r'''
    (\d{2}.\d{2}.\d{4})
''', re.VERBOSE)

start_time_regex = re.compile(r'''
    (\d{2}:\d{2})
''', re.VERBOSE)

location_regex = re.compile(r'''
    <p>
    ([a-zA-Z\w\s.-]+)
''', re.VERBOSE)

def scrape_website(url:str):

    #create an empty movie titles dictionary to use at the end after we have obtained all the info
    movie_titles = {}
   

    data = requests.get(url).content
    soup = BeautifulSoup(data, 'lxml') #get the entire website
    filtered_html = str(soup.find_all(class_='controller-content')) #filter by only the content inside this div, then we can filter further
    soup = BeautifulSoup(filtered_html, 'lxml') #create another soup based on above new filter

    titles = soup.find_all(class_='media-title') ### get all the titles from this i can filter
    dates = soup.find_all(class_='media-date')   ##get all the dates now from this we can filter to get the month/day/year and also the time

    start_time = soup.find_all('span', class_='start-date') #filter by start time
    end_time = soup.find_all('span', class_='end-date')     #filter by end date
    locations = soup.find_all(class_='media-text')          #filter locations
    
  

   
 
   #------------------------final values---------------------

    titles = titles = title_regex.findall(str(titles))           #done with titles

    date = month_year_regex.findall(str(dates))                  #done with month/day/year
    start_time = start_time_regex.findall(str(start_time))       #done with start time
    end_time = [date.get_text() for date in end_time]            #done with the end time  the get_text gets the text inside, not including the tags
    location = location_regex.findall(str(locations))            #done with locations, all are the same location :}
    image_link = [img['src'] for img in soup.find_all('img')]    #done with all the images

    #now that we have all the values, lets add these values into our dictionary that we have created in the beginning
    
    for index, movie in enumerate(titles):
        movie_titles[movie] = {
            'date':date[index] if index < len(date) else 'None',
            'start_time':start_time[index] if index < len(start_time) else 'None',
            'end_time': end_time[index] if index < len(end_time) else 'None',
            'location':location[index] if index < len(location) else 'None',
            'image_link':image_link[index] if index < len(image_link) else 'None'
        }
    

    #now we convert this python dictionary to json like requested
    movie_titles_json = json.dumps(movie_titles, indent=4, ensure_ascii=False) ## the ensure, makes it so that those wierd characters are correct 
    print(movie_titles_json)
    # return movie_titles_json



scrape_website('https://www.vdl.lu/en/whats-on')
# scrape_website('https://www.vdl.lu/en/whats-on?page=1')

   




