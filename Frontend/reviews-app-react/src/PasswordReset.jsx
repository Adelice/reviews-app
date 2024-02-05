import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from 'axios';

const PasswordReset = () => {
  // State for form data
  const [formData, setFormData] = useState({
    email: '',
    newPassword: '',
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
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/reset-password', {
        email: formData.email,
        new_password: formData.newPassword,
      });
      console.log('Password reset successful:', response.data);
      // Redirect to sign-in page upon successful password reset
      navigate('/signin');
    } catch (error) {
      console.error('Error during password reset:', error.response?.data);
      // Display an appropriate error message based on the response
      if (error.response && error.response.status === 404) {
        setError('No account with this email exists.');
      } else {
        setError('An unexpected error occurred. Please try again.');
      }
    }
  };

  // JSX for the password reset form
  return (
    <div className="container mt-5">
      <h2>Reset Your Password</h2>
      {error && <div className="alert alert-danger" role="alert">{error}</div>}
      <form onSubmit={handleSubmit}>
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
          <label htmlFor="newPassword" className="form-label">New Password</label>
          <input
            type="password"
            className="form-control"
            id="newPassword"
            name="newPassword"
            value={formData.newPassword}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary">Reset Password</button>
      </form>
    </div>
  );
};

export default PasswordReset;
