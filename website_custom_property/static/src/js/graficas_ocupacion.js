//INICION DE GRAFICA DE OCUPACION
function  graficas_dinamicas(grafica,data){

const image = new Image();
image.src="website_custom_property/static/src/img/equitopia2.jpeg"

var ctxgrafica_ciruclar=new Chart(grafica,{
    type:'doughnut',
    data:{
        labels:['Libre','Ocupado'],
        datasets:[{
            labels:'Ocupacion',
            data: data,
            backgroundColor: ["#e8c3b9","#3cba9f"],
            borderColor:["#3cba9f","#e8c3b9"],
            borderWidth: 1,
        }]                  
        
    },        
    options: {
        responsive: true,
        legend:{
            display:false
        },
        plugins:{                        
            datalabels:{
                formatter: (value,context)=>{
                    let mes_selecionado=$("#select_meses option:selected").val();
                    let ano=$("#buscardeano").val();
                    let days=new Date(ano,mes_selecionado,0).getDate()
                    let porcet=(value*100)/days 
                    return porcet.toPrecision(4)+"% \n "+ value.toPrecision(4) +" Dias"                                

                },
                font: {
                    weight: 'bold',
                    size: 12,

                }

            },
            tooltip:{
                callbacks:{
                  label: function(tooltipitem,data){
                    var label=ctxgrafica_ciruclar.data.labels[tooltipitem.dataIndex]
                    var value=ctxgrafica_ciruclar.data.datasets[tooltipitem.datasetIndex].data[tooltipitem.dataIndex]
                    let mes_selecionado=$("#select_meses option:selected").val();
                    let ano=$("#buscardeano").val();
                    let days=new Date(ano,mes_selecionado,0).getDate()
                    let porcet=(value*100)/days     


                    return label + "\n\n"+porcet.toPrecision(4)+"% \n " 
                    +value.toPrecision(4)+" Dias"                

                    
                }
            }
        },

    },
},
plugins:[ChartDataLabels],   

});

}