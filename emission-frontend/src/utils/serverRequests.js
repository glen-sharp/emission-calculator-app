import Cookies from 'js-cookie';

const ipAddress = "192.168.0.148";

const BASE_URL = 'http://' + ipAddress + ':8000/'

function handleResponse(res) {
    if (res.status === 401) {
        window.location.replace('/login');
    } else if (res.status !== 200) {
        throw new Error(res.status);
    }
    return res;
  }  

function GetEmissions() {
    return fetch(BASE_URL + 'emissions/', {
        method: 'GET',
        credentials: 'include',
    })
    .then(res => handleResponse(res))
    .then(data => {
        return data
    })
    .catch((error) => {
        throw error;
    });
}

function RegisterUser(user_info) {
    return fetch(BASE_URL + 'register/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
          },
        body: JSON.stringify(user_info)
    })
    .then(res => handleResponse(res))
    .then(data => {
        return data
    })
    .catch((error) => {
        throw error;
    });
}

function UserLogin(login_info) {
    return fetch(BASE_URL + 'auth/login/', {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': Cookies.get('csrftoken'),
        },
        body: JSON.stringify(login_info)
    })
    .then(res => handleResponse(res))
    .then(data => {
        return data
    })
    .catch((error) => {
        throw error;
    });
}

function UserLogout() {
    return fetch(BASE_URL + 'auth/logout/', {
        method: 'GET',
        credentials: 'include',
    })
    .then(res => handleResponse(res))
    .then(data => {
        return data
    })
    .catch((error) => {
        throw error;
    });
}


export {
    GetEmissions,
    RegisterUser,
    UserLogin,
    UserLogout,
}