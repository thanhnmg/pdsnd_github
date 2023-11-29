import time
import pandas as pd
import numpy as np

cities = {'cg': 'chicago.csv', 'chicago': 'chicago.csv',
          'ny': 'new_york_city.csv', 'new york city': 'new_york_city.csv',
          'wa': 'washington.csv', 'washington': 'washington.csv'}

months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']

days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']


def display_data(df):
    """Display raw data upon request by user

    Args:
        df (DataFrame): DataFrame of csv file
    """

    max_line = 5
    current_line = 0

    str_confirm = input("Would you like to see the data?  Enter yes or no.\n ")
    if 'yes' != str_confirm.lower() and 'y' != str_confirm.lower():
        return

    while current_line < len(df):
        for index, row in df[current_line:current_line + max_line].iterrows():
            print(row.to_string(index=True, dtype=False))
            

        current_line += max_line
        # Check for user input
        user_confirm = input("Would you like to see next data?  Enter yes or no.\n")
        if "yes" != user_confirm.lower() and "y" != user_confirm.lower():
            return





def data_input(msg, resource_data, is_check):
    """
    Asks user input data
    Params:
        (str) msg - The message display
        (array) resourceData - data compare
    Returns:
        (str) data from user input
    """

    str_confirm = ''
    while str_confirm not in resource_data:
        # get data from user input
        str_confirm = input("%s, input 'q' to exit: " % msg).lower().strip()

        #  exit the program when user input "q"
        if str_confirm == 'q':
            exit()

        # if data input is month or day then check input all
        if is_check and str_confirm == 'all':
            return str_confirm

        # if data input not in resourceData
        if str_confirm not in resource_data:
            print("Invalid input. Please try again!")

    return str_confirm


def get_filters():
    """
    load data from user input

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for city (chicago, new york city, washington)
    str_city = data_input("Enter a city (Chicago, New York City, Washington) or short name (CG, NY, WA)", cities, False)

    # Get user input for month (all, january, february, ... , june)
    str_month = data_input("Enter a month (all, jan, feb, ..., jun)", months, True)

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    str_day = data_input("Enter a day (all, mon, tue, ..., sun)", days, True)

    

    return str_city, str_month, str_day


def load_data(str_city, str_month, str_day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv('./' + cities[str_city])
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    if str_month != "all":
        print("Filter data by month {}...\n".format(str_month.capitalize()))
        df = df[df["Start Time"].dt.month == months.index(str_month) + 1]

    if str_day != "all":
        print("Filter data by day of week {}...\n".format(str_day.capitalize()))
        df = df[df["Start Time"].dt.dayofweek == days.index(str_day)]

    return pd.DataFrame(df)


def time_stats(df, str_month, str_day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if str_month == "all":
        month_counts = df["Start Time"].dt.month.value_counts()
        if len(month_counts) > 0:
            month_focus = month_counts.idxmax()
            print("The most common month: ", months[month_focus - 1].capitalize())
        else:
            print("The most common month: empty")

    # display the most common day of week
    if str_day == "all":
        counts_by_day = df["Start Time"].dt.dayofweek.value_counts()
        if len(counts_by_day) > 0:
            day_focus = counts_by_day.idxmax()
            print("The most common day of week:", days[day_focus].capitalize())
        else:
            print("The most common day of week: empty")

    # display the most common start hour
    start_hour_counts = df["Start Time"].dt.hour.value_counts()
    hour_focus = 0
    if len(start_hour_counts) > 0:
        hour_focus = start_hour_counts.idxmax()
    print("The most common hour:", hour_focus)

    print("\nThis took %s seconds." % (time.time() - start_time))
    


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    station_stats_focus = df['Start Station'].mode()
    if len(station_stats_focus) > 0:
        print('Most commonly used start station:', station_stats_focus[0])
    else:
        print('Most commonly used start station: empty')
    # display most commonly used end station
    station_ends_focus = df['End Station'].mode()
    if len(station_ends_focus) > 0:
        print('Most commonly used end station:', station_ends_focus[0])
    else:
        print('Most commonly used end station: empty')
    # display most frequent combination of start station and end station trip
    station_combination = (df['Start Station'] + ", " + df['End Station'])
    combination_focus = station_combination.mode()
    if len(combination_focus) > 0:
        print('Most frequent combination of start station and end station trip:', combination_focus[0])
    else:
        print('Most frequent combination of start station and end station trip: empty')
    print("\nThis took %s seconds." % (time.time() - start_time))
    


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print("Total travel time(seconds): ", total_travel)

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print("Mean travel time(seconds): ", mean_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_count = df["User Type"].value_counts()
    print("User types count:\n", user_types_count.to_string(index=True, dtype=False))
    

    # Display counts of gender
    try:
        genders_count = df['Gender'].value_counts()
        print("Genders count:\n", genders_count.to_string(index=True, dtype=False))
    except Exception:
        print("Genders count: empty")
    

    # Display earliest, most recent, and most common year of birth
    earliest = most_recent = most_common = ""
    try:
        birth_year = df['Birth Year']
        earliest = birth_year.min()
        most_recent = birth_year.max()
        most_common = birth_year.mode()[0]
    except Exception:
        earliest = most_recent = most_common = "empty"
    finally:
        print("Earliest year of birth: ", earliest)
        print("Most recent year of birth: ", most_recent)
        print("Most common year of birth: ", most_common)

    print("\nThis took %s seconds." % (time.time() - start_time))
    


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes' and restart.lower() != 'y':
            break


if __name__ == "__main__":
    main()
