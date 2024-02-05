/* jshint esversion: 11, jquery: true */
    /**
     * Script for updating the displayed filename when a new image is selected.
     * It listens for changes on the file input element and updates the text
     * of a specified element to reflect the name of the selected file.
     */

    // Event listener for changes on the file input with ID 'new-image'
    $('#new-image').change(function() {
        // Retrieve the first file from the file input element
        var file = $('#new-image')[0].files[0];

        // Update the text of the element with ID 'filename'
        // to display the name of the selected file
        $('#filename').text(`Image will be set to: ${file.name}`);
    });