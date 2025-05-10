<template>
    <div>
        <h2 class="alert alert-primary text-center">Return Book</h2>
        <div class="table-responsive">
            <table class="table table-striped">
                <thead>
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
                                <button class="btn btn-success btn-sm" @click="openReturnDialog(transaction.id)">
                                    Return Book
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
                    <div class="modal-header">
                        <h5 class="modal-title">Return Book</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <label class="form-label">Return Date</label>
                        <input type="date" v-model="returnDate" class="form-control" />
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button class="btn btn-success" @click="returnBook">Confirm Return</button>
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

// Create a ref for the modal element
const returnModalEl = ref(null);
// Variable to hold the Bootstrap Modal instance.
let returnModal = null;

// Fetch pending transactions
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

// Open return book modal using the reactive modal reference
const openReturnDialog = (borrowId) => {
    selectedBorrowId.value = borrowId;
    returnDate.value = ''; // Reset input
    returnModal.show();
};

// Process return request
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
            Dialog.showPlainDialog(response.data.message);
            fetchTransactions(); // Refresh transactions list
        }
    } catch (error) {
        await Dialog.showMessageDialog('Error', `<div class="alert alert-danger h-100 m-0">${error.response.data.message || error.message}<div>`);
    }
};

onMounted(() => {
    fetchTransactions();
    // Create and assign the Bootstrap Modal instance using the modal element reference
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