<template>
    <div>
        <h2 class="alert alert-primary text-center">Book List</h2>
        <div class="mb-3">
            <button class="btn btn-primary" @click="toggleAddBookForm">
                {{ showAddBookForm ? 'Hide' : 'Add Book' }}
            </button>
        </div>

        <!-- Add Book Form -->
        <div v-if="showAddBookForm" class="card p-3 mb-3">
            <h4>Add New Book</h4>
            <form @submit.prevent="addBook">
                <div class="mb-2">
                    <input v-model="newBook.title" class="form-control" placeholder="Title" required>
                </div>
                <div class="mb-2">
                    <input v-model="newBook.author" class="form-control" placeholder="Author" required>
                </div>
                <div class="mb-2">
                    <input v-model="newBook.isbn" class="form-control" placeholder="ISBN" required>
                </div>
                <div class="mb-2">
                    <input type="number" v-model.number="newBook.copies_available" class="form-control"
                        placeholder="Available copies" required>
                </div>
                <button type="submit" class="btn btn-success">Add Book</button>
            </form>
        </div>

        <!-- Edit Book Form -->
        <div v-if="selectedBook" class="card p-3">
            <h4>Edit Book</h4>
            <form @submit.prevent="updateBook">
                <div class="mb-2">
                    <input v-model="selectedBook.title" class="form-control" placeholder="Title" required>
                </div>
                <div class="mb-2">
                    <input v-model="selectedBook.author" class="form-control" placeholder="Author" required>
                </div>
                <div class="mb-2">
                    <input v-model="selectedBook.isbn" class="form-control" placeholder="ISBN" required>
                </div>
                <div class="mb-2">
                    <input type="number" v-model.number="selectedBook.copies_available" class="form-control"
                        placeholder="Available copies" required>
                </div>
                <button type="submit" class="btn btn-primary me-2">Update</button>
                <button type="button" class="btn btn-secondary" @click="cancelEdit">Cancel</button>
            </form>
        </div>

        <!-- Book List -->
        <div class="table-responsive">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Title</th>
                        <th>Author</th>
                        <th>ISBN</th>
                        <th>Available Copies</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="book in books" :key="book.id">
                        <td>{{ book.title }}</td>
                        <td>{{ book.author }}</td>
                        <td>{{ book.isbn }}</td>
                        <td>{{ book.copies_available }}</td>
                        <td>
                            <button class="btn btn-sm btn-warning me-2" @click="editBook(book)">Edit</button>
                            <button class="btn btn-sm btn-danger" @click="confirmDelete(book.id)">Delete</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import apiService from '@/services/apiService';
import Dialog from '@akamine96204/jsdialog';

const books = ref([]);
const showAddBookForm = ref(false);
const newBook = ref({
    title: '',
    author: '',
    isbn: '',
    copies_available: 0
});
const selectedBook = ref(null);

const fetchBooks = async () => {
    try {
        const response = await apiService.getBooks();

        if (response.status === 200) {
            books.value = response.data;
        }
    } catch (error) {
        await Dialog.showMessageDialog('Error', `<div class="alert alert-danger h-100 m-0">${error.response.data.message || error.message}<div>`);
    }
};

const toggleAddBookForm = () => {
    showAddBookForm.value = !showAddBookForm.value;
};

const addBook = async () => {
    try {
        const response = await apiService.addBook(newBook.value);

        if (response.status === 201) {
            fetchBooks();
            Dialog.showPlainDialog('Book added successfully!');

            // reset form values
            newBook.value = { title: '', author: '', isbn: '', copies_available: 0 };
            showAddBookForm.value = false;
        }
    } catch (error) {
        await Dialog.showMessageDialog('Error', `<div class="alert alert-danger h-100 m-0">${error.response.data.message || error.message}<div>`);
    }
};

const editBook = (book) => {
    // Clone book object to avoid direct mutation.
    selectedBook.value = { ...book };
};

const updateBook = async () => {
    try {
        const response = await apiService.updateBook(selectedBook.value.id, selectedBook.value);

        if (response.status === 200) {
            fetchBooks();
            Dialog.showPlainDialog('Book updated successfully!');

            selectedBook.value = null;
        }
    } catch (error) {
        await Dialog.showMessageDialog('Error', `<div class="alert alert-danger h-100 m-0">${error.response.data.message || error.message}<div>`);
    }
};

const cancelEdit = () => {
    selectedBook.value = null;
};

const confirmDelete = async (bookId) => {
    const response = await Dialog.showConfirmDialog(
        'Confirm Deletion?',
        'Are you sure you want to delete this book?',
        {
            'eventStyles': {
                '#confirmDialogBtnYes': {
                    mouseenter: {
                        'background': 'maroon'
                    }
                }
            }
        }
    );

    if (response.option === Dialog.YES_OPTION) {
        deleteBook(bookId);
    }
};

const deleteBook = async (bookId) => {
    try {
        const response = await apiService.deleteBook(bookId);

        if (response.status === 204) {
            fetchBooks();
            Dialog.showPlainDialog('Book deleted successfully!');
        }
    } catch (error) {
        await Dialog.showMessageDialog('Error', `<div class="alert alert-danger h-100 m-0">${error.response.data.message || error.message}<div>`);
    }
};

onMounted(() => fetchBooks());
</script>

<style scoped>
.table td {
    min-width: 150px;
    max-width: 350px;
    overflow-wrap: break-word;
}
</style>