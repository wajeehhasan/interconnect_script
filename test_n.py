
#used to send get and post requests
import requests
#data dump navigator
from bs4 import BeautifulSoup
#for simple mail use this lib
import smtplib
#regex expresion filter like dial-plan but used for strings
import re
#to attach body to msg
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 
#to attach images and text files use these libs
from email.mime.base import MIMEBase
#to use default encoding as accepted by e-mail servers
from email import encoders
#===========================account settings================
email_sender="ngnnoc321@gmail.com"
# email_reciever="khushbakht@cyber.net.pk"
# email_reciever="ngn-noc@cyber.net.pk"
# email_reciever='wajeeh.hasan322@gmail.com'
# email_reciever='nisar.ali@cyber.net.pk'
email_reciever='officialjunks@yahoo.com'
t_subject="Interconnect Status Report"
t_Cc="s.wajeeh@cyber.net.pk"
msg=MIMEMultipart()
msg['Subject']=t_subject
msg['From']=email_sender
msg['To']=email_reciever
msg['Cc']="s.wajeeh@cyber.net.pk"
server = smtplib.SMTP("smtp.gmail.com",587)
#====================color codes extracted from html for apply logic=====================

blue='background-color:#2B60DE'
red='background-color:#E42217'
hang='background-color:#95B9C7'
in_use='background-color:#348017'
#============================request session initiation================
s=requests.session()
response = s.get("http://10.24.242.6/index.php")

auth = {
    'reserved_username':'admin',
    'reserved_password':'n3tbord3r557'
}
s.post('http://10.24.242.6/index.php',data=auth)
response = s.get('http://10.24.242.6/fusionpbx/tdm_status.php?embedded=NSC')

# ============sending response to beautiful soup to navigate through===========
soup=BeautifulSoup(response.text,"html.parser")

#===========================================
# for channel count
red_list=[]
inuse_list=[]
hang_list=[]
blue_list=[]
# blue='background-color:#2B60DE'
# red='background-color:#E42217'
# hang='background-color:#95B9C7'
# in_use='background-color:#348017'
raw_data=soup.find_all(attrs={'align':'center','width':'10px','height':'14px'})
for x in range(19):
    raw_data.pop()

# #=============================='d recmit============
for item in raw_data:
        if item['style']==red:
            red_list.append(item)
        elif item['style']==blue:
            blue_list.append(item)
        elif item['style']==hang:
            hang_list.append(item)
        elif item['style']==in_use:
            inuse_list.append(item)
        else:
            pass
#============================================
  
## errors on e1 retrieved
raw_data_int=soup.find_all("span")
# =======================================retrieving UP status for each e1=======
e1_status=[]
# ========
send_email=False
# ========
#giving each e1 status as UP
for x in raw_data_int:
    temp_str=str(x)
    if 'wanpipe' in temp_str:
        temp_status=x.find('font')
        temp_s=temp_status.get_text()
        e1_status.append(temp_s)
    else:
        pass
for x in e1_status:
    if 'UP' in x:
        send_email=False
    else:
        send_email=True
        break
#=======================================================


#========================regex for string(to filer required info)=======
LCV= re.compile(r'(\w{4} \w{4} \w{9})\s:\s(\d{1,})')
feb= re.compile(r'(\w{3} \w{3} \w{5} \w{6}\s):\s(\d{0,})')
CRC4= re.compile(r'(\w{3}\d{1} \w{6})\s\s: (\d{0,})')
FAS= re.compile(r'(F\w{2} \w{6})\s\s:\s(\d{1,})')
Sync1= re.compile(r'(S\w{3} \w{6})\s\s: (\d{1,})')
Rx = re.compile(r'(\w{2} \w{5})\s:\s&\w{2};\s(-?\d{1,}.?\d{1,}?\w{2})')
status1= re.compile(r'(<font color="white">)(\w{1,})')
# =======from here till line 188 is just implementation of logic=======
LCV_v=""
feb_v=""
crc4_v=""
fas_v=""
sync_v=""
rx_v=""
status_v=""
master_list=[]
master_string=""
for x in raw_data_int:
    temp_str=str(x)
    if 'wanpipe' in temp_str:
        p=LCV.search(temp_str)
        LCV_v=str(p.group(1))
        LCV_v+=": "
        LCV_v+=str(p.group(2))
        LCV_v+='\n'
                
        p=feb.search(temp_str)
        feb_v=str(p.group(1))
        feb_v+=": "
        feb_v+=str(p.group(2))
        feb_v+='\n'
        
        p=CRC4.search(temp_str)
        crc4_v=str(p.group(1))
        crc4_v+=": "
        crc4_v+=str(p.group(2))
        crc4_v+='\n'
        
        p=FAS.search(temp_str)
        fas_v=str(p.group(1))
        fas_v+=": "
        fas_v+=str(p.group(2))
        fas_v+='\n'
        p=Sync1.search(temp_str)
        sync_v=str(p.group(1))
        sync_v+=": "
        sync_v+=str(p.group(2))
        sync_v+='\n'
        p=Rx.search(temp_str)
        rx_v=str(p.group(1))
        rx_v+=": "
        rx_v+=str(p.group(2))
        rx_v+='\n'
        p=status1.search(temp_str)
        status_v="Status is "
        status_v+=": "
        status_v+=str(p.group(2))
        status_v+='\n'
        master_string=LCV_v+feb_v+crc4_v+fas_v+sync_v+rx_v+status_v
        master_list.append(master_string)
    else:
        pass
#============================file saving to save error report
with open("interconnect_data.txt","w") as file:
    for count,elem in enumerate(master_list,1):
        spasd='============E1/T1#{} Details============\n'.format(count)
        file.write(spasd)
        file.write(elem)
        file.write("\n")
        file.write("=================================")


#===========================navigatig to data========================
soup=BeautifulSoup(response.text,"html.parser")
# print(soup)
data_network_status=soup.find_all(attrs={'color':'white'})
dt_nt_list=[]
for x in data_network_status:
    if x.get_text()=='S          ' or x.get_text()=='X          ' or x.get_text()=='i          ' or x.get_text()=='D          ' or x.get_text()=='r          ' or  x.get_text()=='r          ' or x.get_text()=='d          ' or x.get_text()=='p          ' or x.get_text()=='m          ' or x.get_text()=='u          ' or x.get_text()=='t          ' or x.get_text()=='h          ' or x.get_text()=='h          ' or  x.get_text()=='c          ' or x.get_text()=='r          ' or x.get_text()=='s          ' or  x.get_text()=='C          ' or  x.get_text()=='L          ' or x.get_text()=='?          ' or len(x.get_text())==1:
        pass
    else:
        dt_nt_list.append(x.get_text())

stp_1="Physical : {}, Data layer : {}, Network Layer : {}".format(dt_nt_list[8],dt_nt_list[9],dt_nt_list[10])
stp_2="Physical : {}, Data layer : {}, Network Layer : {}".format(dt_nt_list[12],dt_nt_list[13],dt_nt_list[14])
# ====================specific mesg gen=====
ulti_msg=''
hang_log=(len(red_list)+len(inuse_list)+len(hang_list)+len(blue_list))*0.2

dt_nt_list[9]='DOWN'
if 'UP' not in dt_nt_list[9] or 'UP' not in dt_nt_list[10]:
    ulti_msg+='\n-->stp_1 data/network are down or flapping<--\n'

if 'UP' not in dt_nt_list[13] or 'UP' not in dt_nt_list[14]:
    ulti_msg+='\n-->stp_2 data/network are down or flapping<--\n'

if send_email:
    ulti_msg+="\n-->SOME E1 is down/flap\n"

if len(red_list)>2:
    ulti_msg+="\n-->More than 4 channels are down<--\n"

if len(hang_list)>hang_log:
    ulti_msg+="\n--> 20% of channels are hang\n"

print(ulti_msg)
# =================================
# =================================================
message2="\n"
message2+=ulti_msg

for count,elem in enumerate(e1_status,1):
    if count==3:
        message2+="============= E1#{} ================\n".format(count)
        message2+=stp_1
        message2+='\n'
    elif count==4:
        message2+="============= E1#{} ================\n".format(count)
        message2+=stp_2
        message2+='\n'
    else:
        message2+="============= E1#{} ================\n".format(count)
        message2+="\t\tstatus : {}".format(e1_status[count-1])
        message2+="\n"
#===starting secure connection by tls encrypter==

message="\nLahore Interconnect status(10.24.242.6)\n\tUp(idle) channels : {}\n\tinuse channels : {}\n\thang channels : {}\n\tdown channels : {}\n\t".format(len(blue_list),len(inuse_list),len(hang_list),len(red_list))
message2+=message




if len(red_list)>2 or len(hang_list)>hang_log or send_email:
    server.starttls()
    server.login("ngnnoc321@gmail.com","Cyber@321")
    #=====converting dictionary data type to plain text===
    msg.attach(MIMEText(message2,'plain'))
    final_body=msg.as_string()
    #===giving file patch to be attached
    filename="interconnect_data.txt"
    #===opening file and reading byte by byte
    attachment=open(filename,'rb')
    #===converting byte's into octet stream===
    part=MIMEBase('application','octet-stream')
    #=======those stream of octet into payload====
    part.set_payload((attachment).read())
    #===email server accept data encoded with base64 default==
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',"attachment; filename= "+filename)
    #====attaching txt file to actual mesage
    msg.attach(part)
    #==converting msg into string form
    final_body=msg.as_string()
    #sending email and close connection
    server.sendmail(email_sender,email_reciever,final_body)
    server.quit()
