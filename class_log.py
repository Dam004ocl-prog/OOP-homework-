class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecturer(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and \
           course in self.courses_in_progress and \
           course in lecturer.courses_attached and \
           1 <= grade <= 10:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        avg = self._avg()
        courses = ', '.join(self.courses_in_progress) or 'нет'
        finished = ', '.join(self.finished_courses) or 'нет'
        return (f"Имя: {self.name}\nФамилия: {self.surname}\n"
                f"Средняя оценка: {avg:.1f}\nКурсы: {courses}\n"
                f"Завершено: {finished}")

    def __eq__(self, other):
        return self._avg() == other._avg()
    def __lt__(self, other):
        return self._avg() < other._avg()
    def _avg(self):
        if not self.grades: return 0
        return sum(sum(g) for g in self.grades.values()) / sum(len(g) for g in self.grades.values())


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"

class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def add_grade(self, course, grade):
        self.grades.setdefault(course, []).append(grade)
    def __str__(self):
        avg = self._avg()
        return super().__str__() + f"\nСредняя оценка: {avg:.1f}"

    def __eq__(self, other):
        return self._avg() == other._avg()
    def __lt__(self, other):
        return self._avg() < other._avg()
    def _avg(self):
        if not self.grades: return 0
        return sum(sum(g) for g in self.grades.values()) / sum(len(g) for g in self.grades.values())

class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and \
           course in self.courses_attached and \
           course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

def student_course_avg(students, course):
    total = count = 0
    for student in students:
        if course in student.grades:
            total += sum(student.grades[course])
            count += len(student.grades[course])
    return round(total / count, 1) if count else 0

def lecturer_course_avg(lecturers, course):
    total = count = 0
    for lecturer in lecturers:
        if course in lecturer.grades:
            total += sum(lecturer.grades[course])
            count += len(lecturer.grades[course])
    return round(total / count, 1) if count else 0

student1 = Student('James', 'Bond', 'male')
student1.courses_in_progress = ['Python', 'Git']
student1.finished_courses = ['Введение в программирование']

student2 = Student('Clarice', 'Starling', 'female')
student2.courses_in_progress = ['Python']

lecturer1 = Lecturer('Hannibal', 'Lecter')
lecturer1.courses_attached = ['Python']

lecturer2 = Lecturer('Indiana', 'Jones')
lecturer2.courses_attached = ['Git']

reviewer1 = Reviewer('Michael', 'Corleone')
reviewer1.courses_attached = ['Python']

reviewer2 = Reviewer('Rocky', 'Balboa')
reviewer2.courses_attached = ['Git']

reviewer1.rate_hw(student1, 'Python', 9)
reviewer1.rate_hw(student1, 'Python', 10)
reviewer1.rate_hw(student2, 'Python', 8)

reviewer2.rate_hw(student1, 'Git', 10)
reviewer2.rate_hw(student1, 'Git', 9)

student1.rate_lecturer(lecturer1, 'Python', 10)
student2.rate_lecturer(lecturer1, 'Python', 9)
student1.rate_lecturer(lecturer2, 'Git', 8)

print("=== Проверяющие ===")
print(reviewer1)
print("\n" + str(reviewer2))

print("\n=== Лекторы ===")
print(lecturer1)
print("\n" + str(lecturer2))

print("\n=== Студенты ===")
print(student1)
print("\n" + str(student2))

print("\n=== Сравнения ===")
print("Студент1 > Студент2:", student1 > student2)
print("Лектор1 == Лектор2:", lecturer1 == lecturer2)

print("\n=== Средние оценки по курсам ===")
print("Python (студенты):", student_course_avg([student1, student2], 'Python'))
print("Git (студенты):", student_course_avg([student1, student2], 'Git'))
print("Python (лекторы):", lecturer_course_avg([lecturer1, lecturer2], 'Python'))
print("Git (лекторы):", lecturer_course_avg([lecturer1, lecturer2], 'Git'))
