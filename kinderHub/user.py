import psycopg2
import re
'''
    ToDo 
        1. 이메일을 id로 로그인 구현하기
        2. Role별로 나눌 것인지 ?
'''

class User:
    def __init__(self, con, conn, username, password, email, userrole, student_id):
        self.con = con
        self.conn = conn
        self.username = username
        self.password = password
        self.email = email
        self.userrole = userrole
        self.student_id = student_id

    # email 유효성 검사
    def is_valid_email(self):
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        match = re.match(email_pattern, self.email)
        return bool(match)

    # password 유효성 검사
    def validate_password(self):
        return len(self.password) >= 4
    
    # 로그인
    def log_in(self):
        try:
            query = "SELECT Username, UserID FROM Users WHERE useremail = %s AND UserPassword = %s;"
            self.conn.execute(query, (self.email, self.user_pw))
            result = self.conn.fetchone()
            if result:
                return f"Login successful. UserName: {result[0]}, UserID: {result[1]}"
            else:
                return "Login failed. Invalid credentials."
        except Exception as e:
            return f"Error: {e}"

    # 사용자 등록
    def register(self):
        try:
            # Check if the provided user_role is valid
            valid_roles = ['Principal', 'Teacher', 'Student', 'Guardian', 'OtherSchoolStaff', 'StudentsFamily']
            if self.userrole not in valid_roles:
                raise ValueError(f"Invalid user_role: {self.userrole}. Allowed roles are {', '.join(valid_roles)}.")

            # Check if the provided student_id exists in the Student table
            query_check_student = "SELECT studentid FROM Student WHERE StudentID = %s;"
            self.conn.execute(query_check_student, (self.student_id,))
            if self.conn.fetchone() is None:
                raise ValueError(f"Student with ID {self.student_id} does not exist. Please provide a valid student ID.")

            # Continue with the registration if the user_role and student_id are valid
            query_user = "INSERT INTO Users (UserName, UserRole, StudentID, UserPassword, UserEmail) VALUES (%s, %s, %s, %s, %s) RETURNING UserID;"
            self.conn.execute(query_user, (self.username, self.userrole, self.student_id, self.password, self.useremail))
            user_id = self.conn.fetchone()[0]


            query_student = "INSERT INTO Student (StudentID) VALUES (%s);"
            self.conn.execute(query_student, (user_id,))

            self.con.commit()
            return f"User {self.username} registered successfully User ID : {user_id}."
        except Exception as e:
            self.con.rollback()
            return f"Error: {e}"
