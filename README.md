# Project Structure for a Poetry FastAPI Project

This is a guide to the recommended folder structure for a FastAPI project managed using Poetry. This structure helps maintain a clean and organized codebase, making it easier to manage and understand.

## Project Folders

- **core**: This folder should contain general configurations and utilities that are shared across various parts of your application. For example, you can put application settings and configurations, database connections, or other shared utilities in this directory.

- **engine**: The `engine` folder is where you define your data models. It typically contains a base model class specification that other specific models inherit from. These specific models define the structure of your data. Methods for each model are not explicitly defined here but are usually implemented in the `services` folder.

- **api**: The `api` folder is responsible for managing routing within your FastAPI application. You can organize your API routes into separate classes for better structure and maintainability. Each class in this folder might define a specific set of routes for different parts of your application.

## Why Use This Structure?

Using this folder structure helps maintain a well-organized and modular codebase for your FastAPI project. It separates concerns, making it easier to develop, test, and understand different parts of your application. It also encourages good coding practices and maintainability.

Feel free to adapt and expand this structure based on the specific needs of your project. The key is to keep your code organized and maintainable.

# Model Implementation Status

This repository implements the following models:

- **SENT (Sentiment Analysis):** Provides sentiment analysis for text inputs.

- **SUM (Summarization):** Generates concise summaries of input text.

- **NER (Named Entity Recognition):** Identifies and classifies named entities in text.

## Models Still Missing

The following models are currently under consideration or in progress:

- **QA (Question Answering):** Enables the system to answer questions based on provided context.

- **ZSC (Zero-Shot Classification):** Classifies input into predefined categories even when no training data is available.

- **Wiki:** A general-purpose model for retrieving information from a knowledge base.

## Roadmap

Stay tuned for updates as we continue to expand the range of implemented models!
