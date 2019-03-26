import sqlparse
from sqlparse.sql import IdentifierList, Identifier,Parenthesis,Where ,Comparison
from sqlparse.tokens import Keyword
import sys
import csv
import cx_Oracle


from P4 import P4 ,P4Exception
import json
import datetime
import os
import sys
import os.path
import pymysql
import sys
import csv
import paramiko
import pymysql.cursors
from scp import SCPClient
from datetime import datetime



class RecursiveTokenParser(object):
 def __init__(self, query):
    self.query = query
    self.names = []

 def get_table_names(self):
    elements = sqlparse.parse(self.query)
    #print (elements)

    for token in elements[0].tokens:
        #print (token)
        if isinstance(token, Identifier):
            self.identifier(token)
        elif isinstance(token, Parenthesis):
            self.parenthesis(token)

        elif isinstance(token, Where):
            self.where(token)

    return [str(name).upper() for name in self.names]

 def where(self, token):

    for subtoken in token.tokens:
        if isinstance(subtoken, Comparison):
            self.comparison(subtoken)

 def comparison(self, token):
    for subtoken in token.tokens:
        if isinstance(subtoken, Parenthesis):
            self.parenthesis(subtoken)

 def parenthesis(self, token):

    for subtoken in token.tokens:
        if isinstance(subtoken, Identifier):
            self.identifier(subtoken)
        elif isinstance(subtoken, Parenthesis):
            self.parenthesis(subtoken)

 def identifier(self, token):
    self.names.append(token)

 def get_query(self):  #
    return self.query






timecurrent=datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
mydir_putty = os.path.join(
        "C:\\Users\\amedishetti\\Desktop\\sp\\putty_dump_"+timecurrent)
os.makedirs(mydir_putty)
mydir_perforce = os.path.join(
        "C:\\Users\\amedishetti\\Desktop\\sp\\SQL parser\\Perforce_dump_"+timecurrent)
os.makedirs(mydir_perforce)
x=sys.argv[1] #user story name
y=sys.argv[2] #sub string name
z=sys.argv[3] #env name
a = sys.argv[4] #output_filename
#Deploy inf sql
f = open("C:\\Users\\amedishetti\\Desktop\\sp\\outputfile.txt","w")
connection = pymysql.connect( host='build-prd-mysql1.vmware.com', user='devops_ro', passwd='Dev@ps_r0', db='vdeploy',charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
try:
    with connection.cursor() as cursor:
     
        args = [x,y]
        
        sql = "SELECT distinct file_name,perforce_path FROM vdeploy.vDeploy_build where user_story=%s and subobject_name=%s"
        #sql = "SELECT distinct file_name,perforce_path,user_story FROM vdeploy.vDeploy_build where  subobject_name='Deploy inf sql'"
        cursor.execute(sql,args)
        #cursor.execute(sql)
        #result = cursor.fetchone()
        results=cursor.fetchall()
        #print(results)


        for resultss in results:
            #f.write(resultss["file_name"]+","+resultss["perforce_path"].replace("infa_shared","env/"+z+"/infa_shared"))
            f.write(resultss["file_name"]+","+resultss["perforce_path"].replace("infa_shared","env/"+z+"/infa_shared"))
            f.write("\n")
            
		    

finally:
    connection.close()
def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client

f.close() 


f1 = open("C:\\Users\\amedishetti\\Desktop\\sp\\"+x+"compfile.txt","w")
with open('C:\\Users\\amedishetti\\Desktop\\sp\\outputfile.txt') as f:
    reader = csv.reader(f, delimiter=",")
    for i in reader:
        
        p4 = P4()
        p4.user = "amedishetti"
        p4.password = "Worm#ole1729"
        p4.port = "perforce-it.vmware.com:1947"
        p4.client = "C:\\Users\\amedishetti\\Perforce\\amedishetti_USHYDAMEDISHET6_5037\\informatica\\sales_pulse\\rel-cd\\Sqls"
        p4.connect()
        info = p4.run("info")
        p4.run_print("-q", "-o", mydir_perforce+"\\"+i[0],i[1]+"#head")
        p4.disconnect()
file_1 = set()
file_2 = set()

#directory = os.fsencode('C:\\Users\\sharjain\\Desktop\\sp\\python scripts\\Perforce_dump')
directory = os.fsencode(mydir_perforce)


for file in os.listdir(directory):
    file_1 = set()
    filename = os.fsdecode(file)
    f = open(mydir_perforce+"\\"+filename, 'r')
    contents = f.read()
    f.close()
    new_contents = contents.replace('\n', '')
    new_contents_replacing_backslash=new_contents.replace('/', '\n')
    f = open(mydir_perforce+"\\"+filename+"_format", 'w')
    f.write(new_contents_replacing_backslash)
    f.close()
    #f = open(mydir_perforce+"\\"+filename+"_format", 'r')
    for line in open(mydir_perforce+"\\"+filename+"_format"):
        li=line
        #.strip()
        if (not li.startswith("GRANT") and not li.startswith("exit")):
            
            sql2 =line;
 
            t = RecursiveTokenParser(sql2)

            #print(t.get_query())
            #print(t.get_table_names())
            table_name=str(t.get_table_names()).replace('[]', '\n').replace('[','').replace(']','').split(',')[0].replace('INFAUSER.','').replace('"','')
            #print(table_name)
            f = open(mydir_perforce+"\\"+"all_tablename", 'a')
            f.write(table_name)
            f.write(",")
            f.close()
table_name=''
f = open(mydir_perforce+"\\"+"all_tablename", 'r')
for line in f:
    if not len(line.strip()) < 5 :
        #table_name=line.replace(' ','')[:-1].rstrip(',')
        table_name=line.replace(' ','').rstrip().rstrip(',').replace('INFAUSER.','')
        #print (table_name)
        #print(line.replace(' ','')[:-2])
f.close()

f = open(mydir_perforce+"\\"+"lower_env", 'w')
f.write("\n")
f.close()
f = open(mydir_perforce+"\\"+"higher_env", 'w')
f.write("\n")
f.close()
print ("INFO table_name"+table_name)
os.chdir('C:\instantclient_11_2')
con = cx_Oracle.connect('infauser/asgxiry7t2@sfa3-dev11-ora1.vmware.com:1521/SF3DEV11')
cur = con.cursor()
query1 = ("select * from (  SELECT DISTINCT A.OWNER AS OWNER_NAME,  OBJECT_TYPE AS OBJECT_TYPE,  OBJECT_NAME AS OBJECT_NAME,  CASE WHEN A.OBJECT_TYPE='TABLE' THEN 'TABLE_COLUMNS_COUNT:'||TO_CHAR(NVL(B.COL_CNT,0))  WHEN A.OBJECT_TYPE='VIEW' THEN 'VIEW_TEXT_LNGTH:'||TO_CHAR(NVL(TEXT_LENGTH,0))  WHEN A.OBJECT_TYPE='INDEX' THEN 'INDEX_TABLE_NAME:'||D.TABLE_NAME||'; INDEX_COLUMN_NAME:'||D.COLUMN_NAME  WHEN A.OBJECT_TYPE='TRIGGER' THEN 'TRIGGER_TABLE_NAME:'||E.TABLE_NAME  WHEN A.OBJECT_TYPE='PROCEDURE' THEN 'PROCEDURE_LINE_COUNT:'||TO_CHAR(G.CNT_NAME) ELSE 'NA' END AS COMMENTS  FROM (SELECT * FROM DBA_OBJECTS WHERE OBJECT_TYPE IN ('TABLE','VIEW','TRIGGER','SYNONYM','SEQUENCE','INDEX','TRIGGER','PROCEDURE')    AND OWNER = 'INFAUSER' AND OBJECT_NAME NOT LIKE '%$$%') A    LEFT OUTER JOIN (SELECT TABLE_NAME, COUNT(*) COL_CNT FROM USER_TAB_COLUMNS GROUP BY TABLE_NAME) B    ON A.OBJECT_NAME=B.TABLE_NAME AND A.OBJECT_TYPE IN ('TABLE') AND A.OWNER = 'INFAUSER'    LEFT OUTER JOIN (SELECT * FROM DBA_VIEWS WHERE OWNER = 'INFAUSER') C    ON A.OBJECT_NAME=C.VIEW_NAME AND A.OBJECT_TYPE IN ('VIEW')    LEFT OUTER JOIN (SELECT INDEX_NAME, TABLE_NAME, LISTAGG(COLUMN_NAME,';') within group (order by INDEX_NAME, TABLE_NAME) AS COLUMN_NAME    FROM DBA_IND_COLUMNS WHERE INDEX_OWNER = 'INFAUSER' GROUP BY INDEX_NAME, TABLE_NAME ORDER BY INDEX_NAME, TABLE_NAME) D    ON A.OBJECT_NAME=D.INDEX_NAME AND A.OBJECT_TYPE IN ('INDEX')    LEFT OUTER JOIN (SELECT * FROM ALL_TRIGGERS WHERE OWNER = 'INFAUSER') E    ON A.OBJECT_NAME=E.TRIGGER_NAME AND A.OBJECT_TYPE IN ('TRIGGER')    LEFT OUTER JOIN (select NAME, COUNT(*) CNT_NAME FROM DBA_SOURCE WHERE TYPE='PROCEDURE' AND OWNER = 'INFAUSER' GROUP BY NAME) G    ON A.OBJECT_NAME=G.NAME) where object_name in (" + table_name + ")") ;
cur.execute(query1)
for result in cur:
    print(result,file=open(mydir_perforce+"\\"+"lower_env","a"))
query2 = ("select table_name,column_name,data_type,data_length from dba_tab_columns  where table_name  in (" + table_name + ")") ;
cur.execute(query2)
for result in cur:
    print(result,file=open(mydir_perforce+"\\"+"lower_env","a"))

con = cx_Oracle.connect('infauser/aifzlsbx61@sfa3-test11-ora1.vmware.com:1521/SF3TST11')
cur = con.cursor()
query1 = ("select * from (  SELECT DISTINCT A.OWNER AS OWNER_NAME,  OBJECT_TYPE AS OBJECT_TYPE,  OBJECT_NAME AS OBJECT_NAME,  CASE WHEN A.OBJECT_TYPE='TABLE' THEN 'TABLE_COLUMNS_COUNT:'||TO_CHAR(NVL(B.COL_CNT,0))  WHEN A.OBJECT_TYPE='VIEW' THEN 'VIEW_TEXT_LNGTH:'||TO_CHAR(NVL(TEXT_LENGTH,0))  WHEN A.OBJECT_TYPE='INDEX' THEN 'INDEX_TABLE_NAME:'||D.TABLE_NAME||'; INDEX_COLUMN_NAME:'||D.COLUMN_NAME  WHEN A.OBJECT_TYPE='TRIGGER' THEN 'TRIGGER_TABLE_NAME:'||E.TABLE_NAME  WHEN A.OBJECT_TYPE='PROCEDURE' THEN 'PROCEDURE_LINE_COUNT:'||TO_CHAR(G.CNT_NAME) ELSE 'NA' END AS COMMENTS  FROM (SELECT * FROM DBA_OBJECTS WHERE OBJECT_TYPE IN ('TABLE','VIEW','TRIGGER','SYNONYM','SEQUENCE','INDEX','TRIGGER','PROCEDURE')    AND OWNER = 'INFAUSER' AND OBJECT_NAME NOT LIKE '%$$%') A    LEFT OUTER JOIN (SELECT TABLE_NAME, COUNT(*) COL_CNT FROM USER_TAB_COLUMNS GROUP BY TABLE_NAME) B    ON A.OBJECT_NAME=B.TABLE_NAME AND A.OBJECT_TYPE IN ('TABLE') AND A.OWNER = 'INFAUSER'    LEFT OUTER JOIN (SELECT * FROM DBA_VIEWS WHERE OWNER = 'INFAUSER') C    ON A.OBJECT_NAME=C.VIEW_NAME AND A.OBJECT_TYPE IN ('VIEW')    LEFT OUTER JOIN (SELECT INDEX_NAME, TABLE_NAME, LISTAGG(COLUMN_NAME,';') within group (order by INDEX_NAME, TABLE_NAME) AS COLUMN_NAME    FROM DBA_IND_COLUMNS WHERE INDEX_OWNER = 'INFAUSER' GROUP BY INDEX_NAME, TABLE_NAME ORDER BY INDEX_NAME, TABLE_NAME) D    ON A.OBJECT_NAME=D.INDEX_NAME AND A.OBJECT_TYPE IN ('INDEX')    LEFT OUTER JOIN (SELECT * FROM ALL_TRIGGERS WHERE OWNER = 'INFAUSER') E    ON A.OBJECT_NAME=E.TRIGGER_NAME AND A.OBJECT_TYPE IN ('TRIGGER')    LEFT OUTER JOIN (select NAME, COUNT(*) CNT_NAME FROM DBA_SOURCE WHERE TYPE='PROCEDURE' AND OWNER = 'INFAUSER' GROUP BY NAME) G    ON A.OBJECT_NAME=G.NAME) where object_name in (" + table_name + ")") ;
cur.execute(query1)
for result in cur:
    print(result,file=open(mydir_perforce+"\\"+"higher_env","a"))
query2 = ("select table_name,column_name,data_type,data_length from dba_tab_columns  where table_name  in (" + table_name + ")") ;
cur.execute(query2)
for result in cur:
    print(result,file=open(mydir_perforce+"\\"+"higher_env","a"))
f1 = open(mydir_perforce+"\\"+x+"comparision_file","w")
with open(mydir_perforce+"\\"+"higher_env", 'r') as f:
            for line in f:
                file_1.add(line.strip())

with open(mydir_perforce+"\\"+"lower_env", 'r') as f:
            for line in f:
                file_2.add(line.strip())

f1.write("INFO:Difference in SQL files for user story CSM-1780"+"\n")
f1.write(str(file_1 - file_2))
f1.write(str(file_2 - file_1))

fo = open(a,'a')
fo.write("INFO:Difference in SQL files for user story CSM-1780"+"\n")
fo.write(str(file_1 - file_2))
fo.write(str(file_2 - file_1))
fo.write("\n")