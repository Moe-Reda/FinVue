import React from 'react';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, Tooltip, Legend, ArcElement} from 'chart.js';

ChartJS.register(
  Tooltip, Legend, // Register Tooltip and Legend plugins
  ArcElement
);

const PieChartTransactions = ({ chartData }) => {
  const options = {
    plugins: {
      legend: {
        display: true, // This will show the legend
        position: 'top', // Position of the legend
      },
    },
    responsive: true, // This will make the chart responsive
  };

  return (
    <div>
      {chartData && <Pie data={chartData} options={options} />}
    </div>
  );
};

export default PieChartTransactions;