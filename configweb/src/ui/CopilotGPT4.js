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

function CopilotGPT4() {
    const [config, setConfig] = useFetchData('copilot-gpt4');
    const [saveConfig, dialog, hideDialog] = useSaveConfig('copilot-gpt4', config);
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
            <CellsTitle>Copilot GPT4 服务的 API 地址，必须包含http(s)://（http://localhost）</CellsTitle>
            <CustomFormCell
                label="cp_gpt4_api_host"
                value={config.openai_base_api || ''}
                onChange={e => setConfig({...config, openai_base_api: e.target.value})}
                placeholder="https://api.openai.com"
            />

            <CellsTitle>Copilot 的 Token</CellsTitle>
            <CustomFormCell
                label="cp_token"
                value={config.openai_token || ''}
                onChange={e => setConfig({...config, openai_token: e.target.value})}
                placeholder="sk_your_openai_token"
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

export default CopilotGPT4;
