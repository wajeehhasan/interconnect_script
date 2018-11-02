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
	if x.get_text()=='S          ' or x.get_text()=='X          ' or x.get_text()=='i          ' or x.get_text()=='D          ' or x.get_text()=='r          ' or  x.get_text()=='r          ' or x.get_text()=='d          ' or x.get_text()=='p          ' or x.get_text()=='m          ' or x.get_text()=='u          ' or x.get_text()=='t          ' or x.get_text()=='h          ' or x.get_text()=='h          ' or  x.get_text()=='c          ' or x.get_text()=='r          ' or x.get_text()=='s          ' or  x.get_text()=='C          ' or  x.get_text()=='L          ' or x.get_text()=='?          ':
		pass
	else:
		dt_nt_list.append(x.get_text())
for x in range(19):
	dt_nt_list.pop()
print(dt_nt_list)

stp_1="Physical : {}, Data layer : {}, Network Layer : {}".format(dt_nt_list[8],dt_nt_list[9],dt_nt_list[10])
stp_2="Physical : {}, Data layer : {}, Network Layer : {}".format(dt_nt_list[12],dt_nt_list[13],dt_nt_list[14])













# =========================================================================
# if x.get_text()=='S          ' or  x.get_text()=='X          ' or  x.get_text()=='i          ' orx.get_text()=='D          ' or x.get_text()=='r          ' or  x.get_text()=='r          ' orx.get_text()=='d          ' or x.get_text()=='p          ' or .get_text()=='m          ' or x.get_text()=='u          ' or x.get_text()=='t          ' or x.get_text()=='h          ' or x.get_text()=='h          ' or  x.get_text()=='c          ' or x.get_text()=='r          ' or x.get_text()=='s          ' or  x.get_text()=='C          ' or  x.get_text()=='L          ' or x.get_text()=='?          ':

