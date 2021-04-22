const product = document.getElementById("product");
const quantity = document.getElementById("quantity");
const enrollment_no = document.getElementById("enrollment-no");
const addProductButton = document.getElementById("addProduct");

let products = [];
let totalAmount = 0;
const selected = [];

const productDataList = document.getElementById("products");
const selectedProducts = document.getElementById("selectedProducts");
const totalAmountSpan = document.getElementById("total-amount");
const buyButton = document.getElementById("buy");

const updateSelectedList = () => {
    let content = '';

    selected.forEach((item, i) => {
        const p = item.name;
        const q = item.quantity;

        content +=  `
                <li class="list-group-item my-3">
            <div class="d-flex justify-content-between align-items-center">
                <div class="d-flex justify-content-between align-items-center">
                    <div class="product-name">${p}</div>
                    <div class="product-quantity text-center">
                       <button 
                           class="btn rounded-pill badge p-0" 
                           onclick="(() => incr(${i}))()"
                       >
                           <i class="bi bi-chevron-up"></i>
                       </button>
                       <span>${q}</span>
                       <button 
                           class="btn rounded-pill badge p-0" 
                           onclick="(() => decr(${i}))()"
                       >
                           <i class="bi bi-chevron-down"></i>
                       </button>
                    </div>
                </div>
                <button 
                    class="btn text-danger remove-product" 
                    onclick="(() => removeProduct(${i}))()"
                >
                    <i class="bi bi-trash"></i>
                </button>
            </div>
        </li>
        `
    })

    selectedProducts.innerHTML = content;
    totalAmountSpan.innerHTML = totalAmount;
}

const removeProduct = (index) => {
    const amount = products.find((item) => item.name === selected[index].name).amount;
    totalAmount -= amount * selected[index].quantity;

    selected.splice(index, 1);
    updateSelectedList();
}

const incr = (index) => {
    const amount = products.find((item) => item.name === selected[index].name).amount;
    totalAmount += amount;
    selected[index].quantity += 1;
    updateSelectedList();
}

const decr = (index) => {
    if(selected[index].quantity > 1){
        const amount = products.find((item) => item.name === selected[index].name).amount;
        totalAmount -= amount;
        selected[index].quantity -= 1;
        updateSelectedList();
    } else {
        removeProduct(index);
    }
}

addProductButton.addEventListener("click", () => {

    const p = product.value;
    const q = Number(quantity.value);

    if(!p || !q){
        return;
    }

    const amount = products.find((item) => item.name === p).amount;
    totalAmount += amount * q;

    for(let i=0;i<selected.length;i++){
        if(selected[i].name === p){
            selected[i].quantity += q;
            updateSelectedList();
            return;
        }
    }

    const content = `
        <li class="list-group-item my-3">
            <div class="d-flex justify-content-between align-items-center">
                <div class="d-flex justify-content-between align-items-center">
                    <div class="product-name">${p}</div>
                    <div class="product-quantity text-center">
                       <button 
                           class="btn rounded-pill badge p-0" 
                           onclick="(() => incr(${selected.length}))()"
                       >
                           <i class="bi bi-chevron-up"></i>
                       </button>
                       <span>${q}</span>
                       <button 
                           class="btn rounded-pill badge p-0" 
                           data-index="${selected.length}" 
                           onclick="(() => decr(${selected.length}))()"
                       >
                           <i class="bi bi-chevron-down"></i>
                       </button>
                    </div>
                </div>
                <button 
                    class="btn text-danger remove-product" 
                    data-index="${selected.length}"
                    onclick="(() => removeProduct(${selected.length}))()"
                >
                    <i class="bi bi-trash"></i>
                </button>
            </div>
        </li>
    `

    selected.push({
        'name': p,
        'quantity': q,
    })

    selectedProducts.innerHTML += content;
    totalAmountSpan.innerHTML = totalAmount;
})

const student_data = () => {
    fetch(`http://localhost:8000/student/${enrollment_no.value}/`)
        .then(response => response.json())
        .then(data => {
            data = JSON.parse(data);
            document.getElementById("balance").innerText = `₹ ${data['tokens']}`;
        })
        .catch(err => {
            document.getElementById("balance").innerText = "N/A";
            console.log(err);
        })
}

enrollment_no.addEventListener('input', () => {
    student_data();
})
