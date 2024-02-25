import React, { useState, useEffect } from 'react';
import { useNavigate } from "react-router-dom";
import PieChartTransactions from '../piechart/PieChartTransactions';
import api from '../../api/axiosConfig';
import './TransactionDashboard.css'

const TransactionForm = ({ loggedIn, setLoggedIn }) => {
  const categories = [
    'Groceries',
    'Utilities',
    'Entertainment',
    'Dining Out',
    'Transportation',
    'Healthcare',
    'Rent/Mortgage',
    'Savings/Investments',
    'Education',
    'Clothing',
    'Gifts/Donations',
    'Personal Care',
    'Travel',
    'Kids',
    'Pets',
    'Hobbies',
    'Subscriptions',
    'Other'
  ];

  const navigate = useNavigate();
  const [amount, setAmount] = useState('');
  const [category, setCategory] = useState('Groceries');
  const [transactions, setTransactions] = useState([]);
  const [response, setResponse] = useState([]);
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [
      {
        data: [],
        backgroundColor: [
          '#FF6384', // Radish Red
          '#36A2EB', // Light Blue
          '#FFCE56', // Yellow
          '#4BC0C0', // Soft Turquoise
          '#F77825', // Orange
          '#9966FF', // Amethyst
          '#C9CB3F', // Olive Drab
          '#50EB5A', // Bright Green
          '#E56B6F', // Salmon
          '#69B5FF', // Sky Blue
          '#FF9F40', // Mango
          '#ABE188', // Tea Green
          '#FA8072', // Salmon Pink
          '#6A5ACD', // Slate Blue
          '#FFD700', // Gold
          '#B0E0E6', // Powder Blue
          '#DC143C', // Crimson
          '#20B2AA'  // Light Sea Green
        ]
        ,
      },
    ],
  });


   useEffect(() => {
     fetchTransactions();
     pieChartTransactions();
   }, []);

  const fetchTransactions = async () => {
    try {
      const response = await api.get(`http://127.0.0.1:5000/api/fetch_transactions/${loggedIn}`);
      setTransactions(response.data.transactions);
    } catch (error) {
      console.error('Error fetching transactions:', error);
    }
  };


  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post(`http://127.0.0.1:5000/api/create_transaction`, { username: loggedIn, amount, category });
      setAmount('');
      setCategory('Groceries');
      fetchTransactions();
      pieChartTransactions();
    } catch (error) {
      console.error('Error adding transaction:', error);
    }
  };


  const handleLogout = () => {
    setLoggedIn('');
    setTransactions([]);
    // Redirect the user to a login page
    navigate('/');
  };


  const pieChartTransactions = async () => {
    try {
      const result = await api.get(`http://127.0.0.1:5000/api/piechart/${loggedIn}`);
     
      const data = await result.data;
      setResponse(data); // Assuming the API returns an object with a totals property
      loadChartData(data.totals); // Pass the totals directly to the loading function
    } catch (error) {
        console.error('Error fetching piechart data', error);
    }
  };

  const loadChartData = (totals) => {
    console.log(totals)
    const categories = totals.map((item) => item.category);
    const amounts = totals.map((item) => item.total);

    setChartData({
      labels: categories,
      datasets: [{
        data: amounts,
        backgroundColor: chartData.datasets[0].backgroundColor,
      }],
    });
  };


  return (
    <div className="transaction-form">
      <h2>Add Transaction</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="amount">Amount:</label>
          <input type="text" id="amount" value={amount} onChange={(e) => setAmount(parseFloat(e.target.value))} />
        </div>
        <div className="form-group">
          <label htmlFor="category">Category:</label>
          <select 
            id="category" 
            value={category} 
            onChange={(e) => setCategory(e.target.value)}
            className="category-select"
          >
            {categories.map((cat, index) => (
              <option key={index} value={cat}>{cat}</option>
            ))}
          </select>
        </div>
        <button type="submit" className="btn-primary">Add Transaction</button>
      </form>
      <h2>Transactions</h2>
      <ul className="transaction-list">
      {transactions.slice(-10).map((transaction, index) => ( // Only show the first 10 transactions
        <li key={index} className="transaction-item">
          Amount: ${transaction.amount} | Category: {transaction.category}
        </li>
      ))}
    </ul>
      <p className="transaction-count">Total Transactions: {transactions?.length}</p>
      <PieChartTransactions loggedIn={loggedIn} chartData={chartData}/>
      <div className='logout'>
        <button onClick={handleLogout} className="btn-secondary">Logout</button>
      </div>
    </div>
   
  );
};

export default TransactionForm;
