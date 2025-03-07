async function handleResponse(res) {
     if (res.status !== 200) {
        throw new Error('Error');
     }
    return res;
  }  

function GetEmissions() {
    return fetch('http://localhost:8000/emissions/', {
        method: 'get',
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
}