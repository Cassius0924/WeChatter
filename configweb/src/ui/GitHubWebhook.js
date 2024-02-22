// GithubWebhook.js
import React from 'react';
import useFetchData from '../hooks/useFetchData';
import useSaveConfig from '../hooks/useSaveConfig';

function GithubWebhook() {
    const [config, setConfig] = useFetchData('github-webhook');
    const handleSave = useSaveConfig('github-webhook', config);

    return (
        <div className="border-4 border-dashed border-gray-200 rounded-lg mb-6">
            <div className="flex flex-col items-center justify-center h-full">
                <div className="text-center">
                    <h3 className="mb-4 text-lg leading-6 font-medium text-gray-900">
                        github_webhook_enabled
                    </h3>
                    <p className="mb-4 text-sm leading-5 text-gray-500">
                        是否接收 GitHub Webhook （True/False）
                    </p>
                    <input type="text"
                           className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                           placeholder="False"
                           value={config.github_webhook_enabled || ''}
                           onChange={e => setConfig({...config, github_webhook_enabled: e.target.value})}/>
                    <h3 className="mb-4 text-lg leading-6 font-medium text-gray-900">
                        github_webhook_api_path
                    </h3>
                    <p className="mb-4 text-sm leading-5 text-gray-500">
                        接收 GitHub Webhook 的接口路径（/webhook/github）
                    </p>
                    <input type="text"
                           className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                           placeholder="/webhook/github"
                           value={config.github_webhook_api_path || ''}
                           onChange={e => setConfig({...config, github_webhook_api_path: e.target.value})}/>
                    <h3 className="mb-4 text-lg leading-6 font-medium text-gray-900">
                        github_webhook_receiver_list
                    </h3>
                    <p className="mb-4 text-sm leading-5 text-gray-500">
                        接收 GitHub Webhook 的微信用户
                    </p>
                    <input type="text"
                           className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                           placeholder="[]"
                           value={config.github_webhook_receive_person_list || ''}
                           onChange={e => setConfig({...config, github_webhook_receive_person_list: e.target.value})}/>
                    <h3 className="mb-4 text-lg leading-6 font-medium text-gray-900">
                        github_webhook_receive_group_list
                    </h3>
                    <p className="mb-4 text-sm leading-5 text-gray-500">
                        接收 GitHub Webhook 的微信群
                    </p>
                    <input type="text"
                           className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                           placeholder="[]"
                           value={config.github_webhook_receive_group_list || ''}
                           onChange={e => setConfig({...config, github_webhook_receive_group_list: e.target.value})}/>
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

export default GithubWebhook;
