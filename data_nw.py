import requests
from bs4 import BeautifulSoup
import re
s=requests.session()
response = s.get("http://10.24.242.6/index.php")

auth = {
    'reserved_username':'admin',
    'reserved_password':'n3tbord3r557'
}
s.post('http://10.24.242.6/index.php',data=auth)
response = s.get('http://10.24.242.6/fusionpbx/tdm_status.php?embedded=NSC')

soup=BeautifulSoup(response.text,"html.parser")
# print(soup)
data_network_status=soup.find_all(attrs={'color':'white'})
dt_nt_list=[]
for x in data_network_status:
	if x.get_text()=='i          ' or x.get_text()=='s          ' or x.get_text()=='u          ' or x.get_text()=='S          ' or len(x.get_text())==1:
		pass
	else:
		dt_nt_list.append(x.get_text())

stp_1="Physical : {}, Data layer : {}, Network Layer : {}".format(dt_nt_list[8],dt_nt_list[9],dt_nt_list[10])
stp_2="Physical : {}, Data layer : {}, Network Layer : {}".format(dt_nt_list[12],dt_nt_list[13],dt_nt_list[14])

