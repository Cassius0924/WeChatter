import React from 'react';
import {
    Button,
    ButtonArea,
    CellBody,
    CellHeader,
    CellsTitle,
    Dialog,
    Form,
    FormCell,
    Input,
    Label,
    Page
} from 'react-weui';
import useFetchData from '../hooks/useFetchData';
import useSaveConfig from '../hooks/useSaveConfig';
import CustomFormCell from "./CustomFormCell";


// 添加样式
const headerStyle = {
    width: '20%',
    paddingRight: '10px',
    whiteSpace: 'nowrap'
};

const bodyStyle = {
    width: '80%'
};


function WxBotWebhook() {
    const [config, setConfig] = useFetchData('wx-bot-webhook');
    const [saveConfig, dialog, hideDialog] = useSaveConfig('wx-bot-webhook', config);

    const dialogStyle = {
        title: "保存成功",
        buttons: [
            {
                type: 'default',
                label: '确定',
                onClick: () => hideDialog()
            }
        ]
    };


    return (
        <Page className="input">
            <CellsTitle>发送消息的 API 地址，必须包含http(s)://ip:端口（http://localhost:3001）</CellsTitle>
            <CustomFormCell
                label="wx_webhook_host"
                value={config.wx_webhook_base_api || ''}
                onChange={e => setConfig({...config, wx_webhook_base_api: e.target.value})}
                placeholder="http://localhost:3001"
            />

            <CellsTitle>接收消息的接口路径，RECV_MSG_API的路径（/receive_msg）</CellsTitle>
            <CustomFormCell
                label="wx_webhook_recv_api_path"
                value={config.wx_webhook_recv_api_path || ''}
                onChange={e => setConfig({...config, wx_webhook_recv_api_path: e.target.value})}
                placeholder="/receive_msg"
            />

            <CellsTitle>用于验证消息的token（wxbot）</CellsTitle>
            <CustomFormCell
                label="wx_webhook_token"
                value={config.wx_webhook_token || ''}
                onChange={e => setConfig({...config, wx_webhook_token: e.target.value})}
                placeholder="your_wx_webhook_token"
            />

            <ButtonArea>
                <Button
                    onClick={saveConfig}
                >
                    保存
                </Button>
            </ButtonArea>
            <Dialog type="ios" title={dialog.title} buttons={dialogStyle.buttons} show={dialog.show}>
                {dialog.message}
            </Dialog>
        </Page>
    );
}

export default WxBotWebhook;


// // WxBotWebhook.js
// import React from 'react';
// import useFetchData from '../hooks/useFetchData';
// import useSaveConfig from '../hooks/useSaveConfig';
//
// function WxBotWebhook() {
//     const [config, setConfig] = useFetchData('wx-bot-webhook');
//     const [saveConfig, dialog, hideDialog] = useSaveConfig('wx-bot-webhook', config);
//
//         return (
//             <div className="border-4 border-dashed border-gray-200 rounded-lg mb-6">
//                 <div className="flex flex-col items-center justify-center h-full">
//                     <div className="text-center">
//                         <h2 className="mb-4 text-lg leading-6 font-medium text-gray-900">
//                             wx_webhook_host
//                         </h2>
//                         <p className="mb-4 text-sm leading-5 text-gray-500">
//                             发送消息的 API 地址，必须包含http(s)://ip:端口（http://localhost:3001）
//                         </p>
//                         <input type="text"
//                                className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
//                                placeholder="http://localhost:3001"
//                                value={config.wx_webhook_base_api || ''}
//                                onChange={e => setConfig({...config, wx_webhook_base_api: e.target.value})}/>
//
//                         <h2 className="mb-4 text-lg leading-6 font-medium text-gray-900">
//                             wx_webhook_recv_api_path
//                         </h2>
//                         <p className="mb-4 text-sm leading-5 text-gray-500">
//                             接收消息的接口路径，RECV_MSG_API的路径（/receive_msg）                        </p>
//                         <input type="text"
//                                className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
//                                placeholder="/receive_msg"
//                                value={config.wx_webhook_recv_api_path || ''}
//                                onChange={e => setConfig({...config, wx_webhook_recv_api_path: e.target.value})}/>
//
//                         <h2 className="mb-4 text-lg leading-6 font-medium text-gray-900">
//                             wx_webhook_token
//                         </h2>
//                         <p className="mb-4 text-sm leading-5 text-gray-500">
//                             用于验证消息的token（wxbot）
//                         </p>
//                         <input type="text"
//                                className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
//                                placeholder="wxbot"
//                                value={config.wx_webhook_token || ''}
//                                onChange={e => setConfig({...config, wx_webhook_token: e.target.value})}/>
//
//                         <button
//                             onClick={handleSave}
//                             className="mt-4 px-4 py-2 bg-gray-800 text-white text-sm font-medium rounded-md">
//                             保存
//                         </button>
//                     </div>
//                 </div>
//             </div>
//         );
// }
//
// export default WxBotWebhook;
