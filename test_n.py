import requests
from bs4 import BeautifulSoup
#for simple mail use this lib
import smtplib
import re
#to attach body to msg
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 
#to attach images and text files use these libs
from email.mime.base import MIMEBase
from email import encoders

email_sender="ngnnoc321@gmail.com"
email_reciever="s.wajeeh@cyber.net.pk"
t_subject="Interconnect Status Report"
t_Cc="s.wajeeh@cyber.net.pk"
msg=MIMEMultipart()
msg['Subject']=t_subject
msg['From']=email_sender
msg['To']=email_reciever
msg['Cc']="s.wajeeh@cyber.net.pk"
server = smtplib.SMTP("smtp.gmail.com",587)


blue='background-color:#2B60DE'
red='background-color:#E42217'
hang='background-color:#95B9C7'
in_use='background-color:#348017'
s=requests.session()
response = s.get("http://10.24.242.6/index.php")

auth = {
    'reserved_username':'admin',
    'reserved_password':'n3tbord3r557'
}
s.post('http://10.24.242.6/index.php',data=auth)
response = s.get('http://10.24.242.6/fusionpbx/tdm_status.php?embedded=NSC')
soup=BeautifulSoup(response.text,"html.parser")
  
## errors on e1 retrieved
raw_data_int=soup.find_all("span")

#========================ERRORSR=======
LCV= re.compile(r'(\w{4} \w{4} \w{9})\s:\s(\d{1,})')
feb= re.compile(r'(\w{3} \w{3} \w{5} \w{6}\s):\s(\d{0,})')
CRC4= re.compile(r'(\w{3}\d{1} \w{6})\s\s: (\d{0,})')
FAS= re.compile(r'(F\w{2} \w{6})\s\s:\s(\d{1,})')
Sync1= re.compile(r'(S\w{3} \w{6})\s\s: (\d{1,})')
Rx = re.compile(r'(\w{2} \w{5})\s:\s&\w{2};\s(-?\d{1,}.?\d{1,}?\w{2})')
status1= re.compile(r'(<font color="white">)(\w{1,})')
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
with open("interconnect_data.txt","w") as file:
    for count,elem in enumerate(master_list,1):
        spasd='============E#{} Details============\n'.format(count)
        file.write(spasd)
        file.write(elem)
        file.write("\n")
        file.write("=================================")




# for channel counts
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

for item in raw_data:
        if item['style']==red:
            red.append(item)
        elif item['style']==blue:
            blue_list.append(item)
        elif item['style']==hang:
            hang_list.append(item)
        elif item['style']==in_use:
            inuse_list.append(item)
e1_status=[]
#For e1 status
for x in raw_data_int:
    temp_str=str(x)
    if 'wanpipe' in temp_str:
        temp_status=x.find('font')
        temp_s=temp_status.get_text()
        e1_status.append(temp_s)
    else:
        pass

message2=""
for count,elem in enumerate(e1_status,1):
    message2+="============= E1#{} ================\n".format(count)
    message2+="\t\tstatus : {}".format(e1_status[count-1])
    message2+="\n"
server.starttls()
server.login("ngnnoc321@gmail.com","Cyber@321")
message="\nLahore Interconnect status(10.24.242.6)\n\tUp(idle) channels : {}\n\tinuse channels : {}\n\thang channels : {}\n\tdown channels : {}\n\t".format(len(blue_list),len(inuse_list),len(hang_list),len(red_list))
message2+=message



msg.attach(MIMEText(message2,'plain'))
final_body=msg.as_string()
filename="interconnect_data.txt"
attachment=open(filename,'rb')
part=MIMEBase('application','octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition',"attachment; filename= "+filename)
msg.attach(part)
final_body=msg.as_string()

server.sendmail(email_sender,email_reciever,final_body)
server.quit()