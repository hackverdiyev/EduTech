var say_female=0;
var say_male=1;
function choose_male(){
    if(say_male == 0){
        document.getElementsByClassName("male_option_ai")[0].style.color = "white";
        document.getElementsByClassName("male_option_ai")[0].style.backgroundColor = "rgb(34, 90, 150)";
        document.getElementsByClassName("female_option_ai")[0].style.color = "rgb(248, 6, 6)";
        document.getElementsByClassName("female_option_ai")[0].style.backgroundColor = "white";
        say_male=1;
        say_female=0;
    }
    else{
        document.getElementsByClassName("male_option_ai")[0].style.color = "rgb(34, 90, 150)";
        document.getElementsByClassName("male_option_ai")[0].style.backgroundColor = "white";
        say_male=0;
    }
}

function choose_female(){
    if(say_female == 0){
        document.getElementsByClassName("male_option_ai")[0].style.color = "rgb(34, 90, 150)";
        document.getElementsByClassName("male_option_ai")[0].style.backgroundColor = "white";
        document.getElementsByClassName("female_option_ai")[0].style.backgroundColor = "rgb(248, 6, 6)";
        document.getElementsByClassName("female_option_ai")[0].style.color = "white";
        say_female=1;
        say_male=0;
    }
    else{
        document.getElementsByClassName("female_option_ai")[0].style.color = "rgb(248, 6, 6)";
        document.getElementsByClassName("female_option_ai")[0].style.backgroundColor = "white";
        say_female=0;
    }
}

document.getElementById("text_for_ai").addEventListener("keyup", function(){
    if(document.getElementById("text_for_ai").value.length>=0){
        document.getElementsByClassName("send_txt_msg_toai")[0].style.display="block";
        document.getElementsByClassName("voice_msg_toai")[0].style.display="none";
    }
    if(document.getElementById("text_for_ai").value.length==0){
        document.getElementsByClassName("send_txt_msg_toai")[0].style.display="none";
        document.getElementsByClassName("voice_msg_toai")[0].style.display="block";
    }
})

var say_mic=0;
const GetSpeech = (k) => {
    const SpeechRecognition =  window.SpeechRecognition || window.webkitSpeechRecognition;
   
    let recognition = new SpeechRecognition();
    recognition.onstart = () => {
        k.style.backgroundColor="red";
    }
    recognition.onspeechend = () => {
        k.style.backgroundColor="#4a4abd";
        recognition.stop();
    }
    recognition.onresult = (result) => {
        $(document).ready(function(){
            $.ajax({
                type:"POST",
                url:"/ai/",
                data:JSON.stringify({"ai_data":result.results[0][0].transcript}),
                contentType:'application/json; charset=utf-8',
                dataType:'json',
                success:function(data){
                    $("#text_ai_appear").text(data.result);
                    let utterance = new SpeechSynthesisUtterance();
                    utterance.lang='en-US';
                    utterance.text = data.result;
                    utterance.voice = window.speechSynthesis.getVoices()[0];
                    utterance.pitch = 2.0; 
                    utterance.rate = 1.0; 
                    utterance.volume = 1.0;
                    let vid=document.getElementById("vid");
                    if(say_male == 1){
                        vid.src='/media/AI - Man.mp4'
                        vid.play();
                        vid.style.display='block';
                    }
                    if(say_female == 1){
                        vid.src='/media/AI - Woman.mp4'
                        vid.play();
                        vid.style.display='block';
                    }
                    window.speechSynthesis.speak(utterance);
                    utterance.addEventListener("end", (event) => {vid.pause();vid.style.display='none';});
                },
                error:function(error){
                    console.log('Error', error);
                }
            })
        })
    }
    recognition.start();
}

function send_question(){
    $(document).ready(function(){
        $.ajax({
            type:"POST",
            url:"/ai/",
            data:JSON.stringify({"ai_data":document.getElementById("text_for_ai").value}),
            contentType:'application/json; charset=utf-8',
            dataType:'json',
            success:function(data){
                var words=data.result,part,offset=0,forwards=true,skip_count=0,skip_delay=15,speed=70;
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
                    $('.text_ai_speaking').text(part);
                },speed);
                };
                $(document).ready(function(){
                wordflick();
                });
                let utterance = new SpeechSynthesisUtterance();
                utterance.lang='en-US';
                utterance.text = data.result;
                utterance.voice = window.speechSynthesis.getVoices()[0];
                utterance.pitch = 2.0; 
                utterance.rate = 1.0; 
                utterance.volume = 1.0;
                let vid=document.getElementById("vid");
                vid.play();
                vid.style.display='block';
                document.getElementById("text_for_ai").value="";
                window.speechSynthesis.speak(utterance);
                utterance.addEventListener("end", (event) => {vid.pause();vid.style.animationName='stopmove';vid.style.display='none';});
            },
            error:function(error){
                console.log('Error', error);
            }
        })
    })
}
