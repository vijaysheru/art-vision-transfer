document.getElementById('upload-form').onsubmit = function(event) {
    event.preventDefault();

    const formData = new FormData(this);

    document.getElementById('loading').style.display = 'block';

    fetch('/style-transfer', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('loading').style.display = 'none';
        if (data.success) {
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = `<img src="${data.image_url}" alt="Stylized Image">`;
        } else {
            alert('An error occurred while processing your request.');
        }
    })
    .catch(error => console.error('Error:', error));
};