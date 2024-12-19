document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.getElementById("fileInput");
    const dragArea = document.getElementById("dragArea");
    const previewContainer = document.getElementById("previewContainer");
    const previewImage = document.getElementById("previewImage");
    const discardButton = document.getElementById("discardButton");

    // Open file picker when clicking "Choose File"
    const chooseButton = document.getElementById("chooseButton");
    chooseButton.addEventListener("click", () => {
        fileInput.click();
    });

    // Handle file selection
    fileInput.addEventListener("change", (event) => {
        handleFile(event.target.files[0]);
    });

    // Drag and drop functionality
    dragArea.addEventListener("dragover", (event) => {
        event.preventDefault();
        dragArea.classList.add("drag-over");
    });

    dragArea.addEventListener("dragleave", () => {
        dragArea.classList.remove("drag-over");
    });

    dragArea.addEventListener("drop", (event) => {
        event.preventDefault();
        dragArea.classList.remove("drag-over");
        const file = event.dataTransfer.files[0];
        fileInput.files = event.dataTransfer.files; // Set file input
        handleFile(file);
    });

    // Display image preview
    const handleFile = (file) => {
        if (file) {
            const reader = new FileReader();
            reader.onload = () => {
                previewImage.src = reader.result;
                previewContainer.style.display = "block";
            };
            reader.readAsDataURL(file);
        }
    };

    // Remove preview
    discardButton.addEventListener("click", () => {
        previewImage.src = "";
        previewContainer.style.display = "none";
        fileInput.value = ""; // Clear input value
    });
});
