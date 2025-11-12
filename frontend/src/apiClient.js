const token = localStorage.getItem('token');
const host = window.location.host === '' ? 'localhost:8000' : window.location.host;
const protocol = window.location.protocol === 'file:' ? 'http:' : window.location.protocol;
const apiUrl =  `${protocol}//${host}/api`;

async function post(path, requestBody) {

    const apiResponse = await fetch(apiUrl + path,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(requestBody)
        }
        ).then(response => response.json()
        ).catch(error => null);

    return apiResponse;
};

async function get(path) {

    const apiResponse = await fetch(apiUrl + path + `?token=${token}`
        ).then(response => response.json()
        ).catch(error => null);

    return apiResponse;
};

async function del(path) {

    const apiResponse = await fetch(apiUrl + path + `?token=${token}`,
        {
            method: "DELETE",
        }
        ).then(response => response.json()
        ).catch(error => null);

    return apiResponse;
};