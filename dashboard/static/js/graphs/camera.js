document.addEventListener('DOMContentLoaded', function() {
    let imgElement = document.getElementById('camimg');
    const endpoint = window.location.origin + '/zone1cameradata'; // Your Flask endpoint URL

    async function fetchImageUrl() {
        try {
            const response = await fetch(endpoint, { mode: 'cors' });
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            const data = await response.json();
            if (data.length > 0 && data[0].camera) {
                // Add a unique query parameter to the URL to prevent caching
                const newImageUrl = `${data[0].camera}?t=${new Date().getTime()}`;
                updateImage(newImageUrl);
            } else {
                console.error('Invalid data format:', data);
            }
        } catch (error) {
            console.error('Error fetching the image URL:', error);
        }
    }

    function updateImage(newImageUrl) {
        // Create a new image element
        const newImgElement = new Image();
        newImgElement.src = newImageUrl;
        newImgElement.className = 'camera-img enter';

        // Once the new image is loaded, start the transition
        newImgElement.onload = () => {
            imgElement.classList.add('exit');

            // Append the new image
            imgElement.parentElement.appendChild(newImgElement);

            // Trigger reflow to apply the transition
            newImgElement.offsetWidth; // forces a reflow

            // Start the transition
            newImgElement.classList.add('active');

            // Remove the old image after the transition
            setTimeout(() => {
                imgElement.parentElement.removeChild(imgElement);
                newImgElement.classList.remove('enter', 'active');
                imgElement = newImgElement; // Reassign imgElement to the new image element
            }, 600); // Duration must match the CSS transition duration
        };
    }

    // Fetch and update the image every 10 seconds
    setInterval(fetchImageUrl, 10000);

    // Initial fetch
    fetchImageUrl();
});
