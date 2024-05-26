# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes with structured error handling
# Change Log: Michael Okimura, 05/26/2024, Created Script
# ------------------------------------------------------------------------------------------ #
import json

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME: str = "enrollments.json"

# Define the Data Variables
students: list = []  # a table of student data
menu_choice: str  # Hold the choice made by the user.
student_first_name: str
student_last_name: str
course_name: str

# Person class ------------------------------------- #
class Person:
    
    # Adding first_name and last_name to the constructor
    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name

    # Creating getting for first_name
    @property
    def first_name(self):
        return self.__first_name.title()

    # Creating setter for first_name    
    @first_name.setter
    def first_name(self, value: str):
        if value.isalpha() or value == "":
            self.__first_name = value
        else:
            raise ValueError("The first name should not contain numbers.")

    # Creating getting for last_name    
    @property
    def last_name(self):
        return self.__last_name.title()

    # Creating setter for last_name    
    @last_name.setter
    def last_name(self, value: str):
        if value.isalpha() or value == "":
            self.__last_name = value
        else:
            raise ValueError("The last name should not contain numbers.")

    # Override __str__() method to return Person data        
    def __str__(self):
        return f"{self.first_name},{self.last_name}"

# Student class inheriting Person class ---------------------------- #
class Student(Person):

    # Call to Person constructor to pass first_name and last_name data
    # Adding assignment to course_name property          
    def __init__(self, first_name: str, last_name: str, course_name: str):
        super().__init__(first_name=first_name, last_name=last_name, course_name=course_name)
        self.course_name = course_name

    # Creating setter for course_name    
    @property
    def course_name(self):
        return self.__course_name
    
    # Creating getter for course_name. Used replace method to remove "space" from triggering error in "isalnum" method
    @course_name.setter
    def course_name(self, value: str):
        if value.replace(" ","").isalnum() or value == "":
            self.__course_name = value
        else:
            raise ValueError("The course name should not contain special characters.")

    # Override __str__() method to return Student data
    def __str__(self):
        return f"{self.first_name},{self.last_name},{self.course_name}"

# Processing --------------------------------------- #
class FileProcessor:

    # Reading data from exiting json file and saving to a list
    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        try:
            file = open(file_name, "r")
            student_data = json.load(file)
            file.close()
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with reading the file.", error=e)
        finally:
            if file.closed == False:
                file.close()
        return student_data

    # Writes data to existing json file adding on to any existing data
    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        try:
            file = open(file_name, "w")
            json.dump(student_data, file)
            file.close()
            IO.output_student_and_course_names(student_data=student_data)
        except Exception as e:
            message = "Error: There was a problem with writing to the file.\n"
            message += "Please check that the file is not open by another program."
            IO.output_error_messages(message=message,error=e)
        finally:
            if file.closed == False:
                file.close()

# Presentation --------------------------------------- #
class IO:

    # Displays custom error message to the user
    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    # Displays the menu to the user
    @staticmethod
    def output_menu(menu: str):
        print()
        print(menu)
        print()

    # Gets the menu choice from the user
    @staticmethod
    def input_menu_choice():
        choice = "0"
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1","2","3","4"):
                raise Exception("Please choose option 1, 2, 3, or 4.")
        except Exception as e:
            IO.output_error_messages(e.__str__())  # Not passing e to avoid the technical message
        return choice

    # Displays current data to the user
    @staticmethod
    def output_student_and_course_names(student_data: list):
        print("-" * 50)
        for student in student_data:
            print(f'Student {student["FirstName"]} {student["LastName"]} is enrolled in {student["CourseName"]}')
        print("-" * 50)

    # Gets student first, student last, and course name from user.
    @staticmethod
    def input_student_data(student_data: list):
        try:
            student_first_name = input("Enter the student's first name: ")
            if not student_first_name.isalpha():
                raise ValueError("The first name should not contain numbers.")
            student_last_name = input("Enter the student's last name: ")
            if not student_last_name.isalpha():
                raise ValueError("The last name should not contain numbers.")
            course_name = input("Please enter the name of the course: ")
            if not course_name:
                raise ValueError("The course name should not be left blank.")
            student = {"FirstName": student_first_name, "LastName": student_last_name, "CourseName": course_name}
            student_data.append(student)
            print()
            print(f"You have registered {student_first_name} {student_last_name} for {course_name}.")
        except ValueError as e:
            IO.output_error_messages(message="One of the values was the incorrect type of data!", error=e)
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with your entered data.", error=e)
        return student_data

# Start of main body

# When the program starts, read the file data into a list of lists (table)
# Extract the data from the file
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

# Present and Process the data
if __name__ == "__main__":
    while (True):

        # Present the menu of choices
        IO.output_menu(menu=MENU)

        menu_choice = IO.input_menu_choice()
        match menu_choice:

            # Input user data
            case "1":
                students = IO.input_student_data(student_data=students)
                continue

            # Present the current data
            case "2":
                IO.output_student_and_course_names(students)
                continue

            # Save the data to a file
            case "3":
                FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
                continue

            # Stop the loop
            case "4":
                print("Program Ended")
                break