const category_select = document.getElementById("add-category");
const subcategory_select = document.getElementById("add-subcategory");
const subcategory_section = document.getElementById("subcategory-section");
const sector_select = document.getElementById("add-sector");

let categories = [];

async function getSectors() {
    try {
      const response = await fetch('/get-sectors')
      const data = await response.json();
      if (data) {
        sector_select.innerHTML = '';
        sector_select.innerHTML = '<option selected>Choose a Sector</option>';
        data.map(v => {
          sector_select.innerHTML += `
            <option value='${v.id}'>${v.name}</option>
          `
        })
      }
    } catch (error) {
      console.log("getSectors() ", error)
    }
  }


async function getCategories() {
    try {
        const response = await fetch("/get-categories");
        const data = await response.json();
        categories=[];
        categories = data.map(item => ({
            id: item.category_id,
            name: item.category_name,
            subcategories: item.subcategories.map(sub => ({
                subcategory_id : sub.subcategory_id,
                subcategory_name : sub.subcategory_name
            }))
        }));

        category_select.innerHTML='';
        category_select.innerHTML='<option selected>Choose a Category</option>';
        categories.map((v,i)=>{
            category_select.innerHTML+=`<option value='${v.id}'>${v.name}</option>`
        })
        
    } catch (error) {
        console.log("getCategories() ",error)
    }
}

category_select.addEventListener("change",(e)=>{
    const category_id = e.target.value;
    let category = categories.filter(p=>p.id===category_id);
    if (category){
        category = category[0];
    }
    else{
        return
    }
    if (category.subcategories?.length > 0){
        const subcategories = category.subcategories;
        subcategory_select.innerHTML='';
        subcategory_select.innerHTML='<option selected>Choose a SubCategory</option>';
        subcategories.map((v,i)=>{
            subcategory_select.innerHTML+=`<option value='${v.subcategory_id}'>${v.subcategory_name}</option>`
        })
        subcategory_section.classList.remove("hidden");
    }
})

document.getElementById('create-product-form').addEventListener("submit",async(e)=>{
    e.preventDefault();

    const importExcel = document.getElementById('import-excel').files[0]
    const add_product_btn = document.getElementById("add-product-btn");

    if(importExcel!==undefined){
        // excel send
        const formData = new FormData();
        formData.append('importExcel',importExcel);
        // document.getElementById('close-add-product-modal').click();
        let originalText = add_product_btn.textContent;

        try {
            add_product_btn.setAttribute('disabled',true);
            add_product_btn.textContent = 'Loading...'
            utils.showToast('Data seeding is started!','success');

            const response = await fetch("/create-product", {
                method: 'POST',
                body: formData,
            });
    
            if (response.ok) {
                const result = await response.json();
                utils.showToast('Data seeded successfully!','success');
            } else {
                const error = await response.json();
                utils.showToast(`Failed to seed data: ${error.message}`,'error');
            }
        } catch (error) {
            console.error('Error:', error);
            utils.showToast('An unexpected error occurred. Please try again later.','error');
        }
        finally{
            add_product_btn.removeAttribute('disabled');
            add_product_btn.textContent=originalText;
            document.getElementById('import-excel').value = "";
        }
    }
    else{
        const name = document.getElementById("addName").value;
        const price = document.getElementById("addPrice").value;
        const image = document.getElementById("addImage").files[0];
        const type = document.getElementById("addType").value;
        const description = document.getElementById("addDesc").value;
        const category = document.getElementById('add-category').value;
        const unit = document.getElementById('addUnit').value;

        if (!name || !price || !image || !type || !description || !category || !unit){
            utils.showToast('Some Fields Are missing!','error');
            return;
        }
        else{
            document.getElementById('create-product-form').submit();
        }
    }
})

getCategories();
getSectors();