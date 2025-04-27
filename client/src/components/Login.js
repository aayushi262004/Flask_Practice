import React from 'react';
import { Form, Button } from 'react-bootstrap';
import { Link, useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { login } from '../auth';

const LoginPage = () => {
  const { register, handleSubmit, reset, formState: { errors } } = useForm();
  const navigate = useNavigate();

  const loginUser = (data) => {
    console.log(data);

    const requestOptions = {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
    };

    fetch('/auth/login', requestOptions)
      .then(res => res.json())
      .then(responseData => {
        console.log(responseData.access_token);

        if (responseData.access_token) {
          login(responseData.access_token);
          navigate('/'); // redirect to home page
        } else {
          alert('Invalid username or password');
        }
      });

    reset();
  };

  return (
    <div className="container">
      <div className="form">
        <h1>Login Page</h1>
        <form onSubmit={handleSubmit(loginUser)}>
          <Form.Group>
            <Form.Label>Username</Form.Label>
            <Form.Control
              type="text"
              placeholder="Your username"
              {...register('username', { required: true, maxLength: 25 })}
            />
          </Form.Group>
          {errors.username?.type === "required" && (
            <p style={{ color: 'red' }}><small>Username is required</small></p>
          )}
          {errors.username?.type === "maxLength" && (
            <p style={{ color: 'red' }}><small>Username must be 25 characters max</small></p>
          )}

          <br />

          <Form.Group>
            <Form.Label>Password</Form.Label>
            <Form.Control
              type="password"
              placeholder="Your password"
              {...register('password', { required: true, minLength: 8 })}
            />
          </Form.Group>
          {errors.password?.type === "required" && (
            <p style={{ color: 'red' }}><small>Password is required</small></p>
          )}
          {errors.password?.type === "minLength" && (
            <p style={{ color: 'red' }}><small>Password should be at least 8 characters</small></p>
          )}

          <br />
          <Form.Group>
            <Button type="submit" variant="primary">Login</Button>
          </Form.Group>
          <br />
          <Form.Group>
            <small>Don’t have an account? <Link to='/signup'>Create One</Link></small>
          </Form.Group>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;
