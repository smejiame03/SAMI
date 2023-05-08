const hamburger = document.querySelector('.hamburger'),//seleccionar la clase
      menu = document.querySelector('.menu-navegacion');

//cuando se de click a hamburger se quiere desplegar
hamburger.addEventListener('click',()=>{
    menu.classList.toggle('spread');//toggle añade o quita una clase, en este caso la clase menu, o sea el menu de navegacion
})

window.addEventListener('click', e => { //cuando se de click en cualquier parte de la ventana se cierre el menu
    if(menu.classList.contains('spread') && e.target != menu && e.target != hamburger){ //condicional para que el menu de navegacion se quite en el momento que se de click a cualquier lugar de la
        //ventana ,menos al mismo menu
        menu.classList.toggle('spread');
    }
})