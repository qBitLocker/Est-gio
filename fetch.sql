USE test;

SELECT * FROM INFORMATION_SCHEMA.TABLES;
SELECT * FROM polls_user;

DESCRIBE django_session;
SELECT * FROM django_session;

SELECT * FROM polls_choice;
SELECT * FROM polls_question;

-- DROP TABLE polls_choice;
-- DROP TABLE polls_question;

-- Configurando conexões no VSCode
/*ALTER USER root@localhost
IDENTIFIED WITH mysql_native_password BY 'avance';*/