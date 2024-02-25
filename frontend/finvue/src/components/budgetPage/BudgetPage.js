import React, { useState, useEffect } from 'react';
import api from '../../api/axiosConfig';
import BudgetTable from '../budgetTable/budgetTable';
import BudgetProgressBar from '../budgetbars/Budgets';
import './BudgetPage.css'

const BudgetPage = ({ loggedIn }) => {
  const [budgetData, setBudgetData] = useState({ budgets: [], overall_budget: {} });

  useEffect(() => {
    getBudgetLists();
  }, [loggedIn]);

  
  const getBudgetLists = async () => {
    try {
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
      <div className="budget-tables">
        <h2>Budget Table</h2>
        <BudgetTable loggedIn={loggedIn} budgetData={budgetData} getBudgetLists={getBudgetLists}/>
      </div>
      <div className="budget-bars">
        <h2>Budget Progress</h2>
         <BudgetProgressBar
          category={'Overall Progress'}
          spent={budgetData.overall_budget.total_spent}
          percentage={budgetData.overall_budget.overall_percentage_spent} 
          total={budgetData.overall_budget.total_allowance}
        /> 
      {budgetData.budgets.map((budget, index) => (
        <BudgetProgressBar
          key={index}
          category={budget.category}
          spent={budget.spent}
          percentage={budget.percentage_spent}
          total={budget.allowance}
        />
      ))}
      </div>
    </div>
  );
};

export default BudgetPage;