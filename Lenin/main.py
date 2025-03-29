from pwn import *

l = listen(9999) 
svr = l.wait_for_connection()


print(l.sendline(b"hello my friend in new osint task"))
#нужна ссылка на фото выложенное на google disk
print(l.sendline(b"we have several commands use help"))
while(True):
    line= l.recvline().decode('utf-8')
   
   #print(line[:-1] == "ls")
    workline = line[:-1]
    
    if workline =="help":
        l.sendline(b" comand is :\n hints\n drink\n putflag\n")

    elif workline == "putflag":
        l.sendline(b"give me flag")
        flag=l.recvline().decode('utf-8')
        if flag[:-1]=="flag{refer_to_Atomic_Heart}":
            l.sendline(b"You WIN!")
        else:
            l.sendline(b"You Loose!")
            #вставить блокировку


    elif workline == "hints":
        while(True):
            l.sendline(b"We have 6 hint for you. Give number hint please!")
            for i in range(1,7):
                l.send((str(i)+" ").encode())
                #Замени ответы на нужные тебе
            while(True):
                number=l.recvline().decode('utf-8')
                if int(number[:-1]) ==1:
                    l.sendline(b"more\n time to drink\n")
                    #вставить блокировку
                elif int(number[:-1]) ==2:
                    l.sendline(b"less\n time to drink\n")
                    #вставить блокировку
                elif int(number[:-1]) ==3:  
                    l.sendline(b"")
                    #вставить блокировку
                elif int(number[:-1]) ==4:  
                    l.sendline(b"")
                    #вставить блокировку
                elif int(number[:-1]) ==5:  
                    l.sendline(b"")
                    #вставить блокировку
                elif int(number[:-1]) ==6:  
                    l.sendline(b"")
                    #вставить блокировку
                else:
                    l.sendline(b"wrong number\n time to drink\n")
                    #вставить блокировку
    else:
        l.sendline(b"time to drink")
        #вставить блокировку