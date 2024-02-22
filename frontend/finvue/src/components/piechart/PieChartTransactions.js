import React, { useState, useEffect } from 'react';
import { Pie } from 'react-chartjs-2';

const PieChartTransactions = ({ loggedIn }) => {
  const [showChart, setShowChart] = useState(false);
  const [response, setResponse] = useState([]);
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [
      {
        data: [],
        backgroundColor: [
          '#FF6384',
          '#36A2EB',
          '#FFCE56',
          '#4BC0C0',
          '#F77825',
          '#9966FF',
          // Add more colors as needed
        ],
      },
    ],
  });

  useEffect(() => {
    if (showChart) {
      pieChartTransactions();
    }
  }, [showChart]);

  const pieChartTransactions = async () => {
    try {
      const result = await api.get(`http://127.0.0.1:5000/api/piechart/${loggedIn}`);
      // Create usestate variable and set it to the categories and totals gotten in response
      // I will implement this below
      const data = await result.json();
      setResponse(data); // Assuming the API returns an object with a totals property
      loadChartData(data.totals); // Pass the totals directly to the loading function
    } catch (error) {
      console.error('Error fetching piechart data', error);
    }
  };

  const loadChartData = (totals) => {
    const categories = totals.map((item) => item[0]);
    const amounts = totals.map((item) => item[1]);

    setChartData({
      labels: categories,
      datasets: [{
        data: amounts,
        backgroundColor: chartData.datasets[0].backgroundColor,
      }],
    });
  };

  const toggleShowChart = () => {
    setShowChart(!showChart);
  };

  return (
    <div>
      <button onClick={toggleShowChart}>
        {showChart ? 'Hide Piechart' : 'Show Piechart'}
      </button>
      {showChart && <Pie data={chartData} />}
    </div>
  );
};

export default PieChartTransactions;