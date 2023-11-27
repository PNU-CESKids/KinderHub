import psycopg2
import re
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Connect to Database
def connect_to_database():
    con = psycopg2.connect(
        database='termkk',
        user='db2023',
        password='db!2023',
        host='::1',
        port='5432'
    )
    conn = con.cursor()
    return con, conn

# password 유효성 검사
def validate_password(self):
    return len(self.password) >= 4

# 사용자 등록
def register(con, conn, user_name, user_email, user_pw, user_role, student_id):
    hashed_password = generate_password_hash(user_pw, method='pbkdf2:sha256')
    try:
        # Insert into Users table
        user_insert_query = "INSERT INTO Users (UserName, UserRole, StudentID, UserPassword, UserEmail) VALUES (%s, %s, %s, %s, %s) RETURNING UserID;"
        conn.execute(user_insert_query, (user_name, user_role, student_id, hashed_password, user_email))
        user_id = conn.fetchone()[0]

        con.commit()
        return f"User {user_id} registered successfully."
    except Exception as e:
        con.rollback()
        return f"Error: {e}"
    finally:
        con.close()


 # 로그인
def log_in(con, conn, user_email, user_pw):
    try:
        query = "SELECT UserID FROM Users WHERE UserEmail = %s AND UserPassword = %s;"
        conn.execute(query, (user_email, user_pw))
        result = conn.fetchone()
        if result and check_password_hash(result[1], user_pw) :
            return result[0]  # Return the user ID directly
        else:
            return None  # Return None if login fails
    except Exception as e:
        return None  # Handle the exception or log it, return None for simplicity


# 로그아웃
def log_out(con, conn):
    con.close()
    return "Logout successful."

# user 정보 조회
def view_user_info(conn, user_id):
    try:
        query = "SELECT * FROM Users WHERE UserID = %s;"
        conn.execute(query, (user_id,))
        result = conn.fetchone()
        return result
    except Exception as e:
        return f"Error: {e}"

def view_user_info(conn, user_id):
    try:
        query = "SELECT UserName, UserRole, studentid, useremail FROM Users WHERE UserID = %s;"
        conn.execute(query, (user_id,))
        result = conn.fetchone()
        return result
    except Exception as e:
        return f"Error: {e}"


# 원아 정보 조회
def view_student_info(conn, user_id):
    try:
        query = "SELECT * FROM Student WHERE StudentID = (SELECT StudentID FROM Users WHERE UserID = %s);"
        conn.execute(query, (user_id,))
        result = conn.fetchone()
        return result
    except Exception as e:
        return f"Error: {e}"


# 원아 정보 관리
def manage_student_info(con, conn, user_id, attendance, health_status, address):
    try:
        query = "UPDATE Student SET Attendance = %s, HealthStatus = %s, Address = %s WHERE StudentID = (SELECT StudentID FROM Users WHERE UserID = %s);"
        conn.execute(query, (attendance, health_status, address, user_id))
        con.commit()
        return "Student information updated successfully."
    except Exception as e:
        con.rollback()
        return f"Error: {e}"

# 알림장 조회
def view_chat(con, conn, receiver_id, user_role):
    try:
        if user_role in ["Principal", "Teacher"]:
            query = "SELECT SenderID, Message, TimeStamp, Image FROM Chat WHERE ReceiverID = %s;"
            conn.execute(query, (receiver_id,))
            result = conn.fetchall()
            return result
        else:
            return "Unauthorized. Only Principal and Teacher can view chat messages."
    except Exception as e:
        return f"Error: {e}"

# 알림장 작성
def insert_chat(con, conn, user_id, receiver_id, message, image):
    try:
        sender_id =  user_id
        query = "INSERT INTO Chat (SenderID, ReceiverID, Message, TimeStamp, Image) VALUES (%s, %s, %s, %s, %s);"
        conn.execute(query, (sender_id, receiver_id, message, datetime.now(), image))
        con.commit()
        return "Chat message added successfully."
    except Exception as e:
        con.rollback()
        return f"Error: {e}"

# 스케줄 등록
def set_schedule(con, conn, date, time, event_type, student_ids):
    try:
        query = "INSERT INTO Schedule (EventType, Date, Time) VALUES (%s, %s, %s) RETURNING ScheduleID;"
        conn.execute(query, (event_type, date, time))
        schedule_id = conn.fetchone()[0]

        for student_id in student_ids:
            query = "INSERT INTO ScheduleStudent (ScheduleID, StudentID) VALUES (%s, %s);"
            conn.execute(query, (schedule_id, student_id))

        con.commit()
        return f"Schedule added successfully. ScheduleID: {schedule_id}"
    except Exception as e:
        con.rollback()
        return f"Error: {e}"

# 스케줄 조회
def view_schedule(con, conn, date=None):
    try:
        if date:
            query = "SELECT EventType, Date, Time FROM Schedule WHERE Date = %s;"
            conn.execute(query, (date,))
        else:
            query = "SELECT EventType, Date, Time FROM Schedule;"
            conn.execute(query)
        
        result = conn.fetchall()
        return result
    except Exception as e:
        return f"Error: {e}"

# 하원 주체 선택
def guardian_select(con, conn, user_id, guardian_id):
    try:
        # 현재 로그인한 사용자의 StudentID를 가져오는 코드
        query1 = "SELECT StudentID FROM Users WHERE UserID = %s;"
        conn.execute(query1, (user_id,))
        result = conn.fetchone()
        if result is None:
            raise Exception("Student not found.")

        student_id = result[0]

        # GuardianSelection에 데이터 추가
        query2 = "INSERT INTO GuardianSelection (GuardianID, StudentID) VALUES (%s, %s);"
        conn.execute(query2, (guardian_id, student_id))
        con.commit()
        return "Guardian selection successful."
    except Exception as e:
        con.rollback()
        return f"Error: {e}"

# 자유게시판 글 등록

def post_free_board (con, title, content, poster_id, image=None):
    try:
        with con, con.cursor() as cursor:
            cursor.execute("""
                INSERT INTO FreeBoardQA (PosterID, Title, Content, Image, TimeStamp)
                VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
                RETURNING PostID;
            """, (poster_id, title, content, image))

            post_id = cursor.fetchone()[0]
            return post_id
    except Exception as e:
        print(f"Error: Unable to create post\n{e}")
    finally:
        close(con)

# 게시판 글에 댓글 등록 함수
def write_post_comment(con, conn, post_id, commenter_id, comment_content):
    try:
        query = "INSERT INTO Comment (PostID, CommenterID, CommentContent, TimeStamp) VALUES (%s, %s, %s, %s);"
        conn.execute(query, (post_id, commenter_id, comment_content, datetime.now()))
        con.commit()
        return "Comment added successfully."
    except Exception as e:
        con.rollback()
        return f"Error: {e}"

# 자유게시판 보기 함수
def view_free_board(con, conn):
    try:
        query = "SELECT PostID, Title FROM FreeBoardQA;"
        conn.execute(query)
        result = conn.fetchall()
        return result
    except Exception as e:
        return f"Error: {e}"

# 자유게시판 글 보기 함수
def view_post(con, conn, post_id):
    try:
        query = "SELECT Title, Content, TimeStamp, Image FROM FreeBoardQA WHERE PostID = %s;"
        conn.execute(query, (post_id,))
        post_info = conn.fetchone()

        query = "SELECT CommentContent FROM Comment WHERE PostID = %s;"
        conn.execute(query, (post_id,))
        comments = conn.fetchall()

        return {"post_info": post_info, "comments": comments}
    except Exception as e:
        return f"Error: {e}"

# 자유게시판 글 삭제 함수
def delete_post_free_board(con, conn, post_id, user_id):
    try:
        # user_id와 post_id가 일치하는지 확인
        query = "SELECT PosterID FROM FreeBoardQA WHERE PostID = %s;"
        conn.execute(query, (post_id,))
        poster_id = conn.fetchone()

        if poster_id and poster_id[0] == user_id:
            # 게시글 삭제
            query = "DELETE FROM FreeBoardQA WHERE PostID = %s;"
            conn.execute(query, (post_id,))

            # 게시글에 속한 댓글 삭제
            query = "DELETE FROM Comment WHERE PostID = %s;"
            conn.execute(query, (post_id,))

            con.commit()
            return "Post deleted successfully."
        else:
            return "Unauthorized. You cannot delete this post."
    except Exception as e:
        con.rollback()
        return f"Error: {e}"

# 게시판 글의 댓글 삭제 함수
def delete_comment(con, conn, comment_id, user_id):
    try:
        # user_id와 comment_id가 일치하는지 확인
        query = "SELECT CommenterID FROM Comment WHERE CommentID = %s;"
        conn.execute(query, (comment_id,))
        commenter_id = conn.fetchone()

        if commenter_id and commenter_id[0] == user_id:
            # 댓글 삭제
            query = "DELETE FROM Comment WHERE CommentID = %s;"
            conn.execute(query, (comment_id,))
            con.commit()
            return "Comment deleted successfully."
        else:
            return "Unauthorized. You cannot delete this comment."
    except Exception as e:
        con.rollback()
        return f"Error: {e}"

# 식단표 등록 함수
def register_meal(con, conn, date, meal1, meal2, snack):
    try:
        query = "UPDATE MealPlan SET Meal1 = %s, Meal2 = %s, Snack = %s WHERE Date = %s;"
        conn.execute(query, (meal1, meal2, snack, date))
        con.commit()
        return "Meal plan registered successfully."
    except Exception as e:
        con.rollback()
        return f"Error: {e}"

# 오늘의 식단 열람 함수
def view_todays_meal(con, conn):
    try:
        today = datetime.now().date()
        query = "SELECT Meal1, Meal2, Snack FROM MealPlan WHERE Date = %s;"
        conn.execute(query, (today,))
        result = conn.fetchone()
        return result
    except Exception as e:
        return f"Error: {e}"

# 다른 날짜의 식단 열람 함수
def view_other_days_meal(con, conn, date):
    try:
        query = "SELECT Meal1, Meal2, Snack FROM MealPlan WHERE Date = %s;"
        conn.execute(query, (date,))
        result = conn.fetchone()
        return result
    except Exception as e:
        return f"Error: {e}"

def main():
    con, conn = connect_to_database()
    
    try:
        # 로그인
        user_id = input("Enter your username: ")
        user_pw = input("Enter your password: ")

        logged_in_user_id = log_in(con, conn, user_id, user_pw)
        print(logged_in_user_id)

        if logged_in_user_id.startswith("Login successful"):
            '''
            print("\n==========[Example of using the view_student_info function]==========")
            student_info = view_student_info(conn, int(logged_in_user_id.split(": ")[1]))
            print("Student Information:")
            print(student_info)

            print("\n==========[Example of using the manage_student_info function]==========")
            attendance = input("Enter attendance (e.g., 1 for present, 0 for absent): ")
            health_status = input("Enter health status: ")
            address = input("Enter address: ")
            manage_student_info(con, conn, int(logged_in_user_id.split(": ")[1]), attendance, health_status, address)
            print("Student information updated successfully.")

            print("\n==========[Example of using the view_chat function]==========")
            receiver_id = int(input("Enter receiver ID: "))
            user_role = "Principal"  # Assuming the logged-in user is the Principal for testing
            chat_messages = view_chat(con, conn, receiver_id, user_role)
            print("Chat Messages:")
            print(chat_messages)

            print("\n==========[Example of using the insert_chat function]==========")
            receiver_id = int(input("Enter receiver ID for chat message: "))
            message = input("Enter chat message: ")
            image = None  # You can add image handling later
            insert_chat(con, conn, int(logged_in_user_id.split(": ")[1]), receiver_id, message, image)
            print("Chat message added successfully.")

            print("\n==========[Example of using the set_schedule function]==========")
            date = input("Enter date for schedule (YYYY-MM-DD): ")
            time = input("Enter time for schedule (HH:MM:SS): ")
            event_type = input("Enter event type: ")
            student_ids_str = input("Enter student IDs for the schedule (comma-separated): ")
            student_ids = [int(student_id) for student_id in student_ids_str.split(",")]
            schedule_result = set_schedule(con, conn, date, time, event_type, student_ids)
            print(schedule_result)

            print("\n==========[Example of using the guardian_select function]==========")
            guardian_id = int(input("Enter Guardian ID for selection: "))
            guardian_select_result = guardian_select(con, conn, int(logged_in_user_id.split(": ")[1]), guardian_id)
            print(guardian_select_result)

            print("\n==========[Example of using the post_free_board function]==========")
            title = input("Enter post title: ")
            content = input("Enter post content: ")
            image = None  # You can add image handling later
            #(con, title, content, poster_id, image=None)
            post_result = post_free_board(con,  title, content, int(logged_in_user_id.split(": ")[1]), image)
            print(post_result)

            print("\n==========[Example of using the write_post_comment function]==========")
            post_id = int(input("Enter Post ID for comment: "))
            commenter_id = int(input("Enter commenter ID: "))
            comment_content = input("Enter comment content: ")
            comment_result = write_post_comment(con, conn, post_id, commenter_id, comment_content)
            print(comment_result)

            print("\n==========[Example of using the view_free_board function]==========")
            free_board_result = view_free_board(con, conn)
            print("Free Board Posts:")
            print(free_board_result)

            print("\n==========[Example of using the view_post function]==========")
            view_post_id = int(input("Enter Post ID to view details: "))
            view_post_result = view_post(con, conn, view_post_id)
            print("Post Details:")
            print(view_post_result)

            print("\n==========[Example of using the delete_post_free_board function]==========")
            delete_post_id = int(input("Enter Post ID to delete: "))
            delete_post_result = delete_post_free_board(con, conn, delete_post_id, int(logged_in_user_id.split(": ")[1]))
            print(delete_post_result)

            print("\n==========[Example of using the delete_comment function]==========")
            delete_comment_id = int(input("Enter Comment ID to delete: "))
            delete_comment_result = delete_comment(con, conn, delete_comment_id, int(logged_in_user_id.split(": ")[1]))
            print(delete_comment_result)
            
            print("\n==========[Example of using the register_meal function]==========")
            date = input("Enter date for meal registration (YYYY-MM-DD): ")
            meal1 = input("Enter meal 1: ")
            meal2 = input("Enter meal 2: ")
            snack = input("Enter snack: ")
            register_meal_result = register_meal(con, conn, date, meal1, meal2, snack)
            print(register_meal_result)

            print("\n==========[Example of using the view_todays_meal function]==========")
            view_todays_meal_result = view_todays_meal(con, conn)
            print("Today's Meal:")
            print(view_todays_meal_result)

            print("\n==========[Example of using the view_other_days_meal function]==========")
            view_other_date = input("Enter date to view meal (YYYY-MM-DD): ")
            view_other_days_meal_result = view_other_days_meal(con, conn, view_other_date)
            print("Meal for the specified date:")
            print(view_other_days_meal_result)
            '''
        # 로그아웃
        log_out(con, conn)
        print("Logout successful.")

    finally:
        # Close cursor and connection if they are still open
        if conn is not None and not conn.closed:
            conn.close()
        if con is not None and not con.closed:
            con.close()

if __name__ == '__main__':
    main()



    