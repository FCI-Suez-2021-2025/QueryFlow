import pandas as pd
import random
import datetime

class Utility:
    @staticmethod
    def create_random_csv(csv_file_path, num_rows):
        """A function that create a csv file with random data (Name, Date_of_birth, Role, Phone_number, City)."""

        df = pd.DataFrame()

        # Generate random names column
        first_names = (
            'Mostafa', 'Mahmoud', 'Ibrahim', 'Hager', 'Abir', 'Ahmed', 'Ali', 'Fady', 'Menna', 'Kawther',
            'Abdo', 'Khaled', 'Mohammed', 'Mona', 'Manar', 'Fatma', 'Mark', 'Abdallah', 'Nour'
        )
        last_names = (
            'Mosa','Amin','Abbas', 'Ahmed', 'Saad', 'Mansour', 'Mahrous', 'Saeed', 'Shahin', 'Shazly', 
            'Nabil', 'Ibrahim', 'Walid', 'Mohamed', 'Gaber', 'Adel', 'Youssef', 'Emad', 'Ramadan', 'Mohsen'
        )
        df['name'] = list(random.choice(first_names) + " " + random.choice(last_names) for _ in range(num_rows))

        # Generate random date of birth column
        random_dates = []
        start_date = datetime.date(1999, 1, 1)
        end_date = datetime.date(2000, 12, 30)

        for _ in range(num_rows):
            random_number_of_days = random.randrange((end_date - start_date).days)
            random_date = start_date + datetime.timedelta(days=random_number_of_days)

            random_dates.append(random_date)

        df['date_of_birth'] = random_dates

        # Generate random role column with more Students
        roles = ('Student', 'Professor', 'Clerk')
        df['role'] = random.choices(roles, weights=[8, 1, 2], k=num_rows)
        
        # Geneare random phone numbers column
        phone_number_beginnings = ('010', '012', '011', '015')
        df['phone_number'] = [
            (random.choice(phone_number_beginnings) 
            + str(random.randint(pow(10, 7), pow(10, 8)))) 
            for _ in range (num_rows)
        ]

        # Generate random city column with more Suez
        cities = ('Suez', 'Ismailia', 'Cairo', 'Sadr', 'Alex', 'Giza')
        df['city'] = random.choices(cities, weights=[10, 2, 2, 1, 1, 1], k=num_rows)
        
        # Save the data into a zipped csv file
        df.to_csv(csv_file_path + ".csv", index_label='id')
    