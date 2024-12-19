document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("uploadForm");
    const processButton = document.getElementById("processButton");
    const previewContainer = document.getElementById("previewContainer");
    const previewImage = document.getElementById("previewImage");

    processButton.addEventListener("click", function (event) {
        event.preventDefault();

        const formData = new FormData(form);

        fetch(form.action, {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": form.querySelector("[name=csrfmiddlewaretoken]").value,
            },
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then((data) => {
                if (data.success) {
                    previewImage.src = data.processed_image_url;
                    previewContainer.style.display = "block";
                } else {
                    alert("Processing failed: " + data.error);
                }
            })
            .catch((error) => {
                console.error("Error:", error);
                alert("An error occurred while processing the image.");
            });
    });
});
