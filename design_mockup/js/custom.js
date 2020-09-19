$(document).ready(function () {
    // for Drop Down menu in login navbar
    $("#Dropdown").click(function (){
        console.log("clicked");
        $(".profile-toggle").fadeToggle();
    });
    // for toggle the main feed page
    $('.profile-panel .user-links li').click(function(){
        console.log($(this).data('class'));
        $(this).addClass('active').siblings().removeClass('active');
        $($(this).data('class')).removeClass('d-none').fadeIn("slow").siblings().addClass('d-none');
    });
   
     // for challenges toggling 
     $(".dailyChallenge .challenge-bar li").on('click', function(){
        console.log($(this).data('class'));
        $(this).addClass('active').siblings().removeClass('active');
        if($(this).data('class') === 'all'){
            $(".dailyChallenge .row > div").css('opacity' , 1);
        }else{
            $(".dailyChallenge .row > div").css('opacity' , 0.3);
            $($(this).data('class')).css('opacity',1);
        }
    });	
    // for the popup for more info about the challenge
    $('#details').click(function(){
        console.log('clicked');
        $('.pop-details').fadeIn(500);
        $('.off').click(function(){
            $(this).parent().parent().parent().parent().fadeOut(500);
        });
    });
});