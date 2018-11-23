import commands
import datetime
secret_KEY=6668


RawDT= str(datetime.datetime.now().replace(second=0,microsecond=0))
#numDT = int(str(RawDT.replace("-","").replace(":","").replace(" ",""))[:-2])
numDT = hash(RawDT)
print ("DEBUG current time hashed: "+str(numDT))

secretValue=(numDT)%secret_KEY

#print secretValue
newP= (secretValue%1000)+3000

interface ="ens33"

new_portnum=newP
print ("DEBUG new port gen: "+str(new_portnum))




#start portspoof
low= new_portnum-1
high= new_portnum+1

commands.getoutput("iptables -F")
commands.getoutput("iptables -t nat -F")

#output = commands.getoutput("iptables -t nat -A PREROUTING -i "+ interface+" -p tcp -m tcp -m multiport --dports 2000:"+str(low)+","+str(high)+":65535  -j REDIRECT --to-ports 4444")
output = commands.getoutput("iptables -t nat -A PREROUTING -i "+interface+" -p tcp -m tcp --dport 1:"+str(low)+" -j REDIRECT --to-ports 4444")
output = commands.getoutput("iptables -t nat -A PREROUTING -i "+interface+" -p tcp -m tcp --dport "+str(high)+":65535 -j REDIRECT --to-ports 4444")
print output

commands.getoutput("portspoof -D")







chgSSHconfig = commands.getoutput("sed -i 's/^Port .*/Port "+str(new_portnum)+"/g'  /etc/ssh/sshd_config")
print chgSSHconfig

chgSEmanager = commands.getoutput("semanage port -a -t ssh_port_t -p tcp "+str(new_portnum))
print("semanage command ran: "+ chgSEmanager)

#TODO: update iptables


#restart service
print commands.getoutput("service sshd restart")



