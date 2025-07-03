document.addEventListener("DOMContentLoaded", function(){
    numbers=document.getElementsByClassName("number0");
    numbers1=document.getElementsByClassName("number1");
    for(var i=1; i<=numbers.length; i++){
        numbers[i-1].innerHTML=i;
    }
    for(var i=1; i<=numbers1.length; i++){
        numbers1[i-1].innerHTML=i;
    }
})

var problems_added_btn=document.getElementsByClassName("problems_added")[0];
var solutions_added_btn=document.getElementsByClassName("solutions_added")[0];
var profile_btn=document.getElementsByClassName("account_about")[0];
var pass_change_btn=document.getElementsByClassName("pass_change")[0];
var profile_div=document.getElementsByClassName("profile_about")[0];
var problems_div=document.getElementsByClassName("problems")[0];
var solution_div=document.getElementsByClassName("solutions")[0];
var pass_div=document.getElementsByClassName("passcode_change")[0];


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

function open_view1(k){

    var view_div = document.querySelector('.view_page1'+k.toString());
    view_div.style.display = "block";
    view_div.animate([{opacity:'0.0'}, {opacity:'1.0'}],
    {duration: 500, fill:'forwards'});

}
function close_view1(k){

    var view_div = document.querySelector('.view_page1'+k.toString());
    view_div.style.display = "none";
    
}


function show_pass(){
    problems_div.style.display = "none";
    solution_div.style.display = "none";
    pass_div.style.display = "block";
    profile_div.style.display = "none";
    problems_added_btn.style.background = "#4a4abd";
    problems_added_btn.style.color = "white";
    solutions_added_btn.style.background = "#4a4abd";
    solutions_added_btn.style.color = "white";
    pass_change_btn.style.background = "white";
    pass_change_btn.style.color = "#4a4abd";
    profile_btn.style.background = "#4a4abd";
    profile_btn.style.color = "white";
}

function show_solutions(){
    problems_div.style.display = "none";
    solution_div.style.display = "block";
    pass_div.style.display = "none";
    profile_div.style.display = "none";
    problems_added_btn.style.background = "#4a4abd";
    problems_added_btn.style.color = "white";
    solutions_added_btn.style.background = "white";
    solutions_added_btn.style.color = "#4a4abd";
    pass_change_btn.style.background = "#4a4abd";
    pass_change_btn.style.color = "white";
    profile_btn.style.background = "#4a4abd";
    profile_btn.style.color = "white";
}

function show_profile(){
    problems_div.style.display = "none";
    solution_div.style.display = "none";
    pass_div.style.display = "none";
    profile_div.style.display = "block";
    problems_added_btn.style.background = "#4a4abd";
    problems_added_btn.style.color = "white";
    solutions_added_btn.style.background = "#4a4abd";
    solutions_added_btn.style.color = "white";
    pass_change_btn.style.background = "#4a4abd";
    pass_change_btn.style.color = "white";
    profile_btn.style.background = "white";
    profile_btn.style.color = "#4a4abd";
}

function show_problems(){
    problems_div.style.display = "block";
    solution_div.style.display = "none";
    pass_div.style.display = "none";
    profile_div.style.display = "none"
    problems_added_btn.style.background = "white";
    problems_added_btn.style.color = "#4a4abd";
    solutions_added_btn.style.background = "#4a4abd";
    solutions_added_btn.style.color = "white";
    pass_change_btn.style.background = "#4a4abd";
    pass_change_btn.style.color = "white";
    profile_btn.style.background = "#4a4abd";
    profile_btn.style.color = "white";
}

document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("profile_img");
    const image = document.getElementById("photo_uploaded_preview");

    input.addEventListener("change", function () {
        const input_file = input.files[0];
        if (input_file) {
            const reader = new FileReader();

            reader.onload = function (event) {
                image.src = event.target.result;
            }

            reader.readAsDataURL(input_file);
        } else {
            image.src = "/static/images/{{ islogin.profile_photo }}";
        }
    });
});


if(profile_div.dataset.defaultId=='profile') show_profile();
else if(profile_div.dataset.defaultId=='password') show_pass();