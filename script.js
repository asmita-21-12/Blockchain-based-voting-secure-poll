$(document).ready(function() {
    $('#votingForm').submit(function(event) {
      event.preventDefault(); // Prevent form submission
    
      // Get form data
      var voterId = $('#voterId').val();
      var party = $('#party').val();
  
      // Perform client-side validation
      if (!validateVoterId(voterId)) {
        showMessage("Invalid Voter ID. Voter ID must be exactly 10 characters long and contain only alphanumeric characters.");
        return;
      }
  
      // Send data to the server for further validation
      $.ajax({
        type: "POST",
        url: "/cast_vote",
        data: JSON.stringify({voterId: voterId, party: party}),
        contentType: "application/json",
        success: function(response) {
          showMessage(response.message);
        },
        error: function(xhr, status, error) {
          showMessage("An error occurred: " + error);
        }
      });
    });
  
    // Function to validate voter ID format (example)
    function validateVoterId(voterId) {
      // Check if voter ID is exactly 10 characters long and contains only alphanumeric characters
      return /^[a-zA-Z0-9]{10}$/.test(voterId);
    }
  
    // Function to display message to the user
    function showMessage(message) {
      $('#message').text(message);
    }
  });


  