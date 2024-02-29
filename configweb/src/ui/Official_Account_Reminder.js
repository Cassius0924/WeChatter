// Official_Account_Reminder.js
import React, {useEffect} from 'react';
import useFetchData from '../hooks/useFetchData';
import useSaveConfig from '../hooks/useSaveConfig';

function OfficialAccountReminder() {
    const [config, setConfig] = useFetchData('official_account_reminder');
    const handleSave = useSaveConfig('official-account-reminder', config);
    useEffect(() => {
        console.log('config changed');
        console.log(config);
    }, [config]);

    const ruleList = config.official_account_reminder_rule_list ? config.official_account_reminder_rule_list[0] : {};

    return (
        <div className="border-4 border-dashed border-gray-200 rounded-lg mb-6">
            <div className="flex flex-col items-center justify-center h-full">
                <div className="text-center">
                    <h3 className="mb-4 text-lg leading-6 font-medium text-gray-900">
                        official_account_reminder_enabled
                    </h3>
                    <p className="mb-4 text-sm leading-5 text-gray-500">
                        是否开启公众号提醒（True/False）
                    </p>
                    <input type="text"
                           className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                           placeholder="False"
                           value={config.official_account_reminder_enabled || ''}
                           onChange={e => setConfig({...config, official_account_reminder_enabled: e.target.value})}/>

                    <h3 className="mb-4 text-lg leading-6 font-medium text-gray-900">
                        official_account_reminder_rule_list
                    </h3>
                    <p className="mb-4 text-sm leading-5 text-gray-500">
                        oa_name_list: 公众号名称列表
                    </p>
                    <input type="text"
                           className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                           placeholder=""
                           value={ruleList.oa_name_list || ''}
                           onChange={e => setConfig({...config, official_account_reminder_rule_list: [{...ruleList, oa_name_list: e.target.value}]})} />
                    <p className="mb-4 text-sm leading-5 text-gray-500">
                        to_person_list: 提醒给个人列表
                    </p>
                    <input type="text"
                            className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                            placeholder=""
                            value={ruleList.to_person_list || ''}
                            onChange={e => setConfig({...config, official_account_reminder_rule_list: [{...ruleList, to_person_list: e.target.value}]})}   />
                    <p className="mb-4 text-sm leading-5 text-gray-500">
                        to_group_list: 提醒给群组列表
                    </p>
                    <input type="text"
                            className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                            placeholder=""
                            value={ruleList.to_group_list || ''}
                            onChange={e => setConfig({...config, official_account_reminder_rule_list: [{...ruleList, to_group_list: e.target.value}]})} />
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

export default OfficialAccountReminder;
