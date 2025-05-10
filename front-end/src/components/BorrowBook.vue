<template>
  <div>
    <h2 class="alert alert-primary text-center">Borrow Book</h2>
    <div class="card p-3">
      <form @submit.prevent="borrow">
        <!-- Books Dropdown -->
        <div class="mb-2">
          <label class="form-label">Book to Borrow</label>
          <select v-model.number="borrowData.book_id" class="form-control" required>
            <option disabled value="" selected>Select Book</option>
            <option v-for="book in books" :key="book.id" :value="book.id">
              {{ book.title }} ({{ book.copies_available }} available)
            </option>
          </select>
        </div>

        <!-- Users Dropdown -->
        <div class="mb-2">
          <label class="form-label">User Borrowing</label>
          <select v-model.number="borrowData.user_id" class="form-control" required>
            <option disabled value="" selected>Select User</option>
            <option v-for="user in users" :key="user.id" :value="user.id">
              {{ user.username }}
            </option>
          </select>
        </div>

        <!-- Borrow Date -->
        <div class="mb-2">
          <label class="form-label">Borrow Date</label>
          <input type="date" v-model="borrowData.borrow_date" class="form-control" required>
        </div>

        <button type="submit" class="btn btn-success">Borrow Book</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import apiService from '@/services/apiService';
import Dialog from '@akamine96204/jsdialog';

const borrowData = ref({
  book_id: '',
  user_id: '',
  borrow_date: ''
});
const books = ref([]);
const users = ref([]);

// Fetch available books with copies > 0.
const fetchBooks = async () => {
  try {
    const response = await apiService.getAvailableBooks();
    // Assumes your API returns an object with a "data" property that's an array of books.
    books.value = response.data.data;
  } catch (error) {
    await Dialog.showMessageDialog('Error', `<div class="alert alert-danger h-100 m-0">${error.response.data.message || error.message}<div>`);
  }
};

// Fetch registered users.
const fetchUsers = async () => {
  try {
    const response = await apiService.getUsers();
    users.value = response.data;
  } catch (error) {
    await Dialog.showMessageDialog('Error', `<div class="alert alert-danger h-100 m-0">${error.response.data.message || error.message}<div>`);
  }
};

// Fetch both lists when the component is mounted.
onMounted(() => {
  fetchBooks();
  fetchUsers();
});

const borrow = async () => {
  try {
    const response = await apiService.borrowBook(borrowData.value);
    if (response.status === 201) {
      Dialog.showPlainDialog(response.data.message);
      // Reset the form after a successful borrow.
      borrowData.value = { book_id: '', user_id: '', borrow_date: '' };
      // Optionally refresh the available books list if copies count is updated.
      fetchBooks();
    }
  } catch (error) {
    await Dialog.showMessageDialog('Error', `<div class="alert alert-danger h-100 m-0">${error.response.data.message || error.message}<div>`);
  }
};
</script>