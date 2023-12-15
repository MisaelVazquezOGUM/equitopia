function convert(original){
  const formato = new Intl.NumberFormat('es-MX',
    {style:'currency',
     currency:'MXN'}).format(original);
  return formato
}

function generarNumero(numero){
    return (Math.random()*numero).toFixed(0);
}
function fondocolorRGB(){
   var coolor ="("+generarNumero(255)+","+generarNumero(255)+","+generarNumero(255)+","+0.2+")";
   return "rgba"+coolor;
}
function colorcolorRGB(){
    var coolor ="("+generarNumero(255)+","+generarNumero(255)+","+generarNumero(255)+","+1+")";
    return "rgba"+coolor;
}
