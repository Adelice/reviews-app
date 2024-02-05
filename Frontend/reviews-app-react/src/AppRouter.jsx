import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './NavbarSection';
import BodySection from './BodySection';
import FooterSection from './FooterSection';
import SignUpForm from './SignUpForm';
import SignInForm from './SignInForm';
import PasswordReset from './PasswordReset';

const AppRouter = () => {
  return (
    <Router>
      <div>
        <Navbar />
        
        <Routes>
          <Route path="/signup" element={<SignUpForm />} />
          <Route path="/signin" element={<SignInForm />} />
          <Route path="/reset-password" element={<PasswordReset/>} />"
          <Route path="/" element={<BodySection />} />
        </Routes>
        <FooterSection />
      </div>
    </Router>
  );
};

export default AppRouter;