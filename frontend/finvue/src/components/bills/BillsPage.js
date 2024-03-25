import React, { useState, useEffect } from 'react';
import MyCalendar from '../calendar/Calendar';
import './BillsPage.css'
import api from '../../api/axiosConfig';

const BillsPage = ({ loggedIn }) => {
    const [bills, setBills] = useState([]);
    const [billName, setBillName] = useState('');
    const [amount, setAmount] = useState('');
    const [dueDate, setDueDate] = useState('');
    const [isRecurring, setIsRecurring] = useState(false);
    const [frequency, setFrequency] = useState('onetime');


    useEffect(() => {
        fetchBills();
    }, []); 


    const fetchBills = async () => {
        try {
            const response = await api.get(`http://127.0.0.1:5000/api/fetch_bills/${loggedIn}`);
            setBills(response.data.bills);
        } catch (error) {
            console.error('Error fetching bills:', error);
        }
    };

    const handleAddBill = async (e) => {
        e.preventDefault();
        const newBill = {
          user: loggedIn,
          name: billName,
          amount: amount,
          dueDate: dueDate,
          recurring: isRecurring,
          frequency: frequency
        };
        try {
            console.log(dueDate);
            await api.post('http://127.0.0.1:5000/api/create_bill', newBill);
            fetchBills();
            setBillName('');
            setAmount('');
            setDueDate('');
            setIsRecurring(false);
            setFrequency('onetime');
        } catch (error) {
            console.error('Error creating the bill:', error);
        }
    };

    const generateRecurringEvents = (bill) => {
        const events = [];
        const startDate = new Date(bill.dueDate);
        let currentDate = new Date(startDate);
      
        const endDate = new Date(startDate);
        endDate.setFullYear(startDate.getFullYear() + 1); // Example: End after 1 year
      
        while (currentDate <= endDate) {
          events.push({
            title: `${bill.name}: $${bill.amount}`,
            resource: bill,
            start: new Date(currentDate),
            end: new Date(currentDate),
            allDay: true
          });
      
          switch (bill.frequency) {
            case 'weekly':
              currentDate.setDate(currentDate.getDate() + 7);
              break;
            case 'biweekly':
                currentDate.setDate(currentDate.getDate() + 7);
                break;
            case 'monthly':
              currentDate.setMonth(currentDate.getMonth() + 1);
              break;
            case 'yearly':
              currentDate.setFullYear(currentDate.getFullYear() + 1);
              break;
            default:
              console.log('Unknown frequency:', bill.frequency);
              return [];
          }
        }
      
        return events;
      };
      

    const billEvents = bills.flatMap(bill => {
  if (bill.recurring) {
    return generateRecurringEvents(bill);
  } else {
    return {
      title: `${bill.name}: $${bill.amount}`,
      start: new Date(bill.dueDate),
      end: new Date(bill.dueDate),
      allDay: true,
      resource: bill
    };
  }
});

  
return (
    <><div className="bill-page">
        <div className='title'>
            <h2>Bills</h2>
        </div>
        <div className="my-calendar-container">
        <MyCalendar events={billEvents} />
        </div>
            <form onSubmit={handleAddBill} className="add-bill-form">
                <input
                    type="text"
                    value={billName}
                    onChange={(e) => setBillName(e.target.value)}
                    placeholder="Bill Name"
                    required />
                <input
                    type="number"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                    placeholder="Amount"
                    required />
                <input
                    type="date"
                    value={dueDate}
                    onChange={(e) => setDueDate(e.target.value)}
                    placeholder="Due Date"
                    required />
                <label>
                    <input
                        type="checkbox"
                        checked={isRecurring}
                        onChange={(e) => setIsRecurring(e.target.checked)} />
                    Recurring?
                </label>
                {isRecurring && (
                    <select
                        value={frequency}
                        onChange={(e) => setFrequency(e.target.value)}
                        required
                    >
                        <option value="onetime">Select Frequency</option>
                        <option value="weekly">Weekly</option>
                        <option value="biweekly">Biweekly</option>
                        <option value="monthly">Monthly</option>
                        <option value="yearly">Yearly</option>
                    </select>
                )}
                <button type="submit">Add Bill</button>
            </form>
        </div></>
);
};

  export default BillsPage;
