import React from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS } from 'chart.js/auto'
import { Chart }            from 'react-chartjs-2'

const StockChart = ({ data, symbol }) => {
    const chartData = {
        labels: data.map(item => item.day),
        datasets: [
            {
                label: 'Price',
                data: data.map(item => item.price),
                fill: true,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                tension: 0.1
            }
        ]
    };

    return (
        <div>
            <h2>{symbol}</h2>
            <Line data={chartData} />
        </div>
    );
};

export default StockChart;

