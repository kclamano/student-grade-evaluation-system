dict_student = {}
dict_grades = {}


def validate_section(section):
    if len(section) != 9 or section[4] != "-":
        return False

    if (section[:4].isalpha() and
            section[5:7].isdigit() and
            section[7].isalpha() and
            section[8].isdigit()):
        return True

    if (section[:3].isalpha() and
            section[3].isdigit() and
            section[5:7].isdigit() and
            section[7].isalpha() and
            section[8].isdigit()):
        return True

    return False


def store_student(name, student_num, section):
    dict_student[student_num] = {
        "name": name,
        "section": section
    }
    return dict_student[student_num]


def edit_student_info():
    if not dict_student:
        print("No registered students yet.")
        input("Press Enter to return to main menu...")
        return

    print("=" * 50)
    print("EDIT STUDENT INFORMATION")
    print("=" * 50)

    print("Registered Students:")
    for i, (student_num, info) in enumerate(dict_student.items(), 1):
        print(f"{i}. {info['name']} - {student_num} - Section: {info['section']}")

    student_num = input("Enter student number to edit: ")

    if student_num not in dict_student:
        print("Student not found!")
        input("Press Enter to return to main menu...")
        return

    current_info = dict_student[student_num]

    while True:
        print(f"Editing: {current_info['name']}")
        print("1. Edit Name")
        print("2. Edit Section")
        print("3. Edit Student Number")
        print("4. Return to Main Menu")

        try:
            choice = int(input("Select what to edit: "))
        except ValueError:
            print("Please enter a number.")
            continue

        if choice == 1:
            while True:
                new_name = input(f"Current name: {current_info['name']}\nEnter new name: ")

                if len(new_name) < 3 or len(new_name) > 20:
                    print("Name must be between 3 and 20 characters.")
                    continue

                dict_student[student_num]['name'] = new_name

                if student_num in dict_grades:
                    dict_grades[student_num]['name'] = new_name

                print(f"Name updated to: {new_name}")
                current_info['name'] = new_name
                break

        elif choice == 2:
            while True:
                new_section = input(
                    f"Current section: {current_info['section']}\nEnter new section (format: ABCD-12A3 or BSE1-12A3): ")

                if validate_section(new_section):
                    dict_student[student_num]['section'] = new_section

                    if student_num in dict_grades:
                        dict_grades[student_num]['section'] = new_section

                    print(f"Section updated to: {new_section}")
                    current_info['section'] = new_section
                    break
                else:
                    print("Invalid format. Use format: ABCD-12A3 or BSE1-12A3")

        elif choice == 3:
            while True:
                new_student_num = input(f"Current student number: {student_num}\nEnter new student number: ")

                if len(new_student_num) != 6 or not new_student_num.isdigit():
                    print("Student number must be 6 digits.")
                    continue

                if new_student_num in dict_student and new_student_num != student_num:
                    print("This student number is already taken.")
                    continue

                dict_student[new_student_num] = dict_student[student_num]
                del dict_student[student_num]

                if student_num in dict_grades:
                    dict_grades[new_student_num] = dict_grades[student_num]
                    del dict_grades[student_num]

                print(f"Student number updated from {student_num} to {new_student_num}")
                student_num = new_student_num
                break

        elif choice == 4:
            break

        else:
            print("Invalid choice. Please select 1-4.")

    print("Student information updated successfully!")
    input("Press Enter to return to main menu...")


def compute_grades():
    if not dict_student:
        print("No registered students yet. Please register students first.")
        input("Press Enter to return to main menu...")
        return

    print("=" * 50)
    print("TEACHER'S LOG - GRADE COMPUTATION")
    print("=" * 50)

    while True:
        print("Registered Students:")
        for i, (student_num, info) in enumerate(dict_student.items(), 1):
            print(f"{i}. {info['name']} - {student_num} - {info['section']}")

        print("Select student to compute grades:")
        print("1. Enter student number")
        print("2. Return to main menu")

        try:
            choice = int(input("Enter choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == 2:
            break

        elif choice == 1:
            student_num = input("Enter student number: ")

            if student_num not in dict_student:
                print("Student not found. Please enter a registered student number.")
                continue

            student_name = dict_student[student_num]['name']

            print(f"Computing grades for: {student_name}")
            print("-" * 40)

            try:
                print("Enter grades (0-100):")
                pre_lim = float(input("  PRE-LIM grade: "))
                midterm = float(input("  MIDTERM grade: "))
                pre_finals = float(input("  PRE-FINALS grade: "))
                finals = float(input("  FINALS grade: "))

                grades = [pre_lim, midterm, pre_finals, finals]
                if any(grade < 0 or grade > 100 for grade in grades):
                    print("Grades must be between 0 and 100.")
                    continue

                final_grade = (pre_lim * 0.20) + (midterm * 0.25) + (pre_finals * 0.25) + (finals * 0.30)

                if final_grade >= 75:
                    remarks = "PASSED"
                else:
                    remarks = "FAILED"

                dict_grades[student_num] = {
                    'name': student_name,
                    'section': dict_student[student_num]['section'],
                    'pre_lim': pre_lim,
                    'midterm': midterm,
                    'pre_finals': pre_finals,
                    'finals': finals,
                    'final_grade': round(final_grade, 2),
                    'remarks': remarks
                }

                print(f"Grades computed successfully for {student_name}!")
                print(f"Final Grade: {final_grade:.2f} - {remarks}")

                another = input("Compute grades for another student? (y/n): ").lower()
                if another != 'y':
                    break

            except ValueError:
                print("Invalid input. Please enter numeric values for grades.")

        else:
            print("Invalid choice. Please select 1 or 2.")


def view_student_grades():
    print("=" * 50)
    print("VIEW STUDENT GRADES")
    print("=" * 50)

    if not dict_student:
        print("No registered students yet.")
    else:
        print(f"Total Registered Students: {len(dict_student)}")
        print(f"Students with Computed Grades: {len(dict_grades)}")
        print("-" * 90)
        print(
            f"{'No.':<4} {'Name':<20} {'Section':<12} {'Student No':<10} {'P-L':<6} {'MID':<6} {'P-F':<6} {'FIN':<6} {'Final':<7} {'Remarks':<10}")
        print("-" * 90)

        for i, (student_num, student_info) in enumerate(dict_student.items(), 1):
            if student_num in dict_grades:
                grades = dict_grades[student_num]
                print(f"{i:<4} {grades['name']:<20} {grades['section']:<12} {student_num:<10} "
                      f"{grades['pre_lim']:<6.1f} {grades['midterm']:<6.1f} "
                      f"{grades['pre_finals']:<6.1f} {grades['finals']:<6.1f} "
                      f"{grades['final_grade']:<7.2f} {grades['remarks']:<10}")
            else:
                print(f"{i:<4} {student_info['name']:<20} {student_info['section']:<12} {student_num:<10} "
                      f"{'---':<6} {'---':<6} {'---':<6} {'---':<6} {'---':<7} {'NO GRADES':<10}")

        students_without_grades = [num for num in dict_student.keys() if num not in dict_grades]
        if students_without_grades:
            print(f"{len(students_without_grades)} student(s) need grades computed:")
            for student_num in students_without_grades:
                print(f"   - {dict_student[student_num]['name']} ({student_num})")

        if dict_grades:
            total = len(dict_grades)
            passed = sum(1 for g in dict_grades.values() if g['remarks'] == 'PASSED')
            failed = total - passed
            average = sum(g['final_grade'] for g in dict_grades.values()) / total

            print(f"CLASS STATISTICS (for students with grades):")
            print(f"   Class Average: {average:.2f}")
            print(f"   Passed: {passed} ({passed / total * 100:.1f}%)")
            print(f"   Failed: {failed} ({failed / total * 100:.1f}%)")

    input("Press Enter to return to main menu...")


def main_menu():
    while True:
        print("=" * 50)
        print("Welcome to the Student Grade Evaluation System")
        print("=" * 50)
        print("--- Main Menu ---")
        print("1. Register Student")
        print("2. View Student Grades")
        print("3. Teacher's log")
        print("4. Edit Student Information")
        print("5. Exit")

        try:
            choice = int(input("Please input a number: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == 1:
            while True:
                student_num = input("Enter your Student Number: ")

                if len(student_num) != 6 or not student_num.isdigit():
                    print("Invalid input. Student number must be 6 digits.")
                    continue
                if student_num in dict_student:
                    print("This student number has already been registered.")
                    continue
                break

            while True:
                name = input("Enter your name: ")

                if len(name) < 3 or len(name) > 20:
                    print("Name must be between 3 and 20 characters.")
                    continue
                else:
                    break

            while True:
                section = input("Enter your Section (format: ABCD-12A3 or BSE1-12A3): ")

                if validate_section(section):
                    store_student(name, student_num, section)
                    print(f"Successfully registered {name}!")
                    break
                else:
                    print("Invalid format. Use format: ABCD-12A3 or BSE1-12A3")

        elif choice == 2:
            view_student_grades()

        elif choice == 3:
            compute_grades()

        elif choice == 4:
            edit_student_info()

        elif choice == 5:
            print("Thank you for using Student Grade Evaluation System!")
            print("Exiting program...")
            break

        else:
            print("Invalid choice. Please select 1-5.")


main_menu()