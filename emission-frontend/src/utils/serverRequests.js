import Cookies from 'js-cookie';

async function handleResponse(res) {
     if (res.status !== 200) {
        throw new Error('Error');
     }
    return res;
  }  

function GetEmissions() {
    return fetch('http://localhost:8000/emissions/', {
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
    return fetch('http://localhost:8000/register/', {
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
    return fetch('http://localhost:8000/auth/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
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

// headers: {
//     'Content-Type': 'application/json',
//     'X-CSRFToken': Cookies.get('csrftoken'),
//   },      


export {
    GetEmissions,
    RegisterUser,
    UserLogin,
}