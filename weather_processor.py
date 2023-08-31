from db_operations import DBOperations
from plot_operations import PlotOperations
from scrape_weather import WeatherHTMLParser

class WeatherProcessor():
    """
    The WeatherProcessor class represents the app the processes the weather data of the application.
    """
    def __init__(self):
        self.choices = {
            "1": self.download_data, 
            "2": self.generate_box_plot,
            "3": self.generate_line_plot, 
            "4": self.exit_menu, 
        }

        self.database = DBOperations('weather_data.sqlite')
        self.data = WeatherHTMLParser()

    def display_menu(self):
        """
        Displays the menu.
        """
        print("""
            Menu:
            1. Download data
            2. Generate box plot 
            3. Generate line plot
            4. Exit
        """)

    def run_menu(self):
        """
        Runs the menu.
        """
        while True:
            self.display_menu()
            choice = input("Enter an option: ")
            action = self.choices.get(choice)
            if action:
                action()
            else:
                print(f"{0} is not a valid choice".format(choice))
    
    def download_data(self):
        """
        Downloads weather data from today as far back as available.
        """
        self.database.save_data(self.data.scrape_from_today())

    def generate_box_plot(self):
        """
        Generates box plot given a year range.
        """
        plot = PlotOperations()

        first_year = input('Enter the first year in the format of YYYY (lower year): ')
        second_year = input('Enter the second year in the format of YYYY (higher year): ')

        plot.make_boxplot(self.database.fetch_data(), int(first_year), int(second_year))
        
    def generate_line_plot(self):
        """
        Generates line plot given a month and year. 
        """
        plot = PlotOperations()

        month = input('Enter in a month in the format of M: ')
        year = input('Enter in a year in the format of YYYY: ')

        plot.make_lineplot(self.database.fetch_data(), int(year), int(month))

    def exit_menu(self):
        """
        Exits the menu.
        """
        exit()

processor = WeatherProcessor()
processor.run_menu()

        