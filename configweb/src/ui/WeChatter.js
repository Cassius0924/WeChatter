// WxBotWebhook.js
import React from 'react';
import useFetchData from '../hooks/useFetchData';
import useSaveConfig from '../hooks/useSaveConfig';

function WeChatter() {
    const [config, setConfig] = useFetchData('wechatter');
    const handleSave = useSaveConfig('wechatter', config);

    return (
        <div className="border-4 border-dashed border-gray-200 rounded-lg mb-6">
            <div className="flex flex-col items-center justify-center h-full">
                <div className="text-center">
                    <h3 className="mb-4 text-lg leading-6 font-medium text-gray-900">
                        wechatter
                    </h3>
                    <p className="mb-4 text-sm leading-5 text-gray-500">
                        微信机器人服务的端口，接收消息的端口，RECV_MSG_API的端口（4000）
                    </p>
                    <input type="text"
                           className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                           placeholder="4000"
                           value={config.wechatter_port || ''}//这里的config.wechatter_port是从useFetchData('wechatter')中获取的
                           onChange={e => setConfig({...config, wechatter_port: e.target.value})}/>
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

export default WeChatter;
