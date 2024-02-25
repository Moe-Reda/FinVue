import React, { useState } from 'react';
import axios from 'axios';
import SavingChart from '../savingChart/savingChart';
import './savingsPage.css'

const SavingsPage = () => {
    const [initialSavings, setInitialSavings] = useState(0);
    const [monthlySavings, setMonthlySavings] = useState(0);
    const [interestRate, setInterestRate] = useState(0);
    const [timePeriod, setTimePeriod] = useState(0);
    const [chartData, setChartData] = useState([]);

    const handleCalculate = async () => {
        try {
            const response = await axios.post('http://127.0.0.1:5000/api/make_savings', {
                'initial_savings': initialSavings,
                'monthly_added_savings': monthlySavings,
                'predicted_interest_rate': interestRate,
                'months': timePeriod
            });
            setChartData(response.data);
        } catch (error) {
            console.error('Error calculating savings:', error);
        }
    };

    return (
        <div className="savings-calculator">
            <h2>Savings Calculator</h2>
            <div className="input-group">
                <label htmlFor="initialSavings">Initial Savings:</label>
                <input
                    type="number"
                    id="initialSavings"
                    value={initialSavings}
                    onChange={(e) => setInitialSavings(parseFloat(e.target.value))}
                    className="input-field"
                />
            </div>
            <div className="input-group">
                <label htmlFor="monthlySavings">Monthly Savings:</label>
                <input
                    type="number"
                    id="monthlySavings"
                    value={monthlySavings}
                    onChange={(e) => setMonthlySavings(parseFloat(e.target.value))}
                    className="input-field"
                />
            </div>
            <div className="input-group">
                <label htmlFor="interestRate">Predicted Interest Rate:</label>
                <input
                    type="number"
                    id="interestRate"
                    value={interestRate}
                    onChange={(e) => setInterestRate(parseFloat(e.target.value))}
                    className="input-field"
                />
            </div>
            <div className="input-group">
                <label htmlFor="timePeriod">Time Period (months):</label>
                <input
                    type="number"
                    id="timePeriod"
                    value={timePeriod}
                    onChange={(e) => setTimePeriod(parseFloat(e.target.value))}
                    className="input-field"
                />
            </div>
            <button onClick={handleCalculate} className="calculate-button">Calculate</button>
            <SavingChart data={chartData}/>
        </div>
    );
};

export default SavingsPage;
