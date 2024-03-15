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
import CustomFormCell from './CustomFormCell';


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
                    <CellHeader>
                        message_forwarding_enabled
                    </CellHeader>
                    <CellBody></CellBody>
                    <Switch
                        checked={config.message_forwarding_enabled || false}
                        onChange={e => setConfig({...config, message_forwarding_enabled: e.target.checked})}
                    />
                </FormCell>
            </Form>

            <CellsTitle>消息来源列表</CellsTitle>
            <CustomFormCell
                label="from_list"
                value={ruleList.from_list}
                onChange={e => setConfig({
                    ...config,
                    message_forwarding_rule_list: [{...ruleList, from_list: e.target.value}]
                })}
                placeholder="%ALL"
            />


            <CellsTitle>消息来源排除列表</CellsTitle>
            <CustomFormCell
                label="from_list_exclude"
                value={ruleList.from_list_exclude}
                onChange={e => setConfig({
                    ...config,
                    message_forwarding_rule_list: [{...ruleList, from_list_exclude: e.target.value}]
                })}
                placeholder="You"
            />

            <CellsTitle>转发给个人列表</CellsTitle>
            <CustomFormCell
                label="to_person_list"
                value={ruleList.to_person_list}
                onChange={e => setConfig({
                    ...config,
                    message_forwarding_rule_list: [{...ruleList, to_person_list: e.target.value}]
                })}
                placeholder="You"
            />

            <CellsTitle>转发给群组列表</CellsTitle>
            <CustomFormCell
                label="to_group_list"
                value={ruleList.to_group_list}
                onChange={e => setConfig({
                    ...config,
                    message_forwarding_rule_list: [{...ruleList, to_group_list: e.target.value}]
                })}
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

export default MessageForwarding;
