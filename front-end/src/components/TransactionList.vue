<template>
    <div>
        <h2 class="alert alert-primary text-center">Transactions</h2>
        <div class="table-responsive">
            <table class="table table-striped">
                <thead>
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
                        <td>{{ transaction.user.username }}</td>
                        <td>{{ transaction.book.title }}</td>
                        <td>
                            <div
                                :class="['m-0 p-0 text-center rounded-4 alert', transaction.status === 'returned' ? 'alert-success' : 'alert-warning']">
                                {{ transaction.status }}
                            </div>
                        </td>
                        <td>{{ formatLongDate(transaction.borrow_date) }}</td>
                        <td>{{ transaction.return_date ? formatLongDate(transaction.return_date) : 'Pending Return' }}
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
import { formatLongDate } from '@/utils/dateUtils';

const transactions = ref([]);

const fetchTransactions = async () => {
    try {
        const response = await apiService.getTransactions();

        if (response.status === 200) {
            transactions.value = response.data.data;
        }
    } catch (error) {
        await Dialog.showMessageDialog('Error', `<div class="alert alert-danger h-100 m-0">${error.response.data.message || error.message}<div>`);
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