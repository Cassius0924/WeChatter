//后端配置

//本地
// export const BACKEND_IP = "localhost";
// export const BACKEND_PORT = "8000";
//服务器
// export const BACKEND_IP = "47.92.99.199";
// export const BACKEND_PORT = "8000";

// export const BACKEND_IP = jsonConfig.backend_ip;
// export const BACKEND_PORT = jsonConfig.backend_port;

//config.js
import useFetchData from './hooks/useFetchData';

function get_BACKEND_IP_and_BACKEND_PORT() {
    const [config, setConfig] = useFetchData('backend');
    return [config.backend_ip, config.backend_port];
}


export const [BACKEND_IP, BACKEND_PORT] = get_BACKEND_IP_and_BACKEND_PORT();
