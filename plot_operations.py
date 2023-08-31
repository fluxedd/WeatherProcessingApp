import datetime
import matplotlib.pyplot as plt
import numpy as np

class PlotOperations():
    """
    The PlotOperations class represents the class that does the boxplot and lineplot given the data.
    """
    def __init__(self):
        self.weather_data = {}
        self.months_means = {1: [], 2: [], 3: [], 4: [], 5:[], 6:[], 
                             7:[], 8:[], 9:[], 10:[], 11:[], 12:[]}
        self.line_plot_data = {}
        self.line_plot = []

    def make_boxplot(self, data, first_year, second_year):
        """
        Generates box plot given a range of year.
        """
        for mean_data in data:
            date_obj = datetime.datetime.strptime(mean_data[0], '%Y-%m-%d')
            if date_obj.year in range(first_year, second_year):
                month = date_obj.month
                self.months_means[month].append(mean_data[1])

        for month, mean_data in self.months_means.items():
            if mean_data:
                self.weather_data[month] = mean_data    
        figure, plot = plt.subplots()
        plot.boxplot(self.weather_data.values())
        plot.set_xticklabels(self.weather_data.keys())
        plot.set_xlabel('Month')
        plot.set_ylabel('Temperature (Celsius)')
        plot.set_title('Monthly Temperture Distribution: ' + str(first_year) + '-' + str(second_year))

        plt.show()

    def make_lineplot(self, data, year, month):
        """
        Generates line plot given year and month.
        """
        input_test = datetime.datetime(year, month, 1)
        input_convert = input_test.strftime('%Y-%m')
        for mean_data in data:
            date_obj = datetime.datetime.strptime(mean_data[0], '%Y-%m-%d')
            month_year = date_obj.strftime('%Y-%m')
            if month_year == input_convert:
                self.line_plot.append(mean_data[1])
        
        temps = np.array(self.line_plot)
        dates_size = np.arange(1, temps.size + 1)
        dates = []
        for i in dates_size:
            date_format = str(input_test.strftime('%B ')) + str(i) + ' ' + input_test.strftime('%Y')
            dates.append(date_format)
        line_plot = plt.subplot()
        line_plot.plot(dates, self.line_plot)
        line_plot.set_xticklabels(dates, rotation=70)
        
        line_plot.set_xlabel('Day of Month')
        line_plot.set_ylabel('Avg Daily Temp')
        date_month = input_test.strftime('%B ')
        date_year = input_test.strftime('%Y')
        line_plot.set_title('Daily Average Temperature for ' + date_month + 'of ' + date_year)
        
        plt.show()
        