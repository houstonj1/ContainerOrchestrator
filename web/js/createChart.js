$(function(){
	  $.ajax({
	    url: 'http://localhost/ContainerOrchestrator/php/createChart.php',
	    type: 'GET',
	    success : function(data) {
	      chartData = data;
	      var chartProperties = {
	        "caption": "Most Containers Created",
	        "xAxisName": "Image Name",
	        "yAxisName": "Number of Creation",
	        "rotatevalues": "0",
			"paletteColors": "#029f5b"
	      };
	      apiChart = new FusionCharts({
	        type: 'column2d',
	        renderAt: 'chart-container',
	        width: '550',
	        height: '350',
	        dataFormat: 'json',
	        dataSource: {
	          "chart": chartProperties,
	          "data": chartData
	        }
	      });
	      apiChart.render();
	    }
	  });
	});