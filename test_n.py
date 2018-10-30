import requests
from bs4 import BeautifulSoup
import csv
import smtplib
email_sender="ngnnoc321@gmail.com"
email_reciever="ngn-noc@cyber.net.pk"
server=smtplib.SMTP('smtp.gmail.com',587)
# Start_urls=['http://10.24.242.6/SAFe/fs_tdmgw_status']
# LOGIN_URL = "http://10.24.242.6/index.php"
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
raw_data=soup.find_all(attrs={'align':'center','width':'10px','height':'14px'})
for x in range(19):
    raw_data.pop()
# for x in range(16):
#     print("\n")










red_list=[]
inuse_list=[]
hang_list=[]
blue_list=[]
# blue='background-color:#2B60DE'
# red='background-color:#E42217'
# hang='background-color:#95B9C7'
# in_use='background-color:#348017'
for item in raw_data:
        if item['style']==red:
            red.append(item)
        elif item['style']==blue:
            blue_list.append(item)
        elif item['style']==hang:
            hang_list.append(item)
        elif item['style']==in_use:
            inuse_list.append(item)


server.starttls()
server.login("ngnnoc321@gmail.com","Cyber@321")
message="Lahore Interconnect status(10.24.242.6)\n\tUp(idle) channels : {}\n\tinuse channels : {}\n\thang channels : {}\n\tdown channels : {}\n\t".format(len(blue_list),len(inuse_list),len(hang_list),len(red_list))
server.sendmail(email_sender,email_reciever,message)
server.quit()


