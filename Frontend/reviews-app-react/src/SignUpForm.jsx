import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from 'axios';

const SignUpForm = () => {
  // State for form data
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    birthday: '',
  });

  // State for error messages
  const [error, setError] = useState('');

  // Hook to navigate programmatically
  const navigate = useNavigate();

  // Update form data on user input
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
    setError(''); // Clear any existing error messages
  };

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    // Post request to your backend
    axios.post('http://localhost:5000/signup', {
      firstname: formData.firstName,
      lastname: formData.lastName,
      email: formData.email,
      password: formData.password,
      birthday: formData.birthday
    })
    .then(response => {
      console.log('Signup successful:', response.data);
      // Redirect to sign-in page upon successful sign-up
      navigate('/signin');
    })
    .catch(error => {
      console.error('Error during signup:', error.response.data);
      // Display an error message if the account already exists
      if (error.response && error.response.status === 409) {
        setError('An account with this email already exists.');
      } else {
        setError('An unexpected error occurred. Please try again.');
      }
    });
  };

  // JSX for the sign-up form
  return (
    <div className="container mt-5">
      <h2>Create Your Account</h2>
      {error && <div className="alert alert-danger" role="alert">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label htmlFor="firstName" className="form-label">First Name</label>
          <input
            type="text"
            className="form-control"
            id="firstName"
            name="firstName"
            value={formData.firstName}
            onChange={handleChange}
            required
          />
        </div>
        <div className="mb-3">
          <label htmlFor="lastName" className="form-label">Last Name</label>
          <input
            type="text"
            className="form-control"
            id="lastName"
            name="lastName"
            value={formData.lastName}
            onChange={handleChange}
            required
          />
        </div>
        <div className="mb-3">
          <label htmlFor="email" className="form-label">Email</label>
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
          <label htmlFor="password" className="form-label">Password</label>
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
        <div className="mb-3">
          <label htmlFor="birthday" className="form-label">Birthday</label>
          <input
            type="date"
            className="form-control"
            id="birthday"
            name="birthday"
            value={formData.birthday}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit" className="btn btn-danger">Sign Up</button>
      </form>
    </div>
  );
};

export default SignUpForm;
