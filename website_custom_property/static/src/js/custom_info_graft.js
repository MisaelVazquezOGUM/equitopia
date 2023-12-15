function Mensual_informacion_graficas(){  
var programado=$("#input_programado").val()
var total_recibido=$("#input_total_recibido").val()


  
$("#informacion_mensual").append("<canvas id='show_informacion_mensual' name='informacion_mensual' ></canvas>")
const $grafica = document.querySelector("#show_informacion_mensual");

const data={
   label:"Informacion Mensual",
   data:[programado,total_recibido],
   backgroundColor: ["#FFFF00","#3ADF00"], // Color de fondo
   borderColor: ["#3ADF00","#FFFF00"], // Color del borde
   borderWidth: 1,// Ancho del borde

}

 //crear grafica
 var ctxiformacionmensual= new Chart($grafica, {
     type: 'bar',// Tipo de gráfica
     data: {
         labels: ['Rentas Programadas','Rentas Efectivas'],
         datasets:[
           data,
         ]
     },
       options:{
                    maintainAspectRatio:false,
                    indexAxis: 'y',
                    scales: {
                        xAxes: [{
                            barThickness: 6,
                            maxBarThickness: 8,
                        }]
                    },
                    legend:{
                            labels:{
                                font:{
                                    size: 14
                                }
                            },
                        },
                        plugins:{                        
                        datalabels:{
                            formatter: (value,context)=>{
                                if(value>0){
                                  return " \n"+ convert(value);    
                                }
                                else{
                                    return ''
                                }
                                                                
                                
                          },
                          font: {
                                weight: 'bold',
                                size: 12,
                                color:'red',
                           }

                        },
                        tooltip:{
                            callbacks:{
                             label: function(tooltipitem,data){
                                 var label=ctxiformacionmensual.data.labels[tooltipitem.dataIndex]
                                 var value=ctxiformacionmensual.data.datasets[tooltipitem.datasetIndex].data[tooltipitem.dataIndex]
                                 return label +" \n"+convert(value)                 

                        
                               }
                            }
                          },

                    },
                },
                plugins:[ChartDataLabels]
 });

}




