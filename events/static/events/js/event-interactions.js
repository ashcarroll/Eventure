
// Form Validation

document.addEventListener('DOMContentLoaded', function() {
    const eventForm = document.getElementById('event-form');
    if (eventForm) {

        eventForm.addEventListener('input', function(e) {
            const target = e.target;

            // Title Validation
            if (target.id === 'id_title') {
                const titleLength = target.value.length;
                const titleFeedback = document.getElementById('title-feedback') || createFeedbackElement(target, 'title-feedback');

                if (titleLength < 3) {
                    showError(target, titleFeedback, 'Title must be at least 3 characters long');    
                } else if (titleLength > 200) {
                    showError(target, titleFeedback, 'Title must be at less than 200 characters');
                } else {
                    showSuccess(target, titleFeedback);
                }
            }
            
            // Description Validation
            if (target.id === 'id_description') {
                const descLength = target.value.length;
                const descFeedback = document.getElementById('desc-feedback') || createFeedbackElement(target, 'desc-feedback');
                
                if (descLength < 10) {
                    showError(target, descFeedback, 'Description must be at least 10 characters long');
                } else {
                    showSuccess(target, descFeedback);
                }
            }

            // Capacity Validation
            if (target.id === 'id_max_capacity') {
                const capacity = parseInt(target.value);
                const capacityFeedback = document.getElementById('capacity-feedback') || createFeedbackElement(target, 'capacity-feedback');
                
                if (isNaN(capacity) || capacity < 1) {
                    showError(target, capacityFeedback, 'Capacity must be at least 1');
                } else if (capacity > 500) {
                    showError(target, capacityFeedback, 'Capacity cannot exceed 500');
                } else {
                    showSuccess(target, capacityFeedback);
                }
            }

            // Date/Time Validation
            if (target.id === 'id_end_date' || target.id === 'id_end_time_input') {
                validateDateTime();
            }
        });

        //  Form Submit Validation
        eventForm.addEventListener('submit', function(e) {
            if (!validateDateTime()) {
                e.preventDefault();
            }
        });
    }
});


function createFeedbackElement(inputElement, id) {
    const feedback = document.createElement('div');
    feedback.id = id;
    feedback.className = 'invalid-feedback';
    inputElement.parentNode.appendChild(feedback);
    return feedback;
}

function showError(inputElement, feedbackElement, message) {
    inputElement.classList.add('is-invalid');
    inputElement.classList.remove('is-valid');
    feedbackElement.textContent = message;
    feedbackElement.style.display = 'block';
}

function showSuccess(inputElement, feedbackElement) {
    inputElement.classList.remove('is-invalid');
    inputElement.classList.add('is-valid');
    feedbackElement.style.display = 'none';
}

function validateDateTime() {
    const startDate = document.getElementById('id_start_date').value;
    const startTime = document.getElementById('id_start_time_input').value;
    const endDate = document.getElementById('id_end_date').value;
    const endTime = document.getElementById('id_end_time_input').value;

    if (startDate && startTime && endDate && endTime) {
        const startDateTime = new Date(startDate + 'T' + startTime);
        const endDateTime = new Date(endDate + 'T' + endTime);

        const endDateFeedback = document.getElementById('end-date-feedback') || 
            createFeedbackElement(document.getElementById('id_end_date'), 'end-date-feedback');

        if (endDateTime <= startDateTime) {
            showError(document.getElementById('id_end_date'), endDateFeedback, 
                'End date/time must be after start date/time');
            return false;
        } else {
            showSuccess(document.getElementById('id_end_date'), endDateFeedback);
            return true;
        }
    }
    return true;
}