// JS for Forms
// Apply datepicker styling for reservation form
function datePicker() {
    $("#id_requested_date").datepicker({
        dateFormat: 'dd/mm/yy'
    });
}

// If there is a form error, swing the form 
function formError() {
    if ($(".alert.alert-danger").length) {
        $(".full-form").addClass("animate__animated animate__swing");
    }
}

// Prevents dates in the past from being submitted on the booking form
function checkDate() {
    $(".booking-enquiry").one('submit', (function (e) {
        e.preventDefault();
        var $this = $(this);
        var selectedDate = $('#id_requested_date').datepicker('getDate');
        if ((selectedDate.getTime() < Date.now())) {
            alert("Selected date is in the past, please choose a date in the future.");
        } else {
            $this.submit();
        }
    }));
}

// Remove disabled attribute so that the form can be submitted without throwing errors
function removeDisableAttrOnSubmit() {
    $("#customer-details-form").one('submit', (function (e) {
        e.preventDefault();
        var $this = $(this);
        $("#customer-details-form>.full-form>#div_id_email>.controls>.emailinput").attr("disabled", false);
        $this.submit();
    }));
}


// Opens the modal on delete_booking
function deleteModal() {
    $("#delete-booking").on('click', function () {
        $('#confirmationModal').modal('show');
    });

    $(".close").on('click', function () {
        $('#confirmationModal').modal('hide');
    });
}

// Adds and removes classes in map section depending on screen width.
function screenSize() {
    if (window.innerWidth < 994) {
        $('#map-section').addClass('hidden');
    } else {
        $('#map-section').removeClass('hidden');
    }
}

// The debounce function is eadded to ensure a 
//given task doesn't fire so often that it 
// bricks browser performance
function debounce(func, wait, immediate) {
    var timeout;
    return function () {
        var context = this,
            args = arguments;
        var later = function () {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        var callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

var screenChangeEfficient = debounce(function () {
    screenSize();
}, 150);

// Trigger efficient screen class function each time screen resizes
window.addEventListener('resize', screenChangeEfficient);

// Call all functions 
$(document).ready(function () {

    datePicker();

    deleteModal();

    formError();

    checkDate();

    removeDisableAttrOnSubmit();

    screenSize();
});


