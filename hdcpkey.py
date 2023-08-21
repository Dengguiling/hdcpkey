"""
hdcpkey generator
"""
import os
import requests
from bs4 import BeautifulSoup


# block
head = "01000000"
ksv = ""
key = ""
hash = "0000000000000000000000000000000000000000"


def str2hex(s, reverse=1):
	if reverse <= 0:
		print("reverse error: %d" % reverse)
		return []
	print("reverse: ", reverse)
	print("s: ", s)

	data = []
	while s:
		tmp1 = s[ : reverse * 2]

		if reverse > 1:
			tmp_list = []
			while tmp1:
				tmp2 = tmp1[:2]
				tmp_list.append(int(tmp2, 16))
				tmp1 = tmp1[2:]
			tmp_list.reverse()
			data.extend(tmp_list)
		else:
			data.append(int(tmp1, 16))
		
		s = s[reverse * 2 : ]
	
	return data
	

def generate_ksv_and_key():
	global ksv, key

	html = requests.get("https://frigolit.net/tools/hdcp-keygen?k=")
	soup = BeautifulSoup(html.text, "html.parser")
	table = soup.find("table")
	# print(table)
	tmp = []
	for row in table.tbody.find_all("tr"):
		for cell in row.find_all("td"):
			tmp.append(cell.text.strip())
	# print(tmp)
	ksv = str(tmp[0])
	key = str(tmp[1])


def main():
	generate_ksv_and_key()

	data = str2hex(head) + str2hex(ksv, 5) + str2hex("000000") + str2hex(key, 7) + str2hex(hash)

	# debug
	i = 0
	for d in data:
		if i and not i % 16:
			print(" ")
		print("0x%02X " % d, end='')
		i += 1
	
	with open("./hdcpkey"+ f"_{ksv}" +".bin", "wb+") as f:
		f.write(bytearray(data))


if __name__ == "__main__":
	main()
