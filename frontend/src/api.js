import axios from 'axios';

// This connects our React app to the FastAPI backend we built earlier
const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/v1',
});

export default api;