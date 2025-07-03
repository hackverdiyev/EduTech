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
var solved_prob=document.getElementsByClassName("solved_problems")[0] ;
var unsolved_prob=document.getElementsByClassName("unsolved_problems")[0] ;
var all_table=document.getElementsByClassName("all_problems_table")[0] ;
var solved_table=document.getElementsByClassName("solved_problems_table")[0] ;
var unsolved_table=document.getElementsByClassName("unsolved_problems_table")[0] ;

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
    solved_table.style.display = "none";
    unsolved_table.style.display = "none";
    all_prob.style.background = "white";
    all_prob.style.color = "#4a4abd";
    solved_prob.style.background = "#4a4abd";
    solved_prob.style.color = "white";
    unsolved_prob.style.background = "#4a4abd";
    unsolved_prob.style.color = "white";
}
function show_solved_problems(){
    all_table.style.display = "none";
    solved_table.style.display = "table";
    unsolved_table.style.display = "none";
    all_prob.style.background = "#4a4abd";
    all_prob.style.color = "white";
    solved_prob.style.background ="white";
    solved_prob.style.color = "#4a4abd";
    unsolved_prob.style.background = "#4a4abd";
    unsolved_prob.style.color = "white";
}
function show_unsolved_problems(){
    all_table.style.display = "none";
    solved_table.style.display = "none";
    unsolved_table.style.display = "table";
    all_prob.style.background = "#4a4abd";
    all_prob.style.color = "white";
    solved_prob.style.background = "#4a4abd";
    solved_prob.style.color = "white";
    unsolved_prob.style.background = "white";
    unsolved_prob.style.color = "#4a4abd";
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

document.addEventListener("keydown", function(event){
    if(event.key == "Escape"){
        if(document.getElementById("view_div").style.display == "block"){
            document.getElementById("view_div").style.display = "none";
        }
    }
})


