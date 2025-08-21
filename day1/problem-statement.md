### 📖 Problem Statement

A small community library maintains its book catalog in a simple **CSV file**. To modernize access to its catalog, the library wants to expose the book data as a **RESTful API**.

The system should support **GET requests only**, with the following requirements:

1. **Retrieve all books**

   - Endpoint: `/books`
   - Returns the full list of books available in the catalog.

2. **Retrieve a specific book by ID**

   - Endpoint: `/books/{id}`
   - Returns details of a single book identified by its unique ID.
   - If the book does not exist, the system should return an error with HTTP status `404 Not Found`.

3. **Retrieve books by author**

   - Endpoint: `/books?author={author_name}`
   - Returns all books written by the specified author.
   - If no books by that author exist, the system should return an empty list.

Additional Requirements:

- Data must be read from a **CSV file** that stores book details (`id`, `title`, `author`, `year`).
- API responses should be returned in **JSON format**.
- The design should follow **REST best practices**, including:

  - Resource-oriented URIs (`/books`, `/books/{id}`)
  - Statelessness (each request is independent)
  - Standard HTTP status codes (`200 OK`, `404 Not Found`)

The goal is to provide a simple yet robust example of applying **REST concepts** in a real-world context where data is stored in a flat file but exposed as a structured, resource-based service.
