var contest_btn=document.getElementsByClassName("contest_btn")[0];
var create_contest_btn=document.getElementsByClassName("create_contest_btn")[0];
var group_participants_btn=document.getElementsByClassName("group_participants_btn")[0];
var group_settings_btn=document.getElementsByClassName("group_settings_btn")[0];

var contest_div=document.getElementsByClassName("contests")[0];
var create_contest_div=document.getElementsByClassName("create_contest")[0];
var group_participants_div=document.getElementsByClassName("group_participants")[0];
var group_settings_div=document.getElementsByClassName("group_settings")[0];


function open_contest(){
    contest_div.style.display="block";
    group_participants_div.style.display="none";

    contest_btn.style.backgroundColor="#313197";
    group_participants_btn.style.backgroundColor="#4a4abd";
    
    if(create_contest_btn!=undefined){
        create_contest_div.style.display="none";
        group_settings_div.style.display="none";

        create_contest_btn.style.backgroundColor="#4a4abd";
        group_settings_btn.style.backgroundColor="#4a4abd";
    }
}

function open_group_part(){
    contest_div.style.display="none";
    group_participants_div.style.display="block";

    contest_btn.style.backgroundColor="#4a4abd";
    group_participants_btn.style.backgroundColor="#313197";
    
    if(create_contest_btn!=undefined){
        create_contest_div.style.display="none";
        group_settings_div.style.display="none";
        
        create_contest_btn.style.backgroundColor="#4a4abd";
        group_settings_btn.style.backgroundColor="#4a4abd";
    }
}

function open_create(){
    contest_div.style.display="none";
    group_participants_div.style.display="none";

    contest_btn.style.backgroundColor="#4a4abd";
    group_participants_btn.style.backgroundColor="#4a4abd";
    
    if(create_contest_btn!=undefined){
        create_contest_div.style.display="block";
        group_settings_div.style.display="none";

        create_contest_btn.style.backgroundColor="#313197";
        group_settings_btn.style.backgroundColor="#4a4abd";
    }
}

function open_settings(){
    contest_div.style.display="none";
    group_participants_div.style.display="none";

    contest_btn.style.backgroundColor="#4a4abd";
    group_participants_btn.style.backgroundColor="#4a4abd";
    
    if(create_contest_btn!=undefined){
        create_contest_div.style.display="none";
        group_settings_div.style.display="block";

        create_contest_btn.style.backgroundColor="#4a4abd";
        group_settings_btn.style.backgroundColor="#313197";
    }
}

function open_delete_group(){
    var delete_div = document.querySelector('.delete_group_div');
    delete_div.style.display="flex";
    delete_div.animate([{opacity:'0.0'}, {opacity:'1.0'}],
    {duration: 500, fill:'forwards'});
}

function close_delete_group(){
    var delete_div = document.querySelector('.delete_group_div');
    delete_div.style.display="none";
}

function open_delete_user(k){
    var delete_div = document.querySelector('.delete_user_div'+k.toString());
    delete_div.style.display="flex";
    delete_div.animate([{opacity:'0.0'}, {opacity:'1.0'}],
    {duration: 500, fill:'forwards'});
}

function close_delete_user(k){
    var delete_div = document.querySelector('.delete_user_div'+k.toString());
    delete_div.style.display="none";
}

if(contest_div.dataset.defaultId==1) open_contest();
else if(contest_div.dataset.defaultId==2) open_group_part();
else if(contest_div.dataset.defaultId==3) open_create();
else if(contest_div.dataset.defaultId==4) open_settings();

document.addEventListener("keydown", function(event){
    if(event.key == "Escape"){
        if(document.getElementById("delete_div_cont_id").style.display == "flex"){
            console.log(1);
            document.getElementById("delete_div_cont_id").style.display = "none";
        }
    }
})