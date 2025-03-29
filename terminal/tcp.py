from pwn import *

l = listen(9999) 
svr = l.wait_for_connection()


print(l.sendline(b"hello my friend it is my secret server"))
print(l.sendline(b"we have several commands use help"))
while(True):
    line= l.recvline().decode('utf-8')
   
   #print(line[:-1] == "ls")
    workline = line[:-1]
    if workline == "ls":
        l.sendline(b"ls is tired")
    elif workline =="help":
        l.sendline(b" comand is :\n ls\n cd\n drink\n getflag\n")
    elif workline == "cd":
        l.sendline(b"cd it is dificalt to me")
    elif workline == "getflag":
        while(True):
            l.sendline(b"you need to use binary search to find the flag")
            for i in range(1,1000):
                l.send((str(i)+" ").encode())
            while(True):
                number=l.recvline().decode('utf-8')
                if int(number[:-1]) < 88:
                    l.sendline(b"more\n time to drink\n")
                    #вставить блокировку
                elif int(number[:-1]) > 88:
                    l.sendline(b"less\n time to drink\n")
                    #вставить блокировку
                elif int(number[:-1]) == 88:  
                    l.sendline(b"flag{blablabla}")
                    #обязательно залогировать флаг иначе будет не оч приятно
                else:
                    l.sendline(b"error\n time to drink\n")
                    #вставить блокировку
    else:
        l.sendline(b"time to drink")
        #вставить блокировку
