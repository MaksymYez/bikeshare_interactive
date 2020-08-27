import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

### This function gets filters from user input


def get_filters():

    print('Hello! Let\'s explore some US bikeshare data!')

    city = []
    city_av = ['chicago', 'washington', 'new york city']
    month = []
    month_av = ['january', 'february', 'march', 'april', 'may', 'june','all']
    day = []
    day_av = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']

    while True:
        city = (input('\nEnter a name of city you would like to learn about\nChoose one of the following: Chicago, New York City, Washington: \n').lower())
        if city in city_av:
            break

        elif city not in city_av:
            print('\n', city.upper(),' is not available, Please enter one of the available cities\n')
            city = []
        continue


    while True:
        month = (input('\nChoose month you are interested in (January, February, March, April, May, June or ALL):\n').lower())
        if month in month_av:
            break
        elif month not in month_av:
            print('\nUnfortunately, we don\'t have data for this month. Please choose another month')
            month = []
        continue

    while True:
        day = (input('\nChoose day of the week you are interested in.\nPrint day name or for the overall stats print ALL:\n').lower())
        if day in day_av:
            break
        elif day not in day_av:
            print('\n Please type in name for the day of the week you are interested in\
            or type ALL to see an overall data')
            day = []
        continue


    print('-'*40)
    return city, month, day

#### This function pulls filtered data from CSV filles according to user input

def load_data(city, month, day):

    df = pd.read_csv(CITY_DATA[city])

    df ['Start Time'] = pd.to_datetime(df['Start Time'])
    df ['month'] = df ['Start Time'].dt.month
    df ['day_of_week'] = df ['Start Time'].dt.weekday

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    if day != 'all':
        days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        day = days.index(day)


        df= df[df['day_of_week'] == day]


    return df



#### This function offers users to see some raw data from the requested data set
def raw_data(df):
    start = 0
    end = 5
    answer = (input('\nWould you like to see some raw data before seeing the requesed stats? (Yes/No):\n').lower())
    while True:
        if answer != 'yes':
            break
        else:
            print(df[start:end])
            start += 5
            end += 5
            answer = (input('\nWould you like to see more raw data? (Yes/No):\n').lower())
        continue



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    most_common_month = df['month'].mode()[0]

    print('\nThe most common month to travel is: \n', most_common_month)


    most_common_day = df['day_of_week'].mode()[0]
    print('\nThe most common day of the week to travel is: \n', most_common_day)




    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()


    most_used_station = df['Start Station'].value_counts().head(1)
    print('\nThe most popular start station is: \n', most_used_station)



    most_end_station = df['End Station'].value_counts().head(1)
    print('\nThe most popular end station is: \n', most_end_station)

    most_common_combo = df.groupby(['Start Station','End Station']).size().sort_values(ascending=False).head(1)

    print('\nThe most frequent combination of start station and end station is: \n', most_common_combo)



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()


    total_travel_time = sum(df['Trip Duration'])
    print('\nTotal travel time is: \n', total_travel_time/60,' Minutes')



    mean_travel_time = (df['Trip Duration']).mean()

    print('\nMean travel time is: \n', mean_travel_time/60, ' Minutes')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):

    print('\nCalculating User Stats...\n')
    start_time = time.time()


    count_by_user_type = df['User Type'].value_counts()

    print(count_by_user_type)



    if 'Gender' not in df:
        print('\nNo gender data available for this city\n')
    else:
        gender_split = df['Gender'].value_counts()
        print(gender_split)


    if 'Birth Year' not in df:
        print('\nNo age data available for this city\n')

    else:
        df['Birth Year'].dropna(axis=0, inplace=True)

        oldest_person = df['Birth Year'].min()

        print('\nThe oldest person was born in: \n', oldest_person)

        youngest_person = df['Birth Year'].max()

        print('\nThe youngest person was born in: \n', youngest_person)


        most_common_year = df['Birth Year'].value_counts().head(1)

        print('\nThe most common birth year is: \n', most_common_year)



        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
