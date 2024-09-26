document.addEventListener("DOMContentLoaded", function() {
    const typingText = document.getElementById("typing-text");
    const text = typingText.textContent;
    typingText.textContent = "";

    let index = 0;
    function type() {
        if (index < text.length) {
            typingText.textContent += text.charAt(index);
            index++;
            setTimeout(type, 100);
        }
    }

    type();
});