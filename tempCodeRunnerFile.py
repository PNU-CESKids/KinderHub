def main():
    con, conn = connect_to_database()

    # 로그인
    user_id = input("Enter your username: ")
    user_pw = input("Enter your password: ")

    logged_in_user_id = log_in(con, conn, user_id, user_pw)
    print(logged_in_user_id)

    if logged_in_user_id.startswith("Login successful"):
        # Example of using the view_student_info function
        student_info = view_student_info(con, conn, int(logged_in_user_id.split(": ")[1]))
        print("Student Information:")
        print(student_info)