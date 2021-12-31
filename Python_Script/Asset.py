import pymssql
import pymysql
import psycopg2
import datetime

try :
        #자산 Postgres db서버 연결
        conn_postgres =  psycopg2.connect(host="1.1.1.1", dbname='***', user="***", password="***", port="****")
        cursor_postgres = conn_postgres.cursor()

        #자산 Postgres db서버 접속후 데이터 select
        cursor_postgres.execute("select *  from Test_jasan")

        #로컬 Mysql서버 연결
        conn_mysql = pymysql.connect(host='127.0.0.1', user='***', password='***',db='***', charset='utf8')
        cursor_mysql = conn_mysql.cursor()

        #로컬 Mysql서버 접속후 데이터 전체 삭제
        cursor_mysql.execute("delete from Test")
        curs = conn_mysql.cursor()


        #자산 서버 postgres db 에서 정보 한줄 가져오기
        row_jasan = cursor_postgres.fetchone()

        #증가값 을 위한 i 변수 선언
        i = 0

        #가져온 데이터 출력 반복문        
        while row_jasan:
            i += 1 
            #데이터 insert
            sql = "insert into Test (jasan_assetcode, jasan_num, jasan_site, jasan_buseo, jasan_userid, jasan_username, jasan_location, jasan_locationdetail, jasan_macaddr, num) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (row_jasan[0], row_jasan[1], row_jasan[2], row_jasan[3], row_jasan[4], row_jasan[5], row_jasan[6], row_jasan[7], row_jasan[8], i)
            curs.execute(sql, val)

            #자산 서버 postgres db 에서 정보 한줄 가져오기
            row_jasan = cursor_postgres.fetchone()


        conn_postgres.commit()
        conn_mysql.commit()
        conn_postgres.close()
        conn_mysql.close()
except Exception as e:
        print(e)
