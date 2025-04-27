import React, { useState } from 'react';
import { Form, Button, Alert } from 'react-bootstrap';
import { useForm } from 'react-hook-form';

const CreateRecipePage = () => {
  const { register, handleSubmit, reset, formState: { errors } } = useForm();
  const [showSuccess, setShowSuccess] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const createRecipe = async (data) => {
    const token = localStorage.getItem('REACT_TOKEN_AUTH_KEY');

    try {
      const response = await fetch('/recipes/recipes', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ ...data, id: 0 })  // Important: Add id field
      });

      if (!response.ok) {
        const errorData = await response.text();
        throw new Error(`Failed to create recipe: ${errorData}`);
      }

      const result = await response.json();
      console.log('Recipe created:', result);

      setShowSuccess(true);
      setErrorMessage('');
      reset(); // clear form
    } catch (error) {
      console.error(error);
      setErrorMessage(error.message || 'Something went wrong');
      setShowSuccess(false);
    }
  };

  return (
    <div className="container mt-4">
      <h1>Create A Recipe</h1>

      {showSuccess && (
        <Alert variant="success">
          Recipe created successfully!
        </Alert>
      )}

      {errorMessage && (
        <Alert variant="danger">
          {errorMessage}
        </Alert>
      )}

      <Form onSubmit={handleSubmit(createRecipe)}>
        <Form.Group className="mb-3">
          <Form.Label>Title</Form.Label>
          <Form.Control
            type="text"
            {...register('title', { required: true, maxLength: 25 })}
            placeholder="Enter title"
          />
          {errors.title && (
            <small style={{ color: 'red' }}>
              {errors.title.type === "maxLength"
                ? "Title should be less than 25 characters"
                : "Title is required"}
            </small>
          )}
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Description</Form.Label>
          <Form.Control
            as="textarea"
            rows={5}
            {...register('description', { required: true, maxLength: 255 })}
            placeholder="Enter description"
          />
          {errors.description && (
            <small style={{ color: 'red' }}>
              {errors.description.type === "maxLength"
                ? "Description should be less than 255 characters"
                : "Description is required"}
            </small>
          )}
        </Form.Group>

        <Button type="submit" variant="primary">
          Save
        </Button>
      </Form>
    </div>
  );
};

export default CreateRecipePage;
