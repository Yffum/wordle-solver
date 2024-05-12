from typing import List
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

class ReportDataCollector:
    def __init__(self):
        self.RunTimeData = []

    def recordData(self, record):
        [ answer, guess_count, successful, avg_guess_time, game_duration ] = record

        self.RunTimeData.append(
            {
                'Answer': answer,
                'Guess Count': guess_count,
                'Success' :  successful,
                'Avg Guess Time (ms)': 1000 * avg_guess_time,
                'Game Duration (ms)' : 1000 * game_duration
            }
        )

    def generateReport(self, agent_type: str, duration: float, test_mode:str):
        self.report_df = pd.DataFrame.from_records(self.RunTimeData)
        self.agent_type = agent_type
        self.duration = duration
        self.test_mode = test_mode

        self.current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Write to file
        self.generateReportSummaryFile(agent_type, duration, test_mode)

        # Write to file
        self.generateReportFullFile(agent_type, duration, test_mode)
        
        # Generate plot
        self.generateReportPlot()


    def generateReportSummaryFile(self, agent_type: str, duration: float, test_mode:str):

        # Count successes 
        success_count = self.report_df['Success'].value_counts().get(True, 0)
    
        # Precision
        p = 2 # num of digits after decimal

        # Calculate stats
        win_percentage = round(100 * success_count/len(self.report_df), p)
        avg_guess_count = round(self.report_df['Guess Count'].mean(), p)
        total_avg_guess_time = round(self.report_df['Avg Guess Time (ms)'].mean(), p)
        avg_game_duration = round(self.report_df['Game Duration (ms)'].mean(), p)
    
        # Round stats
        self.report_df = self.report_df.round(p)

        filename = f"test_results/wordle_test_{self.current_datetime}.txt"
    
        with open(filename, 'w') as f:
            f.write("")

        # Write overall statistics
        with open(filename, 'w') as f:
            f.write("Date: {}\n".format(datetime.now().strftime("%Y-%m-%d")))
            f.write("Search Mode: {}\n".format(agent_type))
            f.write("Dataset mode: {}\n".format(test_mode))
            f.write("Test Size: {}\n".format(len(self.report_df)))
            f.write("Test Duration (min): {}\n".format(duration))
            f.write("Win Percentage (%): {}\n".format(win_percentage))
            f.write("Avg Guess Count: {}\n".format(avg_guess_count))
            f.write("Total Avg Guess Time (ms): {}\n".format(total_avg_guess_time))
            f.write("Avg Game Duration (ms): {}\n".format(avg_game_duration))

        # Sort by easiest games (fewest guesses)
        self.report_df.sort_values(by='Guess Count', ascending=True, inplace=True)
        # Write to file
        with open(filename, 'a') as f:
            f.write("\n")
            f.write("Top 10 Easiest Games (fewest guesses):\n")
        self.report_df.head(10).to_csv(filename, mode='a', index=False)

        # Sort by hardest games (most guesses)
        self.report_df.sort_values(by='Guess Count', ascending=False, inplace=True)
        # Write to file
        with open(filename, 'a') as f:
            f.write("\n")
            f.write("Top 10 Hardest Games (most guesses):\n")
        self.report_df.head(10).to_csv(filename, mode='a', index=False)

    def generateReportFullFile(self, agent_type: str, duration: float, test_mode:str):

        # Count successes 
        success_count = self.report_df['Success'].value_counts().get(True, 0)
    
        # Precision
        p = 2 # num of digits after decimal

        # Calculate stats
        win_percentage = round(100 * success_count/len(self.report_df), p)
        avg_guess_count = round(self.report_df['Guess Count'].mean(), p)
        total_avg_guess_time = round(self.report_df['Avg Guess Time (ms)'].mean(), p)
        avg_game_duration = round(self.report_df['Game Duration (ms)'].mean(), p)
    
        # Round stats
        self.report_df = self.report_df.round(p)

        filename = f"test_results/wordle_test_full_{self.current_datetime}.txt"
    
        with open(filename, 'w') as f:
            f.write("")

        # Write overall statistics
        with open(filename, 'w') as f:
            f.write("Date: {}\n".format(datetime.now().strftime("%Y-%m-%d")))
            f.write("Search Mode: {}\n".format(agent_type))
            f.write("Dataset mode: {}\n".format(test_mode))
            f.write("Test Size: {}\n".format(len(self.report_df)))
            f.write("Test Duration (min): {}\n".format(duration))
            f.write("Win Percentage (%): {}\n".format(win_percentage))
            f.write("Avg Guess Count: {}\n".format(avg_guess_count))
            f.write("Total Avg Guess Time (ms): {}\n".format(total_avg_guess_time))
            f.write("Avg Game Duration (ms): {}\n".format(avg_game_duration))

        # Sort by easiest games (fewest guesses)
        self.report_df.sort_values(by='Guess Count', ascending=True, inplace=True)
        # Write to file
        with open(filename, 'a') as f:
            f.write("\n")
            f.write("Top 10 Easiest Games (fewest guesses):\n")
        self.report_df.to_csv(filename, mode='a', index=False)

    def sortWordsByDifficulty(self):
        filename = f"Data/valid_solutions_ordered.csv"
    
        with open(filename, 'w') as f:
            f.write("")

        # Sort by easiest games (fewest guesses)
        self.report_df.sort_values(by='Guess Count', ascending=True, inplace=True)

        # Write words to file
        self.report_df['Answer'].to_csv(filename, mode='a', index=False, header=False)

    def generateReportPlot(self):
        """ generate plot with guess count. """
        # Convert data to DataFrame
        counts = self.report_df['Guess Count'].value_counts().to_dict()

        filename = f"test_results/wordle_test_plot_{self.current_datetime}.png"
        
        x_axis = list(counts.keys())
        y_axis = list(counts.values())

        # configuration for the bar plot 
        plt.bar(x_axis, y_axis, edgecolor='black')
        plt.xticks(x_axis)
        plt.title('Distribution of Game Results [' + self.agent_type + '/' + self.test_mode + '/' + str(len(self.report_df)) + ']')
        plt.xlabel('Number of Guesses')
        plt.ylabel('Number of Games')

        # save the plot
        plt.savefig(filename)

        #show the plot
        #plt.show()    
