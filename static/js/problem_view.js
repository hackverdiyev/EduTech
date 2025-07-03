other_report=document.getElementById("other_report_cont");
textarea=document.getElementById("report_other_textarea");

other_report.addEventListener("change", function(){
    if(other_report.checked){
        textarea.disabled=false;
    }
    else{
        textarea.disabled=true;
    }
})

let solution_btn = document.querySelector(".solution_context_btn_open");
let solution_span = document.querySelector(".solution_cont_span");
let solution_icn = document.querySelector("#feature_icon");
let solution_div = document.querySelector('.solution_context_container');

var say=0;

if (solution_btn!=null) solution_btn.onclick = () => {
    if(say==0){
        solution_span.innerHTML="Həlli gizlət"
        say=1;
    }
    else{
        solution_span.innerHTML="Həlli göstər"
        say=0;
    }
    solution_icn.classList.toggle("bi-chevron-up");
    solution_div.classList.toggle("opened_solution");
};

function close_div_ai(){
    document.getElementsByClassName("view_ai")[0].style.display="none";
}


if(document.getElementById("asking_ai")!=null){
    var words=document.getElementById("asking_ai").dataset.aiId,part,offset=0,forwards=true,skip_count=0,skip_delay=15,speed=70;
    var wordflick=function(){
    setInterval(function(){
        if(forwards && offset>=words.length){
            ++skip_count;
            if (skip_count==skip_delay) {
                forwards = false;
                skip_count = 0;
            }
        }
        part=words.substr(0, offset);
        if (skip_count==0 && forwards) offset++;
        $('.asking_ai').text(part);
    },speed);
    };
    $(document).ready(function(){
    wordflick();
    });
    let utterance = new SpeechSynthesisUtterance();
    utterance.lang='en-US';
    utterance.text = words;
    utterance.voice = window.speechSynthesis.getVoices()[0];
    utterance.pitch = 2.0; 
    utterance.rate = 1.0; 
    utterance.volume = 1.0;
    window.speechSynthesis.speak(utterance);
}