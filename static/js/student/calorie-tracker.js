const option = 'Calorie';
let days;

const fetchData = async () => {
    const URL = `http://localhost:8000/student/tracker/calorie/${days}/`;
    const response = await fetch(URL);

    if (response.status !== 200)
        return [];

    return await response.json();
}
