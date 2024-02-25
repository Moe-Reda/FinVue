import React, { useState } from 'react';

const ForgotPassword = () => {
  const [email, setEmail] = useState('');

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    // Here you would typically send the email to your backend to handle the password reset
    console.log("Email submitted:", email);
    // You can make an API call to your backend to handle the password reset process
  }

  return (
    <div className="forgot-password-page">
      <h2>Forgot Password</h2>
      <form onSubmit={handleSubmit}>
        <div className="forgot-password-form-group">
          <label htmlFor="email">Enter your email:</label>
          <input type="email" id="email" value={email} onChange={handleEmailChange} className="forgot-password-email-input" />
        </div>
        <button type="submit" className="forgot-password-submit-button">Submit</button>
      </form>
    </div>
  );
}

export default ForgotPassword;
