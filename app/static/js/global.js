function showToast(message, options = "info") {
    const typeSymbols = {
        success: "✅",
        error: "❌",
        info: "ℹ️",
        warn: "⚠️",
    };

    const typeColors = {
        success: "#4caf50", // Green
        error: "#f44336", // Red
        info: "#2196f3", // Blue
        warn: "#ff9800", // Orange
    };

    let config = {
        text: `${typeSymbols[options] || ""} ${message}`,
        duration: 1500,
        gravity: "top",
        position: "left",
        stopOnFocus: true, // Prevents toast from hiding on hover
        style: {
            background: typeColors[options] || "gray",
            color: "#fff",
            borderRadius: "8px",
            padding: "10px 15px",
            fontFamily: "Arial, sans-serif",
            fontSize: "14px",
            boxShadow: "0px 4px 8px rgba(0, 0, 0, 0.2)",
            maxWidth: "300px",
        },
    };

    if (typeof options === "object") {
        config = {
            ...config,
            ...options,
            text: `${typeSymbols[options.type] || ""} ${message}`,
            style: {
                ...config.style,
                background: typeColors[options.type] || config.style.background,
                ...(options.style || {}),
            },
        };
    }

    Toastify(config).showToast();
}

function debounce(func, delay) {
    let timeoutId;

    return function(...args) {
        const context = this;

        clearTimeout(timeoutId);

        timeoutId = setTimeout(() => {
            func.apply(context, args);
        }, delay);
    };
}

function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith(name + '=')) {
            return cookie.substring(name.length + 1);
        }
    }
    return null;
}

async function get_session_data() {
    try {
        const res = await fetch('/session-data');
        const data = await res.json();
        return data;
    } catch (error) {
        console.log(error)
    }
}

window.utils={
    debounce:debounce,
    showToast:showToast,
    getCookie:getCookie,
    get_session_data:get_session_data
}