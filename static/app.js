/**
 * Task Management API - Vanilla JavaScript Frontend
 * Communicates directly with FastAPI REST Backend.
 */

// Base API URL configuration
const API_BASE_URL =
  window.location.origin.startsWith('http') &&
  !window.location.origin.startsWith('file:')
    ? window.location.origin
    : 'http://127.0.0.1:8000';

let currentFilter = 'all';

// DOM Elements
const alertContainer = document.getElementById('alertContainer');
const alertMessage = document.getElementById('alertMessage');
const totalTasksCount = document.getElementById('totalTasksCount');
const completedTasksCount = document.getElementById('completedTasksCount');
const pendingTasksCount = document.getElementById('pendingTasksCount');
const createTaskForm = document.getElementById('createTaskForm');
const taskTitleInput = document.getElementById('taskTitle');
const taskDescriptionInput = document.getElementById('taskDescription');
const createSubmitBtn = document.getElementById('createSubmitBtn');
const taskListContainer = document.getElementById('taskList');
const loadingIndicator = document.getElementById('loadingIndicator');
const emptyState = document.getElementById('emptyState');
const editModal = document.getElementById('editModal');
const editTaskForm = document.getElementById('editTaskForm');
const editTaskIdInput = document.getElementById('editTaskId');
const editTaskTitleInput = document.getElementById('editTaskTitle');
const editTaskDescriptionInput = document.getElementById('editTaskDescription');
const editTaskCompletedCheckbox = document.getElementById('editTaskCompleted');

// Initialize Dashboard on DOM Load
document.addEventListener('DOMContentLoaded', () => {
  fetchStats();
  fetchTasks('all');

  createTaskForm.addEventListener('submit', handleCreateTask);
  editTaskForm.addEventListener('submit', handleSaveEditTask);
});

/**
 * Display Alert Notification
 */
function showAlert(message, type = 'error') {
  alertMessage.textContent = message;
  alertContainer.className = `alert-container ${type}`;
  alertContainer.classList.remove('hidden');

  // Auto-hide success alerts after 4 seconds
  if (type === 'success') {
    setTimeout(() => {
      closeAlert();
    }, 4000);
  }
}

function closeAlert() {
  alertContainer.classList.add('hidden');
}

/**
 * Update Dashboard Stats (Total, Completed, Pending)
 */
async function fetchStats() {
  try {
    const res = await fetch(`${API_BASE_URL}/tasks/`);
    if (!res.ok) return;

    const allTasks = await res.json();
    const total = allTasks.length;
    const completed = allTasks.filter((t) => t.is_completed).length;
    const pending = total - completed;

    totalTasksCount.textContent = total;
    completedTasksCount.textContent = completed;
    pendingTasksCount.textContent = pending;
  } catch (err) {
    console.error('Failed to update stats:', err);
  }
}

/**
 * Set Current Filter & Fetch Tasks
 * Real API endpoint call: GET /tasks/?completed=true or GET /tasks/?completed=false
 */
function setFilter(filter) {
  currentFilter = filter;

  // Update active filter button styling
  document.querySelectorAll('.filter-btn').forEach((btn) => {
    if (btn.getAttribute('data-filter') === filter) {
      btn.classList.add('active');
    } else {
      btn.classList.remove('active');
    }
  });

  fetchTasks(filter);
}

/**
 * Fetch Tasks from FastAPI Backend
 */
async function fetchTasks(filter = 'all') {
  loadingIndicator.classList.remove('hidden');
  emptyState.classList.add('hidden');
  taskListContainer.innerHTML = '';

  let fetchUrl = `${API_BASE_URL}/tasks/`;
  if (filter === 'completed') {
    fetchUrl = `${API_BASE_URL}/tasks/?completed=true`;
  } else if (filter === 'pending') {
    fetchUrl = `${API_BASE_URL}/tasks/?completed=false`;
  }

  try {
    const res = await fetch(fetchUrl);
    loadingIndicator.classList.add('hidden');

    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.detail || 'Failed to fetch tasks from server.');
    }

    const tasks = await res.json();

    if (tasks.length === 0) {
      emptyState.classList.remove('hidden');
    } else {
      renderTaskList(tasks);
    }
  } catch (err) {
    loadingIndicator.classList.add('hidden');
    showAlert(`Error: ${err.message}`, 'error');
  }
}

/**
 * Render Task Cards into List
 */
function renderTaskList(tasks) {
  taskListContainer.innerHTML = '';

  tasks.forEach((task) => {
    const card = document.createElement('div');
    const isCompleted = task.is_completed;
    card.className = `task-card ${isCompleted ? 'completed-card' : 'pending-card'}`;

    const createdFormatted = task.created_at
      ? new Date(task.created_at).toLocaleString()
      : 'N/A';

    card.innerHTML = `
      <div class="task-main">
        <div class="task-title-row">
          <span class="task-card-title ${isCompleted ? 'completed-title' : ''}">${escapeHtml(task.title)}</span>
          <span class="status-tag ${isCompleted ? 'tag-completed' : 'tag-pending'}">
            ${isCompleted ? 'Completed' : 'Pending'}
          </span>
        </div>
        ${
          task.description
            ? `<p class="task-desc">${escapeHtml(task.description)}</p>`
            : ''
        }
        <div class="task-meta">
          <span>Created: ${createdFormatted}</span>
        </div>
      </div>
      <div class="task-actions">
        ${
          !isCompleted
            ? `<button class="btn btn-sm btn-success" onclick="markCompleted(${task.id})">✓ Complete</button>`
            : ''
        }
        <button class="btn btn-sm btn-secondary" onclick="openEditModal(${task.id}, '${escapeQuote(task.title)}', '${escapeQuote(task.description || '')}', ${task.is_completed})">Edit</button>
        <button class="btn btn-sm btn-danger" onclick="deleteTask(${task.id})">Delete</button>
      </div>
    `;

    taskListContainer.appendChild(card);
  });
}

/**
 * Handle Create Task Form Submit
 * Backend Endpoint: POST /tasks/
 */
async function handleCreateTask(e) {
  e.preventDefault();
  closeAlert();

  const title = taskTitleInput.value.trim();
  const description = taskDescriptionInput.value.trim() || null;

  if (!title) {
    showAlert('Task title is required.', 'error');
    return;
  }

  createSubmitBtn.disabled = true;

  try {
    const res = await fetch(`${API_BASE_URL}/tasks/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, description }),
    });

    createSubmitBtn.disabled = false;

    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      let msg = 'Failed to create task.';
      if (errData.detail && Array.isArray(errData.detail)) {
        msg = errData.detail.map((d) => d.msg).join(', ');
      } else if (errData.detail) {
        msg = errData.detail;
      }
      throw new Error(msg);
    }

    // Clear form inputs
    taskTitleInput.value = '';
    taskDescriptionInput.value = '';

    showAlert('Task created successfully!', 'success');
    fetchStats();
    fetchTasks(currentFilter);
  } catch (err) {
    createSubmitBtn.disabled = false;
    showAlert(`Create failed: ${err.message}`, 'error');
  }
}

/**
 * Mark Task as Completed
 * Backend Endpoint: PATCH /tasks/{task_id}/complete
 */
async function markCompleted(taskId) {
  closeAlert();
  try {
    const res = await fetch(`${API_BASE_URL}/tasks/${taskId}/complete`, {
      method: 'PATCH',
    });

    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.detail || 'Failed to mark task as completed.');
    }

    showAlert('Task marked as completed!', 'success');
    fetchStats();
    fetchTasks(currentFilter);
  } catch (err) {
    showAlert(`Action failed: ${err.message}`, 'error');
  }
}

/**
 * Delete Task
 * Backend Endpoint: DELETE /tasks/{task_id}
 */
async function deleteTask(taskId) {
  if (!confirm('Are you sure you want to permanently delete this task?')) {
    return;
  }

  closeAlert();
  try {
    const res = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
      method: 'DELETE',
    });

    if (!res.ok && res.status !== 204) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.detail || 'Failed to delete task.');
    }

    showAlert('Task deleted successfully.', 'success');
    fetchStats();
    fetchTasks(currentFilter);
  } catch (err) {
    showAlert(`Delete failed: ${err.message}`, 'error');
  }
}

/**
 * Open Edit Modal
 */
function openEditModal(id, title, description, isCompleted) {
  closeAlert();
  editTaskIdInput.value = id;
  editTaskTitleInput.value = title;
  editTaskDescriptionInput.value = description;
  editTaskCompletedCheckbox.checked = isCompleted;
  editModal.classList.remove('hidden');
}

function closeEditModal() {
  editModal.classList.add('hidden');
}

/**
 * Submit Edit Form
 * Backend Endpoint: PUT /tasks/{task_id}
 */
async function handleSaveEditTask(e) {
  e.preventDefault();
  const taskId = editTaskIdInput.value;
  const title = editTaskTitleInput.value.trim();
  const description = editTaskDescriptionInput.value.trim() || null;
  const is_completed = editTaskCompletedCheckbox.checked;

  if (!title) {
    showAlert('Task title is required.', 'error');
    return;
  }

  try {
    const res = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, description, is_completed }),
    });

    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.detail || 'Failed to update task.');
    }

    closeEditModal();
    showAlert('Task updated successfully!', 'success');
    fetchStats();
    fetchTasks(currentFilter);
  } catch (err) {
    showAlert(`Update failed: ${err.message}`, 'error');
  }
}

// Helpers to sanitize HTML strings
function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function escapeQuote(str) {
  return str.replace(/'/g, "\\'").replace(/"/g, '&quot;');
}
