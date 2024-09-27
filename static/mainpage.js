document.addEventListener("DOMContentLoaded", function() {
    const typingText = document.getElementById("typing-text");
    const typingDots = document.getElementById("typing-dots");
    const text = typingText.textContent;
    typingText.textContent = "";

    let index = 0;
    function type() {
        if (index < text.length) {
            typingText.textContent += text.charAt(index);
            index++;
            setTimeout(type, 100);
        } else {
            setTimeout(rewriteDots, 500);
        }
    }

    function rewriteDots() {
        typingDots.textContent = "";
        let dots = 0;
        function addDot() {
            if (dots < 3) {
                typingDots.textContent += "?";
                dots++;
                setTimeout(addDot, 500);
            } else {
                setTimeout(removeDots, 500);
            }
        }
        addDot();
    }

    function removeDots() {
        let dots = typingDots.textContent.length;
        function removeDot() {
            if (dots > 0) {
                typingDots.textContent = typingDots.textContent.slice(0, -1);
                dots--;
                setTimeout(removeDot, 500);
            } else {
                setTimeout(rewriteDots, 500);
            }
        }
        removeDot();
    }

    type();
});