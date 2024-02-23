import React from 'react'
import { useState } from 'react';
import {Icon} from 'react-icons-kit';
import {eyeOff} from 'react-icons-kit/feather/eyeOff';
import {eye} from 'react-icons-kit/feather/eye';
import "./Login.css";
import api from '../../api/axiosConfig';
import { useNavigate } from "react-router-dom";

function Login({loggedIn, setLoggedIn}) {
    const navigate = useNavigate();

    const [password, setPassword] = useState('');
    const [username, setUsername] = useState('');
    const [type, setType] = useState('password');
    const [icon, setIcon] = useState(eyeOff);

    const handleToggle = () => {
        if (type==='password'){
           setIcon(eye);
           setType('text')
        } else {
           setIcon(eyeOff)
           setType('password')
        }
     }

    const handleUsernameChange = (e) => {
        setUsername(e.target.value);
    }

    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        // Add login logic here
        console.log("Username:", username);
        console.log("Password:", password);
        // You can send the username and password to the server for authentication
        var status = 0;
        try {
            const response = await api.post('http://127.0.0.1:5000/api/login_user', {
              username,
              password
            });
            status = response.status;
        } catch (error) {
            console.error('Error fetching user login:', error);
            return null;
        }
        if(status === 200){
            setLoggedIn(username);
            navigate('/transaction-dashboard');
        }
    }

    return (
        <div className="container-login">
            <h1>FinVue</h1>
            <form onSubmit={handleSubmit} className="form-login">
                <div className="username-login-form-group">
                    <label htmlFor="username" className='username-login-label'>Username</label>
                    <input type="text" id="username" placeholder="Username" value={username} onChange={handleUsernameChange} className='username-login-input'/>
                </div>
                <div className="password-login-form-group">
                    <div class="password-container">
                        <label htmlFor="password" className='password-login-label'>Password</label>
                        <input
                            type={type}
                            name="password"
                            id="password"
                            placeholder="Password"
                            value={password}
                            onChange={handlePasswordChange}
                            autoComplete="current-password"
                            className='password-login-input'
                        />
                        <span class="password-eye-icon" onClick={handleToggle}>
                            <Icon class="absolute mr-10" icon={icon} size={25}/>
                        </span>
                    </div>
                </div>
                <button type="submit" className='submit-login-button'>Submit</button>
                <button onClick={() => { navigate('/register') }} className='register-login-button'>Register</button>
                <div className='forgot-password-login-container'>
                    <a href="/forgot-password" className='forgot-password-login-link'>Forgot your password ?</a>
                </div>
            </form>
        </div>
    );
}

export default Login
