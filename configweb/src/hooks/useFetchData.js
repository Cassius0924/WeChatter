import { useState, useEffect } from 'react';
import axios from 'axios';

function useFetchData(path) {
    const [data, setData] = useState({});
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        // axios.get(`http://127.0.0.1:8000/${path}`)
        // axios.get(`http://47.92.99.199:30/api/${path}`)
        axios.get(`172.24.191.12:3000/${path}`)
            .then(res => {
                setData(res.data);
                setIsLoading(false);
            })
            .catch(err => {
                console.error(err);
                setError(err);
                setIsLoading(false);
            });
    }, [path]);  // 当path改变时，useEffect会重新执行

    return [data, setData, isLoading, error];
}

export default useFetchData;
