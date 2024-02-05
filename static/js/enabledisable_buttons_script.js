/* jshint esversion: 11, jquery: true */

/**
 * Script to enable or disable increment and decrement buttons based on the quantity input value.
 * 
 * This script is used on both the product detail and bag pages
 */

// Function to disable or enable increment and decrement buttons based on the quantity input value.
function handleEnableDisable(itemId) {
    // Parse the current value of the quantity input as an integer.
    var currentValue = parseInt($(`#id_qty_${itemId}`).val());
    // Determine whether the decrement button should be disabled (true if quantity is less than 2).
    var minusDisabled = currentValue < 2;
    // Determine whether the increment button should be disabled (true if quantity is more than 98).
    var plusDisabled = currentValue > 98;
    // Update the disabled property of the decrement and increment buttons based on the conditions above.
    $(`#decrement-qty_${itemId}`).prop('disabled', minusDisabled);
    $(`#increment-qty_${itemId}`).prop('disabled', plusDisabled);
}

// Upon page load, iterate through all quantity inputs to set the correct enabled/disabled state.
var allQtyInputs = $('.qty_input');
for(var i = 0; i < allQtyInputs.length; i++){
    // Extract the item ID from the data attribute of each quantity input.
    var itemId = $(allQtyInputs[i]).data('item_id');
    // Call handleEnableDisable for each item to ensure buttons are correctly enabled or disabled.
    handleEnableDisable(itemId);
}

// Add an event listener to quantity input fields to check and update the enabled/disabled state upon change.
$('.qty_input').change(function() {
    // Extract the item ID from the changed input's data attribute.
    var itemId = $(this).data('item_id');
    // Update the enabled/disabled state for the corresponding item's buttons.
    handleEnableDisable(itemId);
});
