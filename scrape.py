from bs4 import BeautifulSoup
import requests
import pandas as pd
from csv import writer

def to_xlsx(Links_with_titles, date):
    #initialize data frame
    data = {
        'date': date,
        'Article': Links_with_titles
    }
    df = pd.DataFrame(data)

    #convert the date column to date time to make sure it correctly sorts
    df['date'] = pd.to_datetime(df['date'], errors = 'coerce') #handles invalid date format as NaT (Not a Time)
    
    #sort by date
    df_sorted = df.sort_values(by = 'date', ascending= True) # ascending false for descending order
    
    #convert it back to original string format
    df_sorted['date'] = df_sorted['date'].dt.strftime('%B %d, %Y') 

    #save to excel
    df_sorted.to_excel("news.xlsx", index= False, engine= 'openpyxl')

#Gets all links from startIndex until EndIndex first page is 0
def get_njit_news_links(startIndex, endIndex):
    base_url = "https://news.njit.edu"

    #lists to store links and data across all pages
    all_links_with_titles = []
    all_dates = []
    for page in range( (int)(startIndex), (int) (endIndex) + 1):
        url = f"https://news.njit.edu/news?page={page}"
        #send a Get Request to fetch the page content
        page = requests.get(url)

        #parse content with BeatifulSoup
        soup = BeautifulSoup(page.text, 'html.parser')

        #extracting all anchaor tags with the class news-link
        links = soup.find_all('a', class_='news-link')

        #Gets the title and dates and puts then in a list
        titles = [h4.find('span', class_='field-content').get_text() for h4 in soup.find_all('h4', class_='media-heading ng-binding')]
        date = [div.find('span', class_='date-display-single').get_text() for div in soup.find_all('div', class_ ='story-date ng-binding')]

        link_List =[]
        #concatenate the base URL with all the links
        for link in links:
            link_List.append(base_url + link.get('href')) 

        Links_with_titles = [f'=HYPERLINK("{link}","{title}")' for link, title in zip(link_List,titles)]

        #add results from all pages to the lists
        all_links_with_titles.extend(Links_with_titles)
        all_dates.extend(date)

    return all_links_with_titles,all_dates


startindex = input("Starting Page Number: ")
endIndex = input("Ending Page Number: ")

links_with_titles, date = get_njit_news_links(startindex, endIndex)

to_xlsx(links_with_titles, date)




