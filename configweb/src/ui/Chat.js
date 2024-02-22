// Chat.js
import React, {useEffect} from 'react';
import useFetchData from '../hooks/useFetchData';
import useSaveConfig from '../hooks/useSaveConfig';

function Chat() {
    const [config, setConfig] = useFetchData('chat');
    const handleSave = useSaveConfig('chat', config);
    useEffect(() => {
        console.log('config changed');
        console.log(config);
    }, [config]);
    return (
        <div className="border-4 border-dashed border-gray-200 rounded-lg mb-6">
            <div className="flex flex-col items-center justify-center h-full">
                <div className="text-center">
                    <h3 className="mb-4 text-lg leading-6 font-medium text-gray-900">
                        command_prefix
                    </h3>
                    <p className="mb-4 text-sm leading-5 text-gray-500">
                        命令前缀，用于区分命令和普通消息（/）
                    </p>
                    <input type="text"
                           className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                           placeholder="/"
                           value={config.command_prefix || ''}
                           onChange={e => setConfig({...config, command_prefix: e.target.value})}/>
                    <h3 className="mb-4 text-lg leading-6 font-medium text-gray-900">
                        need_mentioned
                    </h3>
                    <p className="mb-4 text-sm leading-5 text-gray-500">
                        群消息命令是否需要@机器人才能触发（True/False）
                    </p>
                    <input type="text"
                           className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                           placeholder="True"
                           value={config.need_mentioned || ''}
                           onChange={e => setConfig({...config, need_mentioned: e.target.value})}/>
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

export default Chat;
