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
            <Form>
                <FormCell>
                    <CellHeader style={headerStyle}>
                        <Label>cp_gpt4_api_host</Label>
                    </CellHeader>
                    <CellBody style={bodyStyle}>
                        <Input
                            type="text"
                            placeholder="http://localhost"
                            value={config.openai_base_api || ''}
                            onChange={e => setConfig({...config, openai_base_api: e.target.value})}
                        />
                    </CellBody>
                </FormCell>
            </Form>

            <CellsTitle>Copilot 的 Token</CellsTitle>
            <Form>
                <FormCell>
                    <CellHeader style={headerStyle}>
                        <Label>cp_token</Label>
                    </CellHeader>
                    <CellBody style={bodyStyle}>
                        <Input
                            type="text"
                            placeholder="ghu_your_token"
                            value={config.openai_token || ''}
                            onChange={e => setConfig({...config, openai_token: e.target.value})}
                        />
                    </CellBody>
                </FormCell>
            </Form>

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
