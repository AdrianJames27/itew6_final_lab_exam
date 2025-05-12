<template>
  <div class="container-fluid">
    <div class="row">
      <!-- Sidebar -->
      <aside class="col-12 col-md-3">
        <div class="sidebar">
          <div class="sidebar-header text-center">
            <h2 class="mb-0">
              <i class="bi bi-book" style="font-size: 2rem; color: white;"></i>
              Library Management System
            </h2>
          </div>
          <ul class="nav flex-column mt-3">
            <li class="nav-item" @click="activeTab = 'books'">
              <span :class="['nav-link', { active: activeTab === 'books' }]">
                <i :class="['bi bi-journal-bookmark', { 'active-icon': activeTab === 'books' }]" style="font-size: 1.2rem; margin-right: 8px;"></i> Books
              </span>
            </li>
            <li class="nav-item" @click="activeTab = 'borrow'">
              <span :class="['nav-link', { active: activeTab === 'borrow' }]">
                <i :class="['bi bi-arrow-right-circle', { 'active-icon': activeTab === 'borrow' }]" style="font-size: 1.2rem; margin-right: 8px;"></i> Borrow Book
              </span>
            </li>
            <li class="nav-item" @click="activeTab = 'return'">
              <span :class="['nav-link', { active: activeTab === 'return' }]">
                <i :class="['bi bi-arrow-left-circle', { 'active-icon': activeTab === 'return' }]" style="font-size: 1.2rem; margin-right: 8px;"></i> Return Book
              </span>
            </li>
            <li class="nav-item" @click="activeTab = 'transactions'">
              <span :class="['nav-link', { active: activeTab === 'transactions' }]">
                <i :class="['bi bi-credit-card', { 'active-icon': activeTab === 'transactions' }]" style="font-size: 1.2rem; margin-right: 8px;"></i> Transactions
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
  background: #551622;
  padding: 15px;
  border-right: 1px solid #ddd;
  color: white;
}


@media (min-width: 768px) {
  .sidebar {
    min-height: 100vh;
  }
}

.sidebar-header h2 {
  font-size: 1.5rem;
  margin: 0;
  color: white;
}

/* Navigation links styling */
.nav-link {
  cursor: pointer;
  user-select: none;
  padding: 10px;
  display: block;
  transition: background-color 0.2s;
  color: white;
}

.nav-link:hover {
  background-color: #e9ecef;
  color: #551622;
  border-radius: 14px;
  font-weight: bolder;
}

.nav-link.active {
  background-color: white;
  color: #551622;
  border-radius: 14px;
  font-weight: bolder;
}

.active-icon {
  color: #551622;
}




.container-fluid {
  background-color: #f8f9fa;
}

.tab-content {
  margin-left: 15px;
  margin-right: 15px;
}


i {
  color: white;
  transition: color 0.2s, font-weight 0.2s;
}

aside {
  padding: 0px;
}

ul li{
  padding-bottom: 10px;
}

.nav-link:hover i {
  color: #551622;
}
</style>
