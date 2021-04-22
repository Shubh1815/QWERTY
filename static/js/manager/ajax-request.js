document.addEventListener('DOMContentLoaded', () => {
        fetch(URL)
            .then((response) => response.json())
            .then((data) => {
                data = JSON.parse(data);
                data.forEach((item) => {
                    let name = item.pk[0].toUpperCase() + item.pk.slice(1);
                    products.push({
                        'name': name,
                        'amount': Number(item.fields.amount),
                    })
                    productDataList.innerHTML += `<option value="${name}"></option>`
                })
            })
            .catch((err) => {
                console.log(err);
            })
})


const getCookie = (name) => {
    const cookies = document.cookie;
    if(!cookies) return "";

    let cvalue = "";

    cookies.split(";").forEach(cookie => {
        let [key, value] = cookie.split("=");
        key = key.trim();
        value = value.trim();

        if(key === name && !cvalue) {
            cvalue = value;
        }
    })

    return cvalue;
}

buyButton.addEventListener('click', () => {
    if(!selected || !enrollment_no.value) return;

    const csrftoken = getCookie("csrftoken");

    const data = {
        'enrollment_no': enrollment_no.value,
        'selected': selected,
        'total_amount': totalAmount,
    }

    fetch(URL, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(data),
    })
        .then(async (response) => {
            const data = await response.text();
            if(response.status === 400){
                document.querySelector(".messages").innerHTML = `
                <div class="alert alert-error alert-dismissible fade show" role="alert">
                    ${data}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
                `
            } else if(response.status > 400){
                document.querySelector(".messages").innerHTML = `
                <div class="alert alert-error alert-dismissible fade show" role="alert">
                    Invalid Data
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
                `
            } else {
                document.querySelector(".messages").innerHTML = `
                <div class="alert alert-success alert-dismissible fade show" role="alert">
                    ${data}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
                `
            }
        })

        .catch((err) => {
            console.log(err);
        })
})