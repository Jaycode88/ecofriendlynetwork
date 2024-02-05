/* jshint esversion: 11, jquery: true */

/**
 * Script to manage incrementing and decrementing quantity inputs on product detail page.
 * 
 * This script provides functionality to increment and decrement values in quantity
 * input fields. 
 */

// Handle click event on increment buttons.
$('.increment-qty').click(function(e) {
    e.preventDefault(); // Prevent default button action.
    console.log('increment button clicked');
    // Find the closest '.qty_input' related to the clicked button.
    var closestInput = $(this).closest('.input-group').find('.qty_input')[0];
    // Parse its current value as an integer.
    var currentValue = parseInt($(closestInput).val());
    console.log(`currentValue : ${currentValue}`);
    // Increment the value and update the input field.
    $(closestInput).val(currentValue + 1);
    // Retrieve the item ID from the button's data attribute.
    var itemId = $(this).data('item_id');
    // Call a function to potentially enable/disable buttons based on the new quantity.
    handleEnableDisable(itemId);
});

// Handle click event on decrement buttons.
$('.decrement-qty').click(function(e) {
    e.preventDefault(); // Prevent default button action.
    console.log('decrement button clicked');
    // Find the closest '.qty_input' related to the clicked button.
    var closestInput = $(this).closest('.input-group').find('.qty_input')[0];
    // Parse its current value as an integer.
    var currentValue = parseInt($(closestInput).val());
    // Decrement the value and update the input field.
    $(closestInput).val(currentValue - 1);
    // Retrieve the item ID from the button's data attribute.
    var itemId = $(this).data('item_id');
    // Call a function to potentially enable/disable buttons based on the new quantity.
    handleEnableDisable(itemId);
});
