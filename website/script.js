function showMessage() {
    const message = document.getElementById("message");

    message.textContent =
        "✓ Deployment test successful! Your website is running on Amazon S3.";

    message.style.opacity = "1";
}