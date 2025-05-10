import axios from 'axios';

// Create an Axios instance with a default base URL (assumes your Django API endpoints start with /api/)
const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/',
    headers: {
        'Content-Type': 'application/json'
    }
});

// Books endpoints
export default {
    // Book endpoints
    async getBooks() {
        return api.get('books/');
    },
    async addBook(bookData) {
        return api.post('books/', bookData);
    },
    async updateBook(bookId, bookData) {
        return api.put(`books/${bookId}/`, bookData);
    },
    async deleteBook(bookId) {
        return api.delete(`books/${bookId}/`);
    },
    async getAvailableBooks() {
        return api.get('books/available/');
    },

    // User list
    async getUsers() {
        return api.get('users/');
    },

    // Borrow and return endpoints
    async borrowBook(borrowData) {
        return api.post('borrow/', borrowData);
    },
    async returnBook(borrowId, returnDate) {
        return api.post(`return/${borrowId}/`, returnDate);
    },
    
    // Transactions endpoint
    async getTransactions() {
        return api.get('transactions/');
    }
};