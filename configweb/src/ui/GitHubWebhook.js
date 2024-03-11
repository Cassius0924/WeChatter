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
    Page,
    Switch
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

function GithubWebhook() {
    const [config, setConfig] = useFetchData('github-webhook');
    const [saveConfig, dialog, hideDialog] = useSaveConfig('github-webhook', config);
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
            <CellsTitle>是否接收 GitHub Webhook （True/False）</CellsTitle>
            <Form>
                <FormCell switch>
                    <CellBody>github_webhook_enabled</CellBody>
                    <Switch
                        checked={config.github_webhook_enabled || false}
                        onChange={e => setConfig({...config, github_webhook_enabled: e.target.checked})}
                    />
                </FormCell>
            </Form>

            <CellsTitle>接收 GitHub Webhook 的接口路径（/webhook/github）</CellsTitle>
            <Form>
                <FormCell>
                    <CellHeader style={headerStyle}>
                        <Label>github_webhook_api_path</Label>
                    </CellHeader>
                    <CellBody style={bodyStyle}>
                        <Input
                            type="text"
                            placeholder="/webhook/github"
                            value={config.github_webhook_api_path || ''}
                            onChange={e => setConfig({...config, github_webhook_api_path: e.target.value})}
                        />
                    </CellBody>
                </FormCell>
            </Form>

            <CellsTitle>接收 GitHub Webhook 的微信用户</CellsTitle>
            <Form>
                <FormCell>
                    <CellHeader style={headerStyle}>
                        <Label>github_webhook_receiver_list</Label>
                    </CellHeader>
                    <CellBody style={bodyStyle}>
                        <Input
                            type="text"
                            placeholder="[]"
                            value={config.github_webhook_receive_person_list || ''}
                            onChange={e => setConfig({...config, github_webhook_receive_person_list: e.target.value})}
                        />
                    </CellBody>
                </FormCell>
            </Form>

            <CellsTitle>接收 GitHub Webhook 的微信群</CellsTitle>
            <Form>
                <FormCell>
                    <CellHeader style={headerStyle}>
                        <Label>github_webhook_receive_group_list</Label>
                    </CellHeader>
                    <CellBody style={bodyStyle}>
                        <Input
                            type="text"
                            placeholder="[]"
                            value={config.github_webhook_receive_group_list || ''}
                            onChange={e => setConfig({...config, github_webhook_receive_group_list: e.target.value})}
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

export default GithubWebhook;
