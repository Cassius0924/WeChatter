// CustomCommandKey.js
import React, {useEffect} from 'react';
import useFetchData from '../hooks/useFetchData';
import useSaveConfig from '../hooks/useSaveConfig';

function CustomCommandKey() {
    const [config, setConfig] = useFetchData('custom-command-key');
    const handleSave = useSaveConfig('custom-command-key', config);
    useEffect(() => {
        console.log('config changed');
        console.log(config);
    }, [config]);

    const commandKeyDict = config.custom_command_key_dict || {};
    console.log(commandKeyDict);

    const handleChange = (key, value) => {
        setConfig({
            ...config,
            custom_command_key_dict: {
                ...commandKeyDict,
                [key]: value.split(',').map(item => item.trim()),
            },
        });
    };

    return (
        <div className="border-4 border-dashed border-gray-200 rounded-lg mb-6">
            <div className="flex flex-col items-center justify-center h-full">
                <div className="text-center">
                    <h3 className="mb-4 text-lg leading-6 font-medium text-gray-900">
                        自定义命令键
                    </h3>
                    {Object.keys(commandKeyDict).map((key) => (
                        <div key={key}>
                            <h4 className="mb-2 text-md leading-6 font-medium text-gray-900">
                                {key}
                            </h4>
                            <input
                                type="text"
                                className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                                placeholder={key}
                                value={commandKeyDict[key].join(', ')}
                                onChange={e => handleChange(key, e.target.value)}
                            />
                        </div>
                    ))}
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
