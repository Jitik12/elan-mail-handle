# What does it do ?
## After form submission
  Make sure that you trigger this app script from the google sheet and not the form submission
```
function elan_form_entry(e) {
  var formData = e.values; // Get form response data

  // Define FastAPI endpoint
  var fastApiEndpoint = "https://7b79-103-232-241-243.ngrok-free.app";

  // Prepare payload
  var payload = {
    time: formData[0],
    name: formData[1],
    email: formData[2],
    phone: formData[3],
    accommodation: formData[4]
  };

  // Send POST request to FastAPI server
  var options = {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify(payload)
  };

  UrlFetchApp.fetch(fastApiEndpoint, options);
}
```
1. Submit the Google Form
2. App Script gets triggerred
3. The object is sent from google server to my server

## Functionality
1. The names are added into the people database
2. The tickets are mailed to the people via email that they entered