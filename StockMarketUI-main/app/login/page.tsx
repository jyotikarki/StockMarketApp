"use client";

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import styled from 'styled-components';
import { FaEye, FaEyeSlash } from 'react-icons/fa';

// Styled components
const LoginContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: linear-gradient(135deg, #00aaff, #0077ff); /* Attractive gradient background */
`;

const LoginForm = styled.form`
  display: flex;
  flex-direction: column;
  width: 350px;
  background-color: rgba(255, 255, 255, 0.9); /* Slightly transparent white background */
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  text-align: center;
`;

const InputGroup = styled.div`
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
`;

const InputLabel = styled.label`
  text-align: left;
  font-size: 14px;
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
`;

const Input = styled.input`
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 16px;
  color: #333;
  width: 100%; /* Ensures the input takes full width */
  box-sizing: border-box; /* Includes padding and border in element's total width and height */
`;

const Button = styled.button`
  padding: 15px;
  background-color: #0077ff;
  color: #ffffff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  font-size: 16px;
  width: 100%; /* Ensures the button takes full width */
  box-sizing: border-box;
  
  &:hover {
    background-color: #005bb5;
  }
`;

const ErrorMessage = styled.p`
  color: #e74c3c;
  margin-top: 15px;
`;

const PasswordContainer = styled.div`
  position: relative;
  width: 100%;
`;

const PasswordInput = styled(Input)`
  padding-right: 40px; /* Space for the toggle button */
`;

const ToggleButton = styled.button`
  position: absolute;
  top: 50%;
  right: 10px; /* Space from the right edge */
  transform: translateY(-50%);
  background: transparent;
  border: none;
  cursor: pointer;
  color: #0077ff;
  font-size: 20px;
`;

const WelcomeMessage = styled.h1`
  color: #333;
  font-weight: bold;
  margin-bottom: 20px;
  font-size: 2.2em; /* Slightly larger font size */
  background: -webkit-linear-gradient(45deg, #ff6b6b, #f9ca24, #1dd1a1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
`;

const Disclaimer = styled.p`
  color: #e74c3c; /* Red color for attention */
  font-size: 14px;
  margin-top: 20px;
  text-align: center;
  font-style: italic;
  max-width: 350px;
`;

// Login component
const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const router = useRouter();

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    if (username === 'testuser' && password === 'password') {
      localStorage.setItem('authenticated', 'true');
      router.push('/'); // Redirect to the dashboard
    } else {
      setError('Invalid credentials');
    }
  };

  return (
    <LoginContainer>
      <LoginForm onSubmit={handleLogin}>
        <WelcomeMessage>Welcome to Stock Market App</WelcomeMessage>

        <InputGroup>
          <InputLabel htmlFor="username">Username</InputLabel>
          <Input
            id="username"
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </InputGroup>

        <InputGroup>
          <InputLabel htmlFor="password">Password</InputLabel>
          <PasswordContainer>
            <PasswordInput
              id="password"
              type={showPassword ? 'text' : 'password'}
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <ToggleButton
              type="button"
              onClick={() => setShowPassword(!showPassword)}
            >
              {showPassword ? <FaEyeSlash /> : <FaEye />}
            </ToggleButton>
          </PasswordContainer>
        </InputGroup>

        <Button type="submit">Login</Button>
        {error && <ErrorMessage>{error}</ErrorMessage>}
        
        <Disclaimer>
          Stocks investments are subject to market risks. Read all related documents carefully.
        </Disclaimer>
      </LoginForm>
    </LoginContainer>
  );
};

export default Login;
