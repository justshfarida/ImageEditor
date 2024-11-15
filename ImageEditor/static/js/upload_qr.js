const fileInput = document.getElementById("id_image");
const uploadButton = document.getElementById("uploadButton");
const submitButton = document.getElementById("submitButton");
const previewImage = document.getElementById("previewImage");

// Trigger file picker when clicking the "Select File" button
uploadButton.addEventListener("click", () => {
    fileInput.click();
});

// Handle file selection
fileInput.addEventListener("change", (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
        if (validateFile(selectedFile)) {
            const reader = new FileReader();
            reader.onload = function (event) {
                // Display the selected image
                previewImage.src = event.target.result;
                previewImage.style.display = "block"; // Make the preview visible
            };
            reader.readAsDataURL(selectedFile);

            // Enable the submit button
            submitButton.disabled = false;
        } else {
            alert("Invalid file type. Please upload an image file.");
            resetFileInput();
        }
    }
});

// Handle form submission
document.getElementById("submitForm").addEventListener("submit", (e) => {
    e.preventDefault(); // Prevent the default form submission

    const formData = new FormData();
    const file = fileInput.files[0];

    if (file) {
        formData.append("image", file); // Append the file to the form data

        // Send the form data to the server
        fetch("/qr/read/", {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
            },
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            if (data.error) {
                console.error("Error in response:", data.error);
            } else {
                console.log("Success:", data);
                document.getElementById("extractedData").innerHTML = `
                    <h3>QR Code Data:</h3>
                    <p>${data.data}</p>
                `;
            }
        })
        .catch((error) => {
            console.error("Fetch error:", error);
        });
        
    } else {
        alert("No file selected!");
    }
});

// Validate file type
function validateFile(file) {
    const validExtensions = /\.(jpe?g|png|gif|bmp|webp|jfif)$/i;
    return validExtensions.test(file.name);
}

// Reset file input and preview when an invalid file is selected
function resetFileInput() {
    fileInput.value = ""; // Clear the file input
    previewImage.src = ""; // Clear the preview image
    previewImage.style.display = "none"; // Hide the preview
    submitButton.disabled = true; // Disable the submit button
}
