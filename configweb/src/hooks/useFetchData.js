import {useEffect, useState} from 'react';
import axios from 'axios';
import { BACKEND_URL, BACKEND_PORT } from '../config';


function useFetchData(path) {
    const [data, setData] = useState({});
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        axios.get(`http://${BACKEND_URL}:${BACKEND_PORT}/${path}`)
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
