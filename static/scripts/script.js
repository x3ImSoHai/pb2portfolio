const profileUrl = "https://www.plazmaburst2.com/?a=&s=7&ac=Nyove";
const youtubeUrl = "https://www.youtube.com/channel/UCYTyKq91Y2eKW5yrmtu9qIA";

//const cursor = $( ".cursor" )
const profileButton = document.querySelector(".profileButton");
const loadingScreen = document.getElementById("loadingScreen");
const notLoadingScreen = document.getElementById("notLoadingScreen");
const cursorMiddle = document.querySelector("#cursorMiddle");
const sideImg = document.querySelector("#sideImg");
const bio = document.querySelector("#bio");
const arrowLeft  = document.querySelector(".arrowLeft");
const arrowRight  = document.querySelector(".arrowRight");
const slideImgArray = document.getElementsByClassName("slideImg");
const slideImgSize = slideImgArray.length;
const youtubeIcon = document.querySelector("#youtubeIcon");
const pb2Icon = document.querySelector("#pb2Icon");
const hamIcon = $( "#hamburgerIcon" )
const nav = document.querySelector(".nav");

var imgIndex = 0;

/*
document.addEventListener("mousemove", e => {
    cursor.setAttribute("style","top: " + (e.pageY-11) + "px; left: " + (e.pageX-10.5) + "px;");
    cursorMiddle.setAttribute("style","top: " + (e.pageY-2) + "px; left: " + (e.pageX-2) + "px;");
});

document.addEventListener("click", e => {
    cursor.classList.add("expand");
    setTimeout(() =>
    { 
        cursor.classList.remove("expand");
    }
    , 500);
});
*/


hamIcon.click(function(){
    nav.classList.add("phoneNav");
});

hamIcon.mouseout(function(){
    nav.classList.remove("phoneNav");
});

/*
$(document).on('click',function(){
    if(nav !== event.target && !nav.has(event.target).length){
        $(".dropdown-menu").slideUp("fast");
    }            
    
    $(document).off('click');
});
*/

profileButton.addEventListener("click", e => {
    window.open(profileUrl, '_blank');
});

arrowLeft.addEventListener("click", e => {
    imgIndex -= 1;
    resetIndexCounter()
});

arrowRight.addEventListener("click", e => {
    imgIndex += 1;
    resetIndexCounter()
});

function resetIndexCounter(){
    if(imgIndex == -1){
        imgIndex = slideImgSize - 1;
    }
    else if(imgIndex == slideImgSize)
    {
        imgIndex = 0;
    }

    for(i = 0; i < slideImgSize; i++){
        if(i != imgIndex)
        {
            slideImgArray[i].classList.add("hide");
        }
        else{
            slideImgArray[i].classList.remove("hide");
        }
    }
}

youtubeIcon.addEventListener("click", e => {
    window.open(youtubeUrl, '_blank');
});

pb2Icon.addEventListener("click", e => {
    window.open(profileUrl, '_blank');
});
/*
setTimeout(() =>
    { 
        loadingScreen.classList.add("slideOut");
        notLoadingScreen.classList.remove("hide");

        setTimeout(() =>
        {
            sideImg.classList.remove("hide");
            bio.classList.remove("hide");
            sideImg.classList.add("slideIn");
            bio.classList.add("slideIn");
        }
        , 500);

        setTimeout(() =>
        { 
            loadingScreen.classList.add("hide");
        }
        , 1500);
    }
, 2000);
*/


