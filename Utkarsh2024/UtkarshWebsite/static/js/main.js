

$('#regbtn').click((e) => {
    $("#PopForm").removeClass("h-0")
});
let wrapper = $("#wrapper");
$("#PopForm").click((e)=>{
  if(e.target == wrapper[0]){
    $("#PopForm").addClass("h-0");
  }
});

$("#closeform").click(()=>{
  $("#PopForm").addClass("h-0");
});

tailwind.config = {
    theme: {
      extend: {
        colors: {
          shubham: '#5F58FF',
        }
      }
    }
}

// $("#AboutBtn").click(()=>{
//     $("#About").toggle((this)=>{
//         $(this).animate({"left":"0px"})
//     }, (e)=>{});
// });

var b = 1
var a = 1
$("#AboutBtn" ).click(()=>
{
    if(b%2==0){
      $("#ContactBtn")[0].click()
    }
    if(a %2==0){$("#About").animate({"left":"-1000px"});}
    else{$("#About").animate({"left":"0px"});}
    a+=1;
});


$("#ContactBtn" ).click(()=>{
  //  $("#About").click();
  if(a %2==0){
    $("#AboutBtn" )[0].click();
  }

    if(b%2==0){$("#Contact").animate({"right":"-1000px"});}
    else{$("#Contact").animate({"right":"0px"});}
    b+=1;
});


$(document).ready(function(){
    $("#utkarsh").addClass('animate__animated animate__zoomInDown');
   // $("#sd").addClass('animate__animated animate__bounceInDown');
   // $("#ed").addClass('animate__animated animate__bounceInUp');
   // $("#regbtn").addClass("animate__animated animate__heartBeat animate__delay-1s");
});