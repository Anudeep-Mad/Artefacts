import datetime
import sys
import cx_Oracle
import pymysql
import os
import json
import csv
import paramiko
from scp import SCPClient
from datetime import datetime
from P4 import P4
import subprocess

os.chdir('C:\instantclient_11_2')
args=sys.argv[1:]
timecurrent=datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
mydir_putty = os.path.join(
        "C:\\Users\\amedishetti\\Desktop\\sp\\putty_dump_"+timecurrent)
os.makedirs(mydir_putty)
mydir_perforce = os.path.join(
        "C:\\Users\\amedishetti\\Desktop\\sp\\Perforce_dump_"+timecurrent)
os.makedirs(mydir_perforce)

y=sys.argv[1] #sub string name
z=sys.argv[2] #env name
start = sys.argv[3]
end = sys.argv[4]
email = sys.argv[5]

name = "compare_"+timecurrent
file_final = "C:\\Users\\amedishetti\\Desktop\\sp\\"+name+".txt"
fo = open(file_final,'a')
connection = pymysql.connect( host='build-prd-mysql1.vmware.com', user='devops_ro', passwd='Dev@ps_r0', db='vdeploy',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
try:
    cursor = connection.cursor()
    query = ("SELECT DISTINCT(user_story) FROM vDeploy_execution_status AS exe LEFT JOIN vDeploy_build AS bld ON bld.id = exe.build_primary_id WHERE env_name = 'PROD' AND application_name = 'Informatica' AND bld.build_id IN (SELECT distinct(exe.BUILD_ID) FROM vDeploy_execution_status AS exe LEFT JOIN vDeploy_build AS bld ON bld.id = exe.build_primary_id WHERE env_name='PROD' and application_name='Informatica' AND STR_TO_DATE(START_TIME, '%Y-%m-%d %H:%i:%s') >= STR_TO_DATE('"+start+"', '%Y-%m-%d %H:%i:%s') AND STR_TO_DATE(START_TIME, '%Y-%m-%d %H:%i:%s') <= STR_TO_DATE('"+end+"', '%Y-%m-%d %H:%i:%s'));")
    #query = ("SELECT distinct(user_story) FROM vDeploy_execution_status AS exe LEFT JOIN vDeploy_build AS bld ON bld.id = exe.build_primary_id WHERE env_name='PROD' and application_name='Informatica' and bld.build_id in (SELECT max(bld.build_id)  FROM vDeploy_execution_status AS exe LEFT JOIN vDeploy_build AS bld ON bld.id = exe.build_primary_id WHERE env_name='PROD' and application_name='Informatica' )")
    cursor.execute(query)
    res = cursor.fetchall()
    for row in res:
        r = row["user_story"]
        query = ("SELECT distinct file_name FROM vdeploy.vDeploy_build where user_story='"+r+"'")
        file_prod = "C:\\Users\\amedishetti\\Desktop\\sp\\Archive\\"+r+"_prod.txt"
        file_env = "C:\\Users\\amedishetti\\Desktop\\sp\\Archive\\"+r+"_"+z+".txt"
        file_output= "C:\\Users\\amedishetti\\Desktop\\sp\\Archive\\outputfile.txt"
        file_us = "C:\\Users\\amedishetti\\Desktop\\sp\\"+r+"_"+z+"_compare.txt"
        f = open(file_output,"w")
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            s=row["file_name"]
            if(s[0:2]=="wf"):
                con = cx_Oracle.connect('INFAREP_PROD_READ/infarep_prod_read@inf-prd-ora1.vmware.com:1521/INFPRD')
                cur = con.cursor()
                query1 = ("SELECT * FROM (SELECT WF.WORKFLOW_NAME, COUNT(TSK.INSTANCE_NAME) AS TSK_COUNT FROM INFAREP_PROD.REP_WORKFLOWS WF INNER JOIN INFAREP_PROD.REP_TASK_INST TSK ON WF.WORKFLOW_ID=TSK.WORKFLOW_ID GROUP BY WF.WORKFLOW_NAME) S WHERE S.WORKFLOW_NAME='"+s[0:-4]+"'")
                cur.execute(query1)
                for result in cur:
                    print(result,file=open(file_prod,"a"))
                query2 = ("SELECT * FROM (SELECT WF.WORKFLOW_NAME, COUNT(TSK.INSTANCE_NAME) AS TSK_COUNT FROM INFAREP_"+z+".REP_WORKFLOWS WF INNER JOIN INFAREP_"+z+".REP_TASK_INST TSK ON WF.WORKFLOW_ID=TSK.WORKFLOW_ID GROUP BY WF.WORKFLOW_NAME) S WHERE S.WORKFLOW_NAME='"+s[0:-4]+"'")
                con = cx_Oracle.connect('infarep_dev15/infarep_dev15_789@inf-dev15-ora1.vmware.com/infdev15')
                cur=con.cursor()
                cur.execute(query2)
                file_1 = set()
                file_2 = set()
                for result in cur:
                    print(result,file=open(file_env, "w"))
                with open(file_prod,'r') as f:
                    for line in f:
                        file_1.add(line.strip())
                with open(file_env, 'r') as f:
                    for line in f:
                        file_2.add(line.strip())
                if file_1-file_2:
                    print("The workflows with the changes in Prod and "+z+" are", file=open(file_us,"w"))
                    print(file_1-file_2,file=open(file_us,"a"))
                else:
                    print("There are no differences in the workflows", file=open(file_us,"w"))
        def createSSHClient(server, port, user, password):
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(server, port, user, password)
            return client
        sql = "SELECT distinct file_name,perforce_path FROM vdeploy.vDeploy_build where user_story='"+r+"'and subobject_name='"+y+"'"
        cursor.execute(sql)
        result = cursor.fetchone()
        results=cursor.fetchall()


        for resultss in results:
            f=open(file_output,"w")
            f.write(resultss["file_name"]+","+resultss["perforce_path"].replace("infa_shared","env/"+z+"/infa_shared"))
            f.write("\n")

        f1 = open(file_us,"a")


        with open("C:\\Users\\amedishetti\\Desktop\\sp\\Archive\\outputfile.txt") as f:
            for line in f:
                
                lines=line.splitlines()
                
        with open('C:\\Users\\amedishetti\\Desktop\\sp\\Archive\\outputfile.txt', 'r') as f2:
            lines = f2.readlines()
        # remove spaces
        lines = [line.replace(' ', '') for line in lines]
        # finally, write lines in the file
        with open('C:\\Users\\amedishetti\\Desktop\\sp\\Archive\\outputfile.txt', 'w') as f3:
            f3.writelines(lines)
            f3.close()
        with open('C:\\Users\\amedishetti\\Desktop\\sp\\Archive\\outputfile.txt') as f:
            reader = csv.reader(f, delimiter=",")
            for i in reader:
                
                p4 = P4()
                p4.user = "amedishetti"
                p4.password = "Worm#ole1729"
                p4.port = "perforce-it.vmware.com:1947"
                #p4.client = "C:\\Users\\sharjain\\Perforce\\sharadj_USBLRSHARJAIN2_6673\\informatica\\sales_pulse\\rel-cd\\Sqls\\"
                p4.connect()
                info = p4.run("info")
                #p4.run_print("-q", "-o", "C:\\Users\\amedishetti\\Desktop\\sp\\Perforce_dump\\"+i[0],i[1]+"#head")
                p4.run_print("-q", "-o", mydir_perforce+"\\"+i[0],i[1]+"#head")
                p4.disconnect()
                ssh=createSSHClient('inf-dev11-inta1', '22', 'infa', 'welcomedev1108')
                scp=SCPClient(ssh.get_transport())
                #scp.get(r'/apps/infa/PowerCenter8.6.1/server/infa_shared/'+i[1].split("infa_shared",1)[1], r'C:\Users\sharjain\Desktop\sp\python scripts\putty_dump')
                scp.get(r'/apps/infa/PowerCenter8.6.1/server/infa_shared/'+i[1].split("infa_shared",1)[1], mydir_putty)

        file_1 = set()
        file_2 = set()

        #directory = os.fsencode('C:\\Users\\sharjain\\Desktop\\sp\\python scripts\\Perforce_dump')
        directory = os.fsencode(mydir_perforce)


        for file in os.listdir(directory):
            file_1 = set()
            file_2 = set()

            filename = os.fsdecode(file)
            if filename.endswith(".properties") or filename.endswith(".sh"):
                with open(mydir_perforce+"\\"+filename, 'r') as f:
                    for line in f:
                        file_1.add(line.strip())

                with open(mydir_putty+"\\"+filename, 'r') as f:
                    for line in f:
                        file_2.add(line.strip())
                f1.write("INFO:Difference in "+filename+"\n")
                f1.write(str(file_1 - file_2))
                f1.write("##########################################################################################################################\n")
                #f1.write(file_2 - file_1)
            else:
                f1.write(" ")
        f1.close() 
        sys.stdout.close()

        f1 = open(file_us,"r")
        #f = open('./test.txt','r')
        a = ['set()']
        lst = []
        for line in f1:
            for word in a:
                if word in line:
                    line = line.replace(word,'')
            lst.append(line)
        f1.close()
        f1 = open(file_us,"w")
        for line in lst:
            f1.write(line)
        f1.close()
        fo.write("User Story: "+r+"\n")
        f4 = open(file_us,'r')
        for line in f4:
            fo.write(line+"\n")   
        f.close()
        
finally:
    connection.close()
    f.close()
    s = "py C:\\Users\\amedishetti\\Documents\\Anudeep\\AI\\python_AI\\Artifact\\Code\\sqlparser.py CSM-1780 \"Deploy inf sql\" uat "+file_final
    os.system(s)
fo.close()
ssh=createSSHClient('inf-dev11-inta1', '22', 'infa', 'welcomedev1108')
scp=SCPClient(ssh.get_transport())
scp.put(file_final,remote_path='/apps/infa/PowerCenter8.6.1/server/infa_shared/ArtifactComparison/')
ssh.exec_command("echo -e 'Thank you for using artifact sync up validator.\n PFA the comparison report.' | mailx -s 'Comparison File Output' -a /apps/infa/PowerCenter8.6.1/server/infa_shared/ArtifactComparison/"+ name +".txt "+email)

