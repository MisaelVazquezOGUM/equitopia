function create_grafic_history(){

  
var global_mes_cobrado=$("#input_global_mes_cobrado").val()
var global_mes_pen_cobrado=$("#input_global_mes_pen_cobrado").val()

$("#informacion_history").append("<canvas id='show_informacion_history' name='informacion_history' ></canvas>")
const $grafica = document.querySelector("#show_informacion_history");

const data={
   label:"Informacion historica",
   data:[global_mes_cobrado,global_mes_pen_cobrado],
   backgroundColor: [fondocolorRGB(),fondocolorRGB()], // Color de fondo
   borderColor: [colorcolorRGB(),colorcolorRGB()], // Color del borde
   borderWidth: 1,// Ancho del borde

}

 //crear grafica
 var ctxiformacionhistorial= new Chart($grafica, {
     type: 'bar',// Tipo de gráfica
     data: {
         labels: ['Rentas cobradas','Rentas ha cobrar'],
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
                            // title: {
                            //     display: true,
                            //     text: 'Flujo de efectivo'
                            // }
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
                                 var label=ctxiformacionhistorial.data.labels[tooltipitem.dataIndex]
                                 var value=ctxiformacionhistorial.data.datasets[tooltipitem.datasetIndex].data[tooltipitem.dataIndex]
                                 return label +" \n"+convert(value)                 

                        
                               }
                            }
                          },

                    },
                },
                plugins:[ChartDataLabels]

 });

}
	
