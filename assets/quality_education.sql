CREATE DATABASE quality_education ;
USE quality_education;

CREATE TABLE student(
student_id INT PRIMARY KEY auto_increment UNIQUE,
student_name VARCHAR(30) UNIQUE NOT NULL,
student_email VARCHAR(50) UNIQUE NOT NULL,
student_birthday DATE,
phone VARCHAR(20) UNIQUE NOT NULL,
password VARCHAR(20) NOT NULL,
created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE teacher(
teacher_id INT PRIMARY KEY auto_increment UNIQUE,
teacher_name VARCHAR(30) UNIQUE NOT NULL,
teacher_email VARCHAR(50) UNIQUE NOT NULL,
teacher_birthday DATE,
phone VARCHAR(20) UNIQUE NOT NULL,
password VARCHAR(20) NOT NULL,
created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE announcement (
announcement_id INT PRIMARY KEY auto_increment UNIQUE,
teacher_id INT,
FOREIGN KEY (teacher_id) REFERENCES teacher(teacher_id),
announcement_desc TEXT NOT NULL,
created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
created_by VARCHAR (25) NOT NULL,
FOREIGN KEY (created_by) REFERENCES teacher(teacher_name)
);

CREATE TABLE course_subjects (
course_subject_id INT PRIMARY KEY auto_increment UNIQUE,
course_subject VARCHAR(25) NOT NULL,
created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE course (
course_id INT PRIMARY KEY auto_increment UNIQUE,
course_name VARCHAR(50) NOT NULL,
course_subject_id INT,
FOREIGN KEY (course_subject_id) REFERENCES course_subjects(course_subject_id),
course_description TEXT NOT NULL,
picture BLOB,
created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE teachers_course (
teachers_course_id INT PRIMARY KEY AUTO_INCREMENT,
teacher_id INT NOT NULL,
course_id INT NOT NULL,
created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (teacher_id) REFERENCES teacher(teacher_id),
FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE students_course (
students_course_id INT PRIMARY KEY AUTO_INCREMENT,
student_id INT NOT NULL,
course_id INT NOT NULL,
created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (student_id) REFERENCES student(student_id),
FOREIGN KEY (course_id) REFERENCES course(course_id)
);

SELECT * FROM course;

SELECT * FROM student;

ALTER TABLE student
ADD COLUMN picture BLOB;

ALTER TABLE teacher
ADD COLUMN picture BLOB;

ALTER TABLE course
ADD COLUMN course_grade ENUM("SD", "SMP", "SMA");

ALTER TABLE student ADD COLUMN role VARCHAR(20) DEFAULT 'student' NOT NULL;

ALTER TABLE teacher ADD COLUMN role VARCHAR(20) DEFAULT 'Teacher' NOT NULL;

ALTER TABLE student DROP COLUMN password;
ALTER TABLE student ADD COLUMN password VARCHAR(255) NOT NULL;

ALTER TABLE teacher DROP COLUMN password;
ALTER TABLE teacher ADD COLUMN password VARCHAR(255) NOT NULL;
