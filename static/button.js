function handleFileSelect(event) {
    // Handle file selection logic here
    console.log(event.target.files);
}
function resetFileInput(){
    document.getElementById('file-field').value = '';
}