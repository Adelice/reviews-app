import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from 'axios';

const SignInForm = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [errorMessage, setErrorMessage] = useState(''); // State to hold error messages

  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    axios.post('http://localhost:5000/logintoken', {
        email: formData.email,
        password: formData.password
    })
    .then(response => {
        console.log('Sign-in successful:', response.data);
        navigate('/', { state : { firstName: response.data.firstname } });
    })
    .catch(error => {
        // Handle login errors
        console.error('Error during sign-in:', error.response ? error.response.data : error);
        // Set error message based on the error response or a default message
        setErrorMessage(error.response && error.response.data ? error.response.data.message : 'Login failed. Please check your email and password.');
    });
  };

  const handleSignUp = () => {
    navigate('/signup');
  };

  const handleForgotPassword = () => {
    navigate('/reset-password');
  };

  return (
    <div className="container mt-5">
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label htmlFor="email" className="form-label">
            Email
          </label>
          <input
            type="email"
            className="form-control"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>
        <div className="mb-3">
          <label htmlFor="password" className="form-label">
            Password
          </label>
          <input
            type="password"
            className="form-control"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>
        {/* Display error message if there is one */}
        {errorMessage && <div className="alert alert-danger" role="alert">{errorMessage}</div>}
        <button type="submit" className="btn btn-primary">
          Sign In
        </button>
        <div className="mt-3">
          <button type="button" className="btn btn-link" onClick={handleSignUp}>
            Don't have an account? Sign up
          </button>
          <button type="button" className="btn btn-link" onClick={handleForgotPassword}>
            Forgot Password?
          </button>
        </div>
      </form>
    </div>
  );
};

export default SignInForm;
