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
        print('What city would you like to look up? Please select from chicago, new york city or washington')
        city = input().lower()
        if city == 'chicago' or city == 'new york city' or city == 'washington':
            break
        else:
            print('Please enter a valid city.')
            continue

    # get user input for month (all, january, february, ... , june)
    while True:
        print('What month would you like to look up? Please select from all, january, february, ... , june')
        month = input().lower()
        if month == 'all' or month == 'january' or month == 'february' or month == 'march' or month == 'april' or month == 'may' or month == 'june':
            break
        else:
            print('Please enter a valid month.')
            continue

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        print('What day of the week would you like to look up? Please select from all, monday, tuesday, ... sunday')
        day = input().lower()
        if day == 'all' or day == 'monday' or day == 'tuesday' or day == 'wednesday' or day == 'thursday' or day == 'friday' or day == 'saturday' or day == 'sunday' :
            break
        else:
            print('Please enter a valid city.')
            continue

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

     # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

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

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    most_c_month = df['month'].value_counts().idxmax()
    print('The most common month is ', months[most_c_month - 1])

    # display the most common day of week
    most_c_dayofweek = df['day_of_week'].value_counts().idxmax()
    print('\nThe most common day of week is ', most_c_dayofweek)

    # display the most common start hour
    most_c_start_hour = df['Start Time'].dt.hour.value_counts().idxmax()
    print('\nThe most common hour for Start Time is ', most_c_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    mc_start_station = df['Start Station'].value_counts().idxmax()
    print('The most commonly used start station is ', mc_start_station)

    # display most commonly used end station
    mc_end_station = df['End Station'].value_counts().idxmax()
    print('\nThe most commonly used end station is ', mc_end_station)

    # display most frequent combination of start station and end station trip
    mf_combination = df[['Start Station', 'End Station']].groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('\nThe most frequest combination is ')
    print(mf_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time is ', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\nThe mean travel time is ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_counts = df['User Type'].value_counts()
    print('The counts of user types are ')
    print(user_types_counts)

    # Display counts of gender
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print('\nThe counts of gender are ')
        print(gender_counts)
    else:
        print('\nThis data set does not contain gender information.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_birth_year = df['Birth Year'].min()
        print('\nThe earliest birth year is ', earliest_birth_year)

        most_recent_birth_year = df['Birth Year'].max()
        print('\nThe most recent birth year is ', most_recent_birth_year)

        most_common_birth_year = df['Birth Year'].mode()[0]
        print('\nThe most common birth year is ', most_common_birth_year)
    else:
        print('\nThis data set does not contain birth year information')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Display raw data 5 lines at a time."""

    current_index = 0
    print('\nDo you want to see the raw data? Enter yes or no.\n')
    display_input = input().lower()
    while True:
        if display_input == 'yes':
            print(df[current_index:current_index+5])
            current_index += 5
            print('\nDo you want to see more? Enter yes or no.')
            display_input_check = input().lower()
            if display_input_check == 'yes':
                continue
            else:
                break
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # Get time statistics for specified city
        time_stats(df)

        # Get station statistics for specfied city
        station_stats(df)

        # Get trip duration statistics for specfied city
        trip_duration_stats(df)

        # Get user statistics for specfied city
        user_stats(df)

        # Display data 
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
