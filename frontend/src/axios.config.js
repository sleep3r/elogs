import axios from 'axios';
import router from './router';
const ajax = axios.create({
    withCredentials: true
});

ajax.interceptors.response.use(undefined, (error) => {
    if (error.response && (error.response.status === 401 || error.response.status === 403)) {
        router.push('/login')
    }
    return Promise.reject(error.response.data);
});

export default ajax