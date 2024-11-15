const dragArea = document.getElementById('dragArea');
const fileInput = document.getElementById('fileInput');
const chooseButton = document.getElementById('chooseButton');
const previewContainer = document.getElementById('previewContainer');
const previewImage = document.getElementById('previewImage');
const discardButton = document.getElementById('discardButton');
const placeholderText = document.getElementById('placeholderText');
const uploadForm = document.getElementById('uploadForm');
const errorMessage = document.getElementById('errorMessage');

function showPreview(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        previewImage.style.display = 'block';
        discardButton.style.display = 'block';
        placeholderText.style.display = 'none';
        errorMessage.style.display = 'none';
    };
    reader.readAsDataURL(file);
}

chooseButton.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        showPreview(file);
    }
});

dragArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    dragArea.classList.add('dragover');
});

dragArea.addEventListener('dragleave', () => {
    dragArea.classList.remove('dragover');
});

dragArea.addEventListener('drop', (e) => {
    e.preventDefault();
    dragArea.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        fileInput.files = files;
        showPreview(files[0]);
    }
});

discardButton.addEventListener('click', () => {
    fileInput.value = '';
    previewImage.style.display = 'none';
    discardButton.style.display = 'none';
    placeholderText.style.display = 'block';
});