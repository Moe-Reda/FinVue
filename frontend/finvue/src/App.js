import logo from './logo.svg';
import './App.css';
import { useState } from 'react';
import Layout from './components/Layout';
import { Route, Routes } from 'react-router-dom';
import Login from './components/login/Login';
import Register from './components/register/Register';
import ForgotPassword from './components/forgotPassword/forgotPassword';
import TransactionForm from './components/transactionDashboard/TransactionDashboard';

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
        </Route>
      </Routes>
    </div>
  );
}

export default App
