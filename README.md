# KinderHub
유치원 커뮤니티 향상을 위한 학부모-교사 소통 플랫폼

## Tech Stack

- Python
- PostgreSQL
- Flask

## 목차

1. 프로젝트 소개
2. 팀 소개
3. 파일 구조
4. 프로그램 사용 매뉴얼

## 프로젝트 소개

이 프로젝트는 유치원 원아들의 정보 체계 관리, 효과적인 일정 관리, 학부모-교사 간의 개별 소통 채널 제공, 식단표 확인, 안심 하원 서비스 도입, 게시판 질문과 답변 기능, 그리고 중요한 알림 서비스를 통해 학부모와 교사 간의 원활한 의사 소통과 안전한 유치원 학습 환경을 제공한다.

## 팀 소개
| 이름 | 김윤하(https://github.com/xdbsgk) | 구지원(https://github.com/kUZEEwon) |
|:------:|:----------:|:----------:|
|  | <img src="https://github.com/xdbsgk.png" width="200"> | <img src="https://github.com/kUZEEwon.png" width="200"> |
| 개발 내용 |  |  |


## 파일 구조
```
📦 KinderHub
.
├── Data
│   └── termkk_backup.sql
├── README.md
├── Report
│   ├── 보고서
│   │   ├── progress report.docx
│   │   ├── project proposal report.docx
│   │   └── review
│   └── 회의록
│       ├── 2023_11_16 회의록.md
│       └── 2023_11_19 회의록.md
└── WEB
    ├── __pycache__
    │   ├── test_all.cpython-310.pyc
    │   └── test_all.cpython-311.pyc
    ├── app.py
    ├── templates
    │   ├── board.html
    │   ├── dashboard.html
    │   ├── error.html
    │   ├── guardianselection.html
    │   ├── index.html
    │   ├── info.html
    │   ├── insert_chat.html
    │   ├── login.html
    │   ├── meal.html
    │   ├── new_free_board.html
    │   ├── notification.html
    │   ├── post_detail.html
    │   ├── registering.html
    │   ├── schedule.html
    │   ├── student_registering.html
    │   └── write_notification.html
    └── test_all.py
```

## 프로그램 사용 매뉴얼

### 데이터베이스 초기 설정

- Create New Database
    - 데이터베이스 강의에서 사용한 기존의 ts_db2023의 TABLESPACE에 새로운 DATABASE를 생성해준다.
        
        ```sql
        postgres=# CREATE DATABASE termkk OWNER db2023 TABLESPACE ts_db2023;
        CREATE DATABASE
        ```
        
- 테스트에 필요한 테이블 및 데이터 추가
    - **Data** 디렉토리 내부의 **termkk_backup.sql**을 다운받고, 다음과 같은 명령어를 실행시켜 데이터베이스의 구조와 데이터를 저장시킨다.
        
        ```sql
        psql -U db2023 -h localhost -d termkk < termkk_backup.sql
        ```
<br>

### 프로그램 실행 방법

- 새 폴더를 생성하고 해당 폴더에 git branch를 열어서 해당 명령어를 입력 한다.
    
    ```c
    git clone https://github.com/PNU-CESKids/KinderHub.git
    ```
    
- cmd창 (Windows), terminal (Mac)를 열어준 후 해당 폴더로 이동한다.
- KinderHub/WEB 으로 이동후 아래의 명령어를 입력하여 `app.py`를 실행시킨다.
    
    ```c
    python app.py
    ```
    
    ![실행이 완료된 화면](Report/imgs/Untitled.png)
    
    실행이 완료된 화면
    
- Chrome에서 [http://127.0.0.1:5000/](http://127.0.0.1:5000/) 으로 이동한다.
<br>

### 기능별 실행 방법

[https://127.0.0.1:5000/](https://127.0.0.1:5000) 으로 접속하면 아래와 같은 화면이 나온다.

| 기능            | 설명               | 화면                                     |
| ----------------------------- | ----------------------------- | ---------------------------------------- |
| **초기 화면**    | index.html      | ![index.html](Report/imgs/Untitled%201.png) |
|                |                | 자신의 계정이 있으면 login 버튼을 눌러 로그인을 진행하고, 계정이 없으면 register 버튼을 눌러 회원 가입을 한다. |
| **회원가입**     | 회원가입 화면     | ![registering.html](Report/imgs/Untitled%202.png) |
|                |               | - `Student`는 회원가입을 진행할 수 없다. 완료 후 [Login here](http://127.0.0.1:5000/login)을 눌러 로그인을 진행한다. |  
|                |               | - 자신의 역할이 `Teacher` 이거나 `OtherSchoolStep` 또는 `Principal` 일 때는 제일 하단의 studentID를 입력하지 않아도 된다. |
|                |               | register 버튼을 누르면 회원가입이 완료 된다. |
|                |               | - 완료 후 [Login here](http://127.0.0.1:5000/login)을 눌러 로그인을 진행한다. |  
| **로그인**       | 로그인 화면       | ![login.html](Report/imgs/Untitled%203.png) 자신의 Email, Password를 입력해서 로그인을 한다. |
| **로그인 실패**  | 실패 화면          | ![로그인 실패화면](Report/imgs/Untitled%204.png) Email 이나 Password를 잘못 입력하여 로그인에 실패하면 이러한 문구가 나온다. |
| **대시보드**     | 대시보드 화면     | ![dashboard.html](Report/imgs/Untitled%205.png) 원하는 기능을 메뉴에서 선택해서 들어갈 수 있다. |
| **로그아웃**     | 로그아웃 버튼     | 하단의 ‘Logout’버튼을 눌러 로그아웃을 할 수 있다.                                            |


<br>

- **Register New Student**
  
| 기능                        | 설명                                           | 화면                                            |
| --------------------------- | ---------------------------------------------- | ----------------------------------------------- |
| **Principal's dashboard**    |Principal은 Register New Student을 통해 학생 등록이 가능하다.|<img width="1470" alt="Untitled 6" src="https://github.com/PNU-CESKids/KinderHub/assets/98088494/c31b9c2a-8226-46df-a347-5f8fe6356b0d">                                         |
|    **학생 등록 화면**            | 학생 정보를 입력하고 학생을 등록할 수 있다.                |<img width="1469" alt="Untitled 7" src="https://github.com/PNU-CESKids/KinderHub/assets/98088494/9f19aa66-7355-4f02-9a17-07832fbeb2ff">                                |

<br>

- **My Information/Child Information**

| 기능                        | 설명                                           | 화면                                            |
| --------------------------- | ---------------------------------------------- | ----------------------------------------------- |
| **My/Child Information**     | 자신의 정보와 자신에게 속한 `Student`정보를 확인할 수 있다. |  ![info.html](Report/imgs/Untitled%206.png) |

<br>

- **Board(게시판)**
 
| 기능            | 설명               | 화면                                     |
| ----------------------------- | ----------------------------- | ---------------------------------------- |
| **기본 화면**    | board.html      | ![board.html(Free Board)](Report/imgs/Untitled%207.png) |
| **글 쓰기**     | 글 작성 화면       | ![new_free_board.html](Report/imgs/%25E1%2584%2589%25E1%2585%25B3%25E1%2584%258F%25E1%2585%25B3%25E1%2584%2585%25E1%2585%25B5%25E1%2586%25AB%25E1%2584%2589%25E1%2585%25A3%25E1%2586%25BA_2023-12-08_%25E1%2584%258B%25E1%2585%25A9%25E1%2584%2592%25E1%2585%25AE_4.17.06.png) |
|                |                   | new_free_board.html                      |
|                |                   | Title: 글의 제목                          |
|                |                   | Content: 글의 내용                       |
|                |                   | 위의 내용을 입력 후 ‘글쓰기’버튼을 눌러 글쓰기를 완료한다. |
|                |                   | 완료한 이 후 ‘글 목록’을 클릭하여 `Free Board`로 돌아온다. |
| **글 전체 조회** | 전체 글 목록 조회 | ![Untitled](Report/imgs/Untitled%208.png) |
| **글 상세 조회** | 글 상세 조회 페이지 이동 | ![post_detail.html](Report/imgs/Untitled%209.png) |
|                |                   | post_detail.html                         |
|                |                   | - 글 상세 조회 가능                       |
|                |                   | - Comments에서 댓글 작성과 조회 가능    |
|                |                   | - 글 목록을 누르면 `Free Board(글 전체 조회)`로 이동한다. |


<br>

- **Meal Plan**

| 기능            | 설명               | 화면                                     |
| ----------------------------- | ----------------------------- | ---------------------------------------- |
| **오늘의 식단** | 오늘의 식단 확인   | ![Today's Meal](Report/imgs/Untitled%2010.png) |
| **식단표 작성** | 식단표 작성 화면  | ![Register Meal](Report/imgs/Untitled%2011.png) Register Meal for Other Dates 에서 식단 등록이 가능하며, 식단에 해당하는 날짜, Meal1, Meal2, Snack을 순서대로 선택 후 Register Meal 버튼을 누르면 등록이 완료된다. |
| **식단표 조회** | 식단표 조회 화면  | ![View Meals](Report/imgs/Untitled%2012.png) View Meals for Other Dates에서 조회를 원하는 식단의 날짜를 (YYYY-MM-DD) 형식으로 입력하고 버튼을 누르면 조회가 된다. |


<br>

- **Notification(알림장) - Teacher, Guardian만 접속가능**

| User Role                     | 설명                                       | 화면                                                                                   |
| -----------------------------   | -----------------------------------------------    | -----------------------------------------------------------------------------------------|
| **Teacher**                     | Notification 선택 시 알림장 작성 및 조회 가능   | ![notification.html](Report/imgs/Untitled%2014.png) <br>  notification.html <br> ![write_notification.html](Report/imgs/Untitled%2015.png) <br> write_notification.html (Message: 자신이 입력하고 싶은 알림 메세지 입력, Select Student: 자신이 알림을 줘야할 학생 선택) 내용을 입력 후 채팅보내기를 누른다. <br> ![Untitled](Report/imgs/Untitled%2016.png) <br> **채팅 보내기가 성공적**으로 이루어질 경우 <br> ![Untitled](Report/imgs/Untitled%2017.png) <br> 자신이 보낸 알림사항을 조회화면에서 확인할 수 있다. Teacher는 자신에게 속한 모든 학생의 알림사항을 조회 할 수 있다. <br> |
| **Guardian**                    | Notification 선택 시 자신의 학생에 대한 알림 조회 가능  | ![Untitled](Report/imgs/Untitled%2018.png) <br> Guardian은 자신의 Student에 대한 알림만 조회 가능하다. 알림장 쓰기의 경우 Teacher와 동일하다.   |
| **그 외의 역할일 경우**              | 경고문구 확인이 가능             | ![Untitled](Report/imgs/Untitled%2013.png)                             |


<br>

- **Schedule**

| 기능                           | 설명                                               | 화면                                                                     |
| -----------------------------   | -----------------------------------------------    | -----------------------------------------------------------------------------------------|
| **스케줄 등록**                 | 초기 화면 및 등록 성공 시 메세지 확인             | ![Untitled](Report/imgs/Untitled%2019.png) <br> ![Untitled](Report/imgs/Untitled%2020.png) |
| **스케줄 조회**                 | Guardian의 경우 자신의 학생에 대한 정보만 확인 가능 | ![Untitled](Report/imgs/Untitled%2021.png) |

<br>

- **안심 하원 서비스**

| User Role                     | 설명                                       | 화면                                                                                   |
| -----------------------------   | -----------------------------------------------    | -----------------------------------------------------------------------------------------|
| **Teacher, Principal, OtherSchoolStaff** | 모든 학생의 하원정보 조회                            | ![Teacher, Principal, OtherSchoolStaff의 조회 화면](Report/imgs/Untitled%2022.png)    |
| **Guardian**                    | Guardian에 속하는 학생의 하원정보 조회 및 선택 가능. Guardian만이 Student의 하원 주체 선택이 가능하다. | ![Guardian의 조회화면](Report/imgs/Untitled%2023.png)      |
| **StudentFamily**               | StudentFamily에 속하는 학생의 하원 정보만이 조회된다. | ![StudentFamily의 조회화면](Report/imgs/Untitled%2024.png)                             |

<br>

## 데이터베이스 스키마 및 다이어그램 (Database schema / Schema diagram)

- **데이터베이스 스키마**

```
                                         Table "public.users"
    Column    |          Type          | Collation | Nullable |                Default                
--------------+------------------------+-----------+----------+---------------------------------------
 userid       | integer                |           | not null | nextval('users_userid_seq'::regclass)
 username     | character varying(20)  |           |          | 
 userrole     | role_enum              |           |          | 
 studentid    | integer                |           |          | 
 userpassword | character varying(255) |           |          | 
 useremail    | character varying(255) |           |          | 
 teacherid    | integer                |           |          | 
Indexes:
    "users_pkey" PRIMARY KEY, btree (userid)
Check constraints:
    "valid_userrole" CHECK (userrole = ANY (ARRAY['Principal'::role_enum, 'Teacher'::role_enum, 'Student'::role_enum, 'Guardian'::role_enum, 'OtherSchoolStaff'::role_enum, 'StudentsFamily'::role_enum]))
Foreign-key constraints:
    "users_studentid_fkey" FOREIGN KEY (studentid) REFERENCES student(studentid)
    "users_teacherid_fkey" FOREIGN KEY (teacherid) REFERENCES users(userid)
Referenced by:
    TABLE "comment" CONSTRAINT "comment_commenterid_fkey" FOREIGN KEY (commenterid) REFERENCES users(userid)
    TABLE "student" CONSTRAINT "fk_teacher" FOREIGN KEY (teacherid) REFERENCES users(userid)
    TABLE "freeboardqa" CONSTRAINT "freeboardqa_posterid_fkey" FOREIGN KEY (posterid) REFERENCES users(userid)
    TABLE "guardianselection" CONSTRAINT "guardianselection_guardianid_fkey" FOREIGN KEY (guardianid) REFERENCES users(userid)
    TABLE "student" CONSTRAINT "student_teacherid_fkey" FOREIGN KEY (teacherid) REFERENCES users(userid)
    TABLE "users" CONSTRAINT "users_teacherid_fkey" FOREIGN KEY (teacherid) REFERENCES users(userid)


                                          Table "public.student"
    Column    |          Type          | Collation | Nullable |                  Default                   
--------------+------------------------+-----------+----------+--------------------------------------------
 studentid    | integer                |           | not null | nextval('student_studentid_seq'::regclass)
 studentname  | character varying(20)  |           |          | 
 classname    | character(1)           |           |          | 
 birthdate    | date                   |           |          | 
 attendance   | integer                |           |          | 
 healthstatus | boolean                |           |          | 
 address      | character varying(100) |           |          | 
 teacherid    | integer                |           |          | 
Indexes:
    "student_pkey" PRIMARY KEY, btree (studentid)
Foreign-key constraints:
    "fk_teacher" FOREIGN KEY (teacherid) REFERENCES users(userid)
    "student_teacherid_fkey" FOREIGN KEY (teacherid) REFERENCES users(userid)
Referenced by:
    TABLE "guardianselection" CONSTRAINT "guardianselection_studentid_fkey" FOREIGN KEY (studentid) REFERENCES student(studentid)
    TABLE "schedulestudent" CONSTRAINT "schedulestudent_studentid_fkey" FOREIGN KEY (studentid) REFERENCES student(studentid)
    TABLE "users" CONSTRAINT "users_studentid_fkey" FOREIGN KEY (studentid) REFERENCES student(studentid)


                                          Table "public.freeboardqa"
  Column   |            Type             | Collation | Nullable |                   Default                   
-----------+-----------------------------+-----------+----------+---------------------------------------------
 postid    | integer                     |           | not null | nextval('freeboardqa_postid_seq'::regclass)
 posterid  | integer                     |           |          | 
 title     | character varying(100)      |           |          | 
 content   | text                        |           |          | 
 timestamp | timestamp without time zone |           |          | 
 image     | bytea                       |           |          | 
Indexes:
    "freeboardqa_pkey" PRIMARY KEY, btree (postid)
Foreign-key constraints:
    "freeboardqa_posterid_fkey" FOREIGN KEY (posterid) REFERENCES users(userid)
Referenced by:
    TABLE "comment" CONSTRAINT "comment_postid_fkey" FOREIGN KEY (postid) REFERENCES freeboardqa(postid) ON DELETE CASCADE


                                              Table "public.comment"
     Column     |            Type             | Collation | Nullable |                  Default                   
----------------+-----------------------------+-----------+----------+--------------------------------------------
 commentid      | integer                     |           | not null | nextval('comment_commentid_seq'::regclass)
 postid         | integer                     |           |          | 
 commenterid    | integer                     |           |          | 
 commentcontent | text                        |           |          | 
 timestamp      | timestamp without time zone |           |          | 
Indexes:
    "comment_pkey" PRIMARY KEY, btree (commentid)
Foreign-key constraints:
    "comment_commenterid_fkey" FOREIGN KEY (commenterid) REFERENCES users(userid)
    "comment_postid_fkey" FOREIGN KEY (postid) REFERENCES freeboardqa(postid) ON DELETE CASCADE


                              Table "public.mealplan"
 Column |  Type   | Collation | Nullable |                 Default                  
--------+---------+-----------+----------+------------------------------------------
 planid | integer |           | not null | nextval('mealplan_planid_seq'::regclass)
 date   | date    |           |          | 
 meal1  | text    |           |          | 
 meal2  | text    |           |          | 
 snack  | text    |           |          | 
Indexes:
    "mealplan_pkey" PRIMARY KEY, btree (planid)


                                          Table "public.schedule"
   Column    |          Type          | Collation | Nullable |                   Default                    
-------------+------------------------+-----------+----------+----------------------------------------------
 scheduleid  | integer                |           | not null | nextval('schedule_scheduleid_seq'::regclass)
 eventtype   | character varying(200) |           |          | 
 date        | date                   |           |          | 
 time        | time without time zone |           |          | 
 description | text                   |           |          | 
 scheduleimg | bytea                  |           |          | 
Indexes:
    "schedule_pkey" PRIMARY KEY, btree (scheduleid)
Referenced by:
    TABLE "schedulestudent" CONSTRAINT "schedulestudent_scheduleid_fkey" FOREIGN KEY (scheduleid) REFERENCES schedule(scheduleid)


            Table "public.schedulestudent"
   Column   |  Type   | Collation | Nullable | Default 
------------+---------+-----------+----------+---------
 scheduleid | integer |           | not null | 
 studentid  | integer |           | not null | 
Indexes:
    "schedulestudent_pkey" PRIMARY KEY, btree (scheduleid, studentid)
Foreign-key constraints:
    "schedulestudent_scheduleid_fkey" FOREIGN KEY (scheduleid) REFERENCES schedule(scheduleid)
    "schedulestudent_studentid_fkey" FOREIGN KEY (studentid) REFERENCES student(studentid)


                                          Table "public.chat"
   Column   |            Type             | Collation | Nullable |               Default                
------------+-----------------------------+-----------+----------+--------------------------------------
 chatid     | integer                     |           | not null | nextval('chat_chatid_seq'::regclass)
 senderid   | integer                     |           |          | 
 receiverid | integer                     |           |          | 
 message    | text                        |           |          | 
 timestamp  | timestamp without time zone |           |          | 
 image      | bytea                       |           |          | 
Indexes:
    "chat_pkey" PRIMARY KEY, btree (chatid)


                                   Table "public.guardianselection"
   Column    |  Type   | Collation | Nullable |                        Default                         
-------------+---------+-----------+----------+--------------------------------------------------------
 selectionid | integer |           | not null | nextval('guardianselection_selectionid_seq'::regclass)
 guardianid  | integer |           |          | 
 studentid   | integer |           |          | 
Indexes:
    "guardianselection_pkey" PRIMARY KEY, btree (selectionid)
Foreign-key constraints:
    "guardianselection_guardianid_fkey" FOREIGN KEY (guardianid) REFERENCES users(userid)
    "guardianselection_studentid_fkey" FOREIGN KEY (studentid) REFERENCES student(studentid)

```

<br> 

- **ER 다이어그램**

![ERdiagram](https://github.com/PNU-CESKids/KinderHub/assets/98088494/c6b13c36-1e1c-45b6-828f-86cde40331b5)


