// MessageForwarding.js
import React, {useEffect} from 'react';
import useFetchData from '../hooks/useFetchData';
import useSaveConfig from '../hooks/useSaveConfig';

function MessageForwarding() {
    const [config, setConfig] = useFetchData('message-forwarding');
    const handleSave = useSaveConfig('message-forwarding', config);
    useEffect(() => {
        console.log('config changed');
        console.log(config);
    }, [config]);

    const ruleList = config.message_forwarding_rule_list ? config.message_forwarding_rule_list[0] : {};

    return (
        <div className="border-4 border-dashed border-gray-200 rounded-lg mb-6">
            <div className="flex flex-col items-center justify-center h-full">
                <div className="text-center">
                    <h3 className="mb-4 text-lg leading-6 font-medium text-gray-900">
                        message_forwarding_enabled
                    </h3>
                    <p className="mb-4 text-sm leading-5 text-gray-500">
                        是否开启消息转发（True/False）
                    </p>
                    <input type="text"
                           className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                           placeholder="False"
                           value={config.message_forwarding_enabled || ''}
                           onChange={e => setConfig({...config, message_forwarding_enabled: e.target.value})}/>
                    <h3 className="mb-4 text-lg leading-6 font-medium text-gray-900">
                        message_forwarding_rule_list
                    </h3>
                    <p className="mb-4 text-sm leading-5 text-gray-500">
                        自定义消息转发规则列表
                    </p>
                    <input type="text"
                           className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                           placeholder=""
                           value={ruleList.from_list || ''}
                           onChange={e => setConfig({...ruleList, from_list: e.target.value})}/>
                    <input type="text"
                            className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                            placeholder=""
                            value={ruleList.to_person_list || ''}
                            onChange={e => setConfig({...ruleList, to_person_list: e.target.value})}/>
                    <input type="text"
                            className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                            placeholder=""
                            value={ruleList.to_group_list || ''}
                            onChange={e => setConfig({...ruleList, to_group_list: e.target.value})}/>
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

export default MessageForwarding;
