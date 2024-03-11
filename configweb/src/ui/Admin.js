import React, { useEffect, useState } from 'react';
import { Button, ButtonArea, CellBody, CellHeader, CellsTitle, Dialog, Form, FormCell, Input, Label, Page } from 'react-weui';
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

function Admin() {
    const [config, setConfig, isLoading, error] = useFetchData('admin');
    const [saveConfig, dialog, hideDialog] = useSaveConfig('admin', config);

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
    useEffect(() => {
        console.log('config changed');
        console.log(config);
        console.log(setConfig);
    }, [config]);

    if (isLoading) {
        return <div>Loading...</div>;
    }

    if (error) {
        console.error(error);
        return (
            <div>
                <div>Error: {error.message}</div>
                <div>Status: {error.response && error.response.status}</div>
                <div>Headers: {error.response && JSON.stringify(error.response.headers)}</div>
                <div>Data: {error.response && JSON.stringify(error.response.data, null, 2)}</div>
            </div>
        );
    }


    return (
        <Page className="input">
            <CellsTitle>管理员</CellsTitle>
            <Form>
                <FormCell>
                    <CellHeader style={headerStyle}>
                        <Label>admin_list</Label>
                    </CellHeader>
                    <CellBody style={bodyStyle}>
                        <Input
                            type="text"
                            placeholder="微信管理员"
                            value={config.admin_list || ''}
                            onChange={e => setConfig({...config, admin_list: e.target.value})}
                        />
                    </CellBody>
                </FormCell>

                <FormCell>
                    <CellHeader style={headerStyle}>
                        <Label>admin_group_list</Label>
                    </CellHeader>
                    <CellBody style={bodyStyle}>
                        <Input
                            type="text"
                            placeholder="微信群名称"
                            value={config.admin_group_list || ''}
                            onChange={e => setConfig({...config, admin_group_list: e.target.value})}
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

export default Admin;
