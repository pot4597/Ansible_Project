import pymssql
import pymysql
import psycopg2
import datetime

##보안을 위해 민감한 정보 삭제 및 테이블명/필드명 변경##

try :
        #postgres db서버 연결
        conn_postgres =  psycopg2.connect(host="***", dbname='***', user="***", password="***", port="***")
        cursor_postgres = conn_postgres.cursor()
        #mssql서버 접속후 데이터 select
        cursor_postgres.execute("select jasan_no, mac_no, ssid from TEST_manage")


        #mysql서버 연결
        conn_mysql = pymysql.connect(host='127.0.0.1', user='***', password='***',db='***', charset='utf8')
        cursor_mysql = conn_mysql.cursor()
        #mysql서버 접속후 데이터 전체 삭제
        cursor_mysql.execute("delete from TEST_wireless")
        curs = conn_mysql.cursor()


        #postgres데이터 베이스에서 한줄 가져오기
        row_jasan = cursor_postgres.fetchone()

        #가져온 데이터 출력 반복문
        i = 0
        while row_jasan:
            #데이터 insert
            print(row_jasan[0])
            i += 1
            sql = "insert into TEST_wireless (wireless_jasannum, wireless_macaddr, wireless_ssid, num) values (%s, %s, %s, %s)"
            val = (row_jasan[0], row_jasan[1], row_jasan[2], i)
            row_jasan = cursor_postgres.fetchone()
            curs.execute(sql, val)


        conn_postgres.commit()
        conn_mysql.commit()
        conn_postgres.close()
        conn_mysql.close()
except Exception as e:
        print(e)
