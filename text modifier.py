import re

'''
this program processes html text files from https://www.crhallberg.com/cah/
it turns them into formats sutable for emailing to cucumbercards
please note the plaintext files contain questions and awnsers
'''

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

file_name = input("what is the filename?\n    ")
file_save_name = input("what should the edit be saved as?\n    ")

file = open(file_name,"r+")
file_text = file.read()
mid_file = file_text.splitlines()

a = len(mid_file)
out_text = ""
b = 0
print (mid_file)

while a>0:
    out_text = out_text+mid_file[b]
    out_text = out_text+"\n"
    a=a-1
    b=b+1
print("====================")
print(out_text)
out_text = striphtml(out_text)

save_file = open("%s.txt"%file_save_name,"w")
save_file.write(out_text)
save_file.close()
