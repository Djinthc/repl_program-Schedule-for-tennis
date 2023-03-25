from datetime import datetime, timedelta  # Native lib. It is used to obtain current time, and managing time in reservations
import pandas as pd
import numpy as np
import json


class Schedule:

    now = datetime.now()            # Getting current date
    index = pd.date_range(start= now, periods= 36040, freq= '30min', normalize= True) # Creating list of dates every 30 minues for few years ahead
    reservations = pd.DataFrame(data= {'Name': [np.NaN for i in range(len(index))], # Creating dataframe as a storage for data with date as a index,
                                        'is_Reserved': [False for i in range(len(index))]},index = index)       # and columns Name and is reserved?
    
    def __init__(self):                     # Here we are creating (initializing) empty conteiners to be used by functions
        self.name = ''                      # name to be prompted by user
        self.now = datetime.now()           # Current date again (it will update every time class will be initialized)
        self.prefered_date = ''             # prefered date prompted by user
        self.reservedfor = ''               # For how long we are making reservation (timedelta in minutes)
        self.schedule = ''                  # a period between dates prompted by user cutted from Data Frame
        self.list_of_reservations = []      # list of reservations made from above schedule

    def menu():
        ''' It prints menu!'''

        print('''
        What would You like to do?\n
        \t 1. Make a reservation
        \t 2. Cancel a reservation
        \t 3. Print schedule
        \t 4. Save schedule to a file
        \t 5. Exit
        ''')



    def get_name(self):
        ''' Asking for name and checking if User has more than 2 reservations already this week'''
        
        print('\nWhat is your name?\n')
        name = str(input('Name: '))
        name = name.upper()

        if len(name) < 3:
            print('\nPlease give us your full name')
            Schedule.get_name(self)
            return
        else:
            self.name = name
            return name

    def check_number_reservations(self):
        ''' Checking a number of reservations in Data Frame and refusing to make another one if user got's 2 already'''


        number_of_reservations = len(self.reservations.where(self.reservations['Name'] == self.name).dropna())

        if number_of_reservations >= 2:
            print('\nWe are sorry, but maximum number of reservations at the moment are 2\n Consider canceling one of the previous reservations.')
            Schedule.menu()
            return True
        else:
            return False


    def update_current_time(self):
        '''Updatung current time'''

        self.now = datetime.now()
        return



    def get_prefered_date(self):
        '''Taking Date and time and validation'''

        self.prefered_date = ''
        prefered_date = str(input('Date: '))
        try:
            minutes = prefered_date[15:16]
            if int(minutes) not in (0,30):
                print('Wrong date! Try again!')
                Schedule.get_prefered_date(self) 
            prefered_date = datetime.strptime(prefered_date, '%Y-%m-%d %H:%M')
            self.prefered_date = prefered_date
            return prefered_date
        except:
               print('Wrong date! Try again!')
               Schedule.get_prefered_date(self)  
                
    def check_if_future_date(self):
        '''Checking if date prompted by user is a future date'''

        if self.prefered_date >= self.now and self.prefered_date <= self.now + timedelta(weeks=104):
            return
        elif self.prefered_date > self.now + timedelta(weeks=104):
            print('Sorry, but We can only make reservations 2 years in advance. Pick another date!')
            Schedule.get_prefered_date(self)
            return
        else:
            print('Let\'s leave past in the past. Pick a future date!')
            Schedule.get_prefered_date(self)
            return


    def check_if_in_hour(self):
        'Checking if prefered date is not within one hour. Return bool'

        now_plus_one = self.now + timedelta(hours= 1)
        if self.prefered_date < now_plus_one:
            return True
        else:
            return False

    def reserved_for(self):
        '''Asking user about time he wants to make a reservation for'''

        print('''For how long wish You make a reservation for?

                1. 30 min
                2. 60 min
                3. 90 min   
                Select number between 1-3 to make a choice''')
        choice = int(input('Choice: '))
        if choice == 1:
            self.reservedfor = timedelta(minutes= 30)
            print('\nYou choose 30min')
        elif choice == 2:
            self.reservedfor = timedelta(minutes= 60)
            print('\nYou choose 60min')
        elif choice == 3:
            self.reservedfor = timedelta(minutes= 90)
            print('\nYou choose 90min')
        else:
            print('Invalid choice! Try again!')
            Schedule.reserved_for(self)



    def check_if_booked(self):
        '''Checking if there is already a reservation in the time specified'''

        if len(self.reservations.loc[f'{self.prefered_date}':f'{self.prefered_date + self.reservedfor - timedelta(minutes = 30)}'].dropna()) > 0:
            return True
        else:
            return False


    def choice():
        '''input validation'''

        choice = input('yes/no?: ')
        if choice == 'yes':
            return 'yes'
        elif choice == 'no':
            return 'no'
        else:
            print('Type: yes or no!')
            Schedule.choice()


    def another_date(self):
        '''Checking for another possible date if one requested is already taken and asking user if it is suitable for him'''

        idx = 1
        Schedule.check_if_booked(self)
        while Schedule.check_if_booked(self) == True:
            self.prefered_date = self.reservations.loc[f'{self.prefered_date}':f'{self.prefered_date + timedelta(days=1)}'].query('is_Reserved == False').index[idx]
            idx += 1
            Schedule.check_if_booked(self)
        print(f'Would You like to book at {self.prefered_date} instead?')
        
        user_choice = Schedule.choice()
        if user_choice == 'yes':
            return True
        else:
            self.prefered_date = ''
            return False
    

    def make_reservation(self):
        '''User should be prompted to give his full name, and date of a reservation this should fail if:
                User has more than 2 reservations already this week
                Court is already reserved for the time user specified
                The date user gives is less than one hour from now
            If the court is reserved the system should suggest the user to make a reservation on the closest possible time.'''
        
        Schedule.get_name(self)
        if Schedule.check_number_reservations(self):
            return
        Schedule.update_current_time(self)
        print('\nWhen would You wish to schedule?\nPlease write a date in format YYYY-MM-DD HH:MM')
        Schedule.get_prefered_date(self)
        Schedule.check_if_future_date(self)
        if Schedule.check_if_in_hour(self) == True:
            print('Sorry we can\'t make that reservation. All reservations needs to be booked with at least 1 hour notice.')
            Schedule.menu()
            return    
        Schedule.reserved_for(self)
        if Schedule.check_if_booked(self) == True:
            print('Sorry we can\'t make that reservation. Court is already booked at this time.')
            choice = Schedule.another_date(self)
            if choice == False:
                print('Maybe some other time!')
                Schedule.menu()
                return

        self.reservations.loc[f'{self.prefered_date}', 'Name'] = self.name
        end_of_reservation = self.prefered_date + self.reservedfor - timedelta(minutes = 30)
        reservation_plus_30 = self.prefered_date + timedelta(minutes= 30)
        self.reservations.loc[f'{self.prefered_date}': f'{end_of_reservation}', 'is_Reserved'] = True
        if end_of_reservation > self.prefered_date:
            self.reservations.loc[f'{reservation_plus_30}': f'{end_of_reservation}', 'Name'] = '-'
        print(f'\nYour reservation at {self.prefered_date} for {self.reservedfor} is saved.\nSee You at court!')
        Schedule.menu()
        return
        

    def cancel_reservation(self):
        '''Function to cancel reservation it is checking if there is a reservation under prompted name on prompted date
            and if it is not in an hour if that is a case then removing that reservation from database'''


        name = Schedule.get_name(self)
        date = Schedule.get_prefered_date(self)
        in_hour = Schedule.check_if_in_hour(self)

        if self.reservations.loc[date,'Name'] != name:
            print(f'/Sorry, there is no reservation for {name} at {date}.')
            Schedule.menu()
            return
        elif in_hour:
            print(f'/Sorry, We could not cancel the reservation becouse it is in an hour from now.')
            Schedule.menu()
            return
        else:
            self.reservations.loc[date, 'Name'] = np.NaN
            self.reservations.loc[date, 'is_Reserved'] = False
            for dates in range(4):
                date = date + timedelta(minutes=30)
                if self.reservations.loc[date, 'Name'] == '-':
                    self.reservations.loc[date, 'Name'] = np.NaN
                    self.reservations.loc[date, 'is_Reserved'] = False
            print('\nReservation has been canceled!\n')
            Schedule.menu()
            return

        
    def get_schedule(self):
        '''Askinng user to prompt dates from when to when he wants to print shedule'''

        print('From when We should start printin the schedule? Please write a date in format YYYY-MM-DD HH:MM')
        date_to_check = Schedule.get_prefered_date(self)
        print('To when We should be printing the schedule? Please write a date in format YYYY-MM-DD HH:MM')
        date_to_check2 = Schedule.get_prefered_date(self)
        self.schedule = self.reservations.loc[date_to_check : date_to_check2].dropna()
        
        df_schedule = self.schedule['Name'].dropna()
        previous_name = ''
        previous_end_date = ''
        self.list_of_reservations = []

        for index, name in df_schedule.items():
            if name == '-':
                name = previous_name
            if name != previous_name:
                if previous_name != '':
                    self.list_of_reservations.append((previous_name, starting_date, previous_end_date))
                starting_date = index
                previous_name = name
                previous_end_date = index + timedelta(minutes=30)
            else:
                previous_end_date += timedelta(minutes=30)
        
        if previous_name != '':
            self.list_of_reservations.append((previous_name, starting_date, previous_end_date))
        return


    def print_schedule(self, if_print=True):
        '''Printing schedule'''

        Schedule.get_schedule(self)
        list_of_reservations = self.list_of_reservations
        if_print = if_print
        previous = (list_of_reservations[0][1]).date()
        to_print = {}
        to_save = {}
        one_date = []
        one_save = []
        for row in range(len(list_of_reservations)):
    
            starting_date = (list_of_reservations[row][1]).date()
            name = list_of_reservations[row][0]
            start_time = (list_of_reservations[row][1]).time()
            end_time = (list_of_reservations[row][2]).time()
    
            if starting_date == previous:
                one_date.append(f'\n*{name}   {start_time} : {end_time}')
                one_save.append({'name':name, 'start_time':str(start_time), 'end_time': str(end_time)})
            else:
                to_print.update({previous:one_date})
                to_save.update({str(previous):one_save})
                one_date = []
                one_save = []
                one_date.append(f'\n*{name}   {start_time} : {end_time}')
                one_save.append({'name':name, 'start_time':str(start_time), 'end_time': str(end_time)})
                previous = starting_date 
        to_print.update({previous:one_date})
        to_save.update({str(previous):one_save})

        if if_print == True:
            for date, entry in to_print.items():
                date_str = ''
                if date == self.now.date():
                    date_str = 'Today'
                elif date == (self.now + timedelta(days=1)).date():
                    date_str = 'Tomorrow'
                else: 
                    date_str = date.strftime("%A")
                reservations_str = ''.join(entry)
                print(f"\n{date_str} {date}: \n{reservations_str}")

        return to_save
    
    def pick_1_2():
        '''Input validation'''

        ext = input('Select number: ')
        if ext == '1':
            return 'csv'
        elif ext == '2':
            return 'json'
        else:
            print('This is not a valid option.\nTry again!')
            Schedule.pick_1_2()


    def save_schedule(self):
        '''Function to save schedule into a file. Possible formats CSV and JSON'''

        print('''\nWhat type of file would You like?
            \t1. CSV
            \t2. JSON''')
        ext = Schedule.pick_1_2()
        to_print = Schedule.print_schedule(self, False)
        file = str(input('Enter file name: ')) + f'.{ext}'
        with open(file, 'w') as doc:
            if ext == 'csv':
                to_print = pd.concat({k: pd.DataFrame(v) for k, v in to_print.items()}, axis=0)
                to_print.to_csv(doc, index_label='Date')
            else:
                json_file = json.dumps(to_print)
                doc.write(json_file)       
        Schedule.menu()
        return



    def if_1_5():
        '''Input validation'''
        
        try:
            command = int(input('Select: '))
            return command
        except ValueError:
            print('\nThis is not a valid number! Please choose a number between 1-5.\n')
            Schedule.if_1_5()


if __name__ == '__main__':

    Schedule.menu()
    command = Schedule.if_1_5()
    
    while command != 5:
        if command == 1:
            Schedule().make_reservation()
            command = Schedule.if_1_5()
            
        elif command == 2:
            Schedule().cancel_reservation()
            command = Schedule.if_1_5()

        elif command == 3:
            Schedule().print_schedule()
            Schedule.menu()
            command = Schedule.if_1_5()
            
        elif command == 4:
            Schedule().save_schedule()
            command = Schedule.if_1_5()

        else:
            print('\nWrong command! You should use numbers 1-5 to indicate Your\'s choice\n')
            command = Schedule.if_1_5()

    print('\nThank You for using our service!\n')

