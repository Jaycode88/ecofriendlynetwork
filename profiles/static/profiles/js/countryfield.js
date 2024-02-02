/* jshint esversion: 11, jquery: true */

/**
 * Script for handling the default country selection in forms.
 * It sets the default color of the country selector based on whether a country is selected.
 * When the country selection changes, it updates the color to reflect the selection status.
 */

// Get the current value of the country selection dropdown
let countrySelected = $('#id_default_country').val();

// If no country is selected initially, set the color to a greyish tone
if(!countrySelected) {
    $('#id_default_country').css('color', '#6c757d');
}

// Add a change event listener to the country selection dropdown
$('#id_default_country').change(function() {
    // Update the countrySelected variable with the new value
    countrySelected = $(this).val();

    // Check if a country is selected
    if(!countrySelected) {
        // If no country is selected, keep the color grey
        $(this).css('color', '#6c757d');
    } else {
        // If a country is selected, set the color to black for better visibility
        $(this).css('color', '#000');
    }
});
