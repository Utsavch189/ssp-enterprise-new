const params = new URLSearchParams(window.location.search);
const sectorId = params.get("sector");
const sectorName = params.get("sector-name");

async function fetchCategories() {
    try {
        if(sectorId){
            var url = `/get-categories?sector-id=${sectorId}`
        }
        else if(sectorName){
            var url = `/get-categories?sector-name=${sectorName}`
        }
        else{
            var url = "/get-categories"
        }
        const response = await fetch(url);
        const data = await response.json();
        
        // Transform data structure to match existing logic
        const categories = data.map(item => ({
            id: item.category_id,
            name: item.category_name,
            subcategories: item.subcategories.map(sub => ({
                subcategory_id : sub.subcategory_id,
                subcategory_name : sub.subcategory_name
            }))
        }));

        setupPagination(categories);
    } catch (error) {
        console.error("Error fetching categories:", error);
    }
}

function setupPagination(categories) {
    const itemsPerPage = 5;
    let currentPage = 1;
    const totalPages = Math.ceil(categories.length / itemsPerPage);

    function displayCategories(page) {
        const start = (page - 1) * itemsPerPage;
        const end = start + itemsPerPage;
        const paginatedCategories = categories.slice(start, end);

        const categoriesContainer = document.getElementById('categories-container');
        categoriesContainer.innerHTML = '';

        paginatedCategories.map((category,i) => {
            const categoryElement = document.createElement('div');
            // categoryElement.onclick=()=>{
            //     window.location.href=`/product-catalog?category-id=${category.id}`;
            // }
            categoryElement.className = 'bg-white cursor-pointer rounded-xl shadow-lg p-6 mb-6 transform transition-all duration-300 hover:scale-[1.02] hover:shadow-xl';
            categoryElement.innerHTML = `
                <div class="flex items-center mb-4">
                  <h3 class="text-xl font-bold text-gray-800">${category.name}</h3>
                </div>
                <div class="grid grid-cols-2 gap-3">
                  ${category.subcategories.map(sub => `
                    <a href='/product-catalog?category-id=${category.id}&subcategory-id=${sub.subcategory_id}' class="flex items-center space-x-2 text-gray-600 hover:text-blue-600 cursor-pointer transition-colors duration-200">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                      </svg>
                      <span>${sub.subcategory_name}</span>
                    </a>
                  `).join('')}
                </div>
            `;
            categoriesContainer.appendChild(categoryElement);
        });

        updatePaginationButtons(page);
    }

    function updatePaginationButtons(currentPage) {
        const paginationContainer = document.getElementById('pagination');
        paginationContainer.innerHTML = '';

        // Previous button
        const prevButton = document.createElement('button');
        prevButton.className = `px-4 py-2 rounded-lg flex items-center space-x-1 ${currentPage === 1
            ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
            : 'bg-blue-500 text-white hover:bg-blue-600 transition-colors duration-200'
            }`;
        prevButton.innerHTML = `
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
            </svg>
            <span>Previous</span>
        `;
        prevButton.disabled = currentPage === 1;
        prevButton.onclick = () => {
            if (currentPage > 1) {
                displayCategories(currentPage - 1);
            }
        };

        // Page numbers
        const pageNumbers = document.createElement('div');
        pageNumbers.className = 'flex space-x-2';
        for (let i = 1; i <= totalPages; i++) {
            const pageButton = document.createElement('button');
            pageButton.className = `w-10 h-10 rounded-lg flex items-center justify-center transition-all duration-200 ${currentPage === i
                ? 'bg-blue-500 text-white'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`;
            pageButton.textContent = i;
            pageButton.onclick = () => displayCategories(i);
            pageNumbers.appendChild(pageButton);
        }

        // Next button
        const nextButton = document.createElement('button');
        nextButton.className = `px-4 py-2 rounded-lg flex items-center space-x-1 ${currentPage === totalPages
            ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
            : 'bg-blue-500 text-white hover:bg-blue-600 transition-colors duration-200'
            }`;
        nextButton.innerHTML = `
            <span>Next</span>
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>
        `;
        nextButton.disabled = currentPage === totalPages;
        nextButton.onclick = () => {
            if (currentPage < totalPages) {
                displayCategories(currentPage + 1);
            }
        };

        paginationContainer.appendChild(prevButton);
        paginationContainer.appendChild(pageNumbers);
        paginationContainer.appendChild(nextButton);
    }

    // Initial display
    displayCategories(currentPage);
}

document.querySelector('#app').innerHTML = `
    <div class="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      <div class="container mx-auto px-4 py-12">
        <h1 class="text-4xl font-bold text-gray-800 mb-2 text-center">Product Categories</h1>
        <p class="text-gray-600 text-center mb-12">Explore our comprehensive range of networking and infrastructure solutions</p>
        <div id="categories-container"></div>
        <div id="pagination" class="flex justify-center items-center space-x-4 mt-12"></div>
      </div>
    </div>
`;

// Fetch categories and initialize pagination
fetchCategories();
