from html.parser import HTMLParser
from urllib.request import urlopen
from datetime import datetime, timedelta
import numpy as np

class WeatherHTMLParser(HTMLParser):
    """
    The WeatherHTMLParser class handles and scrapes the data from the website.
    """
    def __init__(self):
        super().__init__()
        self.inside_table = False
        self.inside_thead = False
        self.inside_tbody = False
        self.inside_tr = False
        self.inside_td = False
        self.current_row = []

        self.temps_data = []
        self.dates_data = []

        self.temps_data_format = {}
        self.dates_data_format = {}

        self.formatted_temps_list = []
        self.formatted_dates_list = []

        self.final_output = {}

        self.pool = []
        self.stop = True
        self.compare = []
        self.test = []
        
    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.inside_table = True
        elif self.inside_table and tag == 'thead':
            self.inside_thead = True
        elif self.inside_table and tag == 'tbody':
            self.inside_tbody = True
        elif self.inside_tbody and tag == 'tr':
            self.inside_tr = True
            self.current_row = []
        elif self.inside_tr and tag == 'td':
            self.inside_td = True

        if tag == "abbr" and self.inside_tr:
            for attr in attrs:
                self.dates_data.append(attr[1])

    
    def handle_data(self, data):
        if self.inside_td and len(self.current_row) < 3:
            self.current_row.append(data.strip())

    def handle_endtag(self, tag):
        if self.inside_td and tag == 'td':
            self.inside_td = False
        elif self.inside_tr and tag == 'tr':
            self.inside_tr = False
            if len(self.current_row) > 0:
                self.temps_data.append(self.current_row)
        elif self.inside_tbody and tag == 'tbody':
            self.inside_tbody = False
        elif self.inside_thead and tag == 'thead':
            self.inside_thead = False
        elif self.inside_table and tag == 'table':
            self.inside_table = False

    def scrape_from_today(self, today = datetime.today()):        
        while self.stop:
            with urlopen(f'https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=1&Year={today.year}&Month={today.month}#') as response: 
                html = str(response.read())
            self.feed(html)

            self.compare = self.final_output.copy()
            self.test = self.dates_data.copy()

            for list in self.temps_data[:-4]:
                if list[0] != '' and list[1] != '' and list[2] != '':
                    max = list[0]
                    min = list[1]
                    mean = list[2]
                if list[0] == 'LegendM' and list[1] == 'M' and list[2] == 'LegendM':
                    max = np.NaN
                    min = np.NaN
                    mean = np.NaN
                if list[0] == '' and list[1] == '' and list[2] == '':
                    max = np.NaN
                    min = np.NaN
                    mean = np.NaN
                if list[0] == '' and list[1] == '' and list[2] == 'LegendM':
                    max = np.NaN
                    min = np.NaN
                    mean = np.NaN
                if list[0] == 'LegendM' or list[1] == '' or list[2] == 'LegendM':
                    max = np.NaN
                    min = np.NaN
                    mean = np.NaN
                if list[0] == 'LegendM' or list[1] == 'LegendM' or list[2] == 'M':
                    max = np.NaN
                    min = np.NaN
                    mean = np.NaN
                if list[0] == '' or list[1] == 'LegendE' or list[2] == 'E':
                    max = np.NaN
                    min = np.NaN
                    mean = np.NaN
                if list[0] == 'LegendE' or list[1] == 'LegendE' or list[2] == 'LegendE':
                    max = np.NaN
                    min = np.NaN
                    mean = np.NaN

                formatted_temps = {'Max': max, 'Min': min, 'Mean': mean}
                self.formatted_temps_list.append(formatted_temps)

            for dates in self.dates_data[:-2]:
                date_object = datetime.strptime(dates, '%B %d, %Y')
                formatted_date = date_object.strftime('%Y-%m-%d') 
                self.formatted_dates_list.append(formatted_date)
            
            for i in range(len(self.formatted_dates_list)):
                self.final_output[self.formatted_dates_list[i]] = self.formatted_temps_list[i]

            print(f'SCRAPED DATA FROM: ' + str(today.date()))
            self.temps_data = []
            self.dates_data = []

            if self.final_output == self.compare and self.dates_data != self.test:
                break   

            today -= timedelta(days=31)
            
        return self.final_output
    