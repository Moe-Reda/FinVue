import React, { useState, useEffect } from 'react';
import { useNavigate } from "react-router-dom";
import api from '../../api/axiosConfig';
import "./budgets.css"



const BudgetProgressBar = ({ category, spent, percentage, total }) => {
  // Calculate the percentage of the budget that has been spent
  const safePercentage = Math.min(percentage, 100);

  return (
    <div className="budget-bars-container">
      <div className="budget-progress-bar">
      <div className="budget-category">{category}</div>
      <div className="budget-bar-container">
        <div className="budget-bar" style={{ width: `${safePercentage}%`, backgroundColor: 'green' }}>
          <span className="budget-spent">${spent}</span>
        </div>
      </div>
      <div className="budget-total">${total} LEFT</div>
    </div>
    </div>
    
  );
};

export default BudgetProgressBar;