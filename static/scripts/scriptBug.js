const profileUrl = "https://www.plazmaburst2.com/?a=&s=7&ac=Nyove";
const youtubeUrl = "https://www.youtube.com/channel/UCYTyKq91Y2eKW5yrmtu9qIA";

const youtubeIcon = document.querySelector("#youtubeIcon");
const pb2Icon = document.querySelector("#pb2Icon");

youtubeIcon.addEventListener("click", e => {
    window.open(youtubeUrl, '_blank');
});

pb2Icon.addEventListener("click", e => {
    window.open(profileUrl, '_blank');
});