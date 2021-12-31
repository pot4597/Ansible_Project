import pymssql
import pymysql
import datetime

##보안을 위해 민감한 정보 삭제 및 테이블명/필드명 변경##
try :
        #Gradius Mssql서버 연결
        conn =  pymssql.connect(server="****" , user="***", password="***", database="***")
        cursor = conn.cursor()

        #Mssql서버 접속후 데이터 select
        cursor.execute("select distinct d.name, a.username, a.currentipaddr, a.version, a.state, l.name, replace(lower(i.macaddr), ':', '')as macaddr,h.cpu, h.memory, h.systemmodel, h.mainboard, i.policyrecivetime from agent as a left join dept as d on a.deptid = d.id left join level as l on a.currentlevelid = l.id left join agent_hw as h on a.id = h.agentid  left join agent_info as i on a.id = i.id where i.macaddr is not NULL and d.name != '(퇴사자)' and i.policyrecivetime >= DATEADD(day,-14,getdate());")

        #로컬 Mysql서버 연결
        conn_mysql = pymysql.connect(host='127.0.0.1', user='***', password='***',db='***', charset='utf8')
        cursor_mysql = conn_mysql.cursor()

        #로컬 Mysql서버 접속후 데이터 전체 삭제
        cursor_mysql.execute("delete from gradius")
        curs = conn_mysql.cursor()

        #mssql데이터 베이스에서 한줄 가져오기
        row = cursor.fetchone()

        #증가값 을 위한 i 변수 선언
        i = 0

        #가져온 데이터 출력 반복문
        while row:
            #if문으로 데이터 치환
            if row[4] == "D":
                stateValue="DLP 미접속"
            elif row[4] == "U":
                stateValue="DLP 미설치"
            elif row[4] == "A":
                stateValue="DLP 정상"
            else:
                stateValue=row[4]

            #MAC Values(row[6]) 안에 다중 값이 들어있어 split하여 저장 하기 위한 변수 선언          
            mac_split = ""
            mac_split2 = ""
            mac_split3 = ""

            #MAC Values(row[6])에 "," 으로 구분점을 잡아 split하여 mac_split, mac_split2, mac_split3변수에 저장 
            if row[6].find(',') > -1:
                mac_split = row[6].split(',')[0]
                mac_split2 = row[6].split(',')[1]
                if row[6].find(',', row[6].find(',')+1) > -1:
                    mac_split3 = row[6].split(',')[2]
            else:
                mac_split = row[6]

            #IP Values(row[2]) 안에 다중 값이 들어 있어 Split하여 저장 하기 위한 변수 선언 
            ip_split = ""
            ip_split2 = ""
            ip_split3 = ""

            #IP Values(row[2])에 "," 으로 구분점을 잡아 split하여 ip_split, ip_split2, ip_split3변수에 저장 
            if row[2].find(',') > -1:
                ip_split = row[2].split(',')[0]
                ip_split2 = row[2].split(',')[1]
                if row[2].find(',', row[2].find(',')+1) > -1:
                    ip_split3 = row[2].split(',')[2]
            else:
                ip_split = row[2]

            #Num 증가값
            i += 1

            #Gradius 서버에서 가져온 정보, 로컬 DB(mysql)에 저장
            sql = "insert into gradius (gra_deptname, gra_username, gra_ipaddr, gra_ipaddr2, gra_ipaddr3, gra_version, gra_state, gra_policyname, gra_macaddr, gra_macaddr2, gra_macaddr3, gra_cpu, gra_memory, gra_model, gra_serialnum, gra_lastaccess, num) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (row[0], row[1], ip_split, ip_split2, ip_split3, row[3], stateValue, row[5], mac_split, mac_split2, mac_split3, row[7], row[8], row[9], row[10],row[11], i)
            curs.execute(sql, val)     
                
            #Mssql 서버에서 다음 한줄 가져오기
            row = cursor.fetchone()
        conn.commit()
        conn_mysql.commit()
        
        conn.close()
        conn_mysql.close()


        #Gradius Mssql서버 연결
        conn =  pymysql.connect(host="***",port=***, user="***", password="***",database="***", charset='utf8')
        cursor = conn.cursor()

        #Mssql서버 접속후 데이터 select
        cursor.execute("select distinct d.name, a.username, a.currentipaddr, a.version, a.state, l.name, replace(lower(i.macaddr), ':', '')as macaddr,h.cpu, h.memory, h.systemmodel, h.mainboard, i.policyrecivetime from agent as a left join dept as d on a.deptid = d.id left join level as l on a.currentlevelid = l.id left join agent_hw as h on a.id = h.agentid  left join agent_info as i on a.id = i.id where d.name != '(퇴사자)' and i.policyrecivetime >= DATE_ADD(NOW(),INTERVAL -7 day);")

        #로컬 Mysql서버 연결
        conn_mysql = pymysql.connect(host='127.0.0.1', user='***', password='***',db='***', charset='utf8')
        cursor_mysql = conn_mysql.cursor()

        #로컬 Mysql서버 접속후 데이터 전체 삭제
        cursor_mysql.execute("delete from china_gradius")
        curs = conn_mysql.cursor()


        #mssql데이터 베이스에서 한줄 가져오기
        row = cursor.fetchone()

        #가져온 데이터 출력 반복문
        while row:
            #if문으로 데이터 치환
            if row[4] == "D":
                stateValue="DLP 미접속"
            elif row[4] == "U":
                stateValue="DLP 미설치"
            elif row[4] == "A":
                stateValue="DLP 정상"
            else:
                stateValue=row[4]

            #MAC Values(row[6]) 안에 다중 값이 들어있어 split하여 저장 하기 위한 변수 선언          
            mac_split = ""
            mac_split2 = ""
            mac_split3 = ""

            #MAC Values(row[6])에 "," 으로 구분점을 잡아 split하여 mac_split, mac_split2, mac_split3변수에 저장             
            if row[6].find(',') > -1:
                mac_split = row[6].split(',')[0]
                mac_split2 = row[6].split(',')[1]
                if row[6].find(',', row[6].find(',')+1) > -1:
                    mac_split3 = row[6].split(',')[2]
            else:
                mac_split = row[6]

            #IP Values(row[2]) 안에 다중 값이 들어 있어 Split하여 저장 하기 위한 변수 선언 
            ip_split = ""
            ip_split2 = ""
            ip_split3 = ""

            #IP Values(row[2])에 "," 으로 구분점을 잡아 split하여 ip_split, ip_split2, ip_split3변수에 저장             
            if row[2].find(',') > -1:
                ip_split = row[2].split(',')[0]
                ip_split2 = row[2].split(',')[1]
                if row[2].find(',', row[2].find(',')+1) > -1:
                    ip_split3 = row[2].split(',')[2]
            else:
                ip_split = row[2]

            #Num 증가값
            i += 1

            #Gradius 서버에서 가져온 정보, 로컬 DB(mysql)에 저장            
            sql = "insert into gradius (gra_deptname, gra_username, gra_ipaddr, gra_ipaddr2, gra_ipaddr3, gra_version, gra_state, gra_policyname, gra_macaddr, gra_macaddr2, gra_macaddr3, gra_cpu, gra_memory, gra_model, gra_serialnum, gra_lastaccess, num) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"            
            val = (row[0], row[1], ip_split, ip_split2, ip_split3, row[3], stateValue, row[5], mac_split, mac_split2, mac_split3, row[7], row[8], row[9], row[10], row[11], i)
            curs.execute(sql, val)

            #Mssql 서버에서 다음 한줄 가져오기
            row = cursor.fetchone()

        conn.commit()
        conn.close()

        conn_mysql.commit()
        conn_mysql.close()

except Exception as e:
        print(e)



