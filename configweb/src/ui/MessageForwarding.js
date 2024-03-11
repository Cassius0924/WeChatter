import React, {useEffect} from 'react';
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

function MessageForwarding() {
    const [config, setConfig] = useFetchData('message-forwarding');
    const [saveConfig, dialog, hideDialog] = useSaveConfig('message-forwarding', config);
    useEffect(() => {
        console.log('config changed');
        console.log(config);
    }, [config]);

    const ruleList = config.message_forwarding_rule_list ? config.message_forwarding_rule_list[0] : {};
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
            <CellsTitle>是否开启消息转发（True/False）</CellsTitle>
            <Form>
                <FormCell switch>
                    <CellBody>message_forwarding_enabled</CellBody>
                    <Switch
                        checked={config.message_forwarding_enabled || false}
                        onChange={e => setConfig({...config, message_forwarding_enabled: e.target.checked})}
                    />
                </FormCell>
            </Form>

            <CellsTitle>消息来源列表</CellsTitle>
            <Form>
                <FormCell>
                    <CellHeader style={headerStyle}>
                        <Label>from_list</Label>
                    </CellHeader>
                    <CellBody style={bodyStyle}>
                        <Input
                            type="text"
                            placeholder=""
                            value={ruleList.from_list || ''}
                            onChange={e => setConfig({...config, message_forwarding_rule_list: [{...ruleList, from_list: e.target.value}]})}
                        />
                    </CellBody>
                </FormCell>
            </Form>

            <CellsTitle>消息来源排除列表</CellsTitle>
            <Form>
                <FormCell>
                    <CellHeader style={headerStyle}>
                        <Label>from_list_exclude</Label>
                    </CellHeader>
                    <CellBody style={bodyStyle}>
                        <Input
                            type="text"
                            placeholder=""
                            value={ruleList.from_list_exclude || ''}
                            onChange={e => setConfig({...config, message_forwarding_rule_list: [{...ruleList, from_list_exclude: e.target.value}]})}
                        />
                    </CellBody>
                </FormCell>
            </Form>

            <CellsTitle>转发给个人列表</CellsTitle>
            <Form>
                <FormCell>
                    <CellHeader style={headerStyle}>
                        <Label>to_person_list</Label>
                    </CellHeader>
                    <CellBody style={bodyStyle}>
                        <Input
                            type="text"
                            placeholder=""
                            value={ruleList.to_person_list || ''}
                            onChange={e => setConfig({...config, message_forwarding_rule_list: [{...ruleList, to_person_list: e.target.value}]})}
                        />
                    </CellBody>
                </FormCell>
            </Form>

            <CellsTitle>转发给群组列表</CellsTitle>
            <Form>
                <FormCell>
                    <CellHeader style={headerStyle}>
                        <Label>to_group_list</Label>
                    </CellHeader>
                    <CellBody style={bodyStyle}>
                        <Input
                            type="text"
                            placeholder=""
                            value={ruleList.to_group_list || ''}
                            onChange={e => setConfig({...config, message_forwarding_rule_list: [{...ruleList, to_group_list: e.target.value}]})}
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

export default MessageForwarding;
