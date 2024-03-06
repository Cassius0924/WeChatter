// CopilotGPT4.js
import React from 'react';
import useFetchData from '../hooks/useFetchData';
import useSaveConfig from '../hooks/useSaveConfig';

function CopilotGPT4() {
    const [config, setConfig] = useFetchData('copilot-gpt4');
    const handleSave = useSaveConfig('copilot-gpt4', config);

    return (
        <div className="border-4 border-dashed border-gray-200 rounded-lg mb-6">
            <div className="flex flex-col items-center justify-center h-full">
                <div className="text-center">
                    <h3 className="mb-4 text-lg leading-6 font-medium text-gray-900">
                        cp_gpt4_api_host
                    </h3>
                    <p className="mb-4 text-sm leading-5 text-gray-500">
                        Copilot GPT4 服务的 API 地址，必须包含http(s)://（http://localhost）
                    </p>
                    <input type="text"
                           className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                           placeholder="http://localhost"
                           value={config.openai_base_api || ''}
                           onChange={e => setConfig({...config, openai_base_api: e.target.value})}/>

                    <h3 className="mb-4 text-lg leading-6 font-medium text-gray-900">
                        cp_token
                    </h3>
                    <p className="mb-4 text-sm leading-5 text-gray-500">
                        Copilot 的 Token
                    </p>
                    <input type="text"
                           className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                           placeholder="ghu_your_token"
                           value={config.openai_token || ''}
                           onChange={e => setConfig({...config, openai_token: e.target.value})}/>
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

export default CopilotGPT4;
