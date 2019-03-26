import os
import sys
from scp import SCPClient
import paramiko
from lxml import etree
from xmldiff import main, formatting

def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client

ssh=createSSHClient('inf-dev11-inta1', '22', 'infa', 'welcomedev1108')
stdin, stdout, stderr = ssh.exec_command('pmrep connect -r infarep_dev11 -d domaindev11 -n batch_user -x batch_user')
stdin, stdout, stderr = ssh.exec_command('pmrep objectexport -o workflow -f Sales_Forecasting -n wf_Pipeline_EDW_WAVE_Scratch_Pad_Snapshot_Load -m -s -b -r -u /apps/infa/PowerCenter8.6.1/server/infa_shared/ArtifactComparison/WORKFLOW.xml')
stdin, stdout, stderr = ssh.exec_command('pmrep objectexport -o workflow -f Sales_Forecasting -n wf_Pipeline_EDW_WAVE_Scratch_Pad_Snapshot_Load_incremental -m -s -b -r -u /apps/infa/PowerCenter8.6.1/server/infa_shared/ArtifactComparison/WORKFLOW_dev.xml')
scp=SCPClient(ssh.get_transport())
scp.get('/apps/infa/PowerCenter8.6.1/server/infa_shared/ArtifactComparison/WORKFLOW.xml')
scp.get('/apps/infa/PowerCenter8.6.1/server/infa_shared/ArtifactComparison/WORKFLOW_dev.xml')
ssh.close()
diff = main.diff_files('WORKFLOW.xml', 'WORKFLOW_dev.xml',formatter=formatting.XMLFormatter())
print(diff, file=open("test_compare.xml",'w'))