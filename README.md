
# Digital Infrastructure for Student Association

This project involves the development of a comprehensive digital infrastructure for a student association, encompassing a database, API, user interface application, and locally hosted Large Language Model (LLM) integration.

## Project Overview

The aim is to create a cohesive system that streamlines the association's operations, facilitates data management, and provides an intuitive interface for users. The integration of an LLM enhances the system's capabilities, offering advanced features such as natural language processing.

## Features

- **Database Management**: Utilizes SQLAlchemy for efficient database interactions.
- **API Development**: Built with Pydantic for data validation and FastAPI for creating robust APIs.
- **User Interface**: Developed using Streamlit to provide an accessible and user-friendly experience.
- **LLM Integration**: Incorporates a locally hosted Large Language Model to enhance functionality.

## Technology Stack

- **Polars**: For efficient data manipulation and analysis.
- **Pydantic**: Ensures data validation and parsing.
- **SQLAlchemy**: Manages database operations.
- **Streamlit**: Creates the web-based user interface.
- **OpenAI**: Powers the Large Language Model integration.

## Installation and Usage

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/koop46/M10_infrastructure.git
   cd M10_infrastructure
   ```

2. **Backend Setup**:

   - Navigate to the backend directory:

     ```bash
     cd backend
     ```

   - Install backend dependencies:

     ```bash
     pip install -r requirements.txt
     ```

   - Start the API server:

     ```bash
     uvicorn main:app --reload
     ```

3. **Frontend Setup**:

   - Navigate to the frontend directory:

     ```bash
     cd ../frontend
     ```

   - Install frontend dependencies:

     ```bash
     pip install -r requirements.txt
     ```

   - Run the Streamlit app:

     ```bash
     streamlit run app.py
     ```

4. **LLM Integration**:

   - Ensure the OpenAI API key is set up in your environment variables.
   - The LLM functionalities will be accessible within the Streamlit app.

## Repository Contents

- **backend/**: Contains the source code and configurations for the backend API.
- **frontend/**: Houses the source code for the user interface application.
- **.gitignore**: Specifies files and directories to be ignored by Git.
- **README.md**: Provides an overview and details about the project.
