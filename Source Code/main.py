import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv("/content/Zomato-data-.csv")

class Zomato:
    def __init__(self, df):
        """
        Initialize the Zomato class with the dataframe.
        """
        self.df = df

    def capitalize_text(self, columns):
        """
        Capitalize the text in the specified columns.
        Handles missing values by filling them with an empty string.
        """
        for col in columns:
            self.df[col] = self.df[col].fillna('').str.capitalize()

    def capitalize_header(self):
        """
        Capitalize the column headers to look clean and professional.
        """
        self.df.columns = self.df.columns.str.title()

    def remove_spaces(self):
        """
        Remove any leading or trailing spaces in column names.
        """
        self.df.columns = self.df.columns.str.strip()

    def remove_extra(self):
        """
        Replace any underscores in column names with spaces.
        """
        self.df.columns = self.df.columns.str.replace('_', ' ')

    def remove_duplicates(self):
        """
        Remove any duplicate rows in the dataframe.
        """
        self.df.drop_duplicates(inplace=True)

    def clean_rate_column(self):
        """
        Clean the 'Rate' column by removing the '/5' and converting it to float.
        Handle errors if any.
        """
        self.df['Rate'] = self.df['Rate'].str.split('/').str[0]
        self.df['Rate'] = pd.to_numeric(self.df['Rate'], errors='coerce')

    def clean_data(self):
        """
        Perform all data cleaning steps in one method.
        """
        self.capitalize_text(['name', 'online_order', 'book_table', 'listed_in(type)'])
        self.capitalize_header()
        self.remove_spaces()
        self.remove_extra()
        self.remove_duplicates()
        self.clean_rate_column()

# Instantiate the Zomato class and clean the data
cleaner = Zomato(df)
cleaner.clean_data()

# Extracting columns for analysis
Votes = df['Votes'].values
Approx_Cost = df['Approx Cost(For Two People)'].values

class Analyse:
    def __init__(self, df):
        """
        Initialize the Analyse class with the dataframe.
        """
        self.df = df

    def top_10_rest(self):
        """
        Plot the Top 10 Restaurants based on Votes.
        """
        Highest = self.df.sort_values(by='Votes', ascending=False).head(10)
        print(Highest[['Name','Votes']].to_string(index=False))

        # Plotting
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Name', y='Votes', data=Highest, palette='Set2')
        plt.xticks(rotation=45, ha='right')
        plt.xlabel('Restaurant Name')
        plt.ylabel('Votes')
        plt.title('Top 10 Restaurants by Votes')
        plt.tight_layout()
        plt.show()

    def avg_cost(self):
        """
        Plot the Average Cost distribution for two people.
        """
        avg = np.nanmean(Approx_Cost)
        print(f"Average Cost for Two People: {avg:.2f}")

        # Plotting
        sns.histplot(Approx_Cost, bins=20, kde=True, color='green')
        plt.axvline(avg, color='red', linestyle='--', label=f'Average Cost: {avg:.2f}')
        plt.xlabel('Approx Cost for Two People')
        plt.ylabel('Frequency')
        plt.title('Distribution of Approx Cost for Two People')
        plt.legend()
        plt.show()

    def plot_counts(self):
        """
        Plot the count of orders and booking types.
        """
        plt.figure(figsize=(12, 5))

        # Count of Listing Types
        plt.subplot(1, 2, 1)
        sns.countplot(x=self.df['Listed In(Type)'], palette='Purples')
        plt.xticks(rotation=45)
        plt.title('Count of Restaurant Types')

        # Count of Online Order Option
        plt.subplot(1, 2, 2)
        sns.countplot(x=self.df['Online Order'], palette='Purples_r')
        plt.title('Online Order Availability')

        plt.tight_layout()
        plt.show()

# Instantiate the Analyse class
analysis = Analyse(df)

# Call the methods to analyze the data
analysis.top_10_rest()
analysis.avg_cost()
analysis.plot_counts()
