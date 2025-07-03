let menu = document.querySelector("#menu-icon");
let navlist = document.querySelector('.navbar-all-elements');
let prob_btn = document.querySelector(".icon_opening");
let prob_icn = document.querySelector("#problem_nav_feature_icon");
let drop_div = document.querySelector('.dropdown-content');

var say=0;
prob_btn.onclick = () => {
    if(say==0){
        drop_div.style.display="block";
        say=1;
    }
    else{
        drop_div.style.display="none";
        say=0;
    }
    prob_icn.classList.toggle("bi-chevron-up");
};

menu.onclick = () => {
    menu.classList.toggle("bx-x");
    navlist.classList.toggle('open');
};