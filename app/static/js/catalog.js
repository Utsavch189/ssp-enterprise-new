let allProducts = [];
let filteredProducts = [];
let currentPage = 1;
const productsPerPage = 12;
let isLoading = false;
let hasMore = true;
let totalProducts = 0;
let user_id;
let role;

const no_product_text = document.getElementById("no-product-text");
const productsContainer = document.getElementById('products');
const debouncedLoadMoreProducts = debounce(loadMoreProducts, 600);
const params = new URLSearchParams(window.location.search);
const categoryId = params.get("category-id");
const subcategoryId = params.get("subcategory-id");

const whole_path = window.location.href;

async function fetchProducts(page, pageSize) {
    try {
        if(categoryId && subcategoryId){
            var url = `/get-products/${page}/${pageSize}?category-id=${categoryId}&subcategory-id=${subcategoryId}`
        }
        else{
            if(categoryId){
                var url = `/get-products/${page}/${pageSize}?category-id=${categoryId}`
            }
            else if(subcategoryId){
                var url = `/get-products/${page}/${pageSize}?subcategory-id=${subcategoryId}`
            }
        }

        const response = await fetch(url);
        const data = await response.json();
        if (!data?.products?.length) {
            no_product_text.classList.remove('hidden');
        } else {
            no_product_text.classList.add('hidden');
        }
        totalProducts = data.total_products;  // Set total products
        return data.products;
    } catch (error) {
        console.error('Error fetching products:', error);
        return [];
    }
}

async function fetchSearchResults(keyword) {
    try {
        if(categoryId && subcategoryId){
            var url = `/search-product/${keyword}?category-id=${categoryId}&subcategory-id=${subcategoryId}`
        }
        else{
            if(categoryId){
                var url = `/search-product/${keyword}?category-id=${categoryId}`
            }
            else if(subcategoryId){
                var url = `/search-product/${keyword}?subcategory-id=${subcategoryId}`
            }
        }
        const response = await fetch(url);
        const data = await response.json();
        if (!data?.products?.length) {
            no_product_text.classList.remove('hidden');
        } else {
            no_product_text.classList.add('hidden');
        }
        return data.products || [];
    } catch (error) {
        console.error('Error searching products:', error);
        return [];
    }
}

function renderProducts(products, append = false) {
    if (!products.length) {
        no_product_text.classList.remove('hidden');
        return;
    }
    no_product_text.classList.add('hidden');

    const productCards = products.map(product => `
        <div class="bg-white rounded-lg shadow-md overflow-hidden transition-transform duration-300 hover:scale-105">
            <a href="/product/${product.id}" class="block">
                <img src="${product.image}" alt="${product.name}" class="w-full h-48 object-cover">
                <div class="p-4">
                    <h3 class="text-lg font-semibold text-gray-800">${product.name}</h3>
                    <p class="text-blue-600 font-bold mt-2">${product.price} INR.</p>
                </div>
            </a>
            <div class="hidden admin-feat px-4 pb-4 flex justify-end space-x-2">
                <button onclick="openEditModal('${product.id}')" class="p-2 text-blue-600 hover:bg-blue-50 rounded-full">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                </button>
                <button onclick="deleteProduct('${product.id}')" class="p-2 text-red-600 hover:bg-red-50 rounded-full">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                </button>
            </div>
        </div>
    `).join('');

    if (append) {
        productsContainer.innerHTML += productCards;
    } else {
        productsContainer.innerHTML = productCards;
    }
    if(user_id && role==='admin'){
        enable_admin_feat('.admin-feat');
    }
}

async function loadMoreProducts() {
    if (isLoading || !hasMore) return;

    const startIndex = (currentPage - 1) * productsPerPage;
    const endIndex = startIndex + productsPerPage;

    // Stop loading if we have reached the total number of products
    if (startIndex > totalProducts) {
        hasMore = false;
        document.getElementById('loading').classList.add('hidden');
        return;
    }
    else {
        isLoading = true;
        document.getElementById('loading').classList.remove('hidden');

        // Fetch the products from the server
        const productsToShow = await fetchProducts(currentPage, productsPerPage);
        renderProducts(productsToShow, true);

        currentPage++;
        isLoading = false;
        document.getElementById('loading').classList.add('hidden');
    }
}

// Infinite scroll handler
function handleScroll() {
    const { scrollTop, clientHeight, scrollHeight } = document.documentElement;
    const isMobile = window.innerWidth <= 768;

    if (scrollHeight - scrollTop <= clientHeight * (isMobile ? 3 : 2) && hasMore) {
        if (totalProducts === 0) return;
        document.getElementById('loading').classList.remove('hidden');
        debouncedLoadMoreProducts();
    }
}

// Search functionality
document.getElementById('search').addEventListener('input', async (e) => {
    const searchTerm = e.target.value.toLowerCase();
    if (searchTerm.length === 0) {
        productsContainer.innerHTML = '';
        loadMoreProducts();
        return;
    }
    if (searchTerm.length > 1) {
        filteredProducts = await fetchSearchResults(searchTerm);
        currentPage = 1;
        hasMore = true;
        renderProducts(filteredProducts.slice(0, productsPerPage));
    }
});

function enable_admin_feat(classname){
    document.querySelectorAll(classname).forEach((elm)=>{
        elm.classList.remove('hidden');
    })
}

utils.get_session_data()
.then(data=>{
    if(data?.data?.user_id){
        user_id=data?.data?.user_id;
        role=data?.data?.role;
        if(data?.data?.role === 'admin'){
            enable_admin_feat('.admin-feat');
        }
    }
})

async function getProductById(product_id) {
    try {
        const res = await fetch(`/get-product/${product_id}`);
        const data = await res.json();
        return data;
    } catch (error) {
        console.error("Error fetching product:", error);
    }
}

function openEditModal(productId) {
    const product = getProductById(productId);
    product.then(data =>{
        if (data?.product) {
            document.getElementById('editProductid').value = data?.product.id;
            document.getElementById('editName').value = data?.product.name;
            document.getElementById('editUnit').value = data?.product.qnt_unit;
            document.getElementById('editPrice').value = data?.product.price;
            document.getElementById('editType').value = data?.product.type || '';
            document.getElementById('editDesc').value = data?.product.desc || '';
            document.getElementById("editImage").value='';
            document.getElementById('editSubCategory').value = data?.product?.category_name || '';
            document.getElementById('editCategory').value = data?.product?.subcategory_name || '';
            document.getElementById('redirectPath').value = whole_path;
            if(data?.product.is_active===1){
                document.getElementById('editVisibility').setAttribute('checked',true);
                document.getElementById('editVisibility').value=1;
            }
            else{
                document.getElementById('editVisibility').removeAttribute('checked');
                document.getElementById('editVisibility').value=0;
            }
        }
        document.getElementById('editmodal-btn').click();
    })
}

function deleteProduct(productId) {
    document.getElementById('deletemodal-btn').click();
    document.getElementById('delete-btn').addEventListener("click",async()=>{
        try {
            const res = await fetch('/delete-product',{
                method:"POST",
                body: JSON.stringify({
                    id:productId
                }),
                headers:{
                    "Content-Type":"application/json"
                }
            })
            const data = await res.json();
            if(data?.status===200){
                utils.showToast(data.message,'success');
                setTimeout(() => {
                    window.location.reload();
                }, 800);
            }
            else{
                utils.showToast(data.message,'error')
            }
        } catch (error) {
            utils.showToast("Something is wrong!","error")
        }
    })
}

window.addEventListener('scroll', handleScroll);

loadMoreProducts();
