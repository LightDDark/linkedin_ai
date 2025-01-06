document.addEventListener('DOMContentLoaded', function() {

    // Prevent form resubmission
    if (window.history.replaceState) {
        window.history.replaceState(null, null, window.location.href);
    }

    document.getElementById('keywords-input').addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            const keyword = this.value.trim();
            let keywordsContainer = document.getElementById('keywords-container');
            const currentKeywordsCount = keywordsContainer.children.length / 2;  // Divide by 2 because we add both tag and hidden input
            let errorMessage = document.getElementById('error-message');

            if (keyword && currentKeywordsCount < 10) {
                let tagContainer = document.createElement('div');
                tagContainer.className = 'keyword-tag';
                tagContainer.innerHTML = `${keyword} <span onclick="this.parentElement.nextElementSibling.remove(); this.parentElement.remove(); checkKeywordLimit()">x</span>`;

                // Create a hidden input to include keywords in form submission
                let hiddenInput = document.createElement('input');
                hiddenInput.type = 'hidden';
                hiddenInput.name = 'keywords';
                hiddenInput.value = keyword;

                keywordsContainer.appendChild(tagContainer);
                keywordsContainer.appendChild(hiddenInput);
                this.value = '';
                errorMessage.style.display = 'none';
            } else if (currentKeywordsCount >= 10) {
                errorMessage.style.display = 'block';
            }
        }
    });

    document.getElementById('dwn_b').addEventListener('click', function() {
            const results = resultsData;
            // If no data, alert the user
            if (!results || results.length === 0) {
                alert('No data to download');
                return;
            }

            // Extract headers from the first object
            const headers = Object.keys(results[0]);

            // Convert data to CSV
            const csvContent = [
                headers.join(','), // Header row
                ...results.map(row =>
                    headers.map(header =>
                        // Escape special characters and handle potential commas in values
                        `"${String(row[header]).replace(/"/g, '""')}"`
                    ).join(',')
                )
            ].join('\n');

            // Create a Blob with the CSV content
            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });

            // Create a link element to trigger the download
            const link = document.createElement('a');
            const url = URL.createObjectURL(blob);
            link.setAttribute('href', url);
            link.setAttribute('download', 'job_data.csv');

            // Append to body, click, and remove
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);

            // Clean up the URL object
            URL.revokeObjectURL(url);
        });

    function checkKeywordLimit() {
        let keywordsContainer = document.getElementById('keywords-container');
        let errorMessage = document.getElementById('error-message');
        if (keywordsContainer.children.length / 2 < 10) {
            errorMessage.style.display = 'none';
        }
    }
});