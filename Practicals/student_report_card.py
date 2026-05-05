# Build student report card using OOPS. 

class Student:
    def __init__(self, name, marks, grade):
        self.name = name     # Instance attributes
        self.marks = marks   # Instance attributes
        self.grade = grade   # Instance attributes
       # print("Hello Bachho")
        
    def calculate_average (self):   # Instance method - works on self
        if len(self.marks) == 0:    # agar marks list empty ho
            return 0                # crash mat kro, 0 eturn karo
        return sum(self.marks)/ len(self.marks)
    
    # Calls calculate_average() internally - methods can talk to each other
    def display_report(self):
        print("Name :", self.name)
        print("Marks :", self.marks)
        print("Grade :", self.grade)
        print("Average: ", self.calculate_average())

class MLStudent (Student):
    def __init__ (self, name, marks, grade, project_score):
        super().__init__(name,marks,grade)
        self.project_score = project_score   # Instance Attributes 
    
    def display_report(self):
        super().display_report()
        print("Project Score :", self.project_score)
    
# Object creation - har baar __init__ automatically runs
stu1 = Student("Jay", [85, 90, 78], "B")
stu1.display_report()   # calling method on stu1's data

stu2 = Student("Prachi", [99, 98, 95], "A")
stu2.display_report()     # same method, different data - that's OOPs magic

stu3 = Student("Kavya", [], "X")
stu3.display_report()   # Zero Division Error - bcoz len[] is 0

# ML Student 
ml1 = MLStudent("Dhrishi", [90, 96, 93], "A", 98)
ml1.display_report()