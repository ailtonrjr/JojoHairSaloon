from os import path
from appointment import Appointment

DAYS_OF_WEEK = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')
FIRST_HOUR_OF_DAY = 9
LAST_HOUR_OF_DAY = 16


class AppointmentManager:

    def __init__(self):
        self.appointments = []

    def create_weekly_calendar(self, appt_calendar):
        appt_calendar.clear()

        for day in range(len(DAYS_OF_WEEK)):
            # Add a calendar appointment entry for every hour of the day that the salon is open
            for hour in range(FIRST_HOUR_OF_DAY, LAST_HOUR_OF_DAY+1):
                new_appt = Appointment(day, hour)
                appt_calendar.append(new_appt)
        
        
    def load_scheduled_appointments(self):
        scheduleCounter = 0
        correctFile = True

        while correctFile:
            filename = input("enter appointment filename: ")
            if path.isfile(filename):
                with open(filename, 'r') as file:
                    for line in file:
                        values = line.strip().split(',')
                        day_of_week, start_time_hour = values[3], int(values[4])
                        appointment = self.find_appointment_by_time(day_of_week, start_time_hour)
                        if appointment:
                            appointment.schedule(values[0], values[1], int(values[2]))
                        scheduleCounter +=1
                        correctFile = False
            else:
                print (f'File not found. Re-',end= "")
        print (f'{scheduleCounter} previously scheduled appointments have been loaded')

    def print_menu(self):
        print("\nJojo's Hair Salon Appointment Manager")
        print("=" * 37)
        print("1) Schedule an appointment")
        print("2) Find appointment by name")
        print("3) Print calendar for a specific day")
        print("4) Cancel an appointment")
        print("9) Exit the system")
        return input("Enter your selection: ")

    def find_appointment_by_time(self, day_of_week, start_time_hour):
        for appointment in self.appointments:
            values = appointment.strip().split(',')
            appt_day_of_week, appt_start_time_hour = values[3], int(values[4])
            if appt_day_of_week == day_of_week and appt_start_time_hour == start_time_hour:
                return appointment
            
        return None

    def show_appointments_by_name(self):
        name = input("Enter client name: ")
        print(f'\nAppointments for {name}')
        print("\nClient Name         Phone          Day       Start     End       Type")
        print("-" * 87)
        #Starting piece of code written by ChatGPT
        matching_appointments = [appointment for appointment in self.appointments if name.lower() in appointment.get_client_name().lower()]
        #Ending piece of code written by ChatGPT
        for appointment in matching_appointments:
            print(appointment)

    def show_appointments_by_day(self):
        day_of_week = input("Enter day of week: ").capitalize()
        print(f'\nAppointments for {day_of_week}')
        print("\nClient Name         Phone          Day       Start     End       Type")
        print("-" * 87)
        #Starting piece of code written by ChatGPT
        matching_appointments = [appointment for appointment in self.appointments if appointment.get_day_of_week() == day_of_week]
        #Ending piece of code written by ChatGPT
        for appointment in matching_appointments:
            print(appointment)

    '''def save_scheduled_appointments(self):
        with open(filename, 'w') as file:
                for appointment in self.appointments:
                    if appointment.get_appt_type() != 0:
                        file.write(appointment.format_record() + '\n')
                print(f"{len(self.appointments)} scheduled appointments have been successfully saved.")
        else:
            print("File not found.")'''

    def main(self):
        print("Starting the Appointment Manager System")
        appt_calendar = []
        self.create_weekly_calendar(appt_calendar)
        print ("Weekly calendar created")
        ask_load = input("Would you like to load previously scheduled appointments from a file (Y/N)? ")
        if ask_load.lower() == "y":
            self.load_scheduled_appointments()

        while True:
            choice = self.print_menu()

            if choice == '1':
                print ("** Schedule an appointment **")
                day_of_week = input("Enter day of week: ").capitalize()
                start_time_hour = int(input("Enter start time hour (24 hour clock): "))
                appointment = self.find_appointment_by_time(day_of_week, start_time_hour)
                if appointment:
                    client_name = input("Enter client name: ")
                    client_phone = input("Enter client phone: ")
                    appt_type = int(input("Enter appointment type (0-4): "))
                    appointment.schedule(client_name, client_phone, appt_type)
                    print(f"OK, {client_name}'s appointment is scheduled!")
                else:
                    print("Sorry that time slot is booked already!")

            elif choice == '2':
                print ("** Find appointment by name **")
                self.show_appointments_by_name()

            elif choice == '3':
                print ("** Print calendar for a specific day **")
                self.show_appointments_by_day()

            elif choice == '4':
                print ("** Cancel an appointment **")
                day_of_week = input("Enter day of week: ").capitalize()
                start_time_hour = int(input("Enter start hour (24 hour clock): "))
                appointment = self.find_appointment_by_time(day_of_week, start_time_hour)
                if appointment:
                    print(f'{day_of_week} {start_time_hour} for {client_name} has been cancelled')
                    appointment.cancel()
                    
                else:
                    print("Appointment not found.")

            elif choice == '9':
                print("\n** Exit the system **")
                scheduleCounter = 0
                saveFile = input ("Would you like to save all scheduled appointments to a file (Y/N): ")
                if saveFile.lower() == "y":
                    filename = input("Enter appointment filename: ")
                    if path.isfile(filename):
                            overwrite = input("File already exists. Do you want to overwrite it (Y/N): ")
                            if overwrite.lower() == "y":
                                with open(filename, 'w') as file:
                                    for appointment in self.appointments:
                                        if appointment.get_appt_type() != 0:
                                            file.write(appointment.format_record() + '\n')
                                            scheduleCounter += 1
                            else:
                                filename = input("Enter appointment filename: ")
                print(f"{scheduleCounter} scheduled appointments have been successfully saved.")
                print("Goodbye!")
                break

            else:
                print("Invalid choice. Please enter a valid option (1-4, 9).")


if __name__ == "__main__":
    appointment_manager = AppointmentManager()
    appointment_manager.main()
    