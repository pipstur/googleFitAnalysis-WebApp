function uploadFile() {
    var form = document.getElementById('uploadForm');
    var formData = new FormData(form);

    fetch('https://pipstur.pythonanywhere.com/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('result').innerHTML = `
            <p>Date with most distance covered: ${data.max_distance.date} (${data.max_distance.value} m)</p>
            <p>Date with most steps: ${data.max_steps.date} (${data.max_steps.value} steps)</p>
            <p>Date with most heart points: ${data.max_heart_points.date} (${data.max_heart_points.value} points)</p>
            <p>Date with most walking duration: ${data.max_walking_duration.date} (${data.max_walking_duration.value})</p>
        `;

        fetch('http://localhost:5000/distance_plot', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(plotData => {
            Plotly.newPlot('distancePlot', plotData.plot_data);
        })
        .catch(error => console.error('Error:', error));
    })
    .catch(error => console.error('Error:', error));
}


function fetchPlots() {
    var form = document.getElementById('uploadForm');
    var formData = new FormData(form);

    if (formData.has('file')) {
        const plotUrls = [
            'https://pipstur.pythonanywhere.com/average_steps_plot', 
            'https://pipstur.pythonanywhere.com/heart_points_vs_steps',
            'https://pipstur.pythonanywhere.com/mean_steps_by_day_of_week',
            'https://pipstur.pythonanywhere.com/mean_steps_by_month',
            //'http://localhost:5000/activity_distribution'
            //'http://localhost:5000/walking_distribution_heatmap'
        ];

        const plotPromises = plotUrls.map(url => fetch(url, { method: 'POST', body: formData }));

        Promise.all(plotPromises)
            .then(responses => Promise.all(responses.map(response => response.json())))
            .then(dataArray => {
                
                dataArray.forEach((data, index) => {
                    const title = getTitleForIndex(index);  
                    const targetElementId = 'plot';  
                    appendPlotData(data.plot_data, title, targetElementId);
                });
            })
            .catch(error => {
                console.error('Error fetching and plotting plots:', error);
                alert('Error fetching and plotting data. Please try again.');
                console.log(error)
            });
    } else {
        console.error('No file selected');
    }
}

function appendPlotData(data, title, targetElementId) {
    const layout = {
        title: title,
        xaxis: { title: '' },
        yaxis: { title: '' },
    };

    const newPlotDiv = document.createElement('div');
    newPlotDiv.id = `plot-${title.toLowerCase().replace(/\s/g, '-')}`;
 
    document.getElementById(targetElementId).appendChild(newPlotDiv);
    Plotly.newPlot(newPlotDiv, data, layout);
}



function appendHeatmapData(heatmapData, title, targetElementId) { // this is unused but will remain here
   
    var targetElement = document.getElementById(targetElementId);
    var heatmapDiv = document.createElement('div');
    heatmapDiv.id = 'heatmap-' + title.replace(/\s+/g, '-').toLowerCase(); 

    targetElement.appendChild(heatmapDiv);

    var heatmapPlot = {
        x: heatmapData.xValues,
        y: heatmapData.yValues,
        z: heatmapData.zValues,
        type: 'heatmap',
        colorscale: 'Viridis' 
    };

    var heatmapLayout = {
        title: title,
        xaxis: {
            title: 'Hour'
        },
        yaxis: {
            title: 'Day'
        }
    };

    Plotly.newPlot(heatmapDiv.id, [heatmapPlot], heatmapLayout);
}

function getTitleForIndex(index) {
    switch (index) {
        case 0:
            return 'Average Steps over weeks of the year';
        case 1:
            return 'Heart points vs steps'; 
        case 2:
            return 'Mean steps by day of the week';
        case 3:
            return 'Mean steps by month'
        // case 4:
        //     return 'Walking distribution heatmap' // this cannot work as i do not have the data onthe specific hours, it is aggregated over a day
        default:
            return `Plot ${index + 1}`;
    }
}
