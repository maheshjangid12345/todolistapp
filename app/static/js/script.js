// Professional TODO App JavaScript

class TodoApp {
    constructor() {
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.initializeComponents();
        this.setupAutoSave();
    }

    setupEventListeners() {
        // Form submissions
        document.addEventListener('submit', this.handleFormSubmit.bind(this));
        
        // Modal events
        document.addEventListener('show.bs.modal', this.handleModalShow.bind(this));
        document.addEventListener('hidden.bs.modal', this.handleModalHidden.bind(this));
        
        // Keyboard shortcuts
        document.addEventListener('keydown', this.handleKeyboardShortcuts.bind(this));
        
        // Auto-save on input changes
        document.addEventListener('input', this.debounce(this.handleAutoSave.bind(this), 1000));
    }

    initializeComponents() {
        // Initialize tooltips
        this.initTooltips();
        
        // Initialize form validation
        this.initFormValidation();
        
        // Initialize task filters
        this.initTaskFilters();
        
        // Initialize drag and drop (if enabled)
        this.initDragAndDrop();
    }

    setupAutoSave() {
        // Auto-save form data to localStorage
        this.autoSaveData = JSON.parse(localStorage.getItem('todoAutoSave') || '{}');
        
        // Restore form data on page load
        this.restoreFormData();
    }

    handleFormSubmit(event) {
        const form = event.target;
        const submitBtn = form.querySelector('button[type="submit"]');
        
        if (submitBtn) {
            // Show loading state
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
            submitBtn.disabled = true;
            
            // Re-enable button after a delay (in case of validation errors)
            setTimeout(() => {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }, 3000);
        }
    }

    handleModalShow(event) {
        const modal = event.target;
        const form = modal.querySelector('form');
        
        if (form) {
            // Focus first input
            const firstInput = form.querySelector('input, select, textarea');
            if (firstInput) {
                setTimeout(() => firstInput.focus(), 100);
            }
        }
    }

    handleModalHidden(event) {
        const modal = event.target;
        const form = modal.querySelector('form');
        
        if (form) {
            // Reset form
            form.reset();
            
            // Clear validation errors
            this.clearValidationErrors(form);
        }
    }

    handleKeyboardShortcuts(event) {
        // Ctrl/Cmd + Enter to submit forms
        if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
            const activeForm = document.querySelector('form:focus-within');
            if (activeForm) {
                event.preventDefault();
                activeForm.requestSubmit();
            }
        }
        
        // Escape to close modals
        if (event.key === 'Escape') {
            const openModal = document.querySelector('.modal.show');
            if (openModal) {
                const modalInstance = bootstrap.Modal.getInstance(openModal);
                if (modalInstance) {
                    modalInstance.hide();
                }
            }
        }
        
        // Ctrl/Cmd + N to add new task
        if ((event.ctrlKey || event.metaKey) && event.key === 'n') {
            event.preventDefault();
            const addTaskBtn = document.querySelector('[data-bs-target="#addTaskModal"]');
            if (addTaskBtn) {
                addTaskBtn.click();
            }
        }
    }

    handleAutoSave(event) {
        const form = event.target.closest('form');
        if (form) {
            const formData = new FormData(form);
            const data = {};
            
            for (let [key, value] of formData.entries()) {
                data[key] = value;
            }
            
            // Save to localStorage
            this.autoSaveData[form.id || 'default'] = data;
            localStorage.setItem('todoAutoSave', JSON.stringify(this.autoSaveData));
        }
    }

    restoreFormData() {
        Object.entries(this.autoSaveData).forEach(([formId, data]) => {
            const form = document.getElementById(formId) || document.querySelector('form');
            if (form) {
                Object.entries(data).forEach(([key, value]) => {
                    const input = form.querySelector(`[name="${key}"]`);
                    if (input) {
                        input.value = value;
                    }
                });
            }
        });
    }

    initTooltips() {
        // Initialize Bootstrap tooltips
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    initFormValidation() {
        // Custom validation for forms
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', this.validateForm.bind(this));
        });
    }

    validateForm(event) {
        const form = event.target;
        let isValid = true;
        
        // Clear previous validation errors
        this.clearValidationErrors(form);
        
        // Validate required fields
        const requiredFields = form.querySelectorAll('[required]');
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                this.showValidationError(field, 'This field is required');
                isValid = false;
            }
        });
        
        // Validate email fields
        const emailFields = form.querySelectorAll('input[type="email"]');
        emailFields.forEach(field => {
            if (field.value && !this.isValidEmail(field.value)) {
                this.showValidationError(field, 'Please enter a valid email address');
                isValid = false;
            }
        });
        
        // Validate password confirmation
        const passwordField = form.querySelector('input[name="password"]');
        const confirmPasswordField = form.querySelector('input[name="confirm_password"]');
        if (passwordField && confirmPasswordField && passwordField.value !== confirmPasswordField.value) {
            this.showValidationError(confirmPasswordField, 'Passwords do not match');
            isValid = false;
        }
        
        if (!isValid) {
            event.preventDefault();
            event.stopPropagation();
        }
        
        return isValid;
    }

    showValidationError(field, message) {
        // Remove existing error
        const existingError = field.parentNode.querySelector('.invalid-feedback');
        if (existingError) {
            existingError.remove();
        }
        
        // Add error class
        field.classList.add('is-invalid');
        
        // Create error message
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        errorDiv.textContent = message;
        
        // Insert error message
        field.parentNode.appendChild(errorDiv);
    }

    clearValidationErrors(form) {
        const invalidFields = form.querySelectorAll('.is-invalid');
        invalidFields.forEach(field => {
            field.classList.remove('is-invalid');
            const errorDiv = field.parentNode.querySelector('.invalid-feedback');
            if (errorDiv) {
                errorDiv.remove();
            }
        });
    }

    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    initTaskFilters() {
        // Task filtering functionality
        const filterButtons = document.querySelectorAll('[onclick^="filterTasks"]');
        filterButtons.forEach(button => {
            button.addEventListener('click', (event) => {
                // Remove active class from all buttons
                filterButtons.forEach(btn => btn.classList.remove('active'));
                
                // Add active class to clicked button
                button.classList.add('active');
            });
        });
    }

    initDragAndDrop() {
        // Initialize drag and drop for tasks (if enabled)
        const taskRows = document.querySelectorAll('.task-row');
        taskRows.forEach(row => {
            row.draggable = true;
            row.addEventListener('dragstart', this.handleDragStart.bind(this));
            row.addEventListener('dragend', this.handleDragEnd.bind(this));
        });
        
        // Add drop zones for different status columns
        this.setupDropZones();
    }

    handleDragStart(event) {
        event.dataTransfer.setData('text/plain', event.target.dataset.taskId);
        event.target.classList.add('dragging');
    }

    handleDragEnd(event) {
        event.target.classList.remove('dragging');
    }

    setupDropZones() {
        // Implementation for drag and drop zones
        // This would allow users to drag tasks between different status columns
    }

    // Utility functions
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        // Add to page
        document.body.appendChild(notification);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }

    // API helper functions
    async apiCall(url, options = {}) {
        try {
            const response = await fetch(url, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API call failed:', error);
            this.showNotification('An error occurred. Please try again.', 'danger');
            throw error;
        }
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.todoApp = new TodoApp();
});

// Global utility functions
window.TodoUtils = {
    formatDate(dateString) {
        if (!dateString) return 'No date';
        
        const date = new Date(dateString);
        const now = new Date();
        const diffTime = date - now;
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        
        if (diffDays < 0) {
            return `<span class="text-danger">${Math.abs(diffDays)} days overdue</span>`;
        } else if (diffDays === 0) {
            return '<span class="text-warning">Due today</span>';
        } else if (diffDays === 1) {
            return '<span class="text-info">Due tomorrow</span>';
        } else if (diffDays <= 7) {
            return `<span class="text-warning">Due in ${diffDays} days</span>`;
        } else {
            return date.toLocaleDateString();
        }
    },
    
    getPriorityColor(priority) {
        const colors = {
            'urgent': 'danger',
            'high': 'warning',
            'medium': 'info',
            'low': 'secondary'
        };
        return colors[priority] || 'secondary';
    },
    
    getStatusColor(status) {
        const colors = {
            'pending': 'warning',
            'in_progress': 'info',
            'completed': 'success',
            'cancelled': 'secondary'
        };
        return colors[status] || 'secondary';
    }
};