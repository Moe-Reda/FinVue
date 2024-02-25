import React, { useState, useEffect } from 'react';
import api from '../../api/axiosConfig';
import './budgetTable.css'

const BudgetTable = ({ loggedIn, budgetData, getBudgetLists }) => {
  const categories = [
    'Groceries',
    'Utilities',
    'Cars',
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

  
  const [selectedCategory, setSelectedCategory] = useState(categories[0]);
  const [amount, setAmount] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    const month_year = `${new Date().getFullYear()}-${String(new Date().getMonth() + 1).padStart(2, '0')}`; // Format: "YYYY-MM"
    
    const budget = {
      username: loggedIn,
      category: selectedCategory,
      allowance: parseFloat(amount),
      month_year: month_year,
    };

    try {
      const response = await api.post('http://127.0.0.1:5000/api/create_budget', budget);
      console.log('Budget created:', response.data);
      setAmount(''); // Reset the amount input after successful creation
      // You might want to update the local state to reflect the new budget item or refetch the budget data
      getBudgetLists();
    } catch (error) {
      console.error('Error creating budget:', error);
      // Handle errors, such as displaying a message to the user
    }
  };



  return (
    <div>
      <form onSubmit={handleSubmit} className="budget-form">
        <select 
          value={selectedCategory} 
          onChange={(e) => setSelectedCategory(e.target.value)}
          className="category-select"
        >
          {categories.map((category, index) => (
            <option key={index} value={category}>
              {category}
            </option>
          ))}
        </select>
        <input 
          type="number" 
          value={amount} 
          onChange={(e) => setAmount(e.target.value)} 
          className="amount-input"
          placeholder="Amount"
        />
        <button type="submit" className="create-budget-btn">Create Budget</button>
      </form>
      
      <div className="budget-table">
      <div className="table-header">
        <div>TAG</div>
        <div>BUDGETED</div>
        <div>EXPENSE</div>
        <div>AVAILABLE</div>
      </div>
      <div className="table-content">
        {budgetData.budgets.map((item, index) => (
          <div key={index} className="table-row">
            <div>{item.category}</div>
            <div>{item.allowance}</div>
            <div>{item.spent}</div>
            <div>{item.remaining}</div>
          </div>
        ))}
      </div>
      <div className="table-footer">
        <div>TOTAL</div>
        <div>{budgetData.overall_budget.total_allowance}</div>
        <div>{budgetData.overall_budget.total_spent}</div>
        <div>{budgetData.overall_budget.overall_remaining}</div>
      </div>
    </div>
    </div>
  );
};

export default BudgetTable;
