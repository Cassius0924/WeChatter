// GasolinePriceCron.js
import React from 'react';
import useFetchData from '../hooks/useFetchData';
import useSaveConfig from '../hooks/useSaveConfig';

function GasolinePriceCron() {
    const [config, setConfig] = useFetchData('gasoline-price-cron');
    const handleSave = useSaveConfig('gasoline-price-cron', config);

    return (
        <div className="border-4 border-dashed border-gray-200 rounded-lg mb-6">
            <div className="flex flex-col items-center justify-center h-full">
                <div className="text-center">
                    <h3 className="mb-4 text-lg leading-6 font-medium text-gray-900">
                        gasoline_price_cron_enabled
                    </h3>
                    <p className="mb-4 text-sm leading-5 text-gray-500">
                        是否开启汽油价格自动推送定时任务（True/False）
                    </p>
                    <input type="text"
                           className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                           placeholder="False"
                           value={config.gasoline_price_cron_enabled || ''}
                           onChange={e => setConfig({...config, gasoline_price_cron_enabled: e.target.value})}/>
                    <h3 className="mb-4 text-lg leading-6 font-medium text-gray-900">
                        gasoline_price_cron_rule_list
                    </h3>
                    <p className="mb-4 text-sm leading-5 text-gray-500">
                        自动推送规则列表（JSON格式）
                    </p>
                    <textarea
                        className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                        placeholder='[ { "cron": { "year": "*", "month": "*", "day": "*", "week": "*", "day_of_week": "*", "hour": "7", "minute": "0", "second": "0", "start_date": null, "end_date": null, "timezone": "Asia/Shanghai" }, "tasks": [ { "city": "广州", "to_persons": ["张三", "Tom"], "to_groups": ["测试群"] }, { "city": "北京", "to_persons": ["李四"], "to_groups": [] } ] } ]'
                        value={config.gasoline_price_cron_rule_list || ''}
                        onChange={e => setConfig({...config, gasoline_price_cron_rule_list: e.target.value})}/>
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

export default GasolinePriceCron;
