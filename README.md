# RedButton 2023
## Мы постарались максимально концептуально описать идеи реализации сервисов и их решения

##  Base76

Исходный концепт сервиса выглядел так

```python
    @app.route("/")
    def index():
        return render_template('/index.html')
    
    @app.route("/api/flag", methods = ["POST"])
    def flag():
        flag = request.get_json()["text"]
        if flag != "flag{PudgeAndBase76DonePizdone}":
            otv = "Time to drink!!!!"
            res={"answ":otv}
        else:
            otv = "YAAAAAY YOU WIN!!!"
            res={"answ":otv}
        return res
    
    def main():
        app.run(host='0.0.0.0', debug=True)
    
    
    @app.route("/api/encode", methods = ["POST"])
    def encode():
        arr = request.get_json()["text"]
        str = ""
        for i in arr:
            str += hex(int(i))[2:]
        b = str
        str = int(str, 16)
        c = str
        ost = []
        while True:
            ost.append(str%76)
            str //=76
            if str == 0:
                break
        ost.reverse()
        otv = ""
        for i in ost:
            otv += alph[i]
        otv = otv + "\n Time to drink!!!"
        res={"answ":otv}
        return res
```

Надо было раскодировать флаг, представленный на главной странице

```
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>BASE76</title>
            <link rel="stylesheet" href="static/style.css">
        </head>
        <body>
                <div id="hellp">   
                    <h1>
                        <i>
                            ВСЕМ ПРИВЕТ ЭТО САМЫЙ ЛУЧШИЙ САЙТ ДЛЯ КОДИРОВАНИЯ И ДЕКОДИРОВАНИЯ СООБЩЕНИЙ ПОПЫТАЙТЕ СВОЮ УДАЧУ И РАСКОДИРУЙТЕ СТРОКУ
                            ВоЭФдвнаеАю8К0ШюдЬвзЕшча9ШсЦпэЕ3пТёоЧееХ
                        </i>            
                    </h1>
                </div>
                <div id = "action">
                    <p>
                        <b>
                            ЗАКОДИРОВАТЬ
                        </b>
                        <input type="text">
                    </p>
                </div>
                <div id = "text">
                    <p>
                        <b>
                            <i id = "текст">
                                
                            </i>
                        </b>
                    </p>
                </div>
                <script src="https://code.jquery.com/jquery-3.6.1.min.js" integrity="sha256-o88AwQnZB+VDvE9tvIXrMQaPlFFSUTR+nldQm1LuPXQ=" crossorigin="anonymous"></script>
            <script src="static/script.js"> </script>
        </body>
    </html>
```

Достать алфавит можно одним запросом, а уже с алфавитом раскодировать флаг проблем не предоставит

```python
    import requests
    def find_pos(letter):
        for i in range(len(al)):
            if al[i] == letter:
                return i
    
    alph = 0
    
    for i in range(1, 76):
        alph += 76**i * i
    alph = [f"{b}"]
    json = {"text": alph}
    
    ip = 0
    
    r = requests.post(f"http://{ip}:5000/api/encode", json = json)
    alp = r.json()["answ"]
    
    al = ""
    for i in range(len(alp)-1, -1, -1):
        al += alp[i]
    
    c_fl = "ВоЭФдвнаеАю8К0ШюдЬвзЕшча9ШсЦпэЕ3пТёоЧееХ"
    
    flag = 0
    k = 0
    for i in range(len(c_fl)-1,-1,-1):
        flag += find_pos(c_fl[i])* (76**k)
        k+=1
    
    flag = bytes.fromhex(hex(flag)[2:]).decode()
    
    json = {"text": flag}
    r = requests.post(f"http://{ip}:5000/api/flag", json = json)
    
    print(r.text)
```

## Бинарный поиск или как мы хотели чтобы вы перебрали по красоте (terminal)

Исходный концепт сервиса выглядел так:
```python
  l = listen(9999)
    svr = l.wait_for_connection()

    print(l.sendline(b"hello my friend it is my secret server"))
    print(l.sendline(b"we have several commands use help"))
    while (True):
        line = l.recvline().decode('utf-8')

        # print(line[:-1] == "ls")
        workline = line[:-1]
        if workline == "ls":
            l.sendline(b"ls is tired")
        elif workline == "help":
            l.sendline(b" comand is :\n ls\n cd\n drink\n getflag\n")
        elif workline == "cd":
            l.sendline(b"cd it is dificalt to me")
        elif workline == "getflag":
            while (True):
                l.sendline(b"you need to use binary search to find the flag")
                for i in range(1, 1000):
                    l.send((str(i) + " ").encode())
                while (True):
                    number = l.recvline().decode('utf-8')
                    if int(number[:-1]) < 88:
                        l.sendline(b"more\n time to drink\n")
                        # вставить блокировку
                        jury.alert(team_id, sync=True)
                    elif int(number[:-1]) > 88:
                        l.sendline(b"less\n time to drink\n")
                        # вставить блокировку
                        jury.alert(team_id, sync=True)
                    elif int(number[:-1]) == 88:
                        l.sendline(b"flag{blablabla}")
                    else:
                        l.sendline(b"error\n time to drink\n")
                        # вставить блокировку
                        jury.alert(team_id, sync=True)
        else:
            l.sendline(b"time to drink")
            # вставить блокировку
            jury.alert(team_id, sync=True)

```

Мы надеялись что участники данного мероприятия вспомянят замечательную игру в угадай число и поймут что самым простым способом решения данного задания является применение алгоритма бинарного поиска... 
```
Место душности
Бинарный поиск - это алгоритм поиска элемента в отсортированном массиве путем деления массива пополам и сравнения искомого элемента с элементом в середине массива. Если искомый элемент меньше, чем элемент в середине, поиск продолжается в левой половине массива, иначе - в правой. Этот процесс повторяется до тех пор, пока искомый элемент не будет найден или не останется элементов для поиска.

Идея бинарного поиска заключается в том, что на каждом шаге алгоритм уменьшает область поиска в два раза, что позволяет быстро находить искомый элемент в отсортированном массиве. Этот метод поиска эффективен для больших массивов данных и имеет временную сложность O(log n), где n - количество элементов в массиве.
```

Применяете алгоритм и всё сразу становится отлично))) флаг получен , а много пить не пришлось)))

## Осинт на Великого (Lenin)
Исходный концепт сервиса выглядел так:
```python
 s = server(4444)
    while(True):
        server_conn = s.next_connection()
        server_conn.sendline(b"hello my friend in new osint task\nwhere is this muzhik standing?\n https://drive.google.com/file/d/1EQasJFDujaLIZJh-T3lbsdb4fU61zrV_/view?usp=sharing")
        server_conn.sendline(b"we have several commands use help: \nhints\n drink\nputflag\n")
        while(True):
            try:
                line= server_conn.recvline().decode('utf-8')
                workline = line[:-1]

                if workline =="help":
                    server_conn.sendline(b" comand is :\n hints\n drink\n putflag\n")

                elif workline == "putflag":
                    server_conn.sendline(b"give me flag")
                    flag=server_conn.recvline().decode('utf-8')
                    if flag == "flag{refer_to_Atomic_Heart}":
                        server_conn.sendline(b"You WIN!")
                    else:
                        server_conn.sendline(b"You Loose!")


                elif workline == "hints":
                    while(True):
                        server_conn.sendline(b"We have 6 hint for you. Give number hint please!")
                        for i in range(1,7):
                            server_conn.sendline((str(i)+" ").encode())
                        while(True):
                            server_conn.sendline(b"\n your number > ")
                            number=int(server_conn.recvline().decode('utf-8'))
                            if number ==1:
                                server_conn.sendline(b"time to drink!\n")
                                server_conn.sendline(b"It is located in Seversk")
                            elif number ==2:
                                server_conn.sendline(b"time to drink!\n")
                                server_conn.sendline(b"Located on Communist Avenue")
                            elif number ==3:  
                                server_conn.sendline(b"Near house number 51")
                                server_conn.sendline(b"time to drink!\n")

                            elif number ==4:  
                                server_conn.sendline(b"time to drink!\n")

                                server_conn.sendline(b"https://www.youtube.com/watch?v=wpExy1AmZ-8")
                            elif number ==5:  
                                server_conn.sendline(b"time to drink!\n")
 
                                server_conn.sendline(b"The flag is on Google map")
                            elif number ==6:  
                                server_conn.sendline(b"time to drink!\n")
            
                                server_conn.sendline(b"There are no more hints, but you can check the flag using putflag")
                            else:
                                server_conn.sendline(b"wrong number\n time to drink\n")
                               
                else:
                    server_conn.sendline(b"time to drink")
                   
            except:
                pass
```
Сервис в котором вам надо было используя подсказки найти Ленина из Северска на Google maps и в коментариях найти флаг)))
## Капча (picture)
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>SibirCTF Blog</title>
</head>
<body>
    <div class="row">
        <div class="col-md-6 offset-md-3">
            <h1> This is the last stage in our competitions.</h1>
            <h1> Rewrite the text from the image below in the URL path. </h1>
            <h1> This will be the end of the game.<h1/>
            <img src="{{url_for('static', filename='capcha.png')}}"  width="1000" height="400"" alignИсходный концепт сервиса выглядел так:="middle" />
          
        </div>
    </div>
</body>
</html>
```
![](capcha.png)
Просто сайт с картинкой с которой надо было переписать символы в url_path вот так  <br> `<url>:1111/@!ZKBf3jGWrtK9M6zILxwGv__0tf5eCaSod6eSJX1tyn0XnHji` </br>
И наш сервер выдал вам бы флаг

## Итоги которые были сделаны авторами на основе проведённого мероприятия
Авторами сервисов были @sib_coder && @fanbrawla для нас это был первый опыт работы организаторами подобного мероприятия. <br/>
Основными недочётами в проведении были :
1) Плохая связь между сервисами и ноутами участников - Поправим)
2) Слишком сложные сервисы - Постараемся поправить)
3) Слишком мало категорий - специально для вас мы не будем добавлять pwn мы же не изверги (хотя всё может быть) :)
Мы будем очень рады если вы напишите нам в лс в телеграмм с обратной связью или какими нибудь предложениями по улучшениям формата мероприятия)
