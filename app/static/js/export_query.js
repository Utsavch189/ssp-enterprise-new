function downloadExcel() {
    const start_date = document.getElementById("start-date").value;
    const end_date = document.getElementById("end-date").value;
    const button = document.getElementById("export-query-btn");

    if ((start_date && !end_date) || (end_date && !start_date)) {
        alert("One Date entered and another is missing.");
        return;
    }

    button.innerHTML = 'Exporting...';
    button.setAttribute("disabled", true);

    const requestData = {
        start_date: start_date,
        end_date: end_date
    };

    fetch("/download-query", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(requestData)
    })
    .then(response => {
        const contentDisposition = response.headers.get("Content-Disposition");
        let filename = "default.xlsx"; // Default filename

        if (contentDisposition) {
            const match = contentDisposition.match(/filename="?(.+?)"?$/);
            if (match) {
                filename = match[1];
            }
        }

        return response.blob().then(blob => ({ blob, filename }));
    })
    .then(({ blob, filename }) => {
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    })
    .catch(error => console.error("Error downloading file:", error))
    .finally(() => {
        button.innerHTML = 'Export';
        button.removeAttribute("disabled");
    });
}

