import pandas as pd
import numpy as np
import time

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_inputs():
    global input_month
    global input_day
    
    month = ['january','february', 'march','april','may','june','all']
    day = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    """
    user enters a city, month, and day to analyze.
    This will output:
        city - name of the city to analyze
        month - name of the month to analyze, or select "all" to view data for all months
        day - name of the day of week to analyze, or select "all" to view data for all months
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ['chicago','new york city', 'washington']
    while True:
        input_city = input("Which city would you like to see data for: chicago, new york city, washington?").lower()
        if input_city not in city:
            print("You have selected an invalid city, try again!", end='')
            continue
        else:
            break
        
    while True:
        input_month = input("Select a month or enter all for all months: ").lower()
        if input_month not in month:
            print ("You have selected an invalid month, try again!", end='')
            continue
        else:
            break
    while True:
        input_day = input("Select a day of the week or enter all for all days: ").lower()
        if input_day not in day:
            print("You have selected an invalid day, try again!", end='')
            continue
        else:
            break
        
    print('-'*40)
    return input_city, input_month, input_day


def load_data(city, month, day):
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    #convert start and end time into datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    # extract month and day of week from Start Time
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df["Start hour"] = df["Start Time"].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
        print('You have selected the following filters: \nCity: {}\nMonth: {}\nDay: {}'.format(city, month, day))
    return df

def time_stats(df):

    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Popular month:', popular_month)
    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('The most common day of the week is:',popular_day)
    # display the most common start hour
    popular_hour = df['Start hour'].mode()[0]
    print('The most common start hour is:'.format(popular_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
      
    # display most commonly used start station
   
    popular_start_station = df.loc[:,"Start Station"].mode()[0]
    print('Most Popular start station is:', popular_start_station)
    # display most commonly used end station
    popular_end_station = df.loc[:,"End Station"].mode()[0]
    print('Most Popular end station is:', popular_end_station)
    # display most frequent combination of start station and end station trip
    start_end_station = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('Most frequent combination of start and end station trip:', start_end_station)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    df["Trip Duration"] = df["End Time"] - df["Start Time"]
    # display total travel time
    total_duration = df['Trip Duration'].sum()
    print('total travel time for your trip:', total_duration)
    # display mean travel time
    mean_duration = df['Trip Duration'].mean()
    print('Average travel time for your trip:', mean_duration)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    if "Gender" in df.columns:
        user_gender = df['Gender'].value_counts()
        print('Gender count:', user_gender)
    else:
        print("Gender column outside of range")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        min_user_dob= df['Birth Year'].min()
        print('Earliest date of birth:', min_user_dob)
    else:
        
        print("Date of birth column outside of range")
    
    if 'Birth Year' in df.columns:
        max_user_dob = df['Birth Year'].max()
        print('Latest birth year is:', max_user_dob)
    
    else:
        print("Date of birth column outside of range")
    
    if 'Birth Year' in df.columns:
        dob_count = df['Birth Year'].mode()[0]
        print('most common year of birth', dob_count)
    else:
        print("Date of birth column outside of range")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    input_data = input('\nWould you like to see the first 5 rows of the file? Enter either yes or no:').lower()
    if input_data in ('yes'):
        i = 0
        while True:
            print(df.iloc[i:i+5])
            i += 5
            add_data = input('Would you like to see the next 5 rows of data? Enter either yes or no: ').lower()
            if add_data not in ('yes'):
                break

def main():
    while True:
        city, month, day = get_inputs()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
if __name__ == "__main__":
	main()