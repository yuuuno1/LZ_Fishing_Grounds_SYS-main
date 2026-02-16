// series and label expects an array

const domain = window.location.href
var data_pie = {}
var data_bar = []

$.ajax({
        async:false,

        url: `${domain}chart_data/`,
        success: function (response) {
            // data.series = response.pie
            // data.label = response.pie_data
            data_pie.label_pie = response.pie
            data_pie.series = response.pie_data
            data_bar = response.bar

        }
})




const chartConfig = {
    series: [
      {
        name: "Sales",
        data: data_bar,
      },
    ],
    chart: {
      type: "bar",
      height: 340,
      toolbar: {
        show: true,
      },
    },
    title: {
      show: "Monthly Sales",
    },
    dataLabels: {
      enabled: false,
    },
    colors: ["#020617"],
    plotOptions: {
      bar: {
        columnWidth: "40%",
        borderRadius: 2,
      },
    },
    xaxis: {
      axisTicks: {
        show: false,
      },
      axisBorder: {
        show: false,
      },
      labels: {
        style: {
          colors: "#616161",
          fontSize: "12px",
          fontFamily: "inherit",
          fontWeight: 400,
        },
      },
      categories: [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
      ],
    },
    yaxis: {
      labels: {
        style: {
          colors: "#616161",
          fontSize: "12px",
          fontFamily: "inherit",
          fontWeight: 400,
        },
      },
    },
    grid: {
      show: true,
      borderColor: "#dddddd",
      strokeDashArray: 5,
      xaxis: {
        lines: {
          show: true,
        },
      },
      padding: {
        top: 5,
        right: 20,
      },
    },
    fill: {
      opacity: 0.8,
    },
    tooltip: {
      theme: "dark",
    },
  };
  
  const chart = new ApexCharts(document.querySelector("#bar-chart"), chartConfig);
  
  chart.render();



// pie



  var options = {
    series: data_pie.series,
    chart: {
    width: 400,
    type: 'pie',
  },
  
  labels: data_pie.label_pie,
  responsive: [{
    breakpoint: 380,
    options: {
      chart: {
        width: 400,
        height: 400
      },
      
    }
  }],
  legend: {
    position: 'bottom'
  }
  };

   
  const chart2 = new ApexCharts(document.querySelector("#pie-chart"), options);
   
  chart2.render();