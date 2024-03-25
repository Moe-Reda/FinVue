import React, { useState, useEffect } from 'react';
import api from '../../api/axiosConfig';
import SpendingChart from '../spendingChart/spendingChart';
import './spendings.css'; // Importing the CSS file

const Spendings = ({ loggedIn }) => {
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [{
      label: '',
      data: [],
      backgroundColor: 'rgba(54, 162, 235, 0.2)',
      borderColor: 'rgba(54, 162, 235, 1)',
      borderWidth: 1,
    }],
  });

  const fetchData = async () => {
    try {
      const response = await api.get(`http://127.0.0.1:5000/api/spendings/${loggedIn}`);
      setChartData({
        labels: response.data.spendings.day,
        datasets: [{
          label: `daily spendings`,
          data: response.data.spendings.amount,
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1,
        }],
      });
    } catch (error) {
      console.error('Error fetching spending data:', error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  console.log(chartData)

  return (
    <div className="spendings-container">
      <h1 className="spendings-title">Daily Spendings Chart</h1>
      <SpendingChart data={chartData} />
    </div>
  );
};

export default Spendings;
