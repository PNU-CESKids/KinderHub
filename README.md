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
4. 설치 및 사용법

## 프로젝트 소개

이 프로젝트는 유치원 원아들의 정보 체계 관리, 효과적인 일정 관리, 학부모-교사 간의 개별 소통 채널 제공, 식단표 확인, 안심 하원 서비스 도입, 게시판 질문과 답변 기능, 그리고 중요한 알림 서비스를 통해 학부모와 교사 간의 원활한 의사 소통과 안전한 유치원 학습 환경을 제공한다.

## 팀 소개
| 이름 | 김윤하(https://github.com/xdbsgk) | 구지원(https://github.com/kUZEEwon) |
|:------:|:----------:|:----------:|
|  | <img src="https://github.com/xdbsgk.png" width="200"> | <img src="https://github.com/kUZEEwon.png" width="200"> |
| 개발 내용 |  |  |


## 파일 구조
```
📦KinderHub
.
├── README.md
├── 📂WEB
│   ├── 📂__pycache__
│   │   ├── test_all.cpython-310.pyc
│   │   └── test_all.cpython-311.pyc
│   ├── app.py
│   ├── 📂templates
│   │   ├── board.html
│   │   ├── dashboard.html
│   │   ├── error.html
│   │   ├── guardianselection.html
│   │   ├── index.html
│   │   ├── info.html
│   │   ├── insert_chat.html
│   │   ├── login.html
│   │   ├── meal.html
│   │   ├── new_free_board.html
│   │   ├── notification.html
│   │   ├── post_detail.html
│   │   ├── registering.html
│   │   ├── schedule.html
│   │   ├── student_registering.html
│   │   └── write_notification.html
│   └── test_all.py
├── 📂보고서
└── 📂회의록
```

## 설치 및 사용법

## 데이터베이스 연결 및 각 테이블 초기 설정

### 1. Create New Database

- 데이터베이스 강의에서 사용한 기존의 ts_db2023의 TABLESPACE에 새로운 DATABASE를 생성해준다.
    
    ```sql
    postgres=# CREATE DATABASE termkk OWNER db2023 TABLESPACE ts_db2023;
    CREATE DATABASE
    ```
    

### 2. 테스트에 필요한 테이블 및 데이터 추가

- **termkk_backup.sql**을 다운받고, 다음과 같은 명령어를 실행시켜 데이터베이스의 구조와 데이터를 저장시킨다.
    
    ```sql
    psql -U db2023 -h localhost -d termkk < termkk_backup.sql
    ```
