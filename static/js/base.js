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

document.addEventListener('DOMContentLoaded', function () {
    const viewButtons = document.querySelectorAll('.view_problem');
    const closeButtons = document.querySelectorAll('.close_viewpage');
    const lately_added_div = document.getElementsByClassName("base_lately_added")[0];
    var problem_count = parseInt(lately_added_div.dataset.countId);
    var numbers=document.getElementsByClassName("number0");
    for(var i=0; i<10; i++){
        numbers[i].innerHTML=problem_count;
        problem_count--;
    }
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

