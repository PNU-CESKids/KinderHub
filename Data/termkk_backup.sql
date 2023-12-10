--
-- PostgreSQL database dump
--

-- Dumped from database version 15.4
-- Dumped by pg_dump version 15.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: role_enum; Type: TYPE; Schema: public; Owner: db2023
--

CREATE TYPE public.role_enum AS ENUM (
    'Principal',
    'Teacher',
    'Student',
    'Guardian',
    'OtherSchoolStaff',
    'StudentsFamily'
);


ALTER TYPE public.role_enum OWNER TO db2023;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: chat; Type: TABLE; Schema: public; Owner: db2023
--

CREATE TABLE public.chat (
    chatid integer NOT NULL,
    senderid integer,
    receiverid integer,
    message text,
    "timestamp" timestamp without time zone,
    image bytea
);


ALTER TABLE public.chat OWNER TO db2023;

--
-- Name: chat_chatid_seq; Type: SEQUENCE; Schema: public; Owner: db2023
--

CREATE SEQUENCE public.chat_chatid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.chat_chatid_seq OWNER TO db2023;

--
-- Name: chat_chatid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: db2023
--

ALTER SEQUENCE public.chat_chatid_seq OWNED BY public.chat.chatid;


--
-- Name: comment; Type: TABLE; Schema: public; Owner: db2023
--

CREATE TABLE public.comment (
    commentid integer NOT NULL,
    postid integer,
    commenterid integer,
    commentcontent text,
    "timestamp" timestamp without time zone
);


ALTER TABLE public.comment OWNER TO db2023;

--
-- Name: comment_commentid_seq; Type: SEQUENCE; Schema: public; Owner: db2023
--

CREATE SEQUENCE public.comment_commentid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.comment_commentid_seq OWNER TO db2023;

--
-- Name: comment_commentid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: db2023
--

ALTER SEQUENCE public.comment_commentid_seq OWNED BY public.comment.commentid;


--
-- Name: freeboardqa; Type: TABLE; Schema: public; Owner: db2023
--

CREATE TABLE public.freeboardqa (
    postid integer NOT NULL,
    posterid integer,
    title character varying(100),
    content text,
    "timestamp" timestamp without time zone,
    image bytea
);


ALTER TABLE public.freeboardqa OWNER TO db2023;

--
-- Name: freeboardqa_postid_seq; Type: SEQUENCE; Schema: public; Owner: db2023
--

CREATE SEQUENCE public.freeboardqa_postid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.freeboardqa_postid_seq OWNER TO db2023;

--
-- Name: freeboardqa_postid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: db2023
--

ALTER SEQUENCE public.freeboardqa_postid_seq OWNED BY public.freeboardqa.postid;


--
-- Name: guardianselection; Type: TABLE; Schema: public; Owner: db2023
--

CREATE TABLE public.guardianselection (
    selectionid integer NOT NULL,
    guardianid integer,
    studentid integer
);


ALTER TABLE public.guardianselection OWNER TO db2023;

--
-- Name: guardianselection_selectionid_seq; Type: SEQUENCE; Schema: public; Owner: db2023
--

CREATE SEQUENCE public.guardianselection_selectionid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.guardianselection_selectionid_seq OWNER TO db2023;

--
-- Name: guardianselection_selectionid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: db2023
--

ALTER SEQUENCE public.guardianselection_selectionid_seq OWNED BY public.guardianselection.selectionid;


--
-- Name: mealplan; Type: TABLE; Schema: public; Owner: db2023
--

CREATE TABLE public.mealplan (
    planid integer NOT NULL,
    date date,
    meal1 text,
    meal2 text,
    snack text
);


ALTER TABLE public.mealplan OWNER TO db2023;

--
-- Name: mealplan_planid_seq; Type: SEQUENCE; Schema: public; Owner: db2023
--

CREATE SEQUENCE public.mealplan_planid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mealplan_planid_seq OWNER TO db2023;

--
-- Name: mealplan_planid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: db2023
--

ALTER SEQUENCE public.mealplan_planid_seq OWNED BY public.mealplan.planid;


--
-- Name: schedule; Type: TABLE; Schema: public; Owner: db2023
--

CREATE TABLE public.schedule (
    scheduleid integer NOT NULL,
    eventtype character varying(200),
    date date,
    "time" time without time zone,
    description text,
    scheduleimg bytea
);


ALTER TABLE public.schedule OWNER TO db2023;

--
-- Name: schedule_scheduleid_seq; Type: SEQUENCE; Schema: public; Owner: db2023
--

CREATE SEQUENCE public.schedule_scheduleid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.schedule_scheduleid_seq OWNER TO db2023;

--
-- Name: schedule_scheduleid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: db2023
--

ALTER SEQUENCE public.schedule_scheduleid_seq OWNED BY public.schedule.scheduleid;


--
-- Name: schedulestudent; Type: TABLE; Schema: public; Owner: db2023
--

CREATE TABLE public.schedulestudent (
    scheduleid integer NOT NULL,
    studentid integer NOT NULL
);


ALTER TABLE public.schedulestudent OWNER TO db2023;

--
-- Name: student; Type: TABLE; Schema: public; Owner: db2023
--

CREATE TABLE public.student (
    studentid integer NOT NULL,
    studentname character varying(20),
    classname character(1),
    birthdate date,
    attendance integer,
    healthstatus boolean,
    address character varying(100),
    teacherid integer
);


ALTER TABLE public.student OWNER TO db2023;

--
-- Name: student_studentid_seq; Type: SEQUENCE; Schema: public; Owner: db2023
--

CREATE SEQUENCE public.student_studentid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.student_studentid_seq OWNER TO db2023;

--
-- Name: student_studentid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: db2023
--

ALTER SEQUENCE public.student_studentid_seq OWNED BY public.student.studentid;


--
-- Name: users; Type: TABLE; Schema: public; Owner: db2023
--

CREATE TABLE public.users (
    userid integer NOT NULL,
    username character varying(20),
    userrole public.role_enum,
    studentid integer,
    userpassword character varying(255),
    useremail character varying(255),
    teacherid integer,
    CONSTRAINT valid_userrole CHECK ((userrole = ANY (ARRAY['Principal'::public.role_enum, 'Teacher'::public.role_enum, 'Student'::public.role_enum, 'Guardian'::public.role_enum, 'OtherSchoolStaff'::public.role_enum, 'StudentsFamily'::public.role_enum])))
);


ALTER TABLE public.users OWNER TO db2023;

--
-- Name: users_userid_seq; Type: SEQUENCE; Schema: public; Owner: db2023
--

CREATE SEQUENCE public.users_userid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_userid_seq OWNER TO db2023;

--
-- Name: users_userid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: db2023
--

ALTER SEQUENCE public.users_userid_seq OWNED BY public.users.userid;


--
-- Name: chat chatid; Type: DEFAULT; Schema: public; Owner: db2023
--

ALTER TABLE ONLY public.chat ALTER COLUMN chatid SET DEFAULT nextval('public.chat_chatid_seq'::regclass);


--
-- Name: comment commentid; Type: DEFAULT; Schema: public; Owner: db2023
--

ALTER TABLE ONLY public.comment ALTER COLUMN commentid SET DEFAULT nextval('public.comment_commentid_seq'::regclass);


--
-- Name: freeboardqa postid; Type: DEFAULT; Schema: public; Owner: db2023
--

ALTER TABLE ONLY public.freeboardqa ALTER COLUMN postid SET DEFAULT nextval('public.freeboardqa_postid_seq'::regclass);


--
-- Name: guardianselection selectionid; Type: DEFAULT; Schema: public; Owner: db2023
--

ALTER TABLE ONLY public.guardianselection ALTER COLUMN selectionid SET DEFAULT nextval('public.guardianselection_selectionid_seq'::regclass);


--
-- Name: mealplan planid; Type: DEFAULT; Schema: public; Owner: db2023
--

ALTER TABLE ONLY public.mealplan ALTER COLUMN planid SET DEFAULT nextval('public.mealplan_planid_seq'::regclass);


--
-- Name: schedule scheduleid; Type: DEFAULT; Schema: public; Owner: db2023
--

ALTER TABLE ONLY public.schedule ALTER COLUMN scheduleid SET DEFAULT nextval('public.schedule_scheduleid_seq'::regclass);


--
-- Name: student studentid; Type: DEFAULT; Schema: public; Owner: db2023
--

ALTER TABLE ONLY public.student ALTER COLUMN studentid SET DEFAULT nextval('public.student_studentid_seq'::regclass);


--
-- Name: users userid; Type: DEFAULT; Schema: public; Owner: db2023
--

ALTER TABLE ONLY public.users ALTER COLUMN userid SET DEFAULT nextval('public.users_userid_seq'::regclass);


--
-- Data for Name: chat; Type: TABLE DATA; Schema: public; Owner: db2023
--

COPY public.chat (chatid, senderid, receiverid, message, "timestamp", image) FROM stdin;
1	1	2	Hello, how is John doing?	2023-11-16 10:30:00	\N
2	2	1	Hi, Jane is doing well!	2023-11-16 11:00:00	\N
3	1	2	Hi, are you doing well for everything?	2023-11-19 16:58:30.709065	\N
4	1	3	Nice !!!	2023-11-19 17:12:05.030035	\N
5	1	2	Thank you.	2023-11-19 17:17:30.530193	\N
6	2	1	Hello!	2023-12-01 12:00:00	\N
7	2	2	Hi there!	2023-12-01 12:05:00	\N
8	2	3	How are you?	2023-12-01 12:10:00	\N
9	7	4	I am good!	2023-12-01 12:15:00	\N
10	7	5	\N	2023-12-01 12:20:00	\\xdeadbeef
11	7	6	Another message	2023-12-01 12:25:00	\N
12	3	2	배고파.	2023-12-08 00:45:14.905756	\N
\.


--
-- Data for Name: comment; Type: TABLE DATA; Schema: public; Owner: db2023
--

COPY public.comment (commentid, postid, commenterid, commentcontent, "timestamp") FROM stdin;
19	6	3	Nice work on the second post!	2023-11-28 16:20:23.225879
20	7	2	Thanks for sharing your thoughts.	2023-11-28 16:20:23.225879
21	9	3	graduate from이 옳은 표현입니다. (by ham)	2023-12-08 00:04:32.416452
22	6	4	바보야	2023-12-08 00:13:52.869121
\.


--
-- Data for Name: freeboardqa; Type: TABLE DATA; Schema: public; Owner: db2023
--

COPY public.freeboardqa (postid, posterid, title, content, "timestamp", image) FROM stdin;
6	2	QHomework	Can you provide more details about the history homework?	2023-11-15 18:10:00	\N
7	2	School Event	Reminder: School event next week!	2023-11-16 09:30:00	\N
9	9	I want to graduate this school ..	realro	2023-12-07 21:49:15.52224	\N
10	3	123	ㄴㅇㄹ	2023-12-07 23:14:57.465386	\N
11	4	나는 집에 가고 싶다	왜냐하면 집에 가고 싶기 때문에다. \r\n나는 집에 가고 싶다()	2023-12-08 00:15:27.335583	\N
\.


--
-- Data for Name: guardianselection; Type: TABLE DATA; Schema: public; Owner: db2023
--

COPY public.guardianselection (selectionid, guardianid, studentid) FROM stdin;
3	1	2
9	2	1
10	8	4
11	11	3
12	12	7
\.


--
-- Data for Name: mealplan; Type: TABLE DATA; Schema: public; Owner: db2023
--

COPY public.mealplan (planid, date, meal1, meal2, snack) FROM stdin;
1	2023-11-16	Chicken Salad	Pasta with Tomato Sauce	Fruit Salad
2	2023-11-17	Grilled Salmon	Vegetable Stir-Fry	Yogurt with Granola
3	2023-11-18	Steak with Roasted Vegetables	Shrimp Pasta	Mixed Nuts
5	2023-11-20	carry	rice	tomato juice
4	2023-11-19	rulurala	yellow banana	kaka
6	2023-12-12	iiii	qqqq	wwww
7	2023-11-29	Toast	Egg	Strawberry
8	2023-11-30	Rice	Egg	Kimchi
25	2023-12-01	soba	salad	orange
26	2023-12-02	라면	김치	밥
27	2023-12-03	국밥	깍두기	토마토
28	2023-12-07	밥	빵	면
\.


--
-- Data for Name: schedule; Type: TABLE DATA; Schema: public; Owner: db2023
--

COPY public.schedule (scheduleid, eventtype, date, "time", description, scheduleimg) FROM stdin;
1	Meeting	2023-11-20	14:00:00	Parent-Teacher Conference	\N
2	Field Trip	2023-12-05	09:00:00	Visit to the Science Museum	\N
3	Playing	2023-12-10	10:00:00	\N	\N
4	Party	2023-12-25	12:00:00	\N	\N
5	Sleep	2024-01-01	00:11:00	\N	\N
8	식샤	2023-12-06	11:30:00	아그들아 ~ 식샤를 합시데이 ♥	\N
\.


--
-- Data for Name: schedulestudent; Type: TABLE DATA; Schema: public; Owner: db2023
--

COPY public.schedulestudent (scheduleid, studentid) FROM stdin;
1	2
2	3
3	1
3	2
4	1
4	2
5	1
8	1
8	2
8	3
8	4
8	5
8	6
8	7
\.


--
-- Data for Name: student; Type: TABLE DATA; Schema: public; Owner: db2023
--

COPY public.student (studentid, studentname, classname, birthdate, attendance, healthstatus, address, teacherid) FROM stdin;
1	John Doe	A	2000-01-15	0	f	Jingu, 123456	2
2	Jane Smith	B	2001-03-20	95	t	456 Oak St	2
3	Bob Johnson	A	2002-05-10	88	f	789 Pine St	2
4	New Student	C	2003-08-25	75	t	New Address	13
5	나학생	A	2022-03-01	75	t	부산시 금정구 부산대학로	13
6	김윤하	A	2000-01-29	100	f	부산	13
7	카즈하	B	2022-09-08	90	f	일본	13
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: db2023
--

COPY public.users (userid, username, userrole, studentid, userpassword, useremail, teacherid) FROM stdin;
1	taeri	StudentsFamily	2	pbkdf2:sha256:600000$mxayXhFyJLYYTFQU$7022899c8b12672c87a8ffb71dc527490f45c058a0d963c362913001001d244f	taeri@example.com	\N
3	guardian1	Guardian	2	pbkdf2:sha256:600000$vl9cqHpCPeeOC0h7$619a5e5251c3953fbb311be29b14863e213710ca3c01f25b0b4d90eb2daf08f4	guardian1@example.com	\N
4	yunha	StudentsFamily	2	pbkdf2:sha256:600000$x4V7rkTMt8SmzfMP$536dbc96c87572a9000b57849933adb8f34f6806302b2100f687d93bd153c8ef	yunha@example.com	\N
5	boae	StudentsFamily	2	pbkdf2:sha256:600000$RpVUYXt96T6MTBMh$3db85f38e843cfd74cd9198b552e343039cc7de245dec173ecb6a58d5117df00	boae@xx.com	\N
6	babo	OtherSchoolStaff	1	pbkdf2:sha256:600000$nmIgKL2Ly37lMNt6$6830a7296620d38b80b1131f1799ed81408cdc9bb44f8649900a89136bec9f50	babo@example.com	\N
8	바보멍청이	StudentsFamily	4	pbkdf2:sha256:600000$RYJXQOjDwkVY7X44$9f769351eaa1ca6b782a1058e24670777ba6f18813da90f6875c032536c9aa8f	bbang@example.com	\N
9	나원장	Principal	\N	pbkdf2:sha256:600000$HADmSLWc1e7nqsna$bd55d19a89d85813dc4a6f62e78695505dde9feebc6dda64abba58143ecc0d4b	principal@example.com	\N
10	3번맘	Guardian	3	pbkdf2:sha256:600000$cDR9GwQtJbiuPEdL$b623e1c6c048b92cc7530d4d159d88368b7107df593ae3397979abca4153c87d	three@example.com	\N
11	3번대디	StudentsFamily	3	pbkdf2:sha256:600000$BI4UTnZyyD8BXqgz$883867ca8b2d4a5ad31402388cc95e2ab98cdeb32fd0e7439899adaec1ca8100	threef@exmaple.com	\N
2	teacher1	Teacher	1	pbkdf2:sha256:600000$9DJL7UiQtFcbvbDB$687b536877e46aa5b98ca455110fa30e52d67ec12705f80543d4a4b34d652cef	teacher1@example.com	2
12	즈하맘	Guardian	7	pbkdf2:sha256:600000$3GyT0SnwRppIQOoY$385e55bbed6e6af70490ab03a917663351eaf92901f249399a8ce6bc967af05f	zuhamom@example.com	\N
14	김라라	OtherSchoolStaff	\N	pbkdf2:sha256:600000$vecxO8GCS5SpjndA$dd2cf6b346da4474a52a9005b89dbb1d0391918be0c2571d32b7ca03206b89ff	rara@example.com	\N
15	뽀로로	StudentsFamily	6	pbkdf2:sha256:600000$alxZrJB5BMB8fTfr$5efd8c5698024f95d0c2e41df57630a9f8f95099e1bf4ace06a0c8beed7bea04	pororo@example.com	\N
13	Yana	Teacher	\N	pbkdf2:sha256:600000$4cy3N3KTxEAozIvf$47de2d7fdf142a656af93230f60d87c7e9c89d25eb6942b31c63c4cd32bec9bc	yana@example.com	13
\.


--
-- Name: chat_chatid_seq; Type: SEQUENCE SET; Schema: public; Owner: db2023
--

SELECT pg_catalog.setval('public.chat_chatid_seq', 12, true);


--
-- Name: comment_commentid_seq; Type: SEQUENCE SET; Schema: public; Owner: db2023
--

SELECT pg_catalog.setval('public.comment_commentid_seq', 22, true);


--
-- Name: freeboardqa_postid_seq; Type: SEQUENCE SET; Schema: public; Owner: db2023
--

SELECT pg_catalog.setval('public.freeboardqa_postid_seq', 11, true);


--
-- Name: guardianselection_selectionid_seq; Type: SEQUENCE SET; Schema: public; Owner: db2023
--

SELECT pg_catalog.setval('public.guardianselection_selectionid_seq', 12, true);


--
-- Name: mealplan_planid_seq; Type: SEQUENCE SET; Schema: public; Owner: db2023
--

SELECT pg_catalog.setval('public.mealplan_planid_seq', 28, true);


--
-- Name: schedule_scheduleid_seq; Type: SEQUENCE SET; Schema: public; Owner: db2023
--

SELECT pg_catalog.setval('public.schedule_scheduleid_seq', 8, true);


--
-- Name: student_studentid_seq; Type: SEQUENCE SET; Schema: public; Owner: db2023
--

SELECT pg_catalog.setval('public.student_studentid_seq', 7, true);


--
-- Name: users_userid_seq; Type: SEQUENCE SET; Schema: public; Owner: db2023
--

SELECT pg_catalog.setval('public.users_userid_seq', 15, true);


--
-- Name: chat chat_pkey; Type: CONSTRAINT; Schema: public; Owner: db2023
--

ALTER TABLE ONLY public.chat
    ADD CONSTRAINT chat_pkey PRIMARY KEY (chatid);


--
-- Name: comment comment_pkey; Type: CONSTRAINT; Schema: public; Owner: db2023
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT comment_pkey PRIMARY KEY (commentid);


--
-- Name: freeboardqa freeboardqa_pkey; Type: CONSTRAINT; Schema: public; Owner: db2023
--

ALTER TABLE ONLY public.freeboardqa
    ADD CONSTRAINT freeboardqa_pkey PRIMARY KEY (postid);


--
-- Name: guardianselection guardianselection_pkey; Type: CONSTRAINT; Schema: public; Owner: db2023
--

ALTER TABLE ONLY public.guardianselection
    ADD CONSTRAINT guardianselection_pkey PRIMARY KEY (selectionid);


--
-- Name: mealplan mealplan_pkey; Type: CONSTRAINT; Schema: public; Owner: db2023
--

ALTER TABLE ONLY public.mealplan
    ADD CONSTRAINT mealplan_pkey PRIMARY KEY (planid);


--
-- Name: schedule schedule_pkey; Type: CONSTRAINT; Schema: public; Owner: db2023
--

ALTER TABLE ONLY public.schedule
    ADD CONSTRAINT schedule_pkey PRIMARY KEY (scheduleid);


--
-- Name: schedulestudent schedulestudent_pkey; Type: CONSTRAINT; Schema: public; Owner: db2023
--

ALTER TABLE ONLY public.schedulestudent
    ADD CONSTRAINT schedulestudent_pkey PRIMARY KEY (scheduleid, studentid);


--
-- Name: student student_pkey; Type: CONSTRAINT; Schema: public; Owner: db2023
--

ALTER TABLE ONLY public.student
    ADD CONSTRAINT student_pkey PRIMARY KEY (studentid);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: db2023
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (userid);


--
-- Name: comment comment_commenterid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: db2023
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT comment_commenterid_fkey FOREIGN KEY (commenterid) REFERENCES public.users(userid);


--
-- Name: comment comment_postid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: db2023
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT comment_postid_fkey FOREIGN KEY (postid) REFERENCES public.freeboardqa(postid) ON DELETE CASCADE;


--
-- Name: student fk_teacher; Type: FK CONSTRAINT; Schema: public; Owner: db2023
--

ALTER TABLE ONLY public.student
    ADD CONSTRAINT fk_teacher FOREIGN KEY (teacherid) REFERENCES public.users(userid);


--
-- Name: freeboardqa freeboardqa_posterid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: db2023
--

ALTER TABLE ONLY public.freeboardqa
    ADD CONSTRAINT freeboardqa_posterid_fkey FOREIGN KEY (posterid) REFERENCES public.users(userid);


--
-- Name: guardianselection guardianselection_guardianid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: db2023
--

ALTER TABLE ONLY public.guardianselection
    ADD CONSTRAINT guardianselection_guardianid_fkey FOREIGN KEY (guardianid) REFERENCES public.users(userid);


--
-- Name: guardianselection guardianselection_studentid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: db2023
--

ALTER TABLE ONLY public.guardianselection
    ADD CONSTRAINT guardianselection_studentid_fkey FOREIGN KEY (studentid) REFERENCES public.student(studentid);


--
-- Name: schedulestudent schedulestudent_scheduleid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: db2023
--

ALTER TABLE ONLY public.schedulestudent
    ADD CONSTRAINT schedulestudent_scheduleid_fkey FOREIGN KEY (scheduleid) REFERENCES public.schedule(scheduleid);


--
-- Name: schedulestudent schedulestudent_studentid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: db2023
--

ALTER TABLE ONLY public.schedulestudent
    ADD CONSTRAINT schedulestudent_studentid_fkey FOREIGN KEY (studentid) REFERENCES public.student(studentid);


--
-- Name: student student_teacherid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: db2023
--

ALTER TABLE ONLY public.student
    ADD CONSTRAINT student_teacherid_fkey FOREIGN KEY (teacherid) REFERENCES public.users(userid);


--
-- Name: users users_studentid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: db2023
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_studentid_fkey FOREIGN KEY (studentid) REFERENCES public.student(studentid);


--
-- Name: users users_teacherid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: db2023
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_teacherid_fkey FOREIGN KEY (teacherid) REFERENCES public.users(userid);


--
-- PostgreSQL database dump complete
--

