const ввод = document.querySelector("input")

ввод.addEventListener("keyup", ШИФРОВАНИЕ)

var музыка = new Audio('./static/Pudge_-_Fresh_meat_!!!_[song].mp3')

document.body.addEventListener("mousemove", function () {
    музыка.play()
})

const ОТВЕТ = document.getElementById("текст");

алфавит = "אבגדהוזחטיכךלמםנןסעפףצץקרשתאבגדהוזחטיכךלמםנןסעפףצץקרשתאבגדהוזחטיכךלמםנןסעפףצץקרשת";

let кодировщик = new TextEncoder();

function БайтыВТекст(bytes) {
    return Array.from(
      bytes,
      byte => byte.toString(16).padStart(2, "0")
    ).join("");
}

function ВБазаСтандарт(число){
    алф = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"];
    число = число.split("")
    ответ = 0
    длина = число.lenght - 1
    for (цифр in число){
        позиция = 0;
        for (цифра in алф){
            if (цифр == цифра){
                ответ += позиция*(Math.pow(16, длина))
                длина --;
            }
            позиция++;
        } 
    }
}


function ИзБазы76(база76) {
    база76 = "Добавлю позже!(комментарий)";
    return alert(база76);
}

//function проверка флага(событие){
//    {"text":"flag"}
//    if (событие.code == "Enter") {
//        let исходное_сообщение = ввод.value;
//        let отправить_данные = JSON.stringify({
//            text:исходное_сообщение
//        })
//        $.ajax({
//            type:"POST",
//            url:"./api/flag",
//            data: отправить_данные,
//            contentType: "application/json",
//            dataType: "json",
//            success: function(ответ){
//                ОТВЕТ.innerHTML=(ответ["answ"])
//            }
//        })
//    }
//}

function ШИФРОВАНИЕ(событие){
    if (событие.code == "Enter") {
//      {"text":["int(text)"]}
        let исходное_сообщение = ввод.value;
        исходное_сообщение1 = Array.from(кодировщик.encode(исходное_сообщение));
        let отправить_данные = JSON.stringify({
            text:исходное_сообщение1
        })
        $.ajax({
            type:"POST",
            url:"./api/encode",
            data: отправить_данные,
            contentType: "application/json",
            dataType: "json",
            success: function(ответ){
                ОТВЕТ.innerHTML=(ответ["answ"])
            }
        })
    }
}
