/* jshint esversion: 11, jquery: true */

/**
 * Script for managing item quantities and removal in the shopping bag.
 * 
 * Provides functionality for:
 * - Incrementing and decrementing item quantities through "+" and "-" buttons.
 * - Removing items from the bag.
 * - Dynamically updating the page to reflect these changes without requiring a page reload for quantity adjustments.
 * - Reloading the page upon item removal to update the bag's contents.
 * 
 * - A separate 'handleEnableDisable' function exists, responsible for disabling/enabling buttons based on item quantity.
 */

$(document).ready(function() {
    // Increment quantity on click.
    $(document).on('click', '.increment-qty', function(event) {
        event.preventDefault(); // Prevent the default button action.
        updateQuantity($(this), 1); // Call updateQuantity with a +1 change.
    });

    // Decrement quantity on click.
    $(document).on('click', '.decrement-qty', function(event) {
        event.preventDefault(); // Prevent the default button action.
        updateQuantity($(this), -1); // Call updateQuantity with a -1 change.
    });

    // Remove item and reload on click.
    $(document).on('click', '.remove-item', function() {
        var csrfToken = "{{ csrf_token }}"; // Retrieve CSRF token from the template.
        var itemId = $(this).attr('id').split('_')[1]; // Extract item ID from the button's id attribute.
        var url = `/bag/remove/${itemId}/`; // Construct the URL for the removal endpoint.
        var data = {'csrfmiddlewaretoken': csrfToken}; // Prepare data for POST request.
        
        // Perform the POST request to remove the item.
        $.post(url, data)
            .done(function() {
                location.reload(); // Reload the page to reflect the updated bag contents.
            });
    });

    /**
     * Updates the quantity of an item and submits the form to reflect changes on the server.
     */
    function updateQuantity(button, change) {
        var itemId = button.data('item_id'); // Retrieve the item ID from the button's data attribute.
        var inputField = $('#id_qty_' + itemId); // Select the corresponding quantity input field.
        var currentQuantity = parseInt(inputField.val()); // Parse the current quantity as an integer.

        // Calculate the new quantity.
        var newQuantity = currentQuantity + change;

        // Check if the new quantity is within the valid range.
        if (newQuantity >= inputField.attr('min') && newQuantity <= inputField.attr('max')) {
            inputField.val(newQuantity); // Update the input field with the new quantity.
            button.closest('form').submit(); // Submit the form to update the quantity on the server.

            // Call handleEnableDisable to adjust button states based on the new quantity.
            handleEnableDisable(itemId);
        }
    }
});
