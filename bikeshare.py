import time
import pandas as pd
import numpy as np
import click

# Dictionary to hold the paths to the city data files
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

# Tuple of months for filtering
months = ('january', 'february', 'march', 'april', 'may', 'june')

# Tuple of weekdays for filtering
weekdays = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday')


def get_user_choice(prompt, valid_choices):
    """Prompt the user for input until a valid choice is made.

    Args:
        prompt (str): The prompt to display to the user.
        valid_choices (iterable): A collection of valid choices.

    Returns:
        str or list: The user's choice or choices.
    """
    while True:
        user_input = input(prompt).lower().strip()
        if user_input == 'end':
            raise SystemExit
        elif ',' not in user_input:
            if user_input in valid_choices:
                return user_input
        else:
            choices = [i.strip().lower() for i in user_input.split(',')]
            if all(choice in valid_choices for choice in choices):
                return choices

        print("\nInvalid input. Please enter a valid option:\n>")


def get_filters():
    """Prompt user to specify cities, months, and weekdays for analysis.

    Returns:
        tuple: A tuple containing the selected city(ies), month(s), and weekday(s).
    """
    print("\n\nWelcome to the US bikeshare data explorer!\n")
    print("Type 'end' at any time to exit the program.\n")

    while True:
        city = get_user_choice("\nWhich city(ies) would you like to analyze? "
                               "Options: New York City, Chicago, Washington. "
                               "Use commas for multiple selections.\n>", CITY_DATA.keys())
        month = get_user_choice("\nWhich month(s) would you like to filter by? "
                                "Options: January to June. Use commas for multiple selections.\n>", months)
        day = get_user_choice("\nWhich weekday(s) would you like to filter by? "
                              "Options: Sunday to Saturday. Use commas for multiple selections.\n>", weekdays)

        confirmation = get_user_choice("\nYou have selected the following filters:\n"
                                        "City(ies): {}\nMonth(s): {}\nWeekday(s): {}\n"
                                        "Confirm? [y] Yes [n] No\n\n>".format(city, month, day), ['y', 'n'])
        if confirmation == 'y':
            break
        else:
            print("\nLet's try that again!")

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """Load data based on user-selected filters for cities, months, and weekdays.

    Args:
        city (str or list): The selected city(ies).
        month (str or list): The selected month(s).
        day (str or list): The selected weekday(s).

    Returns:
        DataFrame: A pandas DataFrame containing the filtered data.
    """
    print("\nLoading data based on your selections...")
    start_time = time.time()

    if isinstance(city, list):
        df = pd.concat([pd.read_csv(CITY_DATA[c]) for c in city], sort=True)
    else:
        df = pd.read_csv(CITY_DATA[city])

    # Create new columns for analysis
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.day_name()
    df['Start Hour'] = df['Start Time'].dt.hour

    # Filter by month
    if isinstance(month, list):
        df = pd.concat([df[df['Month'] == (months.index(m) + 1)] for m in month])
    else:
        df = df[df['Month'] == (months.index(month) + 1)]

    # Filter by weekday
    if isinstance(day, list):
        df = pd.concat([df[df['Weekday'] == d.title()] for d in day])
    else:
        df = df[df['Weekday'] == day.title()]

    print("\nData loaded in {} seconds.".format(time.time() - start_time))
    print('-' * 40)

    return df


def display_time_stats(df):
    """Calculate and display statistics on travel times.

    Args:
        df (DataFrame): The DataFrame containing the filtered data.
    """
    print('\nCalculating travel time statistics...\n')
    start_time = time.time()

    most_common_month = df['Month'].mode()[0]
    print('Most common month for travel: ' + months[most_common_month - 1].title() + '.')

    most_common_day = df['Weekday'].mode()[0]
    print('Most common day of the week: ' + most_common_day + '.')

    most_common_hour = df['Start Hour'].mode()[0]
    print('Most common start hour: ' + str(most_common_hour) + '.')

    print("\nThis took {} seconds.".format(time.time() - start_time))
    print('-' * 40)


def display_station_stats(df):
    """Calculate and display statistics on popular stations and trips.

    Args:
        df (DataFrame): The DataFrame containing the filtered data.
    """
    print('\nCalculating popular stations and trips...\n')
    start_time = time.time()

    most_common_start_station = df['Start Station'].mode()[0]
    print("Most common start station: " + most_common_start_station)

    most_common_end_station = df['End Station'].mode()[0]
    print("Most common end station: " + most_common_end_station)

    df['Start-End Combination'] = df['Start Station'] + ' - ' + df['End Station']
    most_common_combination = df['Start-End Combination'].mode()[0]
    print("Most common start-end station combination: " + most_common_combination)

    print("\nThis took {} seconds.".format(time.time() - start_time))
    print('-' * 40)


def display_trip_duration_stats(df):
    """Calculate and display statistics on trip durations.

    Args:
        df (DataFrame): The DataFrame containing the filtered data.
    """
    print('\nCalculating trip duration statistics...\n')
    start_time = time.time()

    total_duration = df['Trip Duration'].sum()
    total_duration_str = f"{total_duration // 86400}d {total_duration % 86400 // 3600}h {total_duration % 3600 // 60}m {total_duration % 60}s"
    print('Total travel time: ' + total_duration_str + '.')

    mean_duration = df['Trip Duration'].mean()
    mean_duration_str = f"{mean_duration // 60}m {mean_duration % 60}s"
    print("Average travel time: " + mean_duration_str + ".")

    print("\nThis took {} seconds.".format(time.time() - start_time))
    print('-' * 40)


def display_user_stats(df, city):
    """Calculate and display statistics on bikeshare users.

    Args:
        df (DataFrame): The DataFrame containing the filtered data.
        city (str): The selected city for which to display user stats.
    """
    print('\nCalculating user statistics...\n')
    start_time = time.time()

    user_types = df['UserType'].value_counts().to_string()
    print("User  type distribution:\n" + user_types)

    try:
        gender_distribution = df['Gender'].value_counts().to_string()
        print("\nGender distribution:\n" + gender_distribution)
    except KeyError:
        print("No gender data available for {}.".format(city.title()))

    try:
        oldest_birth_year = int(df['Birth Year'].min())
        youngest_birth_year = int(df['Birth Year'].max())
        common_birth_year = int(df['Birth Year'].mode()[0])
        print("\nOldest rider was born in: " + str(oldest_birth_year))
        print("Youngest rider was born in: " + str(youngest_birth_year))
        print("Most common birth year: " + str(common_birth_year))
    except KeyError:
        print("No birth year data available for {}.".format(city.title()))

    print("\nThis took {} seconds.".format(time.time() - start_time))
    print('-' * 40)


def display_raw_data(df, start_index):
    """Display raw data in increments of 5 rows.

    Args:
        df (DataFrame): The DataFrame containing the filtered data.
        start_index (int): The index from which to start displaying raw data.

    Returns:
        int: The updated index for the next display of raw data.
    """
    print("\nYou chose to view raw data.")

    if start_index > 0:
        continue_last = get_user_choice("\nContinue from where you left off? [y] Yes [n] No\n>", ['y', 'n'])
        if continue_last == 'n':
            start_index = 0

    while True:
        print(df.iloc[start_index:start_index + 5].to_string())
        start_index += 5

        if start_index >= len(df):
            print("\nNo more data to display.")
            break

        if get_user_choice("Do you want to see more raw data? [y] Yes [n] No\n>", ['y', 'n']) == 'n':
            break

    return start_index


def main():
    """Main function to run the bikeshare data analysis."""
    while True:
        click.clear()
        city, month, day = get_filters()
        df = load_data(city, month, day)

        start_index = 0
        while True:
            selection = get_user_choice("\nSelect the information you want:\n"
                                         "[ts] Time Stats\n[ss] Station Stats\n"
                                         "[tds] Trip Duration Stats\n[us] User Stats\n"
                                         "[rd] Display Raw Data\n[r] Restart\n\n>",
                                         ['ts', 'ss', 'tds', 'us', 'rd', 'r'])
            click.clear()
            if selection == 'ts':
                display_time_stats(df)
            elif selection == 'ss':
                display_station_stats(df)
            elif selection == 'tds':
                display_trip_duration_stats(df)
            elif selection == 'us':
                display_user_stats(df, city)
            elif selection == 'rd':
                start_index = display_raw_data(df, start_index)
            elif selection == 'r':
                break

        if get_user_choice("\nWould you like to restart? [y] Yes [n] No\n>", ['y', 'n']) != 'y':
            break


if __name__ == "__main__":
    main()

