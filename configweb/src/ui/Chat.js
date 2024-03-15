import React, {useEffect} from 'react';
import {Button, ButtonArea, CellBody, CellHeader, CellsTitle, Dialog, Form, FormCell, Page, Switch} from 'react-weui';
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

function Chat() {
    const [config, setConfig] = useFetchData('chat');
    const [saveConfig, dialog, hideDialog] = useSaveConfig('chat', config);
    useEffect(() => {
        console.log('config changed');
        console.log(config);
    }, [config]);
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
            <CellsTitle>命令前缀，用于区分命令和普通消息（/）</CellsTitle>
            <CustomFormCell
                label="command_prefix"
                value={config.command_prefix || ''}
                onChange={e => setConfig({...config, command_prefix: e.target.value})}
                placeholder="/"
            />

            <CellsTitle>群消息命令是否需要@机器人才能触发</CellsTitle>
            <Form>
                <FormCell switch>
                    <CellHeader>
                        need_mentioned
                    </CellHeader>
                    <CellBody>
                    </CellBody>
                    <Switch
                        checked={config.need_mentioned || false}
                        onChange={e => setConfig({...config, need_mentioned: e.target.checked})}
                    />
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

export default Chat;
