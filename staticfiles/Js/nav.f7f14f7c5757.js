const hamburguer = document.getElementById("burger-menu")
const navMenu = document.querySelector(".list-nav-bar")


hamburguer.addEventListener("click", ()=>{
    hamburguer.classList.toggle('active');
    navMenu.classList.toggle('active');
})