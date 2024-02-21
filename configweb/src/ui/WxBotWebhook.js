// WxBotWebhook.js
import React from 'react';
import useFetchData from '../hooks/useFetchData';
import useSaveConfig from '../hooks/useSaveConfig';

function WxBotWebhook() {
    const [config, setConfig] = useFetchData('wx_webhook_base_api');
    const handleSave = useSaveConfig('wx-bot-webhook', config);

        return (
            <div className="border-4 border-dashed border-gray-200 rounded-lg mb-6">
                <div className="flex flex-col items-center justify-center h-full">
                    <div className="text-center">
                        <h2 className="mb-4 text-lg leading-6 font-medium text-gray-900">
                            wx_webhook_host
                        </h2>
                        <p className="mb-4 text-sm leading-5 text-gray-500">
                            发送消息的 API 地址，必须包含http(s)://（http://localhost）
                        </p>
                        <input type="text"
                               className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                               placeholder="http://localhost"
                               value={config.wx_webhook_host || ''}
                               onChange={e => setConfig({...config, wx_webhook_host: e.target.value})}/>
                        <h2 className="mb-4 text-lg leading-6 font-medium text-gray-900">
                            wx_webhook_port
                        </h2>
                        <p className="mb-4 text-sm leading-5 text-gray-500">
                            发送消息的端口，wxBotWebhook Docker 的端口（3001）
                        </p>
                        <input type="text"
                               className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                               placeholder="80"
                               value={config.wx_webhook_port || ''}
                               onChange={e => setConfig({...config, wx_webhook_port: e.target.value})}/>
                        <h2 className="mb-4 text-lg leading-6 font-medium text-gray-900">
                            wx_webhook_recv_api_path
                        </h2>
                        <p className="mb-4 text-sm leading-5 text-gray-500">
                            接收消息的接口路径，RECV_MSG_API的路径（/receive_msg）                        </p>
                        <input type="text"
                               className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                               placeholder="/send"
                               value={config.wx_webhook_recv_api_path || ''}
                               onChange={e => setConfig({...config, wx_webhook_recv_api_path: e.target.value})}/>
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

export default WxBotWebhook;
