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
        avg = sum(sum(g) for g in self.grades.values()) / sum(len(g) for g in self.grades.values()) \
              if self.grades else 0
        return (f"Имя: {self.name}\nФамилия: {self.surname}\n"
                f"Средняя оценка: {avg:.1f}\nКурсы: {', '.join(self.courses_in_progress)}\n"
                f"Завершено: {', '.join(self.finished_courses) or 'нет'}")

    def __eq__(self, other):
        return self._avg() == other._avg()
    def __lt__(self, other):
        return self._avg() < other._avg()
    def _avg(self):
        return sum(map(sum, self.grades.values())) / sum(map(len, self.grades.values())) if self.grades else 0


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
        avg = sum(sum(g) for g in self.grades.values()) / sum(len(g) for g in self.grades.values()) \
               if self.grades else 0
        return super().__str__() + f"\nСредняя оценка: {avg:.1f}"

    def __eq__(self, other):
        return self._avg() == other._avg()
    def __lt__(self, other):
        return self._avg() < other._avg()
    def _avg(self):
        return sum(map(sum, self.grades.values())) / sum(map(len, self.grades.values())) if self.grades else 0

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

lecturer = Lecturer('Hannibal', 'Lecter')
lecturer.courses_attached += ['Python']

reviewer = Reviewer('Indiana', 'Jones')
reviewer.courses_attached += ['Python']

student = Student('James', 'Bond', 'male')
student.courses_in_progress += ['Python']

reviewer.rate_hw(student, 'Python', 10)
reviewer.rate_hw(student, 'Python', 9)

student.rate_lecturer(lecturer, 'Python', 10)
student.rate_lecturer(lecturer, 'Python', 9)

print(lecturer)
print(student)
print(lecturer > Lecturer("Clarice", "Lecter"))
