import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("\nWhich city would you like to select: Chicago, New York, or Washington?\n")
        city = city.lower()
        if city in ['chicago', 'new york', 'washington']:
            break
        else:
            print("Sorry, please try again.")

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("\nWhich month would you like to select: January, February, March, April, May, or June?"\
                           " or select \"all\" for no preference.\n")
        month = month.lower()
        if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            break
        else:
            print("Sorry, please try again.")
       

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nWhich day would you like to select: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?"\
                         " or select \"all\" for no preference.\n")
        day = day.lower()
        if day in ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']:
            break
        else:
            print("Sorry, please try again.")
       
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a DataFrame
    df = pd.read_csv(CITY_DATA[city])

    # convert Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    #filter by month
    if month != 'all':
      # index of months list to get int
      months = ['january', 'february', 'march', 'april', 'may', 'june']
      month = months.index(month) + 1

      # filter by month to create new DataFrame
      df = df[df['month'] == month]

    # filter by day of week
    if day != 'all':
      # filter by day of week to create new DataFrame
      df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print("\nMost common month: ", popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print("\nMost common day: ", popular_day)


    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("\nMost common hour: ", popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print("\nMost commonly used start station: ", start_station)


    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print("\nMost commonly used end station: ", end_station)


    # display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] + " " + df['End Station']
    combo_station = df['combination'].mode()[0]
    print("\nMost commonly used combination of start station and end station trip: ", combo_station)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("\nTotal travel time: ", total_travel_time)


    # display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    print("\nMean travel time: ", avg_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df.groupby(['User Type'])['User Type'].count()
    print(user_types)

    if city != 'washington':
        # Display counts of gender
        gen = df.groupby(['gender'])['gender'].count()
        print(gen)
        # Display earliest, most recent, and most common year of birth
        most_recent = sorted(df.groupby(['birth year'])['birth year'], reverse=True)[0][0]
        earliest = sorted(df.groupby(['birth year'])['birth year'])[0][0]
        most_common = df['birth year'].mode()[0]
        print("\nEarliest year of birth: ", earliest)
        print("\nMost recent year of birth: ", most_recent)
        print("\nMost common year of birth: ", most_common)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    # raw data option
    x = 1
    while True:
        raw = input("\nWould you like to look through the raw data? Yes or no.")
        if raw.lower() == "yes":
            print(df[x:x+5])
            x = x+5
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
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