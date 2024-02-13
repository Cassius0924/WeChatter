import {useEffect, useState} from 'react';
import axios from 'axios';

//前端无法获取config.ini文件，所以这里直接写死
// const fs = require('fs');
// const path = require('path');
// const ini = require('ini');
//
// // 获取项目根目录的路径
// const rootDir = path.resolve(__dirname, '../..');
//
// // 读取并解析 config.ini
// const config = ini.parse(fs.readFileSync(path.join(rootDir, 'config.ini'), 'utf-8'));
//
// // 现在你可以使用 config 对象了
// export const front_url = config.server.front_url;
// export const front_port = config.server.front_port;

//本地
// export const BASE_URL = "localhost";
// export const PORT = "8000";
//服务器
export const BASE_URL = "47.92.99.199";
export const PORT = "8000";

function useFetchData(path) {
    const [data, setData] = useState({});
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        // axios.get(`http://127.0.0.1:8000/${path}`)
        // axios.get(`http://47.92.99.199:30/api/${path}`)
        axios.get(`http://${BASE_URL}:${PORT}/${path}`)
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
