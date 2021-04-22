const params = new URLSearchParams(window.location.search);

const getDate = () => {
    const today = new Date();
    const year = today.getFullYear();

    let month = (Number(today.getMonth()) + 1).toString();
    month = month.length < 2 ? "0" + month : month;

    let date = (Number(today.getDate()) + 1).toString();
    date = date.length < 2 ? "0" + date : date;

    return `${year}-${month}-${date}`;
}

let category = params.get('category') ? params.get('category') : 0;
let date = params.get('date') ? params.get('date') : getDate();

document.getElementById("category").value = category;
document.getElementById("date").value = date;
