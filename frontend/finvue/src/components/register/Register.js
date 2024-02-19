import React from 'react'
import { useState } from 'react';
import {Icon} from 'react-icons-kit';
import {eyeOff} from 'react-icons-kit/feather/eyeOff';
import {eye} from 'react-icons-kit/feather/eye';
import api from '../../api/axiosConfig';
import { useNavigate } from "react-router-dom";

function Register({loggedIn, setLoggedIn}) {
      
      const navigate = useNavigate();

      const [username, setUsername] = useState('');
      const [email, setEmail] = useState('');
      const [password, setPassword] = useState('');
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
    
      const handleEmailChange = (e) => {
        setEmail(e.target.value);
      }
    
      const handlePasswordChange = (e) => {
        setPassword(e.target.value);
      }
    
      const handleSubmit = async (e) => {
        e.preventDefault();
        // Add registration logic here
        console.log("Username:", username);
        console.log("Email:", email);
        console.log("Password:", password);
        // You can send the registration data to the server for processing
        var status = 0;
        try {
            const response = await api.post('http://127.0.0.1:5000/api/register_user', {
              username,
              email,
              password
            });
            status = response.status;
        } catch (error) {
            console.error('Error registering user:', error);
            return null;
        }
        if(status === 201){
            setLoggedIn(username);
            navigate('/transaction-dashboard');
        }
      }
    
      return (
        <div className="container-register">
          <form onSubmit={handleSubmit} className="form-register">
              <div className="username-register-form-group">
                <label htmlFor="username" className='username-register-label'>Username</label>
                <input type="text" id="username" value={username} onChange={handleUsernameChange} className='username-register-input'/>
              </div>
              <div className="email-register-form-group">
                <label htmlFor="email" className='email-register-label'>Email</label>
                <input type="email" id="email" value={email} onChange={handleEmailChange} className='email-register-input'/>
              </div>
              <div className="password-register-form-group">
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
              <button type="submit" className='submit-register-button' onClick={handleSubmit}>Submit</button>
              <button onClick={() => { navigate('/') }} className='submit-register-button'>Login</button>
          </form>
        </div>
      );
    
}

export default Register
