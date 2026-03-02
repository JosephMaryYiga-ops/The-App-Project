import json
import os
from datetime import datetime


# ---------------------------
# Student Class
# ---------------------------
class Student:
    def __init__(self, student_id, name, age):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.courses = {}  # course_name: grade

    def enroll_course(self, course_name):
        if course_name not in self.courses:
            self.courses[course_name] = None
            print(f"{self.name} enrolled in {course_name}")
        else:
            print("Already enrolled in this course.")

    def assign_grade(self, course_name, grade):
        if course_name in self.courses:
            self.courses[course_name] = grade
            print(f"Grade assigned successfully.")
        else:
            print("Student not enrolled in this course.")

    def calculate_gpa(self):
        grades = [grade for grade in self.courses.values() if grade is not None]
        if not grades:
            return 0
        return sum(grades) / len(grades)

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "courses": self.courses
        }

    @staticmethod
    def from_dict(data):
        student = Student(data["student_id"], data["name"], data["age"])
        student.courses = data["courses"]
        return student


# ---------------------------
# School Management System
# ---------------------------
class SchoolManagementSystem:
    def __init__(self, filename="students.json"):
        self.students = {}
        self.filename = filename
        self.load_data()

    def add_student(self, student_id, name, age):
        if student_id in self.students:
            print("Student ID already exists.")
        else:
            self.students[student_id] = Student(student_id, name, age)
            print("Student added successfully.")

    def remove_student(self, student_id):
        if student_id in self.students:
            del self.students[student_id]
            print("Student removed successfully.")
        else:
            print("Student not found.")

    def find_student(self, student_id):
        return self.students.get(student_id, None)

    def list_students(self):
        if not self.students:
            print("No students found.")
            return

        for student in self.students.values():
            print(f"\nID: {student.student_id}")
            print(f"Name: {student.name}")
            print(f"Age: {student.age}")
            print("Courses:")
            for course, grade in student.courses.items():
                print(f"  {course}: {grade}")
            print(f"GPA: {student.calculate_gpa():.2f}")

    def save_data(self):
        data = {sid: student.to_dict() for sid, student in self.students.items()}
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)
        print("Data saved successfully.")

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                data = json.load(f)
                for sid, student_data in data.items():
                    self.students[sid] = Student.from_dict(student_data)


# ---------------------------
# Utility Functions
# ---------------------------
def display_menu():
    print("\n===== SCHOOL MANAGEMENT SYSTEM =====")
    print("1. Add Student")
    print("2. Remove Student")
    print("3. Enroll in Course")
    print("4. Assign Grade")
    print("5. List Students")
    print("6. Save & Exit")


def main():
    system = SchoolManagementSystem()

    while True:
        display_menu()
        choice = input("Enter choice: ")

        if choice == "1":
            sid = input("Enter Student ID: ")
            name = input("Enter Name: ")
            age = int(input("Enter Age: "))
            system.add_student(sid, name, age)

        elif choice == "2":
            sid = input("Enter Student ID to remove: ")
            system.remove_student(sid)

        elif choice == "3":
            sid = input("Enter Student ID: ")
            student = system.find_student(sid)
            if student:
                course = input("Enter Course Name: ")
                student.enroll_course(course)
            else:
                print("Student not found.")

        elif choice == "4":
            sid = input("Enter Student ID: ")
            student = system.find_student(sid)
            if student:
                course = input("Enter Course Name: ")
                grade = float(input("Enter Grade (0-100): "))
                student.assign_grade(course, grade)
            else:
                print("Student not found.")

        elif choice == "5":
            system.list_students()

        elif choice == "6":
            system.save_data()
            

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()