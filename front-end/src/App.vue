<template>
  <div class="container-fluid">
    <div class="row">
      <!-- Sidebar -->
      <aside class="col-12 col-md-3">
        <div class="sidebar">
          <div class="sidebar-header">
            <h2 class="mb-0">Library Management System</h2>
          </div>
          <ul class="nav flex-column mt-3">
            <li class="nav-item" @click="activeTab = 'books'">
              <span :class="['nav-link', { active: activeTab === 'books' }]">
                Books
              </span>
            </li>
            <li class="nav-item" @click="activeTab = 'borrow'">
              <span :class="['nav-link', { active: activeTab === 'borrow' }]">
                Borrow Book
              </span>
            </li>
            <li class="nav-item" @click="activeTab = 'return'">
              <span :class="['nav-link', { active: activeTab === 'return' }]">
                Return Book
              </span>
            </li>
            <li class="nav-item" @click="activeTab = 'transactions'">
              <span :class="['nav-link', { active: activeTab === 'transactions' }]">
                Transactions
              </span>
            </li>
          </ul>
        </div>
      </aside>

      <!-- Main Content -->
      <div class="col-12 col-md-9">
        <div class="tab-content mt-4">
          <BookList v-if="activeTab === 'books'" />
          <BorrowBook v-if="activeTab === 'borrow'" />
          <ReturnBook v-if="activeTab === 'return'" />
          <TransactionList v-if="activeTab === 'transactions'" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import BookList from './components/BookList.vue';
import BorrowBook from './components/BorrowBook.vue';
import ReturnBook from './components/ReturnBook.vue';
import TransactionList from './components/TransactionList.vue';

const activeTab = ref('books');
</script>

<style scoped>
/* Sidebar styling */
.sidebar {
  background: #f8f9fa;
  padding: 15px;
  border-right: 1px solid #ddd;
}

/* On desktop, force the sidebar to take the full viewport height */
@media (min-width: 768px) {
  .sidebar {
    min-height: 100vh;
  }
}

.sidebar-header h2 {
  font-size: 1.5rem;
  margin: 0;
}

/* Navigation links styling */
.nav-link {
  cursor: pointer;
  user-select: none;
  padding: 10px;
  display: block;
  transition: background-color 0.2s;
}

.nav-link:hover {
  background-color: #e9ecef;
}

.nav-link.active {
  background-color: #007bff;
  color: #fff;
  border-radius: 4px;
}
</style>