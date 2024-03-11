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

function OfficialAccountReminder() {
    const [config, setConfig] = useFetchData('official-account-reminder');
    const [saveConfig, dialog, hideDialog] = useSaveConfig('official-account-reminder', config);
    useEffect(() => {
        console.log('config changed');
        console.log(config);
    }, [config]);

    const ruleList = config.official_account_reminder_rule_list ? config.official_account_reminder_rule_list[0] : {};
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
            <CellsTitle>是否开启公众号提醒（True/False）</CellsTitle>
            <Form>
                <FormCell switch>
                    <CellBody>official_account_reminder_enabled</CellBody>
                    <Switch
                        checked={config.official_account_reminder_enabled || false}
                        onChange={e => setConfig({...config, official_account_reminder_enabled: e.target.checked})}
                    />
                </FormCell>
            </Form>

            <CellsTitle>公众号名称列表</CellsTitle>
            <Form>
                <FormCell>
                    <CellHeader style={headerStyle}>
                        <Label>oa_name_list</Label>
                    </CellHeader>
                    <CellBody style={bodyStyle}>
                        <Input
                            type="text"
                            placeholder=""
                            value={ruleList.oa_name_list || ''}
                            onChange={e => setConfig({...config, official_account_reminder_rule_list: [{...ruleList, oa_name_list: e.target.value}]})}
                        />
                    </CellBody>
                </FormCell>
            </Form>

            <CellsTitle>提醒给个人列表</CellsTitle>
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
                            onChange={e => setConfig({...config, official_account_reminder_rule_list: [{...ruleList, to_person_list: e.target.value}]})}
                        />
                    </CellBody>
                </FormCell>
            </Form>

            <CellsTitle>提醒给群组列表</CellsTitle>
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
                            onChange={e => setConfig({...config, official_account_reminder_rule_list: [{...ruleList, to_group_list: e.target.value}]})}
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

export default OfficialAccountReminder;
