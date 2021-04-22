const sidebarButton = document.querySelector(".sidebar-toggle");
const sideBar = document.getElementById("sidebar");
const pageContent = document.querySelector(".page-content");

sidebarButton.addEventListener("click", ()=>{
    sideBar.classList.toggle("shrinked");
    pageContent.classList.toggle("active");
})