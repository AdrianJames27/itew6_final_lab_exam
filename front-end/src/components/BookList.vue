<template>
  <div class="container py-4">
    <h2 class="alert text-center" style="background-color: #551622; color: white">
      <i class="bi bi-book" style="color: white"></i> Book List
    </h2>

    <!-- Add Book Button -->
    <div class="mb-3 text-end">
      <button
        class="btn"
        :style="{ backgroundColor: '#1C324B', color: 'white' }"
        @click="toggleAddBookForm"
      >
        <i class="bi bi-plus-circle"></i> {{ showAddBookForm ? "Add Book" : "Add Book" }}
      </button>
    </div>

    <!-- Add Book Form Modal -->
    <div v-if="showAddBookForm" class="modal fade show" tabindex="-1" style="display: block">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content" :style="{ backgroundColor: 'white' }">
          <div class="modal-header" :style="{ backgroundColor: '#223952', color: 'white' }">
            <h5 class="modal-title">Add New Book</h5>
            <button
              type="button"
              class="btn-close"
              @click="toggleAddBookForm"
              aria-label="Close"
            ></button>
          </div>
          <form @submit.prevent="addBook">
            <div class="modal-body">
              <div class="mb-2">
                <input v-model="newBook.title" class="form-control" placeholder="Title" required />
              </div>
              <div class="mb-2">
                <input
                  v-model="newBook.author"
                  class="form-control"
                  placeholder="Author"
                  required
                />
              </div>
              <div class="mb-2">
                <input v-model="newBook.isbn" class="form-control" placeholder="ISBN" required />
              </div>
              <div class="mb-2">
                <input
                  type="number"
                  v-model.number="newBook.copies_available"
                  class="form-control"
                  placeholder="Available copies"
                  required
                />
              </div>
            </div>
            <div class="modal-footer">
              <button
                type="submit"
                class="btn"
                :style="{ backgroundColor: '#1C324B', color: 'white' }"
              >
                <i class="bi bi-plus-circle"></i> Add Book
              </button>
              
              
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Edit Book Form Modal -->
    <div v-if="selectedBook" class="modal fade show" tabindex="-1" style="display: block">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content" :style="{ backgroundColor: 'white' }">
          <div class="modal-header" :style="{ backgroundColor: '#F7EFE3', color: '#551622' }">
            <h5 class="modal-title">Edit Book</h5>
            <button type="button" class="btn-close" @click="cancelEdit" aria-label="Close"></button>
          </div>
          <form @submit.prevent="updateBook">
            <div class="modal-body">
              <div class="mb-2">
                <input
                  v-model="selectedBook.title"
                  class="form-control"
                  placeholder="Title"
                  required
                />
              </div>
              <div class="mb-2">
                <input
                  v-model="selectedBook.author"
                  class="form-control"
                  placeholder="Author"
                  required
                />
              </div>
              <div class="mb-2">
                <input
                  v-model="selectedBook.isbn"
                  class="form-control"
                  placeholder="ISBN"
                  required
                />
              </div>
              <div class="mb-2">
                <input
                  type="number"
                  v-model.number="selectedBook.copies_available"
                  class="form-control"
                  placeholder="Available copies"
                  required
                />
              </div>
            </div>
            <div class="modal-footer">
              <button
                type="submit"
                class="btn"
                :style="{ backgroundColor: '#F7EFE3', color: '#551622' }"
              >
                Update
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Book List Cards -->
    <div class="row">
      <div class="col-md-4" v-for="book in books" :key="book.id">
        <div
          class="card mb-4"
          style="background-color: white; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1)"
        >
          <div class="card-body">
            <h5 class="card-title" style="color: #223952">{{ book.title }}</h5>
            <p class="card-text" style="color: #223952">
              <strong>Author:</strong> {{ book.author }}
            </p>
            <p class="card-text" style="color: #223952"><strong>ISBN:</strong> {{ book.isbn }}</p>
            <p class="card-text" style="color: #223952">
              <strong>Available Copies:</strong> {{ book.copies_available }}
            </p>
            <div class="d-flex justify-content-end">
              <button
                class="btn btn-sm"
                :style="{ backgroundColor: '#F7EFE3', color: '#551622' }"
                @click="editBook(book)"
              >
                <i class="bi bi-pencil-square"></i> Edit
              </button>
              <button class="btn btn-sm ms-2":style="{ backgroundColor: '#551622', color: 'white' }" @click="confirmDelete(book.id)">
                <i class="bi bi-trash"></i> Delete
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import apiService from "@/services/apiService";
import Dialog from "@akamine96204/jsdialog";

const books = ref([]);
const showAddBookForm = ref(false);
const newBook = ref({
  title: "",
  author: "",
  isbn: "",
  copies_available: 0,
});
const selectedBook = ref(null);

const fetchBooks = async () => {
  try {
    const response = await apiService.getBooks();

    if (response.status === 200) {
      books.value = response.data;
    }
  } catch (error) {
    await Dialog.showMessageDialog(
      "Error",
      `<div class="alert alert-danger h-100 m-0">${
        error.response.data.message || error.message
      }<div>`
    );
  }
};
const showSuccessDialog = (message) => {
  Dialog.showPlainDialog(message, {
    eventStyles: {
      ".dialog-message": {
        backgroundColor: "green", 
        color: "white",
        padding: "15px",
        borderRadius: "8px",
        fontWeight: "bold",
        textAlign: "center",
      },
    },
  });
};

const toggleAddBookForm = () => {
  showAddBookForm.value = !showAddBookForm.value;
};

const addBook = async () => {
  try {
    const response = await apiService.addBook(newBook.value);

    if (response.status === 201) {
      fetchBooks();
      showSuccessDialog("Book added successfully!");

      // reset form values
      newBook.value = { title: "", author: "", isbn: "", copies_available: 0 };
      showAddBookForm.value = false;
    }
  } catch (error) {
    await Dialog.showMessageDialog(
      "Error",
      `<div class="alert alert-danger h-100 m-0">${
        error.response.data.message || error.message
      }<div>`
    );
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
      showSuccessDialog("Book updated successfully!");

      selectedBook.value = null;
    }
  } catch (error) {
    await Dialog.showMessageDialog(
      "Error",
      `<div class="alert alert-danger h-100 m-0">${
        error.response.data.message || error.message
      }<div>`
    );
  }
};

const cancelEdit = () => {
  selectedBook.value = null;
};

const confirmDelete = async (bookId) => {
  const response = await Dialog.showConfirmDialog(
    "Confirm Deletion?",
    "Are you sure you want to delete this book?",
    {
      eventStyles: {
        "#confirmDialogBtnYes": {
          background: "#28a745", // Green color for Yes
          color: "white",
        },
        "#confirmDialogBtnNo": {
          background: "#551622", // Maroon color for No
          color: "white",
        },
      },
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
      showSuccessDialog("Book deleted successfully!");
    }
  } catch (error) {
    await Dialog.showMessageDialog(
      "Error",
      `<div class="alert alert-danger h-100 m-0">${
        error.response.data.message || error.message
      }<div>`
    );
  }
};

onMounted(() => fetchBooks());
</script>

<style scoped>
.card {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.card-title {
  font-weight: bold;
}

.card-text {
  font-size: 14px;
}

.modal-header {
  font-weight: bold;
}

button i {
  margin-right: 5px;
}

/* Center modal */
.modal-dialog-centered {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}
</style>
