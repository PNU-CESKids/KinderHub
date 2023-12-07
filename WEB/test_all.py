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

# Add this function definition in your code
def close(connection):
    try:
        if connection:
            connection.close()
    except Exception as e:
        print(f"Error closing connection: {e}")

# 사용자 등록
def register(con, conn, user_name, user_email, user_pw, user_role, student_id):
    hashed_password = generate_password_hash(user_pw, method='pbkdf2:sha256')
    try:
        # Insert into Users table
        user_insert_query = "INSERT INTO Users (UserName, UserRole, StudentID, UserPassword, UserEmail) VALUES (%s, %s, %s, %s, %s) RETURNING UserID;"
        
        if not student_id and user_role in ('Principal', 'Teacher', 'OtherSchoolStaff'):
            student_id = None

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
        query = "SELECT UserID, UserPassword FROM Users WHERE UserEmail = %s;"
        conn.execute(query, (user_email,))
        result = conn.fetchone()

        if result and check_password_hash(result[1], user_pw):
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
'''
def view_user_info(conn, user_id):
    try:
        query = "SELECT * FROM Users WHERE UserID = %s;"
        conn.execute(query, (user_id,))
        result = conn.fetchone()
        return result
    except Exception as e:
        return f"Error: {e}"
'''

# user id로 username 찾기
def get_user_name_by_id(con, user_id):
    con.execute("SELECT username FROM users WHERE userid = %s", (user_id,))
    result = con.fetchone()
    if result:
        return result[0]
    return None

# 사용자 정보 조회
def view_user_info(conn, user_id):
    try:
        query = "SELECT UserName, UserRole, studentid, useremail FROM Users WHERE UserID = %s;"
        conn.execute(query, (user_id,))
        result = conn.fetchone()
        return result
    except Exception as e:
        return f"Error: {e}"

# 원아 이름 조회
def view_student_info(conn, user_id):
    try:
        query = "SELECT studentname FROM Student WHERE StudentID = (SELECT StudentID FROM Users WHERE UserID = %s);"
        conn.execute(query, (user_id,))
        result = conn.fetchone()
        return result
    except Exception as e:
        return f"Error: {e}"


# 원아 모든 정보 조회
def view_student_all_info(con, conn, user_id):
    con, conn = connect_to_database()
    try:
        query = "SELECT studentid FROM users WHERE userid = %s;"
        conn.execute(query, (user_id,))
        student_id = conn.fetchone()[0]

        query = "SELECT studentid, studentname, classname, birthdate, attendance, healthstatus, address, teacherid FROM Student WHERE studentid = %s;"
        conn.execute(query, (student_id,))
        result = conn.fetchone()

        con.commit()
        return result
    except Exception as e:
        return f"Error: {e}"
        
        
def get_student_info(conn, user_id):
    try:
        query = "SELECT * FROM student WHERE teacherid = %s;"
        conn.execute(query, (user_id,))
        result = conn.fetchall()
        print("result: " + str(result))
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
def view_chat(conn, user_id, user_role):
    try:
        users=view_user_info(conn, user_id)
        if users[1] == 'Teacher':
            query = """
                SELECT chat.*, users.userrole,student.studentname
FROM chat
JOIN users ON chat.senderid = users.userid
JOIN student ON chat.receiverid = student.studentid
WHERE chat.senderid = %s
   OR chat.receiverid IN (
       SELECT studentid
       FROM student
       WHERE teacherid = %s
   )
ORDER BY chat.receiverid;
                """
            conn.execute(query, (user_id,user_id,))
        else:
            query = """
                    SELECT chat.*, users.userrole, users.username
                    FROM chat
                    JOIN users ON chat.senderid = users.userid
                    WHERE chat.receiverid = (SELECT studentid from users where userid=%s);
                    """
            conn.execute(query, (user_id,))
        
        result = conn.fetchall()
        return result
    except Exception as e:
        return f"Error: {e}"
    else:
        return "Unauthorized. Only Guardian and Teacher can view chat messages."

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
def set_schedule(con, conn, date, time, event_type, description, student_ids):
    try:
        query = "INSERT INTO Schedule (EventType, Date, Time, Description) VALUES (%s, %s, %s, %s) RETURNING ScheduleID;"
        conn.execute(query, (event_type, date, time, description))
        schedule_id = conn.fetchone()[0]

        for student_id in student_ids:
            query = "INSERT INTO ScheduleStudent (ScheduleID, StudentID) VALUES (%s, %s);"
            conn.execute(query, (schedule_id, student_id))

        con.commit()
        return f"Schedule added successfully. Last ScheduleID: {schedule_id}"
    except Exception as e:
        con.rollback()
        return f"Error: {e}"

# 스케줄 조회
def view_schedule(con, conn, user_id):
    try:
        # 사용자의 studentid 가져오기
        query = "SELECT studentid FROM users WHERE userid = %s;"
        conn.execute(query, (user_id,))
        student_id = conn.fetchone()[0]

        # 해당 학생의 스케줄 조회
        query = "SELECT EventType, Date, Time, Description FROM Schedule s JOIN ScheduleStudent ss ON s.scheduleid = ss.scheduleid WHERE ss.studentid = %s;"
        conn.execute(query, (student_id,))
        
        result = conn.fetchall()
        con.commit()
        return result
    except Exception as e:
        con.rollback()
        return f"Error: {e}"

# 모든 학생들의 이름 조회
def all_students_name_info(con, conn):
    try:
        query = "SELECT studentid, studentname FROM Student;"
        conn.execute(query)
        result = conn.fetchall()
        con.commit()
        return result
    except Exception as e:
        con.rollback()
        return f"Error: {e}"

# 하원 주체 선택 권한 부여
def grant_guardian_selection_permissions(con, conn, user_role):
    con, conn = connect_to_database()
    try:
        read_permission = 'O'
        write_permission = 'O' if user_role in ['Guardian'] else 'X'

        # 기존에 GRANT 되었던 권한들 다시 철회
        conn.execute(f"REVOKE ALL PRIVILEGES ON guardianselection FROM {user_role};")
        # Role을 확인해 GRANT해 줌
        conn.execute(f"GRANT SELECT ON guardianselection TO {user_role};")
        if write_permission == 'O':
            con.execute(f"GRANT INSERT, UPDATE, DELETE ON guardianselection TO {user_role};")
        print(f"after(1) transaction - user_role: {user_role}")
        con.commit()
    except Exception as e:
        con.rollback()
        return f"Error: {e}"
    finally:
        con.close()

# 하원 주체 보기
def view_guardian(con, conn, student_id):
    con, conn = connect_to_database()
    try:
        query = """
            SELECT gs.guardianid, u.username
            FROM guardianselection gs
            JOIN users u ON gs.guardianid = u.userid
            WHERE gs.studentid = %s;
        """
        conn.execute(query, (student_id,))
        result = conn.fetchall()
        print(f"after(2) transaction - student_id: {student_id}")
        con.commit()
        return result
    except Exception as e:
        con.rollback()
        return f"Error: {e}"
    finally:
        con.close()

# 하원 주체 선택
def guardian_select(con, conn, user_id, student_id, selected_guardian):
    con, conn = connect_to_database()
    try:
        check_query = "SELECT selectionid FROM GuardianSelection WHERE studentid = %s;"
        conn.execute(check_query, (student_id, ))
        existing_entry = conn.fetchone()

        if existing_entry:
            update_query = "UPDATE GuardianSelection SET guardianid = %s WHERE studentid = %s;"
            conn.execute(update_query, (selected_guardian, student_id))
        else:
            insert_query = "INSERT INTO GuardianSelection (guardianid, studentid) VALUES (%s, %s);"
            conn.execute(insert_query, (selected_guardian, student_id))
        print(f"after(3) transaction - user_id: {user_id}, student_id: {student_id}, selected_guardian: {selected_guardian}")
        con.commit()
        return "Guardian selection successful."
    except Exception as e:
        con.rollback()
        return f"Error: {e}"
    finally:
        con.close()

# 선생님, 원장, 스탭들이 모든 학생들의 하원 주체 확인
def view_all_students_and_guardians(con, conn):
    con, conn = connect_to_database()
    try:
        query = """
        SELECT
            s.studentid,
            s.studentname,
            gs.guardianid AS guardian_id,
            u.username AS guardian_name
        FROM
            Student s
        LEFT JOIN
            GuardianSelection gs ON s.studentid = gs.studentid
        LEFT JOIN
            Users u ON gs.guardianid = u.userid;
        """
        conn.execute(query)
        result = conn.fetchall()
        con.commit()
        return result
    except Exception as e:
        con.rollback()
        return f"Error: {e}"
    finally:
        con.close()

# 자유게시판 글 등록
def post_free_board(con, title, content, poster_id, image):
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
        con.close()  # Close the connection here

def get_comments_by_postid(postid):
    con, conn = connect_to_database()
    try:
        query = """
            SELECT 
                comment.commentid,
                comment.postid,
                comment.commenterid,
                comment.commentcontent,
                comment.timestamp,
                users.useremail
            FROM 
                comment
            JOIN 
                users ON comment.commenterid = users.userid
            WHERE 
                comment.postid = %s;
        """
        conn.execute(query, (postid,))
        result_set = conn.fetchall()
        return result_set
    finally:
        conn.close()
        con.close()

def view_post(con, conn, post_id):
    try:
        # Fetch post information
        query = """
        SELECT
            freeboardqa.title,
            freeboardqa.content,
            freeboardqa.timestamp,
            freeboardqa.image,
            freeboardqa.posterid,
            users.useremail
        FROM
            freeboardqa
        JOIN
            users ON freeboardqa.posterid = users.userid
        WHERE
            freeboardqa.postid = %s;
        """

        conn.execute(query, (post_id,))
        post_info = conn.fetchone()

        # Fetch comments for the post using get_comments_by_post_id
        comments = get_comments_by_postid(post_id)

        return {"post_info": post_info, "comments": comments}
    except Exception as e:
        return {"error": f"Error: {e}"}

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
def view_free_board(conn):
    try:
        query = "SELECT PostID, Title FROM FreeBoardQA;"
        conn.execute(query)
        result = conn.fetchall()
        return result
    except Exception as e:
        return f"Error: {e}"

# 자유게시판 글 삭제 함수
def delete_post_free_board(con, conn, post_id):
    try:
        # user_id와 post_id가 일치하는지 확인
        query = "SELECT PosterID FROM FreeBoardQA WHERE PostID = %s;"
        conn.execute(query, (post_id,))
        poster_id = conn.fetchone()

        if poster_id:
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
        # QUERY1 : 해당 날짜에 식단이 이미 있는지 확인
        check_query = "SELECT * FROM MealPlan WHERE Date = %s;"
        conn.execute(check_query, (date,))
        existing_meal = conn.fetchone()
        # 있으면 UPDATE, 없으면 INSERT로
        if existing_meal:
            # If a meal plan exists, update it
            update_query = """
                UPDATE MealPlan 
                SET Meal1 = %s, Meal2 = %s, Snack = %s 
                WHERE Date = %s;
            """
            conn.execute(update_query, (meal1, meal2, snack, date))
        else:
            # If no meal plan exists, insert a new record
            insert_query = """
                INSERT INTO MealPlan (Date, Meal1, Meal2, Snack) 
                VALUES (%s, %s, %s, %s);
            """
            conn.execute(insert_query, (date, meal1, meal2, snack))
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
        result = conn.fetchall()  # Use fetchall instead of fetchone
        return result
    except Exception as e:
        return f"Error: {e}"

# 학생 등록 함수
def register_stud(con, conn, studentname, classname, birthdate, attendance, healthstatus, address, teacherid, guardianid):
    try:
        student_insert_query = "INSERT INTO Student (studentname, classname, birthdate, attendance, healthstatus, address, teacherid) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING studentID;"
        guardian_insert_query = "INSERT INTO GuardianSelection (guardianid, studentid) VALUES (%s, %s) RETURNING selectionID;"

        conn.execute(student_insert_query, (studentname, classname, birthdate, attendance, healthstatus, address, teacherid))
        student_id = conn.fetchone()[0]

        conn.execute(guardian_insert_query, (guardianid, student_id))
        selection_id = conn.fetchone()[0]

        con.commit()
        return f"Student {student_id} registered successfully."
    
    except Exception as e:
        con.rollback()
        return f"Error during student registration: {e}"
    
    finally:
        close(con)

def main():
    con, conn = connect_to_database()

if __name__ == '__main__':
    main()
