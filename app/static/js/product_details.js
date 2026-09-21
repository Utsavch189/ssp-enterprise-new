const quantityInput = document.getElementById('quantity');
const totalPriceElement = document.getElementById('totalPrice');
const productPrice = document.getElementById("productPrice");
const no_product_text = document.getElementById("no-product-text");
const loadingIndicator = document.getElementById('loadingIndicator');
const product_id = document.getElementById("p_id").getAttribute('value');
const product_type = document.getElementById("product_type");

let currentPage = 1;
const pageSize = 12;
let isLoading = false;
const debouncedLoadMoreProducts = debounce(fetchSimilarProducts, 600);
let total_products = 0;

function updateTotalPrice() {
    const price = parseFloat(productPrice.getAttribute('value'))
    const quantity = parseInt(quantityInput.value) || 1;
    const total = (price * quantity).toFixed(2);
    totalPriceElement.textContent = `${total} INR.`;
}

updateTotalPrice();

document.getElementById('decreaseQuantity').addEventListener('click', () => {
    const currentValue = parseInt(quantityInput.value) || 1;
    if (currentValue > 1) {
        quantityInput.value = currentValue - 1;
        updateTotalPrice();
    }
});

document.getElementById('increaseQuantity').addEventListener('click', () => {
    const currentValue = parseInt(quantityInput.value) || 1;
    quantityInput.value = currentValue + 1;
    updateTotalPrice();
});

quantityInput.addEventListener('input', updateTotalPrice);
quantityInput.addEventListener('change', () => {
    if (parseInt(quantityInput.value) < 1) {
        quantityInput.value = 1;
    }
    updateTotalPrice();
});

// Similar product fetch section

async function fetchSimilarProducts() {
    if (isLoading) return;

    isLoading = true;

    const productName = document.getElementById("product_name").innerText;
    const productType = product_type.getAttribute('type');

    const startIndex = (currentPage - 1) * pageSize;
    console.log(startIndex)

    if (startIndex >= total_products && currentPage!==1) {
        isLoading = false;
        no_product_text.classList.add('hidden');
        loadingIndicator.classList.add('hidden');
        return
    }

    try {
        const response = await fetch(`/get-similar-products/${product_id}/${productName}/${productType}/${currentPage}/${pageSize}`);
        const data = await response.json();
        total_products = data?.total_products;

        if (data.similar_products && data.similar_products.length > 0) {
            loadingIndicator.classList.remove('hidden');
            const similarProductsDiv = document.getElementById('similarProducts');
            no_product_text.classList.add('hidden');

            data.similar_products.forEach(product => {
                const productDiv = document.createElement('div');
                productDiv.classList.add('group');
                productDiv.innerHTML = `
                <a href="/product/${product.id}" class="group">
                    <div class="bg-white rounded-lg shadow-md overflow-hidden transition-transform duration-300 group-hover:scale-105">
                        <img src="${product.image}" alt="${product.name}" class="w-full h-48 object-cover">
                        <div class="p-4">
                            <h3 class="text-lg font-semibold text-gray-800">${product.name}</h3>
                            <p class="text-blue-600 font-bold mt-2">${product.price} INR.</p>
                        </div>
                    </div>
                </a>
                `;
                similarProductsDiv.appendChild(productDiv);
            });
            currentPage++;
            no_product_text.classList.add('hidden');
        } else {
            if (currentPage === 1) {
                no_product_text.classList.remove('hidden');
                loadingIndicator.classList.add('hidden');
            }
            else{
                loadingIndicator.classList.add('hidden');
            }
            console.log('No more similar products to load');
        }
    } catch (error) {
        console.error('Error fetching similar products:', error);
    } finally {
        isLoading = false;
    }
}

function onScroll() {
    const { scrollTop, clientHeight, scrollHeight } = document.documentElement;
    const isMobile = window.innerWidth <= 768;

    if (scrollHeight - scrollTop <= clientHeight * (isMobile ? 3 : 2)) {
        if (total_products === 0) return;
        debouncedLoadMoreProducts();
    }
}

window.addEventListener('scroll', onScroll);

fetchSimilarProducts(currentPage);