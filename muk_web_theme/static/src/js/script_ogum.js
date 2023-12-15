window.addEventListener('load', ()=>{
    const nav = document.getElementsByTagName('header');
    const boton = document.createElement('span');
    // boton.textContent = 'Botón';
    nav.innerHTML = boton;
    console.log(nav);
});