// Bot.js
import React from 'react';
import useFetchData from '../hooks/useFetchData';
import useSaveConfig from '../hooks/useSaveConfig';

function Bot() {
    const [config, setConfig] = useFetchData('bot');
    const handleSave = useSaveConfig('bot', config);

    return (
        <div className="border-4 border-dashed border-gray-200 rounded-lg mb-6">
            <div className="flex flex-col items-center justify-center h-full">
                <div className="text-center">
                    <h3 className="mb-4 text-lg leading-6 font-medium text-gray-900">
                        bot_name
                    </h3>
                    <p className="mb-4 text-sm leading-5 text-gray-500">
                        机器人的微信名称（不是微信号，不带引号）
                    </p>
                    <input type="text"
                           className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                           placeholder="BotName"
                           value={config.bot_name || ''}
                           onChange={e => setConfig({...config, bot_name: e.target.value})}/>
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

export default Bot;
