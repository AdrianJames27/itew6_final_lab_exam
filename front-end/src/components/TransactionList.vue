<template>
  <div>
    <!-- Themed Header -->
    <h2 class="text-center text-white py-2 mb-4" style="background-color: #551622;">
      <i class="bi bi-card-list me-2"></i> Transactions
    </h2>

    <div class="table-responsive">
      <table class="table table-striped align-middle">
        <thead class="table-light">
          <tr>
            <th>Borrow ID</th>
            <th>User</th>
            <th>Book Title</th>
            <th>Status</th>
            <th>Date Borrowed</th>
            <th>Date Returned</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="transaction in transactions" :key="transaction.id">
            <td>{{ transaction.id }}</td>
            <td>{{ transaction.user ? transaction.user.username : 'User No Longer Available' }}</td>
            <td>{{ transaction.book ? transaction.book.title : 'Book No Longer Available' }}</td>

           <td>
  <div
    :class="[
      'alert d-flex align-items-center py-1 px-2 m-0 rounded-3',
      transaction.status === 'returned' ? 'alert-success' : 'alert-warning'
    ]"
    role="alert"
    style="font-size: 0.9rem;"
  >
    <i
      :class="transaction.status === 'returned' ? 'bi bi-check-circle-fill me-2' : 'bi bi-exclamation-triangle-fill me-2'"
    ></i>
    <span class="fw-semibold text-capitalize">{{ transaction.status }}</span>
  </div>
</td>


            <td>{{ formatLongDate(transaction.borrow_date) }}</td>
            <td>{{ transaction.return_date ? formatLongDate(transaction.return_date) : 'Pending Return' }}</td>
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
import { formatLongDate } from '@/utils/dateUtils';

const transactions = ref([]);

const fetchTransactions = async () => {
  try {
    const response = await apiService.getTransactions();
    if (response.status === 200) {
      transactions.value = response.data.data;
    }
  } catch (error) {
    await Dialog.showMessageDialog(
      'Error',
      `<div class="alert alert-danger h-100 m-0">${error.response.data.message || error.message}<div>`
    );
  }
};

onMounted(() => fetchTransactions());
</script>

<style scoped>
.table td {
  min-width: 150px;
  max-width: 350px;
  overflow-wrap: break-word;
}
</style>
