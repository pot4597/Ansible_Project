import pymssql
import pymysql
import datetime

##보안을 위해 민감한 정보 삭제 및 테이블명/필드명 변경##

try :
        #시만텍 Mssql서버 연결
        conn_symantec =  pymssql.connect(server="***" , user="***", password="***", database="***")
        cursor_symantec = conn_symantec.cursor()

        #시만텍 Mssql서버 접속후 데이터 select
        cursor_symantec.execute("""select distinct dateadd(s,convert(bigint,LAST_UPDATE_TIME)/1000,'01-01-1970 00:00:00') lastacces
 ,i.computer_name
 , sa.STATUS "Status"
 , g.name as GROUP_NAME
 , sa.AGENT_VERSION "Client_Version"
 , (case when sa.LAST_CONNECTED_IP_ADDR = i.IP_ADDR1 then i.IP_ADDR1_TEXT
WHEN (sa.LAST_CONNECTED_IP_ADDR = i.IP_ADDR2) THEN i.IP_ADDR2_TEXT
WHEN (sa.LAST_CONNECTED_IP_ADDR = i.IP_ADDR3) THEN i.IP_ADDR3_TEXT
WHEN (sa.LAST_CONNECTED_IP_ADDR = i.IP_ADDR4) THEN i.IP_ADDR4_TEXT
ELSE i.IP_ADDR1_TEXT END) AS ipaddr
, (case when sa.LAST_CONNECTED_IP_ADDR = i.IP_ADDR1 then i.SUBNET_MASK1_TEXT
WHEN (sa.LAST_CONNECTED_IP_ADDR = i.IP_ADDR2) THEN i.SUBNET_MASK2_TEXT
WHEN (sa.LAST_CONNECTED_IP_ADDR = i.IP_ADDR3) THEN i.SUBNET_MASK3_TEXT
WHEN (sa.LAST_CONNECTED_IP_ADDR = i.IP_ADDR4) THEN i.SUBNET_MASK4_TEXT
ELSE i.SUBNET_MASK1_TEXT END) AS subnetmask
, (case when sa.LAST_CONNECTED_IP_ADDR = i.IP_ADDR1 then i.GATEWAY1_TEXT
WHEN (sa.LAST_CONNECTED_IP_ADDR = i.IP_ADDR2) THEN i.GATEWAY2_TEXT
WHEN (sa.LAST_CONNECTED_IP_ADDR = i.IP_ADDR3) THEN i.GATEWAY3_TEXT
WHEN (sa.LAST_CONNECTED_IP_ADDR = i.IP_ADDR4) THEN i.GATEWAY4_TEXT
ELSE i.GATEWAY1_TEXT END) AS gateway
, (case when sa.LAST_CONNECTED_IP_ADDR = i.IP_ADDR1 then  replace(lower(i.MAC_ADDR1), '-', '')
WHEN (sa.LAST_CONNECTED_IP_ADDR = i.IP_ADDR2) THEN  replace(lower(i.MAC_ADDR2), '-', '')
WHEN (sa.LAST_CONNECTED_IP_ADDR = i.IP_ADDR3) THEN  replace(lower(i.MAC_ADDR3), '-', '')
WHEN (sa.LAST_CONNECTED_IP_ADDR = i.IP_ADDR4) THEN  replace(lower(i.MAC_ADDR4), '-', '')
ELSE replace(lower(i.MAC_ADDR1), '-', '') END) AS macaddr
, i.DNS_SERVER1_TEXT "DNS_1"
, i.DNS_SERVER2_TEXT "DNS_2"
, i.OPERATION_SYSTEM "Operation System"
, i.SERVICE_PACK "Service Pack"
, BIOS_SERIALNUMBER "SERIALNUMBER"
from test_sem_agent as sa with (nolock) left outer join TEST_pattern pat on sa.pattern_idx=pat.pattern_idx
inner join TEST_v_sem_computer i on i.computer_id=sa.computer_id
inner join TEST_identity_map g on g.id=sa.group_id
where sa.deleted='0' and I.DELETED = 0 order by group_name, i.COMPUTER_name;
""")

        #로컬 Mysql서버 연결
        conn_mysql = pymysql.connect(host='127.0.0.1', user='root', password='***',db='***', charset='utf8')
        cursor_mysql = conn_mysql.cursor()

        #로컬 mysql서버 접속후 데이터 전체 삭제
        cursor_mysql.execute("delete from TEST_symantec")
        curs = conn_mysql.cursor()


        #시만텍 Mssql 데이터 베이스에서 한줄 가져오기
        row = cursor_symantec.fetchone()
        
        #Num 증가값을 위한 변수 선언
        i = 0

        #가져온 데이터 출력 반복문
        while row:
            if row[2] == 1:
                stateValue = "백신 정상"                
            elif row[2] == 0:
                stateValue = "백신 미접속"
            else:
                stateValue = row[2]
            mac = row[8].replace(":","") 
            
            #Num 증가값
            i += 1

            #시만텍 서버에서 가져온 정보, 로컬 DB(Mysql)에 저장
            sql = "insert into TEST_symantec (syman_accesstime, syman_computername, syman_status, syman_groupname, syman_clientversion, syman_ipaddr, syman_subnetmask, syman_gateway, syman_macaddr, syman_dns1, syman_dns2, syman_ostype, syman_serv_pack, syman_serialnum, num) values ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (row[0], row[1], stateValue, row[3], row[4], row[5], row[6], row[7], mac, row[9], row[10], row[11], row[12], row[13], i)
            curs.execute(sql, val)
          
            #시만텍 서버에서 다음 한줄 가져오기
            row = cursor_symantec.fetchone()

        conn_symantec.commit()
        conn_mysql.commit()
        conn_symantec.close()
        conn_mysql.close()
except Exception as e:
        print(e)
