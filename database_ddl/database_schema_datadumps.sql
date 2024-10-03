create schema accp ;
-- Insert test data for Participants
drop table accp.dim_participant cascade;
CREATE TABLE accp.dim_participant (
  ParticipantID VARCHAR(255) PRIMARY KEY,
  Telegram_chatid BIGINT,
  Username VARCHAR(255),
  Email VARCHAR(255),
  Created_dt TIMESTAMP,
  last_login_dt TIMESTAMP
);
INSERT INTO accp.dim_participant (ParticipantID, Telegram_chatid, Username, Email, Created_dt, last_login_dt)
VALUES
  ('1', 23,'Participant1', 'participant1@example.com', '2023-01-01', '2023-11-23'),
  ('2', 43,'Participant2', 'participant2@example.com', '2023-01-02', '2023-11-23'),
  ('3', 456,'Participant3', 'participant3@example.com', '2023-01-03', '2023-11-23'),
  ('4', 6261265168,'Lan', 'lan@example.com', '2023-01-03', '2023-11-23'),

-- Insert test data for dim_quiz_multiple
CREATE TABLE accp.dim_quiz_multiple (
  QuizID INT PRIMARY KEY,
  Quiztopic VARCHAR(255),
  Quizdifficulty INT,
  Quizlevel VARCHAR(255)
);
INSERT INTO accp.dim_quiz_multiple (QuizID, Quiztopic, Quizdifficulty, Quizlevel)
VALUES
  (1, 'English', 1, 'beginners'),
  (2, 'English', 2, 'intermediate'),
  (3, 'Math', 2, 'intermediate'),
  (4, 'Math', 3, 'advanced'),
  (5, 'AWS Certified Solutions Architect Associate', 1, 'Availablity & Scalability')
  ;

-- Insert test data for Questions TODO: add marks
CREATE TABLE accp.dim_question (
  QuestionID INT PRIMARY KEY,
  QuizID INT REFERENCES accp.dim_quiz_multiple(QuizID),
  context VARCHAR(255),
  QuizHasMultipleAnswers BOOLEAN
);
INSERT INTO accp.dim_question (QuestionID, QuizID, context, QuizHasMultipleAnswers) -- add marks
VALUES
  (1, 1, 'Question 1 for English - beginners', FALSE),
  (2, 1, 'Question 2 for English - beginners', FALSE),
  (3, 1, 'Question 3 for English - beginners', FALSE),
  (4, 2, 'Question 1 for English - intermediate', FALSE),
  (5, 2, 'Question 2 for English - intermediate', FALSE),
  (6, 2, 'Question 3 for English - intermediate', FALSE),
  (7, 3, 'Question 1 for Math - intermediate', FALSE),
  (8, 3, 'Question 2 for Math - intermediate', FALSE),
  (9, 3, 'Question 3 for Math - intermediate', FALSE),
  (10, 4, 'Question 1 for Math - advanced', FALSE),
  (11, 4, 'Question 2 for Math - advanced', FALSE),
  (12, 4, 'Question 3 for Math - advanced', FALSE),
  (13, 5, 'What types of traffic can AWS Application Load Balancer (ALB) handle?', FALSE),
  (14, 5, 'Which of the following features is supported by AWS ALB for routing decisions?', FALSE);

-- Insert test data for Options
CREATE TABLE accp.dim_option (
  OptionID INT PRIMARY KEY,
  QuestionID INT REFERENCES accp.dim_question(QuestionID),
  context VARCHAR(255),
  IsCorrect BOOLEAN,
  option_no int,
  quiz_question_option varchar(100) UNIQUE
);
INSERT INTO accp.dim_option (OptionID, QuestionID, context, IsCorrect, option_no, quiz_question_option)
VALUES
-- Options for English - beginners
(1,	1,	'Option 1 for Question 1',	TRUE,	1,	'1-1-1'),
(2,	1,	'Option 2 for Question 1',	FALSE,	2,	'1-1-2'),
(3,	1,	'Option 3 for Question 1',	FALSE,	3,	'1-1-3'),
(4,	1,	'Option 4 for Question 1',	FALSE,	4,	'1-1-4'),
(5,	2,	'Option 1 for Question 2',	TRUE,	1,	'1-2-1'),
(6,	2,	'Option 2 for Question 2',	FALSE,	2,	'1-2-2'),
(7,	2,	'Option 3 for Question 2',	FALSE,	3,	'1-2-3'),
(8,	2,	'Option 4 for Question 2',	FALSE,	4,	'1-2-4'),
(9,	3,	'Option 1 for Question 3',	TRUE,	1,	'1-3-1'),
(10,	3,	'Option 2 for Question 3',	FALSE,	2,	'1-3-2'),
(11,	3,	'Option 3 for Question 3',	FALSE,	3,	'1-3-3'),
(12,	3,	'Option 4 for Question 3',	FALSE,	4,	'1-3-4'),
-- Options for English - intermediate
(13,	4,	'Option 1 for Question 1',	TRUE,	1,	'2-4-1'),
(14,	4,	'Option 2 for Question 1',	FALSE,	2,	'2-4-2'),
(15,	4,	'Option 3 for Question 1',	FALSE,	3,	'2-4-3'),
(16,	4,	'Option 4 for Question 1',	FALSE,	4,	'2-4-4'),
(17,	5,	'Option 1 for Question 2',	TRUE,	1,	'2-5-1'),
(18,	5,	'Option 2 for Question 2',	FALSE,	2,	'2-5-2'),
(19,	5,	'Option 3 for Question 2',	FALSE,	3,	'2-5-3'),
(20,	5,	'Option 4 for Question 2',	FALSE,	4,	'2-5-4'),
(21,	6,	'Option 1 for Question 3',	TRUE,	1,	'2-6-1'),
(22,	6,	'Option 2 for Question 3',	FALSE,	2,	'2-6-2'),
(23,	6,	'Option 3 for Question 3',	FALSE,	3,	'2-6-3'),
(24,	6,	'Option 4 for Question 3',	FALSE,	4,	'2-6-4'),
-- Options for Math - intermediate
(25,	7,	'Option 1 for Question 1',	TRUE,	1,	'3-7-1'),
(26,	7,	'Option 2 for Question 1',	FALSE,	2,	'3-7-2'),
(27,	7,	'Option 3 for Question 1',	FALSE,	3,	'3-7-3'),
(28,	7,	'Option 4 for Question 1',	FALSE,	4,	'3-7-4'),
(29,	8,	'Option 1 for Question 2',	TRUE,	1,	'3-8-1'),
(30,	8,	'Option 2 for Question 2',	FALSE,	2,	'3-8-2'),
(31,	8,	'Option 3 for Question 2',	FALSE,	3,	'3-8-3'),
(32,	8,	'Option 4 for Question 2',	FALSE,	4,	'3-8-4'),
(33,	9,	'Option 1 for Question 3',	TRUE,	1,	'3-9-1'),
(34,	9,	'Option 2 for Question 3',	FALSE,	2,	'3-9-2'),
(35,	9,	'Option 3 for Question 3',	FALSE,	3,	'3-9-3'),
(36,	9,	'Option 4 for Question 3',	FALSE,	4,	'3-9-4'),
-- Options for Math - advanced
(37,	10,	'Option 1 for Question 1',	TRUE,	1,	'4-10-1'),
(38,	10,	'Option 2 for Question 1',	FALSE,	2,	'4-10-2'),
(39,	10,	'Option 3 for Question 1',	FALSE,	3,	'4-10-3'),
(40,	10,	'Option 4 for Question 1',	FALSE,	4,	'4-10-4'),
(41,	11,	'Option 1 for Question 2',	TRUE,	1,	'4-11-1'),
(42,	11,	'Option 2 for Question 2',	FALSE,	2,	'4-11-2'),
(43,	11,	'Option 3 for Question 2',	FALSE,	3,	'4-11-3'),
(44,	11,	'Option 4 for Question 2',	FALSE,	4,	'4-11-4'),
(45,	12,	'Option 1 for Question 3',	TRUE,	1,	'4-12-1'),
(46,	12,	'Option 2 for Question 3',	FALSE,	2,	'4-12-2'),
(47,	12,	'Option 3 for Question 3',	FALSE,	3,	'4-12-3'),
(48,	12,	'Option 4 for Question 3',	FALSE,	4,	'4-12-4'),
-- options for aws
(49, 13, 'HTTP/2 and WebSockets', TRUE, 1, '5-13-1'),
(50, 13, 'FTP and SFTP', FALSE, 2, '5-13-2'),
(51, 13, 'SMTP and POP3', FALSE, 3, '5-13-3'),
(52, 13, 'MQTT and AMQP', FALSE, 4, '5-13-4'),
(53, 14, 'CPU usage of target instances', FALSE, 1, '5-14-1'),
(54, 14, 'URL path-based routing', TRUE, 2, '5-14-2'),
(55, 14, 'The geographical location of the user', FALSE, 3, '5-14-3'),
(56, 14, 'The age of the HTTP request', FALSE, 4, '5-14-4');

-- Insert test data for Answers
--drop table answer;
CREATE TABLE accp.fact_answer (
  AnswerID INT PRIMARY KEY,
  ParticipantID VARCHAR(255) REFERENCES accp.dim_participant(ParticipantID),
  QuizID INT REFERENCES accp.dim_quiz_multiple(QuizID),
  QuestionID INT REFERENCES accp.dim_question(QuestionID),
  quiz_question_option varchar REFERENCES accp.dim_option(quiz_question_option),
  record_answer_dt TIMESTAMP,
  idle_seconds  int
);
INSERT INTO accp.fact_answer (AnswerID, ParticipantID, QuizID, QuestionID, quiz_question_option, record_answer_dt, idle_seconds)
VALUES
  (1, 1, 1, 1, '1-1-2', '2023-11-01', 23 ),
  (2, 1, 1, 2, '1-2-1', '2023-11-05', 3 ),
  (3, 1, 1, 3, '1-3-2', '2023-11-03', 1 ),
  (4, 1, 2, 4, '2-4-2', '2023-11-01', 2 ),
  (5, 1, 2, 5, '2-5-3', '2023-11-05', 4 ),
  (6, 1, 2, 6, '2-6-1', '2023-11-10', 3 ),
  (7, 1, 3, 7, '3-7-1', '2023-11-10', 4 ),
  (8, 1, 3, 8, '3-8-3', '2023-11-17', 27),
  (9, 1, 3, 9, '3-9-4', '2023-11-03', 1 ),
  (10, 1, 4, 10, '4-10-2', '2023-11-10',  7),
  (11, 1, 4, 11, '4-11-1', '2023-11-07', 4 ),
  (12, 1, 4, 12, '4-12-4', '2023-11-01', 2 ),
  (13, 2, 1, 1, '1-1-1', '2023-11-05',  7),
  (14, 2, 1, 2, '1-2-1', '2023-11-03',  7),
  (15, 2, 1, 3, '1-3-3', '2023-11-10', 24 ),
  (16, 2, 2, 4, '2-4-1', '2023-11-03', 1 ),
  (17, 2, 2, 5, '2-5-4', '2023-11-01', 3 ),
  (18, 2, 2, 6, '2-6-4', '2023-11-05', 2 ),
  (19, 2, 3, 7, '3-7-1', '2023-11-07', 14 ),
  (20, 2, 3, 8, '3-8-1', '2023-11-01', 4 ),
  (21, 2, 3, 9, '3-9-4', '2023-11-10', 2 ),
  (22, 2, 4, 10, '4-10-1', '2023-11-05', 4 ),
  (23, 2, 4, 11, '4-11-4', '2023-11-07', 34 ),
  (24, 2, 4, 12, '4-12-3', '2023-11-08' ,7);


CREATE TABLE accp.fact_quizoption_selected (
  QuizSelectedID INT PRIMARY KEY,
  ParticipantID VARCHAR(255),
  QuizID INT REFERENCES accp.dim_quiz_multiple(QuizID),
  selected_quiz_ts TIMESTAMP
);


CREATE TABLE accp.fact_has_accessright_topic (
    ID INT PRIMARY KEY,
    quizID INT REFERENCES accp.dim_quiz_multiple(QuizID),
    participantID VARCHAR(255) REFERENCES accp.dim_participant(participantid),
    valid_from TIMESTAMP,
    valid_until TIMESTAMP
);

INSERT INTO accp.fact_has_accessright_topic (ID, quizID, participantID, valid_from, valid_until )
VALUES
    (1, 1, 1, '2023-11-08', '2024-11-08'),
    (2, 2, 1, '2023-11-08', '2024-11-08'),
    (3, 3, 1, '2023-11-08', '2024-11-08'),
    (4, 5, 2, '2023-11-08', '2024-11-08'),
    (5, 1367, 2, '2023-11-08', '2024-11-08'),
    (6, 8941, 2, '2023-11-08', '2024-11-08'),
    (7, 8941, 4, '2023-11-08', '2024-11-08'),
    (8, 1367, 4, '2023-11-08', '2024-11-08'),
    (9, 630, 4, '2023-11-08', '2024-11-08'),
    (10, 9651, 4, '2023-11-08', '2024-11-08'),
    (11, 589, 4, '2023-11-08', '2024-11-08'),
    (12, 7471, 4, '2023-11-08', '2024-11-08'),
    (13, 8941, 4, '2023-11-08', '2024-11-08'),
    (14, 8323, 4, '2023-11-08', '2024-11-08'),
    (15, 2539, 4, '2023-11-08', '2024-11-08'),
    (16, 7782, 4, '2023-11-08', '2024-11-08'),
    (17, 8216, 4, '2023-11-08', '2024-11-08'),
    (18, 7345, 4, '2023-11-08', '2024-11-08'),
    (19, 5010, 4, '2023-11-08', '2024-11-08'),
    (20, 1583, 4, '2023-11-08', '2024-11-08'),
    (21, 723, 4, '2023-11-08', '2024-11-08'),
    (22, 5218, 4, '2023-11-08', '2024-11-08'),
    (23, 3366, 4, '2023-11-08', '2024-11-08'),
    (24, 8725, 4, '2023-11-08', '2024-11-08'),
    (25, 850, 4, '2023-11-08', '2024-11-08'),
    (26, 8430, 4, '2023-11-08', '2024-11-08')