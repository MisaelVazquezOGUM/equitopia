
//INICIO DE GRAFICA DE FLUJO MENSUAL

 function grafica_efectivo_programdo(grafica,data) {
    
    var ctxgraficaefeprogramado=new Chart(grafica,{
                type:'doughnut',
                data:{
                    labels:['Rentas Efectivo','Rentas Programadas'],
                    datasets:[{
                        labels:'Generado y Pendientes',
                        data: data,
                        backgroundColor: ["#3ADF00","#FFFF00"],
                        borderColor: ["#FFFF00","#3ADF00"],
                        borderWidth: 1,
                    }]                  
            
                },        
                options: {
                    responsive: true,
                    legend:{
                        display:false,
                        
                    },
                    plugins:{                        
                        datalabels:{
                            formatter: (value,context)=>{
                                if(value>0){
                                   return "\n\t" +convert(value)    
                                }
                                else{
                                    return ''
                                }
                                                                 
                                
                          },
                          font: {
                                weight: 'bold',
                                size: 12,
                                
                           }

                        },
                        tooltip:{
                            callbacks:{
                              label: function(tooltipitem,data){
                                var label=ctxgraficaefeprogramado.data.labels[tooltipitem.dataIndex]
                                var value=ctxgraficaefeprogramado.data.datasets[tooltipitem.datasetIndex].data[tooltipitem.dataIndex]
                                return label + convert(value)                

                        
                              }
                            }
                          },

                    },
            },
            plugins:[ChartDataLabels],   

            });
 }