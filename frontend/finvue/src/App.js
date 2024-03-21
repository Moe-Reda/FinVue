import logo from './logo.svg';
import './App.css';
import { useState } from 'react';
import Layout from './components/Layout';
import { Route, Routes } from 'react-router-dom';
import Login from './components/login/Login';
import Register from './components/register/Register';
import ForgotPassword from './components/forgotPassword/forgotPassword';
import TransactionForm from './components/transactionDashboard/TransactionDashboard';
import UserStockDashboard from './components/userStockDashboard/UserStockDashboard';
import BudgetPage from './components/budgetPage/BudgetPage';
import SavingsPage from './components/savingsPage/savingsPage';
import UserCryptoDashboard from './components/userCryptoDashboard/UserCryptoDashboard';

function App() {
  const [loggedIn, setLoggedIn] = useState('');

  function changeLoggedIn(newValue) {
    setLoggedIn(newValue);
 }

  return (
    <div className="App">
     <Routes>
        <Route path="/" element={<Layout/>}>
          <Route path='/' element={<Login loggedIn={loggedIn} setLoggedIn={changeLoggedIn}/>}></Route>
          <Route path='/register' element={<Register loggedIn={loggedIn} setLoggedIn={changeLoggedIn}/>}></Route>
          <Route path='/forgot-password' element={<ForgotPassword/>}></Route>
          <Route path='/transaction-dashboard' element={<TransactionForm loggedIn={loggedIn} setLoggedIn={changeLoggedIn}/>}></Route>
          <Route path='/stocks' element={<UserStockDashboard loggedIn={loggedIn}/>}></Route>
          <Route path='/cryptos' element={<UserCryptoDashboard loggedIn={loggedIn}/>}></Route>
          <Route path='/budget' element={<BudgetPage loggedIn={loggedIn}/>}></Route>
          <Route path='/savings' element={<SavingsPage/>}></Route>
        </Route>
      </Routes>
    </div>
  );
}

export default App
