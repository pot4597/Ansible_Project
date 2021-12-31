import datetime
import pymysql
import CUBRIDdb as cubrid

##보안을 위해 민감한 정보 삭제 및 테이블명/필드명 변경##

try :
        #Cubrid db서버 연결
        conn_cubrid =  cubrid.connect('CUBRID:*:*:*:::','*','*')
        cursor_cubrid = conn_cubrid.cursor()
        
        #mssql서버 접속후 데이터 select
        cursor_cubrid.execute("""select distinct
        o.jasan_no
        ,o.inout_date
        ,(o.sinirum || '(' || o.sinirum_cd ||')') as jasan_reqman
        ,m.ban_sa
        ,m.sin_ilja
        ,m.ban_ilja
        ,m.ban_ye
        ,m.ban_chl
        ,m.ban_ip
        ,s.code_nm
        ,t.code_nm 
        from (select TEST ,Max(TEST) as inout_date from TEST group by jasan_no) G
        left outer join TEST_inout O on (G.jasan_no=O.jasan_no and G.inout_Date=O.inout_Date)
        left outer join TEST_banchool m on (o.sinno=m.idno and o.jasan_no=m.jasan_no and o.rf_tag=m.rf_tag )
        left outer join TEST_oe1tnoecommdetailcd s on (s.code_id='STNB' and decode(m.sangtae,null,o.stat,m.sangtae)=s.code)
        left outer join TEST_nb_assets a on (o.jasan_no=a.jasan_no and o.rf_tag=a.rf_tag)
        left outer join TEST_oe1tnoecommdetailcd t on (t.code_id='NBSG' and m.sign_status=t.code)
        order by o.TEST_date desc
        """)
        
        #mysql서버 연결
        conn_mysql = pymysql.connect(host='127.0.0.1', user='*', password='*',db='*', charset='utf8')
        cursor_mysql = conn_mysql.cursor()
        #mysql서버 접속후 데이터 전체 삭제
        cursor_mysql.execute("delete from TEST_banip")
        curs = conn_mysql.cursor()

        #postgres데이터 베이스에서 한줄 가져오기
        row_banip = cursor_cubrid.fetchone()

        #가져온 데이터 출력 반복문
        i = 0
        while row_banip:
            #데이터 insert
            i += 1
            sql = "insert into TEST_banip (banchul_jasan_num, banchul_inoutdate, banchul_requst_man, banchul_reason, banchul_req_date, banchul_yejung_date, banip_yejung_date, banchul_date, banip_date, banchul_status, banchul_approve_status, num) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (row_banip[0], row_banip[1], row_banip[2], row_banip[3], row_banip[4], row_banip[5], row_banip[6], row_banip[7], row_banip[8], row_banip[9], row_banip[10], i)
            row_banip = cursor_cubrid.fetchone()
            curs.execute(sql, val)

        conn_cubrid.commit()
        conn_mysql.commit()
        conn_cubrid.close()
        conn_mysql.close()
except Exception as e:
        print(e)
