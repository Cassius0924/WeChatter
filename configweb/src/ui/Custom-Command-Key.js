// CustomCommandKey.js
import React from 'react';
import useFetchData from '../hooks/useFetchData';
import useSaveConfig from '../hooks/useSaveConfig';

function CustomCommandKey() {
    const [config, setConfig] = useFetchData('custom-command-key');
    const handleSave = useSaveConfig('custom-command-key', config);

    return (
        <div className="border-4 border-dashed border-gray-200 rounded-lg mb-6">
            <div className="flex flex-col items-center justify-center h-full">
                <div className="text-center">
                    <h3 className="mb-4 text-lg leading-6 font-medium text-gray-900">
                        custom_command_key_dict
                    </h3>
                    <p className="mb-4 text-sm leading-5 text-gray-500">
                        自定义命令关键词字典
                    </p>
                    <textarea
                        className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                        placeholder='{ "gpt4": [">"], "bili-hot": ["bh"], "weather": ["w", "温度"] }'
                        value={config.custom_command_key_dict || ''}
                        onChange={e => setConfig({...config, custom_command_key_dict: e.target.value})}/>
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

export default CustomCommandKey;
