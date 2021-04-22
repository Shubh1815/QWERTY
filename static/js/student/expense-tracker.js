const option = 'Expense';
let days;

const fetchData = async () => {
    const URL = `http://localhost:8000/student/tracker/expense/${days}/`;
    const response = await fetch(URL);

    if (response.status !== 200)
        return [];

    return await response.json();
}
