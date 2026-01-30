import tablib

dict_student = {}
dict_grades = {}
subjects = ["PROGRAMMING", "DISCRETE", "STATISTICS"]


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


def validate_name_format(name):
    """Validate name format: SURNAME, FIRSTNAME M.I."""
    if ',' not in name:
        return False, "Name must be in format: SURNAME, FIRSTNAME M.I."

    parts = name.split(',')
    if len(parts) != 2:
        return False, "Name must be in format: SURNAME, FIRSTNAME M.I."

    surname = parts[0].strip()
    given_names = parts[1].strip()

    if not surname or not given_names:
        return False, "Both surname and given names are required."

    if not all(char.isalpha() or char.isspace() or char in ".," for char in name):
        return False, "Name can only contain letters, spaces, commas, and periods."

    return True, ""


def store_student(name, student_num, section):
    dict_student[student_num] = {
        "name": name.upper(),
        "section": section.upper()
    }
    return dict_student[student_num]


def view_all_students_by_section():
    """View all students organized by section"""
    if not dict_student:
        print("No registered students yet.")
        return

    print("\n" + "=" * 60)
    print("ALL STUDENTS BY SECTION")
    print("=" * 60)

    sections_dict = {}
    for student_num, info in dict_student.items():
        section = info['section']
        if section not in sections_dict:
            sections_dict[section] = []
        sections_dict[section].append((info['name'], student_num))

    for section, students in sections_dict.items():
        print(f"\n{section} SECTION:")
        print("-" * 50)
        print(f"{'No.':<4} {'NAME':<30} {'STUDENT NUMBER':<15}")
        print("-" * 50)

        for i, (name, student_num) in enumerate(students, 1):
            print(f"{i:<4} {name:<30} {student_num:<15}")

        print(f"Total in {section}: {len(students)} students")


def view_section_students():
    """View students in a specific section"""
    if not dict_student:
        print("No registered students yet.")
        return

    section = input("Enter section to view (e.g., BSCS-12M1): ").upper()

    section_students = []
    for student_num, info in dict_student.items():
        if info['section'] == section:
            section_students.append((info['name'], student_num))

    if not section_students:
        print(f"No students found in section {section}.")
        return

    print(f"\n{section} SECTION:")
    print("-" * 50)
    print(f"{'No.':<4} {'NAME':<30} {'STUDENT NUMBER':<15}")
    print("-" * 50)

    for i, (name, student_num) in enumerate(section_students, 1):
        print(f"{i:<4} {name:<30} {student_num:<15}")

    print(f"Total: {len(section_students)} students")


def view_specific_student_grades():
    """View grades of a specific student"""
    if not dict_student:
        print("No registered students yet.")
        return

    student_num = input("Enter student number: ")

    if student_num not in dict_student:
        print("Student not found!")
        return

    student_info = dict_student[student_num]
    print(f"\nStudent: {student_info['name']}")
    print(f"Is this student correct? (y/n): ", end="")
    confirm = input().lower()

    if confirm != 'y':
        print("Returning to menu...")
        return

    if student_num not in dict_grades:
        print("No grades computed for this student yet.")
        return

    grades = dict_grades[student_num]

    print("\n" + "=" * 60)
    print(f"GRADES FOR: {student_info['name'].upper()}")
    print(f"SECTION: {student_info['section']}")
    print(f"STUDENT NUMBER: {student_num}")
    print("=" * 60)

    print(f"\n{'SUBJECT':<15} {'PRELIM':<8} {'MIDTERM':<8} {'PREFINAL':<9} {'FINAL':<8} {'AVERAGE':<8}")
    print("-" * 60)

    for subject in subjects:
        if subject in grades:
            subj_grades = grades[subject]
            avg = (subj_grades['prelim'] * 0.20 +
                   subj_grades['midterm'] * 0.25 +
                   subj_grades['prefinal'] * 0.25 +
                   subj_grades['final'] * 0.30)

            print(f"{subject:<15} "
                  f"{subj_grades['prelim']:<8.1f} "
                  f"{subj_grades['midterm']:<8.1f} "
                  f"{subj_grades['prefinal']:<9.1f} "
                  f"{subj_grades['final']:<8.1f} "
                  f"{avg:<8.2f}")

    if 'final_average' in grades:
        print("\n" + "-" * 60)
        print(f"{'FINAL AVERAGE:':<15} {grades['final_average']:.2f}")
        print(f"{'REMARKS:':<15} {grades['remarks']}")


def view_section_grades():
    """View grades of all students in a section"""
    if not dict_student:
        print("No registered students yet.")
        return

    section = input("Enter section to view (e.g., BSCS-12M1): ").upper()

    section_students = []
    for student_num, info in dict_student.items():
        if info['section'] == section:
            if student_num in dict_grades:
                section_students.append((info['name'], student_num, dict_grades[student_num]))

    if not section_students:
        print(f"No students with grades found in section {section}.")
        return

    print(f"\n" + "=" * 80)
    print(f"GRADES FOR {section} SECTION")
    print("=" * 80)

    for name, student_num, grades in section_students:
        print(f"\n{name} - {student_num}")
        print("-" * 40)
        print(f"{'SUBJECT':<15} {'PRELIM':<8} {'MIDTERM':<8} {'PREFINAL':<9} {'FINAL':<8}")

        for subject in subjects:
            if subject in grades:
                subj_grades = grades[subject]
                print(f"{subject:<15} "
                      f"{subj_grades['prelim']:<8.1f} "
                      f"{subj_grades['midterm']:<8.1f} "
                      f"{subj_grades['prefinal']:<9.1f} "
                      f"{subj_grades['final']:<8.1f}")

        if 'final_average' in grades:
            print(f"\nFINAL AVERAGE: {grades['final_average']:.2f} - {grades['remarks']}")
        print()


def view_student_records_menu():
    """Menu for viewing student records"""
    while True:
        print("\n" + "=" * 50)
        print("VIEW STUDENT RECORDS")
        print("=" * 50)
        print("1. View all students' records (by section)")
        print("2. View a specific section")
        print("3. View a specific student grades")
        print("4. View a section grades")
        print("5. Return to Main Menu")

        try:
            choice = int(input("\nPlease input a number: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == 1:
            view_all_students_by_section()
            input("\nPress Enter to continue...")

        elif choice == 2:
            view_section_students()
            input("\nPress Enter to continue...")

        elif choice == 3:
            view_specific_student_grades()
            input("\nPress Enter to continue...")

        elif choice == 4:
            view_section_grades()
            input("\nPress Enter to continue...")

        elif choice == 5:
            break

        else:
            print("Invalid choice. Please select 1-5.")


def compute_grades():
    """Teacher's log function to compute student grades with subjects"""
    if not dict_student:
        print("No registered students yet. Please register students first.")
        input("Press Enter to return to main menu...")
        return

    print("\n" + "=" * 50)
    print("TEACHER'S LOG - GRADE COMPUTATION")
    print("=" * 50)

    while True:
        print("\nRegistered Students:")
        for i, (student_num, info) in enumerate(dict_student.items(), 1):
            print(f"{i}. {info['name']} - {student_num} - {info['section']}")

        print("\nSelect student to compute grades:")
        print("1. Enter student number")
        print("2. Return to main menu")

        try:
            choice = int(input("\nEnter choice: "))
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

            print(f"\nComputing grades for: {student_name}")
            print("-" * 40)

            student_grades = {}
            final_averages = []

            for subject in subjects:
                print(f"\n{subject}:")
                try:
                    prelim = float(input("  PRELIM grade (0-100): "))
                    midterm = float(input("  MIDTERM grade (0-100): "))
                    prefinal = float(input("  PREFINAL grade (0-100): "))
                    final = float(input("  FINAL grade (0-100): "))

                    subject_grades = [prelim, midterm, prefinal, final]
                    if any(grade < 0 or grade > 100 for grade in subject_grades):
                        print("Grades must be between 0 and 100.")
                        continue

                    student_grades[subject] = {
                        'prelim': prelim,
                        'midterm': midterm,
                        'prefinal': prefinal,
                        'final': final
                    }

                    subject_avg = (prelim * 0.20) + (midterm * 0.25) + (prefinal * 0.25) + (final * 0.30)
                    final_averages.append(subject_avg)

                except ValueError:
                    print("Invalid input. Please enter numeric values.")
                    continue

            if final_averages:
                final_avg = sum(final_averages) / len(final_averages)
                remarks = "PASSED" if final_avg >= 75 else "FAILED"

                dict_grades[student_num] = student_grades
                dict_grades[student_num]['final_average'] = round(final_avg, 2)
                dict_grades[student_num]['remarks'] = remarks
                dict_grades[student_num]['name'] = student_name
                dict_grades[student_num]['section'] = dict_student[student_num]['section']

                print(f"\nGrades computed successfully for {student_name}!")
                print(f"Final Average: {final_avg:.2f} - {remarks}")

                while True:
                    print("\nWhat would you like to do next?")
                    print("1. Compute grades for another student")
                    print("2. Edit this student's grades")
                    print("3. Return to main menu")

                    try:
                        next_choice = int(input("\nEnter choice: "))
                    except ValueError:
                        print("Invalid input.")
                        continue

                    if next_choice == 1:
                        break
                    elif next_choice == 2:
                        edit_student_grades(student_num)
                        break
                    elif next_choice == 3:
                        return
                    else:
                        print("Invalid choice.")

                if next_choice == 1:
                    continue
                elif next_choice == 3:
                    break

        else:
            print("Invalid choice. Please select 1 or 2.")


def edit_student_grades(student_num=None):
    """Edit student grades"""
    if not dict_student:
        print("No registered students yet.")
        return

    if student_num is None:
        print("\nRegistered Students:")
        for i, (num, info) in enumerate(dict_student.items(), 1):
            print(f"{i}. {info['name']} - {num} - {info['section']}")

        student_num = input("\nEnter student number to edit grades: ")

    if student_num not in dict_student:
        print("Student not found!")
        return

    if student_num not in dict_grades:
        print("No grades computed for this student yet.")
        return

    student_name = dict_student[student_num]['name']

    print(f"\nEditing grades for: {student_name}")

    while True:
        print("\nWhat would you like to edit?")
        print("1. PRELIM grades")
        print("2. MIDTERM grades")
        print("3. PREFINAL grades")
        print("4. FINAL grades")
        print("5. Return to previous menu")

        try:
            period_choice = int(input("\nEnter choice: "))
        except ValueError:
            print("Invalid input.")
            continue

        if period_choice == 5:
            break

        if period_choice not in [1, 2, 3, 4]:
            print("Invalid choice.")
            continue

        period_map = {1: 'prelim', 2: 'midterm', 3: 'prefinal', 4: 'final'}
        period = period_map[period_choice]

        print(f"\nEditing {period.upper()} grades:")
        print("Which subject?")
        for i, subject in enumerate(subjects, 1):
            print(f"{i}. {subject}")

        try:
            subject_choice = int(input("\nEnter subject number: "))
        except ValueError:
            print("Invalid input.")
            continue

        if subject_choice < 1 or subject_choice > len(subjects):
            print("Invalid subject choice.")
            continue

        subject = subjects[subject_choice - 1]

        if subject not in dict_grades[student_num]:
            print(f"No grades recorded for {subject} yet.")
            continue

        try:
            new_grade = float(input(f"Enter new {period} grade for {subject} (0-100): "))
            if new_grade < 0 or new_grade > 100:
                print("Grade must be between 0 and 100.")
                continue

            dict_grades[student_num][subject][period] = new_grade

            final_averages = []
            for subj in subjects:
                if subj in dict_grades[student_num]:
                    subj_grades = dict_grades[student_num][subj]
                    subject_avg = (subj_grades['prelim'] * 0.20 +
                                   subj_grades['midterm'] * 0.25 +
                                   subj_grades['prefinal'] * 0.25 +
                                   subj_grades['final'] * 0.30)
                    final_averages.append(subject_avg)

            if final_averages:
                final_avg = sum(final_averages) / len(final_averages)
                dict_grades[student_num]['final_average'] = round(final_avg, 2)
                dict_grades[student_num]['remarks'] = "PASSED" if final_avg >= 75 else "FAILED"

            print(f"\nGrade updated successfully!")
            print(f"New {period} grade for {subject}: {new_grade}")
            print(f"New final average: {dict_grades[student_num]['final_average']:.2f}")

            confirm = input("\nIs this correct? (y/n): ").lower()
            if confirm != 'y':
                print("Changes discarded.")


        except ValueError:
            print("Invalid input. Please enter a number.")


def edit_student_info():
    """Edit student information"""
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

    student_num = input("\nEnter student number to edit: ")

    if student_num not in dict_student:
        print("Student not found!")
        input("Press Enter to return to main menu...")
        return

    current_info = dict_student[student_num]

    while True:
        print(f"\nEditing: {current_info['name']}")
        print("1. Edit Name")
        print("2. Edit Section")
        print("3. Edit Student Number")
        print("4. Edit Student Grades")
        print("5. Return to Main Menu")

        try:
            choice = int(input("\nSelect what to edit: "))
        except ValueError:
            print("Please enter a number.")
            continue

        if choice == 1:
            while True:
                new_name = input(f"Current name: {current_info['name']}\nEnter new name (SURNAME, FIRSTNAME M.I.): ")

                is_valid, error_msg = validate_name_format(new_name)
                if not is_valid:
                    print(error_msg)
                    continue

                if len(new_name) < 3 or len(new_name) > 50:
                    print("Name must be between 3 and 50 characters.")
                    continue

                dict_student[student_num]['name'] = new_name.upper()

                if student_num in dict_grades:
                    dict_grades[student_num]['name'] = new_name.upper()

                print(f"Name updated to: {new_name.upper()}")
                current_info['name'] = new_name.upper()
                break

        elif choice == 2:
            while True:
                new_section = input(
                    f"Current section: {current_info['section']}\nEnter new section (format: ABCD-12A3 or BSE1-12A3): ").upper()

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
                    dict_grades[new_student_num]['name'] = current_info['name']

                print(f"Student number updated from {student_num} to {new_student_num}")
                student_num = new_student_num
                break

        elif choice == 4:
            edit_student_grades(student_num)

        elif choice == 5:
            break

        else:
            print("Invalid choice. Please select 1-5.")

    print("\nStudent information updated successfully!")
    input("Press Enter to return to main menu...")


def main_menu():
    while True:
        print("\n" + "=" * 50)
        print("WELCOME TO STUDENT GRADE EVALUATION SYSTEM")
        print("=" * 50)
        print("\n--- MAIN MENU ---")
        print("1. Register Student")
        print("2. View Student Records")
        print("3. Teacher's Log (Compute Grades)")
        print("4. Edit Student Information")
        print("5. Exit")

        try:
            choice = int(input("\nPlease input a number: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == 1:
            while True:
                student_num = input("\nEnter Student Number (6 digits): ")

                if len(student_num) != 6 or not student_num.isdigit():
                    print("Invalid input. Student number must be 6 digits.")
                    continue
                if student_num in dict_student:
                    print("This student number has already been registered.")
                    continue
                break

            while True:
                name = input("Enter Name (Format: SURNAME, FIRSTNAME M.I.): ")

                is_valid, error_msg = validate_name_format(name)
                if not is_valid:
                    print(error_msg)
                    continue

                if len(name) < 3 or len(name) > 50:
                    print("Name must be between 3 and 50 characters.")
                    continue
                break

            while True:
                section = input("Enter Section (format: ABCD-12A3 or BSE1-12A3): ").upper()

                if validate_section(section):
                    store_student(name, student_num, section)
                    print(f"\nSuccessfully registered {name.upper()}!")
                    break
                else:
                    print("Invalid format. Use format: ABCD-12A3 or BSE1-12A3")

        elif choice == 2:
            view_student_records_menu()

        elif choice == 3:
            compute_grades()

        elif choice == 4:
            edit_student_info()

        elif choice == 5:
            print("\nThank you for using Student Grade Evaluation System!")
            print("Exiting program...")
            break

        else:
            print("Invalid choice. Please select 1-5.")
main_menu()

