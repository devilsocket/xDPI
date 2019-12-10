from pcap import findalldevs, pcap
from struct import unpack
from socket import inet_ntoa, ntohs
import datetime

def flagScanner(flags):
		result = []
		if ( flags & 1 ) != 0:
			result.append('fin')
		if ( flags & 2 ) != 0:
			result.append('syn')
		if ( flags & 4 ) != 0:
			result.append('rst')
		if ( flags & 8 ) != 0:
			result.append('psh')
		if ( flags & 16 ) != 0:
			result.append('ack')
		if ( flags & 32 ) != 0:
			result.append('urg')
		if ( flags & 64 ) != 0:
			result.append('ece')
		if ( flags & 128 ) != 0:
			result.append('cwr')
		return result

def eth_addr (a) :
  b = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (ord(a[0]) , ord(a[1]) , ord(a[2]), ord(a[3]), ord(a[4]) , ord(a[5]))
  return b
def execute(sDevice):
	sessions = {}
	pFilter = 'tcp port 80'
	p = pcap(name=sDevice, snaplen=65535, promisc=True, timeout_ms=0)
	p.setfilter(pFilter, 0)
	p.setnonblock()
	while 1:
		for pkt in p.readpkts():
			ts = datetime.datetime.fromtimestamp(pkt[0]).strftime("%Y-%m-%d %H:%M:%S")
			eth = unpack('!6s6sH' , pkt[1][:14])
			src_mac = eth_addr(str(eth[0]))
			dst_mac = eth_addr(str(eth[1]))
			protocol = ntohs(eth[2])
			if protocol == 8:
				ip_header = pkt[1][14:20+14]
				iph = unpack('!BBHHHBBH4s4s' , ip_header)
				version_ihl = iph[0]
				version = version_ihl >> 4
				ihl = version_ihl & 0xF
				iph_length = ihl * 4
				ttl = iph[5]
				protocol = iph[6]
				s_addr = inet_ntoa(iph[8])
				d_addr = inet_ntoa(iph[9])
				if protocol == 6 :
					t = iph_length + 14
					tcp_header = pkt[1][t:t+20]
					tcph = unpack('!HHLLBBHHH' , tcp_header)  
					#print(tcph)  
					source_port = tcph[0]
					dest_port = tcph[1]
					sequence = tcph[2]
					acknowledgement = tcph[3]
					doff_reserved = tcph[4]
					flags = flagScanner(tcph[5])
					tcph_length = doff_reserved >> 4		             
					h_size = 14 + iph_length + tcph_length * 4
					data_size = len(pkt[1]) - h_size
					data = pkt[1][h_size:]
					unikey = '{}:{}>{}:{}'.format(s_addr,source_port,d_addr,dest_port)
					
					print('*'*30)
					print(flags)
					print(data)
					print(pkt[1])
					"""
					if source_port == 80:
						print('*'*30)
						print(flags)
						if 'syn' in flags:
							if unikey in sessions:
								del sessions[unikey]
							if unikey not in sessions:
								sessions[unikey]=data
						elif 'fin' in flags:
							if unikey in sessions:
								sessions[unikey]+=data
								complete_data = sessions[unikey]
								print(complete_data)
								del sessions[unikey]
						else:
							if unikey in sessions:
								sessions[unikey]+=data


					
					if 'syn' in flags and unikey not in sessions:
						sessions[unikey]=data
					elif 'syn' in flags and unikey in sessions:
						del sessions[unikey]
					elif 'fin' in flags and unikey in sessions:
						complete_data = sessions[unikey]
						del sessions[unikey]
						print(complete_data)
					else:
						if unikey in sessions:
							sessions[unikey]+=data
					"""




	return 1


if __name__ == '__main__':
	selected_device = False
	devices = findalldevs()
	print('[+] available devices:-')
	for dCount, device in enumerate(devices):
		dCount+=1
		print('[D]',dCount, device)
	while 1:	
		dInput = input('[+] Enter a device to capture\n>')
		if dInput in devices:
			selected_device = dInput
			print('[+] selected {} as the target device'.format(dInput))
			break
		else:
			print('[X] please select a valid device from the choices')
	execute(selected_device)
