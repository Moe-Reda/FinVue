import React, { useState, useEffect } from 'react';
import api from '../../api/axiosConfig';
import BudgetTable from '../budgetTable/budgetTable';

const BudgetPage = ({ loggedIn }) => {
  const [budgetData, setBudgetData] = useState({ budgets: [], overall_budget: {} });

  useEffect(() => {
    console.log("Zeb");
    getBudgetLists();
  }, [loggedIn]);

  
  const getBudgetLists = async () => {
    try {
      console.log("Zebi");
      const date = new Date();
      const year = date.getFullYear();
      const month = (date.getMonth() + 1).toString().padStart(2, '0');
      const findate = `${year}-${month}`;
      const response = await api.get(`http://127.0.0.1:5000/api/fetch_budget/${loggedIn}/${findate}`);
      const data = await response.data;
      console.log(data);
      setBudgetData({
        budgets: data.budgets.budgets,
        overall_budget: data.budgets.overall_budget
      });
      console.log(data);
    } catch (error) {
        console.error('Error fetching budget data', error);
    }
  };

  return (
    <div className="budget-page">
        <h2>Budget Table</h2>
        <BudgetTable loggedIn={loggedIn} budgetData={budgetData} getBudgetLists={getBudgetLists}/>
    </div>
  );
};

export default BudgetPage;