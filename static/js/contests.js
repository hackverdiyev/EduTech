document.addEventListener("DOMContentLoaded", function(){
    numbers=document.getElementsByClassName("number0");
    numbers1=document.getElementsByClassName("number1");
    numbers2=document.getElementsByClassName("number2");
    for(var i=1; i<=numbers.length; i++){
        numbers[i-1].innerHTML=i;
    }
    for(var i=1; i<=numbers1.length; i++){
        numbers1[i-1].innerHTML=i;
    }
    for(var i=1; i<=numbers2.length; i++){
        numbers2[i-1].innerHTML=i;
    }
})

var all_prob=document.getElementsByClassName("all_problems")[0] ;
var chat=document.getElementsByClassName("chat")[0] ;
var all_table=document.getElementsByClassName("all_problems_table")[0] ;
var chat_div=document.getElementsByClassName("chat_messages")[0] ;

function open_view(k){
    var view_div = document.querySelector('.view_page'+k.toString());
    view_div.style.display = "block";
    view_div.animate([{opacity:'0.0'}, {opacity:'1.0'}],
    {duration: 500, fill:'forwards'});
}

function close_view(k){
    var view_div = document.querySelector('.view_page'+k.toString());
    view_div.style.display = "none";
}


function show_all_problems(){
    all_table.style.display = "table";
    chat_div.style.display = "none";
    all_prob.style.background = "white";
    all_prob.style.color = "#4a4abd";
    chat.style.background = "#4a4abd";
    chat.style.color = "white";
}

function show_chat(){
    all_table.style.display = "none";
    chat_div.style.display = "block";
    all_prob.style.background = "#4a4abd";
    all_prob.style.color = "white";
    chat.style.background = "white";
    chat.style.color = "#4a4abd";
}


document.addEventListener('DOMContentLoaded', function () {
    const viewButtons = document.querySelectorAll('.view_problem');
    const closeButtons = document.querySelectorAll('.close_viewpage');
    viewButtons.forEach(button => {
        button.addEventListener('click', function () {
            const problemId = this.dataset.problemId;
            open_view(problemId);
        });
    });
    closeButtons.forEach(button => {
        button.addEventListener('click', function () {
            const problemId = this.dataset.problemId;
            close_view(problemId);
        });
    });
});

