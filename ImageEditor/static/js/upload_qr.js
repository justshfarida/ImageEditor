document.getElementById("uploadButton").addEventListener("click", function () {
    const uploadForm = document.getElementById("uploadForm");
    const formData = new FormData(uploadForm); // Grabs the form data, including the file

    // Include CSRF token
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch('/qr/upload/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrfToken // Send CSRF token in the header
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            document.getElementById("submitButton").disabled = false;

            const uploadedImageDiv = document.getElementById("uploadedImage");
            uploadedImageDiv.innerHTML = `
                <h3>Uploaded QR Code:</h3>
                <img src="${data.image_url}" alt="Uploaded QR Code" />
            `;
        } else {
            alert("Upload failed: " + data.message);
        }
    })
    .catch(error => {
        console.error("Error during upload:", error);
        alert("Upload failed. Please try again.");
    });
});
