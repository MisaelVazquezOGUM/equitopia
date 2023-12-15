
 //INICIA GRAFICACION PARA GRAFICAR METRICAS
function graficaciondemetricas(grafica,metricas){ 
    const etiquetas=['Ingresos Netos','Mantenimientos','Servicios','Otros gastos','Comisiones']
    var ctxgraficametricas=new Chart(grafica,{
                type:'pie',
                data:{
                    labels:etiquetas,
                    datasets:[{
                        labels:'Metricas',
                        data: metricas,
                        backgroundColor: [fondocolorRGB(),fondocolorRGB(),fondocolorRGB(),fondocolorRGB(),fondocolorRGB()],
                        borderColor: [colorcolorRGB(),colorcolorRGB(),colorcolorRGB(),fondocolorRGB(),fondocolorRGB()],
                        borderWidth: 1,
                    }]                  
            
                },

                options: {
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
                                var label=ctxgraficametricas.data.labels[tooltipitem.dataIndex]
                                var value=ctxgraficametricas.data.datasets[tooltipitem.datasetIndex].data[tooltipitem.dataIndex]
                                return label +"\n\n"+convert(value)                

                        
                              }
                            }
                          },

                    },
            },
            plugins:[ChartDataLabels],   

    });
    

 }