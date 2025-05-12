<template>
  <div>
    <!-- Styled Header -->
    <h2 class="text-center text-white py-2 mb-4" style="background-color: #551622;">
      <i class="bi bi-arrow-right-circle-fill me-2"></i> Borrow Book
    </h2>

    <!-- Card Form -->
    <div class="card shadow-sm border-0">
      <div class="card-body">
        <form @submit.prevent="borrow">
          <!-- Books Dropdown -->
          <div class="mb-3">
            <label class="form-label fw-bold" style="color: #551622;">Book to Borrow</label>
            <select v-model.number="borrowData.book_id" class="form-control" required>
              <option disabled value="" selected>Select Book</option>
              <option v-for="book in books" :key="book.id" :value="book.id">
                {{ book.title }} ({{ book.copies_available }} available)
              </option>
            </select>
          </div>

          <!-- Users Dropdown -->
          <div class="mb-3">
            <label class="form-label fw-bold" style="color: #551622;">User Borrowing</label>
            <select v-model.number="borrowData.user_id" class="form-control" required>
              <option disabled value="" selected>Select User</option>
              <option v-for="user in users" :key="user.id" :value="user.id">
                {{ user.username }}
              </option>
            </select>
          </div>

          <!-- Borrow Date -->
          <div class="mb-3">
            <label class="form-label fw-bold" style="color: #551622;">Borrow Date</label>
            <input
              type="date"
              v-model="borrowData.borrow_date"
              class="form-control"
              :min="today"
              required
            />
          </div>

          <!-- Submit Button -->
          <div class="text-end">
            <button type="submit" class="btn" style="background-color: #551622; color: white;">
              <i class="bi bi-check-circle me-1"></i> Borrow Book
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import apiService from '@/services/apiService';
import Dialog from '@akamine96204/jsdialog';

const today = new Date().toISOString().split('T')[0];

const borrowData = ref({
  book_id: '',
  user_id: '',
  borrow_date: today
});

const books = ref([]);
const users = ref([]);

const fetchBooks = async () => {
  try {
    const response = await apiService.getAvailableBooks();
    books.value = response.data.data;
  } catch (error) {
    await Dialog.showMessageDialog('Error', `<div class="alert alert-danger h-100 m-0">${error.response.data.message || error.message}</div>`);
  }
};

const fetchUsers = async () => {
  try {
    const response = await apiService.getUsers();
    users.value = response.data;
  } catch (error) {
    await Dialog.showMessageDialog('Error', `<div class="alert alert-danger h-100 m-0">${error.response.data.message || error.message}</div>`);
  }
};

const borrow = async () => {
  const selectedDate = new Date(borrowData.value.borrow_date);
  const now = new Date();
  now.setHours(0, 0, 0, 0);

  if (selectedDate < now) {
    await Dialog.showMessageDialog(
      'Validation Error',
      '<div class="alert alert-warning m-0">Borrow date cannot be in the past.</div>'
    );
    return;
  }

  try {
    const response = await apiService.borrowBook(borrowData.value);
    if (response.status === 201) {
      Dialog.showPlainDialog(`<div class="alert text-white m-0" style="background-color: #28a745;">${response.data.message}</div>`);
      borrowData.value = {
        book_id: '',
        user_id: '',
        borrow_date: today
      };
      fetchBooks();
    }
  } catch (error) {
    await Dialog.showMessageDialog('Error', `<div class="alert alert-danger h-100 m-0">${error.response.data.message || error.message}</div>`);
  }
};

onMounted(() => {
  fetchBooks();
  fetchUsers();
});
</script>
