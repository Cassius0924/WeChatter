import React, {useEffect} from 'react';
import {
    Button,
    ButtonArea,
    CellBody,
    CellFooter,
    CellHeader,
    CellsTitle,
    Dialog,
    Form,
    FormCell,
    Icon,
    Input,
    Page
} from 'react-weui';
import useFetchData from '../hooks/useFetchData';
import useSaveConfig from '../hooks/useSaveConfig';
import {isValueExist} from './CustomFormCell';
import 'weui/dist/style/weui.min.css';
import Picker from "./Picker";
import 'weui';
import weui from 'weui.js';


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
        if (oldKey !== newKey) {
            if (newKey in newCommandKeyDict) {
                weui.alert('这个命令已经存在，请选择一个新的命令', function () {
                    console.log('ok')
                }, {title: '错误'});
                return;
            } else {
                delete newCommandKeyDict[oldKey];
            }
        }
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

    const Pickerdata = [
        {label: '从作者那里获取50块钱疯狂星期四', value: 'kfc-v50', disabled: true},
        {label: '获取 Bilibili 热搜', value: 'bili-hot'},
        {label: '获取食物热量', value: 'calories'},

        //depth设置成2，表示有两级联动，以此类推
        {label: '获取食物热量', value: 'calories', children: [{label: '香蕉',value: '香蕉', children: [{label: '大香蕉',value: '大香蕉', children: [{label: '超级大香蕉',value: '超级大香蕉', children: [{label: '超级无敌大香蕉',value: '超级无敌大香蕉', children: [{label: '小香蕉',value: '小香蕉'}]}]}]}]},{label: '苹果', value: '苹果'}]},

        {label: '获取抖音热搜', value: 'douyin-hot'},
        {label: '继续 GPT3.5 问答', value: 'gpt'},
        {label: '查看 GPT3.5 对话', value: 'gpt-chats'},
        {label: '查看 GPT3.5 记录', value: 'gpt-record'},
        {label: '继续 GPT3.5 继续', value: 'gpt-continue'},
        {label: '进行 GPT4 问答', value: 'gpt4'},
        {label: '查看 GPT4 对话记录', value: 'gpt4-chats'},
        {label: '查看 GPT4 聊天记录', value: 'gpt4-record'},
        {label: '继续 GPT4 对话', value: 'gpt4-continue'},
        {label: '获取汽油价格', value: 'gasoline-price'},
        {label: '获取 GitHub 趋势', value: 'github-trending'},
        {label: '查看命令帮助', value: 'help'},
        {label: '获取少数派早报', value: 'pai-post'},
        {label: '获取人民日报新闻', value: 'people'},
        {label: '获取人民日报新闻', value: 'people-daily'},
        {label: '获取人民日报新闻链接', value: 'people-url'},
        {label: '获取人民日报新闻链接', value: 'people-daily-url'},
        {label: '生成二维码', value: 'qrcode'},
        {label: '添加待办事项', value: 'todo'},
        {label: '删除待办事项', value: 'todo-remove'},
        {label: '获取历史上的今天', value: 'today-in-history'},
        {label: '获取笑话', value: 'trivia'},
        {label: '查询天气预报', value: 'weather'},
        {label: '获取微博热搜', value: 'weibo-hot'},
        {label: '单词/词语翻译', value: 'word'},
        {label: '获取知乎热搜', value: 'zhihu-hot'}
    ];

    //通过输入value从而获取Pickerdata对应的label
    function getLabelFromValuef(data, value) {
        if (value === '新命令键') {
            return '新命令键';
        }
        for (let i = 0; i < data.length; i++) {
            if (data[i].value === value) {
                return data[i].label;
            }
        }
        return '';
    }

    const Pickerconfig = (key) => ({
        depth: 10,
        id: 'Custom_Command_Key_commandPicker',
        title: getLabelFromValuef(Pickerdata, key),
        desc: '请选择命令键',
        closeText: '❌',
        defaultValue: [key],  // 默认选中第一个选项
        onChange: function (result) {
            console.log(result);
        },
        onConfirm: function (result) {
            // 调试信息
            console.log(key);
            // console.log(result);
            // console.log(result[0].value);
            // console.log(commandKeyDict[key]);
            handleChange(key, result[0].value, commandKeyDict[key].join(', '));
        }
    });


    return (
        <Page className="input">
            <CellsTitle>自定义命令键</CellsTitle>
            <ButtonArea>
                <Button
                    onClick={handleAddCommandKey}
                    className="weui-btn weui-btn_primary px-5 py-2 text-lg font-bold"
                >
                    添加命令键
                </Button>
            </ButtonArea>
            {Object.keys(commandKeyDict).map((key) => (
                <div key={key}>
                    <Form>
                        <FormCell>
                            <CellHeader style={headerStyle}>
                                {/*<Input*/}
                                {/*    type="text"*/}
                                {/*    defaultValue={key}*/}
                                {/*    onChange={e => handleChange(key, e.target.value, commandKeyDict[key].join(', '))}*/}
                                {/*/>*/}
                                <Picker
                                    Pickerdata={Pickerdata}
                                    Pickerconfig={Pickerconfig(key)}
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
                            <CellFooter>
                                {isValueExist(commandKeyDict[key]) ? <Icon value='success'/> : <Icon value='cancel'/>}
                            </CellFooter>
                            <div style={{
                                width: '150px',
                            }}>
                                <Button
                                    onClick={() => handleDeleteCommandKey(key)}
                                    className="weui-btn weui-btn_warn px-2 py-2 text-lg font-bold"
                                >
                                    删除命令键
                                </Button>
                            </div>
                        </FormCell>
                    </Form>
                    {/*<div style={{*/}
                    {/*    width: '200px',*/}
                    {/*    marginLeft: 'auto',*/}
                    {/*    marginRight: 'auto',*/}
                    {/*    margin: '1px auto',*/}
                    {/*    backgroundColor: '#f5f5f5',*/}
                    {/*    textAlign: 'center',*/}
                    {/*    borderRadius: '8px'*/}
                    {/*}}>*/}
                    {/*    <ButtonArea>*/}
                    {/*        <Button*/}
                    {/*            onClick={() => handleDeleteCommandKey(key)}*/}
                    {/*            className="weui-btn weui-btn_warn px-2 py-2 text-lg font-bold"*/}
                    {/*        >*/}
                    {/*            删除命令键*/}
                    {/*        </Button>*/}
                    {/*    </ButtonArea>*/}
                    {/*</div>*/}
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
