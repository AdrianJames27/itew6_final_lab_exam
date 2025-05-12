<template>
  <div>
    <!-- Styled Header -->
    <h2 class="text-center text-white py-2 mb-4" style="background-color: #551622;">
      <i class="bi bi-arrow-return-left me-2"></i> Return Book
    </h2>

    <div class="table-responsive">
      <table class="table table-striped">
        <thead class="table-light">
          <tr>
            <th>Borrow ID</th>
            <th>User</th>
            <th>Book Title</th>
            <th>Borrow Date</th>
            <th>Return Date</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <template v-if="pendingTransactions.length > 0">
            <tr v-for="transaction in pendingTransactions" :key="transaction.id">
              <td>{{ transaction.id }}</td>
              <td>{{ transaction.user.username }}</td>
              <td>{{ transaction.book.title }}</td>
              <td>{{ formatLongDate(transaction.borrow_date) }}</td>
              <td>
                {{ transaction.return_date ? formatLongDate(transaction.return_date) : 'Pending' }}
              </td>
              <td>
                <button
                  class="btn btn-sm text-white"
                  style="background-color: #551622;"
                  @click="openReturnDialog(transaction.id)"
                >
                  <i class="bi bi-check-circle me-1"></i> Return Book
                </button>
              </td>
            </tr>
          </template>
          <template v-else>
            <tr>
              <td colspan="6" class="text-center">No pending return/s</td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>

    <!-- Bootstrap Modal for Return Date Input -->
    <div class="modal fade" id="returnModal" tabindex="-1" aria-hidden="true" ref="returnModalEl">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header text-white" style="background-color: #551622;">
            <h5 class="modal-title">
              <i class="bi bi-calendar-check me-2"></i> Confirm Return
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <label class="form-label fw-bold" style="color: #551622;">Return Date</label>
            <input type="date" v-model="returnDate" class="form-control" />
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button
              class="btn text-white"
              style="background-color: #551622;"
              @click="returnBook"
            >
              <i class="bi bi-check2-circle me-1"></i> Confirm Return
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { Modal } from 'bootstrap';
import apiService from '@/services/apiService';
import Dialog from '@akamine96204/jsdialog';
import { formatLongDate } from '@/utils/dateUtils';

const transactions = ref([]);
const pendingTransactions = ref([]);
const selectedBorrowId = ref(null);
const returnDate = ref('');

const returnModalEl = ref(null);
let returnModal = null;

const fetchTransactions = async () => {
  try {
    const response = await apiService.getTransactions();
    if (response.status === 200) {
      transactions.value = response.data.data;
      pendingTransactions.value = transactions.value.filter((t) => t.status === 'borrowed');
    }
  } catch (error) {
    await Dialog.showMessageDialog('Error', `<div class="alert alert-danger h-100 m-0">${error.response.data.message || error.message}<div>`);
  }
};

const openReturnDialog = (borrowId) => {
  selectedBorrowId.value = borrowId;
  returnDate.value = '';
  returnModal.show();
};

const returnBook = async () => {
  if (!returnDate.value) {
    await Dialog.showMessageDialog('Field Required', 'Return date is required.');
    return;
  }

  try {
    const response = await apiService.returnBook(selectedBorrowId.value, {
      return_date: returnDate.value,
    });

    if (response.status === 200) {
      returnModal.hide();
      Dialog.showPlainDialog(`<div class="alert text-white m-0" style="background-color: #28a745;">${response.data.message}</div>`);
      fetchTransactions();
    }
  } catch (error) {
    await Dialog.showMessageDialog('Error', `<div class="alert alert-danger h-100 m-0">${error.response.data.message || error.message}<div>`);
  }
};

onMounted(() => {
  fetchTransactions();
  returnModal = new Modal(returnModalEl.value);
});
</script>

<style scoped>
.table td {
  min-width: 150px;
  max-width: 350px;
  overflow-wrap: break-word;
}
</style>
