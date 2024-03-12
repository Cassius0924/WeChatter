import React from 'react';
import {
    Button,
    ButtonArea,
    CellsTitle,
    Form,
    FormCell,
    CellBody,
    Input,
    Page,
    Panel,
    PanelBody,
    Dialog, CellHeader, Label
} from 'react-weui';
import useFetchData from '../hooks/useFetchData';
import useSaveConfig from '../hooks/useSaveConfig';


const headerStyle = {
    width: '20%',
    paddingRight: '10px',
    whiteSpace: 'nowrap'
};

const bodyStyle = {
    width: '80%'
};
function WeChatter() {
    const [config, setConfig] = useFetchData('wechatter');
    const [saveConfig, dialog, hideDialog] = useSaveConfig('wechatter', config);
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
            <Panel>
                <PanelBody>
                    <CellsTitle>微信机器人服务的端口，接收消息的端口，RECV_MSG_API的端口（4000）</CellsTitle>
                    <Form>
                        <FormCell>
                            <CellHeader style={headerStyle}>
                                <Label>wechatter_port</Label>
                            </CellHeader>
                            <CellBody>
                                <Input
                                    type="text"
                                    placeholder="4000"
                                    value={config.wechatter_port || ''}
                                    onChange={e => setConfig({...config, wechatter_port: e.target.value})}
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
                </PanelBody>
            </Panel>
        </Page>
    );
}

export default WeChatter;
