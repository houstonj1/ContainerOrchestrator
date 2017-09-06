$(function(){
	  $.ajax({
	    url: '/chart',
	    type: 'GET',
	    success : function(response) {
	      chartData = response;
	      var chartProperties = {
	        "caption": "Created Containers",
	        "xAxisName": "Image Name",
	        "yAxisName": "Number of Contianers",
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
