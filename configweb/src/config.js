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
import React, {useEffect} from 'react';
import useFetchData from './hooks/useFetchData';

function get_BACKEND_IP_and_BACKEND_PORT() {
    const [config, setConfig] = useFetchData('backend');
    const BACKEND_IP = config.backend_ip;
    const BACKEND_PORT = config.backend_port;
    useEffect(() => {
        console.log('config changed');
        console.log(config);
    }, [config]);

    return (
        <div className="border-4 border-dashed border-gray-200 rounded-lg mb-6">
            <div className="flex flex-col items-center justify-center h-full">
                <div className="text-center">
                    <h3 className="mb-4 text-lg leading-6 font-medium text-gray-900">
                        backend_ip
                    </h3>
                    <p className="mb-4 text-sm leading-5 text-gray-500">
                        后端IP地址
                    </p>
                    <input type="text"
                           className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                           placeholder="localhost"
                           value={config.backend_ip || ''}
                           onChange={e => setConfig({...config, backend_ip: e.target.value})}/>
                    <h3 className="mb-4 text-lg leading-6 font-medium text-gray-900">
                        backend_port
                    </h3>
                    <p className="mb-4 text-sm leading-5 text-gray-500">
                        后端端口
                    </p>
                    <input type="text"
                           className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                           placeholder="8000"
                           value={config.backend_port || ''}
                           onChange={e => setConfig({...config, backend_port: e.target.value})}/>
                </div>
            </div>
        </div>
    )
}

// export default get_BACKEND_IP_and_BACKEND_PORT;
export const [BACKEND_IP, BACKEND_PORT] = get_BACKEND_IP_and_BACKEND_PORT()
