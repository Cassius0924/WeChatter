import {useEffect, useState} from 'react';
import axios from 'axios';
import { BACKEND_IP, BACKEND_PORT } from '../../../config';


function useFetchData(path) {
    const [data, setData] = useState({});//解释：useState()返回一个数组，第一个元素是状态值，第二个元素是更新状态值的函数
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        axios.get(`http://${BACKEND_IP}:${BACKEND_PORT}/${path}`)
            .then(res => {
                console.log(res.data);
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
