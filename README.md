# Project Structure for a Poetry FastAPI Project

This is a guide to the recommended folder structure for a FastAPI project managed using Poetry. This structure helps maintain a clean and organized codebase, making it easier to manage and understand.

## Project Folders

- **config**: This folder should contain general configurations and utilities that are shared across various parts of your application. For example, you can put application settings and configurations, database connections, or other shared utilities in this directory.

- **models**: The `models` folder is where you define your data models. It typically contains a base model class specification that other specific models inherit from. These specific models define the structure of your data. Methods for each model are not explicitly defined here but are usually implemented in the `services` folder.

- **services**: The `services` folder is where you define the methods and functions that interact with your data models. This is where you can implement all the logic for querying, processing, and manipulating data. For example, services might include functions for database queries, input/output parsing, or any other data-related operations.

- **routers**: The `routers` folder is responsible for managing routing within your FastAPI application. You can organize your API routes into separate classes for better structure and maintainability. Each class in this folder might define a specific set of routes for different parts of your application.

## Why Use This Structure?

Using this folder structure helps maintain a well-organized and modular codebase for your FastAPI project. It separates concerns, making it easier to develop, test, and understand different parts of your application. It also encourages good coding practices and maintainability.

Feel free to adapt and expand this structure based on the specific needs of your project. The key is to keep your code organized and maintainable.
