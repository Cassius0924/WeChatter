// Admin.js
import React, {useEffect} from 'react';
import useFetchData from '../hooks/useFetchData';
import useSaveConfig from '../hooks/useSaveConfig';

function Admin() {
    const [config, setConfig, isLoading, error] = useFetchData('admin');
    const handleSave = useSaveConfig('admin', config);
    useEffect(() => {
        console.log('config changed');
        console.log(config);
        console.log(setConfig);
    }, [config]);
    if (isLoading) {
        return <div>Loading...</div>;
    }

    if (error) {
        console.error(error);
        return (
            <div>
                <div>Error: {error.message}</div>
                <div>Status: {error.response && error.response.status}</div>
                <div>Headers: {error.response && JSON.stringify(error.response.headers)}</div>
                <div>Data: {error.response && JSON.stringify(error.response.data, null, 2)}</div>
            </div>
        );
    }

    return (
        <div className="border-4 border-dashed border-gray-200 rounded-lg mb-6">
            <div className="flex flex-col items-center justify-center h-full">
                <div className="text-center">
                    <h3 className="mb-4 text-lg leading-6 font-medium text-gray-900">
                        admin_list
                    </h3>
                    <p className="mb-4 text-sm leading-5 text-gray-500">
                        微信管理员，用于接收机器人的报警信息和登录登出信息,填入微信名称（不是微信号，也不是微信备注）
                    </p>
                    <input type="text"
                           className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                           placeholder=''
                           value={config.admin_list || ''}
                           onChange={e => setConfig({...config, admin_list: e.target.value})}/>
                    <h3 className="mb-4 text-lg leading-6 font-medium text-gray-900">
                        admin_group_list
                    </h3>
                    <p className="mb-4 text-sm leading-5 text-gray-500">
                        填入微信群名称（不是群备注）
                    </p>
                    <input type="text"
                           className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                           placeholder=''
                           value={config.admin_group_list || ''}
                           onChange={e => setConfig({...config, admin_group_list: e.target.value})}/>
                    <button
                        onClick={handleSave}
                        className="mt-4 px-4 py-2 bg-gray-800 text-white text-sm font-medium rounded-md">
                        保存
                    </button>
                </div>
            </div>
        </div>
    );
}

export default Admin;
