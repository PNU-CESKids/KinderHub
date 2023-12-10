from flask import Flask, render_template, request, session, redirect, url_for, request
import psycopg2
import re
from test_all import *

app = Flask(__name__)

# Configure your database connection here
DATABASE_URI = "postgresql://db2023:db!2023@::1:5432/termkk"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_email = request.form['useremail']
        user_pw = request.form['password']
        con, conn = connect_to_database()
        logged_in_user_id = log_in(con, conn, user_email, user_pw)
        if logged_in_user_id is not None:
            session['user_id'] = logged_in_user_id
           # user = User(logged_in_user_id['user_id'], logged_in_user_id['username'])
            return redirect(url_for('dashboard'))
        else:
            error_message = "Invalid credentials. Please try again."
            return render_template('login.html', error_message=error_message)
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        con, conn = connect_to_database()

        user_info = view_user_info(conn, int(user_id))
        print("User Info : ", user_info)
        
        if user_info:
            user_name = user_info[0]
            user_role = user_info[1]
            #student_id = user_info[2]
            user_email = user_info[3]

            return render_template('dashboard.html', user_id=user_id, user_name=user_name, user_role=user_role, user_email=user_email)
        else:
            return render_template('dashboard.html', user_id=user_id, user_name='Unknown', user_role='Unknown', user_email='Unknown')
        
    return redirect(url_for('login'))
    
# -------------------------------- 게시판

# 게시판 글쓰기
@app.route('/free_board/new', methods=['GET', 'POST'])
def post_board():
    if 'user_id' in session:
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            user_id = session['user_id']
            image = request.files['image'] if 'image' in request.files else None

            con, conn = connect_to_database()

            try:
                 # Save image to disk if available
                image_path = save_image_to_disk(image) if image else None

                post_id = post_free_board(con, title, content, user_id, image_path)

                # Commit changes to the database
                conn.commit()

                return redirect(url_for('view_board', post_id=post_id))

            except Exception as e:
                print(f"Error: Unable to create post\n{e}")

            finally:
                close(con)

        return render_template('new_free_board.html')

    return redirect(url_for('login'))

# 게시판 조회
@app.route('/board')
def view_board():
    con, conn = connect_to_database()

    posts = view_free_board(conn)  # Pass conn to view_free_board

    # userid넘겨 주기
    if 'user_id' in session:
        user_id = session['user_id']
    return render_template('board.html', posts=posts, user_id=user_id)


# 게시물 상세보기
# Route for viewing a specific post and adding comments
@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def view_post_route(post_id):
    con, conn = connect_to_database()
    if 'user_id' in session:
        user_id = session['user_id']

    if request.method == 'POST':
        commenter_id = user_id 
        comment_content = request.form['commentcontent']

        result = write_post_comment(con, conn, post_id, commenter_id, comment_content)

        # Redirect to the same post after adding a comment
        return redirect(url_for('view_post_route', post_id=post_id))

    # If it's a GET request, simply display the post details and comments
    post_data = view_post(con, conn, post_id)

    return render_template('post_detail.html', post_data=post_data)

# 게시물 삭제
@app.route('/delete_post', methods=['POST'])
def delete_post():
    post_id = request.form.get('post_id')

    con, conn = connect_to_database()
    result = delete_post_free_board(con, conn, post_id)
    return redirect('/board')

# -------------------------------- 알림장
# notification
@app.route('/notification')
def notification():
    if 'user_id' in session:
        user_id = session['user_id']
        con, conn = connect_to_database()
        user_info = view_user_info(conn, int(user_id))
        students = get_student_info(conn,int(user_id))
        if user_info:
            user_role = user_info[1]
            student_id = user_info[2]
    else:
        print("Error: please login")

    if user_role in ["Guardian", "Teacher"]:
        chat_messages = view_chat(conn, user_id, user_role)
    else:
        chat_messages = None
        print("권한 없음")

    # Close the cursor
    con.close()

    return render_template('notification.html', chat_messages=chat_messages,user_role=user_role,students=students)


@app.route('/notification/write', methods=['GET', 'POST'])
def insert_chat_route():
    if 'user_id' in session:
        user_id = session['user_id']
        con, conn = connect_to_database()
        insert_messages = None
        students= None
        user_info = view_user_info(conn, int(user_id))
        
        if user_info:
            user_role = user_info[1]
            student_id = user_info[2]  # receiverid
 
            if user_role in ["Guardian", "Teacher"]:
                if user_role == "Teacher":
                        students = get_student_info(conn,int(user_id))

                if request.method == 'POST':
                    message = request.form.get('message')
                    image = request.form.get('image')  # Assuming image is obtained from the form

                    if user_role == "Teacher":
                        selected_student_id = request.form.get('selected_student_id')
                        insert_messages = insert_chat(con, conn, user_id, selected_student_id, message, image)
                    elif user_role == "Guardian":
                        insert_messages = insert_chat(con, conn, user_id, student_id, message, image)
                    
                    # Additional logic or handling as needed
                else:
                    # Handle GET request or any additional logic if needed
                    insert_messages = None
            else:
                print("권한 없음")
    else:
        # Handle the case when 'user_id' is not in session
        return redirect('/login')  # Redirect to login page or handle accordingly

    return render_template('write_notification.html', insert_messages=insert_messages, user_role=user_role, students=students)



@app.route('/meals', methods=['GET', 'POST'])
def meals():
    con, conn = connect_to_database()

    try:
        today_meal = None  # Define today_meal here

        if request.method == 'POST':
            action = request.form['action']

            if action == 'view':
                meal_date = request.form['meal_date']
                today_meal = view_todays_meal(con, conn)
                other_days_meal = view_other_days_meal(con, conn, meal_date)
                return render_template('meal.html', today_meal=today_meal, other_days_meal=other_days_meal)

            elif action == 'register':
                today_meal = view_todays_meal(con, conn)

                register_date = request.form['register_date']
                meal1 = request.form['meal1']
                meal2 = request.form['meal2']
                snack = request.form['snack']

                register_meal(con, conn, register_date, meal1, meal2, snack)
                return render_template('meal.html', today_meal=today_meal)

        else:
            today_meal = view_todays_meal(con, conn)
            return render_template('meal.html', today_meal=today_meal)

    except Exception as e:
        return render_template('error.html', error_message=f"Error: {e}")

    finally:
        close(con)

# 스케줄 페이지
@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    con, conn = connect_to_database()
    try:
        today = datetime.now().date()
        schedule = None
        reg_schedule = None

        if request.method == 'POST':
            action = request.form.get('action')  # Use .get() for safe access

            if action == 'register':
                date = request.form.get('register_date')
                time = request.form.get('register_time')
                event_type = request.form.get('event_type')
                description = request.form.get('description')
                student_ids = request.form.getlist('student_ids')
                numeric_ids = [int(student_id.split(',')[0]) for student_id in student_ids]

                print(f"Form Data: Date={date}, Time={time}, Event Type={event_type}, Description={description}, Student IDs={numeric_ids}")

                reg_schedule = set_schedule(con, conn, date, time, event_type, description, numeric_ids)

        if 'user_id' in session:
            user_id = session['user_id']
            schedule = view_schedule(con, conn, user_id)
            all_students_info = all_students_name_info(con, conn)

        return render_template('schedule.html', today=today, schedule=schedule, reg_schedule=reg_schedule, all_students_info=all_students_info)
    except Exception as e:
        return render_template('error.html', error_message=f"Error: {e}")
    finally:
        close(con)


@app.route('/guardianselection', methods=['GET', 'POST'])
def guardianselection():
    if 'user_id' in session:
        user_id = session['user_id']
        con, conn = connect_to_database()

        try:
            # Fetch user information
            user_info = view_user_info(conn, int(user_id))
            
            if not user_info:
                return render_template('error.html', error_message="User not found.")

            user_role = user_info[1]
            student_id = user_info[2]
            print(f"User Data: user_role={user_role}, user_id={user_id}")

            all_students_info = view_all_students_and_guardians(con, conn)
            print(all_students_info)
            grant_guardian_selection_permissions(con, conn, user_role)

            # 원장이 아닐 경우에만 Student 정보 포함된 것 전달
            if student_id is not None: 
                student_info = view_student_info(conn, student_id)
                student_name = student_info[0]

                guardian = view_guardian(con, conn, student_id)
                if guardian:
                    guardian_id, guardian_name = guardian[0][0], guardian[0][1]

                if user_role == 'Guardian':
                    today_guardian = request.form.get('todayGuardian')
                    
                    print(f"Before transaction - user_id: {user_id}, student_id: {student_id}, guardian: {guardian_id}")
                    
                    # today_guardian 값이 비어 있으면 함수 호출하지 않음
                    if today_guardian:
                        guardian_select_result = guardian_select(con, conn, int(user_id), student_id, today_guardian)
                    
                        if guardian_select_result.startswith("Guardian selection successful"):
                            return render_template('guardianselection.html', user_id=user_id, user_role=user_role, guardian_id=guardian_id, guardian_name=guardian_name,
                                                student_id=student_id, student_name=student_name, user_info=user_info, student_info=student_info, 
                                                all_students_info=all_students_info, message="You can update or insert new Guardian.")
                        else:
                            return render_template('guardianselection.html', user_id=user_id, user_role=user_role, guardian_id=guardian_id, guardian_name=guardian_name, 
                                                student_id=student_id, student_name=student_name, user_info=user_info, student_info=student_info, 
                                                all_students_info=all_students_info, message=f"Error: {guardian_select_result}")
                    else:
                        # today_guardian 값이 비어 있을 때의 처리
                        return render_template('guardianselection.html', user_id=user_id, user_role=user_role, guardian_id=guardian_id, guardian_name=guardian_name, 
                                               student_id=student_id, student_name=student_name, user_info=user_info, student_info=student_info, 
                                               all_students_info=all_students_info, message="Please enter a value before submitting.")

                else:
                    return render_template('guardianselection.html', user_id=user_id, user_role=user_role, guardian_id=guardian_id, guardian_name=guardian_name, 
                                           student_id=student_id, student_name=student_name, user_info=user_info, student_info=student_info, 
                                           all_students_info=all_students_info, message="Unauthorized. Only guardians can perform guardian selection.")

            return render_template('guardianselection.html', user_id=user_id, user_role=user_role, user_info=user_info, 
                                           all_students_info=all_students_info, message="Principal/OtherSchoolStaff/Teacher : 모든 학생 정보 출력.")

        except Exception as e:
            return render_template('error.html', error_message=f"Error: {e}")

        finally:
            close(con)

    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/info')
def info():        
    try:
        con, conn = connect_to_database()
        if 'user_id' in session:
            user_id = session['user_id']

        user_info = view_user_info(conn, user_id)
        student_info = view_student_all_info(con,conn, user_id)

        return render_template('info.html', user_info=user_info, student_info=student_info)
    except Exception as e:
        return render_template('error.html', error_message=f"Error: {e}")


@app.route('/registering', methods=['GET', 'POST'])
def registering():
    if request.method == 'POST':
        username = request.form['username']
        useremail = request.form['useremail']
        password = request.form['password']
        role = request.form['role']
        student_id = request.form['student_id']

        # Validate the form data (you can add more validation as needed)
        if not username or not useremail or not password or not role:
            return render_template('registering.html', error="All fields are required.")
        
        # Process the user data and store it in the database
        try:
            con, conn = connect_to_database()

            print(f"Form Data: {username}, {useremail}, {password}, {role}, {student_id}")
            print(f"Database Connection: {conn}")

            result = register(con, conn, username, useremail, password, role, student_id)
            print(f"Registration Result: {result}")
            conn.close()

            return redirect(url_for('index'))
        except Exception as e:
            session.clear()
            # Handle database errors or other exceptions
            print(f"Error during registration: {e}")
            return render_template('registering.html', error=f"Registration failed: {str(e)}")

    # If it's a GET request, simply render the template
    return render_template('registering.html')

@app.route('/student_registering', methods=['GET', 'POST'])
def student_registering():
    if request.method == 'POST':
        # Retrieve form data
        studentname = request.form['studentname']
        classname = request.form['classname']
        birthdate = request.form['birthdate']
        attendance = request.form['attendance']
        healthstatus = request.form.get('healthstatus') == 'on'  # Convert checkbox value to boolean
        address = request.form['address']
        teacherid = request.form['teacherid']
        # default gaurdian = 원장 자신으로 설정, 즉, user_id로!
        if 'user_id' in session:
            user_id = session['user_id']

        if not studentname or not classname or not birthdate or not attendance or not address or not teacherid:
            return render_template('student_registering.html', error="All fields are required.")


        try:
            con, conn = connect_to_database()

            # Call the registration function
            result = register_stud(con, conn, studentname, classname, birthdate, attendance, healthstatus, address, teacherid, user_id)
            
            return render_template('student_registering.html', success=result)

        except Exception as e:
            print(f"Error during student registration: {e}")
            return render_template('student_registering.html', error=f"Student Registration failed: {str(e)}")

        finally:
            close(con)

    return render_template('student_registering.html')


if __name__ == '__main__':
    app.secret_key = 'your_secret_key'
    app.run(debug=True)
