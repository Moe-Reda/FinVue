import React, { useState, useEffect } from 'react';
import { useNavigate } from "react-router-dom";
import api from '../../api/axiosConfig';

const TransactionForm = ({ loggedIn, setLoggedIn }) => {
  const navigate = useNavigate();
  const [amount, setAmount] = useState('');
  const [category, setCategory] = useState('');
  const [transactions, setTransactions] = useState([]);

   useEffect(() => {
     fetchTransactions();
   }, []);

  const fetchTransactions = async () => {
    try {
      const response = await api.get(`http://127.0.0.1:5000/api/fetch_transactions/${loggedIn}`);
      setTransactions(response.data.transactions);
    } catch (error) {
      console.error('Error fetching transactions:', error);
    }
  };

  const pieChartTransactions = async () => {
    try {
      const response = await api.get(`http://127.0.0.1:5000/api/piechart/${loggedIn}`);
      // Create usestate variable and set it to the categories and totals gotten in response
      // I will implement this below
      
    }  catch (error) {
      console.error('Error making piechart', error);
    }

  }


  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post(`http://127.0.0.1:5000/api/create_transaction`, { username: loggedIn, amount, category });
      setAmount('');
      setCategory('');
      fetchTransactions();
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


  return (
    <div className="transaction-form">
      <h2>Add Transaction</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="amount">Amount:</label>
          <input type="number" id="amount" value={amount} onChange={(e) => setAmount(e.target.value)} />
        </div>
        <div className="form-group">
          <label htmlFor="category">Category:</label>
          <input type="text" id="category" value={category} onChange={(e) => setCategory(e.target.value)} />
        </div>
        <button type="submit" className="btn-primary">Add Transaction</button>
      </form>
      <h2>Transactions</h2>
      <ul className="transaction-list">
        {transactions.map((transaction, index) => (
          <li key={index} className="transaction-item">
            Amount: {transaction.amount} | Category: {transaction.category}
          </li>
        ))}
      </ul>
      <p className="transaction-count">Total Transactions: {transactions?.length}</p>
      <div className='logout'>
        <button onClick={handleLogout} className="btn-secondary">Logout</button>
      </div>
    </div>
   
  );
};

export default TransactionForm;
