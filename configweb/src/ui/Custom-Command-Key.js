import React, { useEffect } from 'react';
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

function CustomCommandKey() {
    const [config, setConfig] = useFetchData('custom-command-key');
    const [saveConfig, dialog, hideDialog] = useSaveConfig('custom-command-key', config);
    useEffect(() => {
        console.log('config changed');
        console.log(config);
    }, [config]);

    const commandKeyDict = config.custom_command_key_dict || {};
    console.log(commandKeyDict);

    const handleChange = (oldKey, newKey, value) => {
        const newCommandKeyDict = {...commandKeyDict};
        delete newCommandKeyDict[oldKey];
        newCommandKeyDict[newKey] = value.split(',').map(item => item.trim());
        setConfig({
            ...config,
            custom_command_key_dict: newCommandKeyDict,
        });
    };

    // 添加新的自定义命令键
    const handleAddCommandKey = () => {
        const newCommandKeyDict = {...commandKeyDict};
        newCommandKeyDict['新命令键'] = [];
        setConfig({
            ...config,
            custom_command_key_dict: newCommandKeyDict,
        });
    };

    // 删除自定义命令键
    const handleDeleteCommandKey = (key) => {
        const newCommandKeyDict = {...commandKeyDict};
        delete newCommandKeyDict[key];
        setConfig({
            ...config,
            custom_command_key_dict: newCommandKeyDict,
        });
    };
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
            <CellsTitle>自定义命令键</CellsTitle>
            <ButtonArea>
                <Button
                    onClick={handleAddCommandKey}
                >
                    添加命令键
                </Button>
            </ButtonArea>
            {Object.keys(commandKeyDict).map((key) => (
                <div key={key}>
                    <Form>
                        <FormCell>
                            <CellHeader style={headerStyle}>
                                <Input
                                    type="text"
                                    defaultValue={key}
                                    onChange={e => handleChange(key, e.target.value, commandKeyDict[key].join(', '))}
                                />
                            </CellHeader>
                            <CellBody style={bodyStyle}>
                                <Input
                                    type="text"
                                    placeholder="输入命令"
                                    value={commandKeyDict[key].join(', ')}
                                    onChange={e => handleChange(key, key, e.target.value)}
                                />
                            </CellBody>
                        </FormCell>
                    </Form>
                    <ButtonArea>
                        <Button
                            onClick={() => handleDeleteCommandKey(key)}
                        >
                            删除命令键
                        </Button>
                    </ButtonArea>
                </div>
            ))}
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

export default CustomCommandKey;
