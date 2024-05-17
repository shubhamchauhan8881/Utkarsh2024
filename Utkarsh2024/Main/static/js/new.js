$(document).ready(()=>{
    $(".window-loader").fadeOut("slow");

    var destination = new Date("feb 21, 2024 00:00:00").getTime();
    var PragalbhMishra= setInterval(function(){
    var rn = new Date().getTime();
    var difference = destination - rn;
    var days = Math.floor(difference / (1000 * 60 * 60 * 24));
    var hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((difference % (1000 * 60)) / 1000);
    // console.log(days , hours, minutes, seconds);
    document.querySelector("#timer-days").textContent = days;
    document.querySelector("#timer-hours").textContent = hours;
    document.querySelector("#timer-minutes").textContent = minutes;
    document.querySelector("#timer-seconds").textContent = seconds;
    // document.getElementById("countdn").innerHTML = days +"day " + hours +"hours " + minutes +"minutes " + seconds +"seconds";
}, 1000)


// $("#cassette").focus();
// $("#cassette").trigger("play");

var swiper = new Swiper(".mySwiper", {
    freeMode: true,  
    freeModeMomentum: false,
    freeModeMomentumBounce: false,
    slidesPerView: 3,
    centeredSlides: false,
    spaceBetween: 1,
    speed: 5000,
    autoplay: {
        delay: 1,
        disableOnInteraction: false,
        reverseDirection: true,
    },
    loop: true,
    grabCursor: true,
    breakpoints: {
      "@0.00": {
        slidesPerView: 2,
        spaceBetween: 10,
      },
      "@0.75": {
        slidesPerView: 2,
        spaceBetween: 20,
      },
      "@1.00": {
        slidesPerView: 3,
        spaceBetween: 40,
      },
      "@1.50": {
        slidesPerView: 4,
        spaceBetween: 50,
      },
    },
   
});

var swiper = new Swiper(".mySwiper2", {
    freeMode: true,  
    freeModeMomentum: false,
    freeModeMomentumBounce: false,
    centeredSlides: false,
    spaceBetween: 1,
    speed: 5000,
    autoplay: {
        delay: 1,
        disableOnInteraction:false,
    },
    slidesPerView: 3,
    loop: true,
    grabCursor: true,
    breakpoints: {
      "@0.00": {
        slidesPerView: 2,
        spaceBetween: 10,
      },
      "@0.75": {
        slidesPerView: 2,
        spaceBetween: 20,
      },
      "@1.00": {
        slidesPerView: 3,
        spaceBetween: 40,
      },
      "@1.50": {
        slidesPerView: 4,
        spaceBetween: 50,
      },
    },
   
});


document.querySelectorAll("#ev-wrapper-btn").forEach((btn, index)=>{

  $(btn).on("click", (e)=>{
    let id = e.target.value;
    $(`#ev-wrapper_${id}`).fadeOut();
  });

});

document.querySelectorAll("#show_ev_wrapper").forEach((btn, index)=>{

  $(btn).on("click", (e)=>{
    let id = e.target.value;
    $(`#ev-wrapper_${id}`).show();
  });

});


// $("#login_btn").on("click",(e)=>{
//   $(".pop-provider-wrapper").show();
//   $(".loginpage").show();
// });

const user_views = ["user-profile-view", "user-events-view", "user-payments-view", "user-ca-view"]

function hideView(){
  user_views.forEach((view, i)=>{
    $(`#${view}`).hide();
  });
}

function showView(index){
  hideView();
  $(`#${user_views[index]}`).fadeIn();
}

$("#user-profile-view-btn").on("click", ()=>{
  showView(0);
});

$("#user-event-view-btn").on("click", ()=>{
  showView(1);
});

$("#user-payment-view-btn").on("click", ()=>{
  showView(2);
});

$("#user-ca-view-btn").on("click", ()=>{
  showView(3);
});

$("#user-profile-view-btn").click();


$("#audio-on").on("click", (e)=>{
  $(e.target).hide();
  $("#bg_audio").trigger('pause');
  $("#audio-off").show();
});

$("#audio-off").on("click", (e)=>{
  $(e.target).hide();
  $("#bg_audio").trigger('play');
  $("#audio-on").show();
});

$("#bg_audio").trigger('play');
});


// $(".pop-provider-wrapper").show()

tailwind.config = {
    theme: {
      extend: {
        colors: {
          shubham: '#5F58FF',
        }
      }
    }
}