import React, {useEffect} from 'react';
import {useNavigate} from 'react-router-dom';
import {
    Button,
    ButtonArea,
    CellBody, CellFooter,
    CellHeader,
    CellsTitle,
    Dialog,
    Form,
    FormCell,
    Input,
    Label,
    Page,
    Switch,
} from 'react-weui';
import useFetchData from '../hooks/useFetchData';
import useSaveConfig from '../hooks/useSaveConfig';
import {TaskCron_pickerData} from "../TaskCron_pickerData";
import Picker from "./Picker";
import {TaskCron_cronData} from "../TaskCron_cronData";

// 添加样式
const headerStyle = {
    width: '20%',
    paddingRight: '10px',
    whiteSpace: 'nowrap'
};

const bodyStyle = {
    width: '80%'
};

function TaskCron() {
    const [config, setConfig] = useFetchData('task-cron');
    const [saveConfig, dialog, hideDialog] = useSaveConfig('task-cron', config);
    useEffect(() => {
        console.log('config changed');
        console.log(config);
    }, [config]);

    const taskCronList = config.task_cron_list || [];

    const handleChange = (taskIndex, field, value) => {
        const newTaskCronList = [...taskCronList];
        newTaskCronList[taskIndex][field] = value;
        setConfig({
            ...config,
            task_cron_list: newTaskCronList,
        });
    };

    const handleCommandChange = (taskIndex, commandIndex, field, value) => {
        const newTaskCronList = [...taskCronList];
        newTaskCronList[taskIndex].commands[commandIndex][field] = value;
        setConfig({
            ...config,
            task_cron_list: newTaskCronList,
        });
    };

    // 在TaskCron组件中添加handleAddCommand事件处理器
    const handleAddCommand = (taskIndex) => {
        const newTaskCronList = [...taskCronList];
        const newCommand = {
            cmd: [],
            args: [],
            to_person_list: [],
            to_group_list: [],
        };
        newTaskCronList[taskIndex].commands.push(newCommand);
        setConfig({
            ...config,
            task_cron_list: newTaskCronList,
        });
    };

    // 在TaskCron组件中添加handleDeleteCommand事件处理器
    const handleDeleteCommand = (taskIndex, commandIndex) => {
        const newTaskCronList = [...taskCronList];
        newTaskCronList[taskIndex].commands.splice(commandIndex, 1);
        setConfig({
            ...config,
            task_cron_list: newTaskCronList,
        });
    };

    // 在TaskCron组件中添加handleAddCron事件处理器
    const handleAddCron = () => {
        const newTaskCronList = [...taskCronList];
        const newCron = {
            task: '新任务',
            enabled: true,
            cron: {
                year: '*',
                month: '*',
                day: '*',
                hour: '8',
                minute: '0',
                second: '0',
                timezone: 'Asia/Shanghai',
            },
            commands: [
                {
                    cmd: [],
                    args: [],
                    to_person_list: [],
                    to_group_list: [],
                }
            ],
        };
        newTaskCronList.push(newCron);
        setConfig({
            ...config,
            task_cron_list: newTaskCronList,
        });
    };

    // 在TaskCron组件中添加handleDeleteCron事件处理器
    const handleDeleteCron = (taskIndex) => {
        const newTaskCronList = [...taskCronList];
        newTaskCronList.splice(taskIndex, 1);
        setConfig({
            ...config,
            task_cron_list: newTaskCronList,
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


    //通过输入value从而获取Pickerdata对应的label
    function getLabelFromValue(data, value) {
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

    const Pickerconfig = (taskIndex, commandIndex, command) => ({
        depth: 10,
        id: 'Task_Cron_commandPicker',
        title: getLabelFromValue(TaskCron_pickerData, command.cmd),
        desc: '请选择命令键',
        closeText: '❌',
        defaultValue: [command.cmd],  // 默认选中第一个选项
        onChange: function (result) {
            console.log(result);
        },
        onConfirm: function (result) {
            // 调试信息
            console.log(taskIndex);
            console.log(commandIndex);
            console.log(result[0].value);
            console.log(result);
            handleCommandChange(taskIndex, commandIndex, 'cmd', result[0].value)

            // 自己写的版本：
            // if (result[1] !== undefined) {// 如果存在第二个选项，选择第二个选项，说明存在args
            //     if (result[2] !== undefined) {// 如果存在第三个选项，就选择第三个选项
            //         if (result[3] !== undefined) {// 如果存在第四个选项，就选择第四个选项
            //             return handleCommandChange(taskIndex, commandIndex, 'args', result[3].value.split(', '))
            //         }
            //         return handleCommandChange(taskIndex, commandIndex, 'args', result[2].value.split(', '))
            //     }
            //     return handleCommandChange(taskIndex, commandIndex, 'args', result[1].value.split(', '))
            // }

            //优化版本：
            // 寻找 result 数组中最后一个定义的元素
            let lastDefinedIndex = result.length - 1;
            while (result[lastDefinedIndex] === undefined && lastDefinedIndex >= 0) {
                lastDefinedIndex--;
            }

            // 如果找到了定义的元素，调用 handleCommandChange 函数
            if (lastDefinedIndex >= 0) {
                return handleCommandChange(taskIndex, commandIndex, 'args', result[lastDefinedIndex].value.split(', '));
            }

        }
    });

    // 通过输入value，判断Pickerdata中对应的value是否存在children
    // 作用：是否需要输入args
    function isargsexist(command) {
        // for (let i = 0; i < Pickerdata.length; i++) {
        //     if (Pickerdata[i].value === command) {
        //         if (Pickerdata[i].children === undefined) {
        //             return false;
        //         }
        //     }
        // }
        // return true;
        const neadargscommands = ['calories', 'gasoline-price', 'qrcode', 'weather'];
        if (neadargscommands.includes(command)) {
            return true;
        }
    }

    const navigate = useNavigate();

    const cronconfig = (taskIndex, cron) => ({
        depth: 5,
        id: 'Task_Cron_cronPicker',
        title: 'Cron',
        desc: '请选择Cron',
        closeText: '❌',
        onChange: function (result) {
            console.log(result);
            console.log(cron);

        },
        onConfirm: function (result) {
            // 调试信息
            console.log(result);

            //如果cron中任意一个在result[0].value里面，就调用对应的handleChange函数
            if (Object.keys(cron).includes(result[0].value)) {
                console.log('result[0].value:', result[0].value);
                handleChange(taskIndex, 'cron', {
                    ...cron,
                    [result[0].value]: result[1].value,
                })
            }
        }
    });


    return (
        <Page className="input">
            <CellsTitle>任务计划列表</CellsTitle>

            <ButtonArea>
                <Button
                    onClick={handleAddCron}
                >
                    添加任务
                </Button>
            </ButtonArea>

            {taskCronList.map((taskCron, taskIndex) => (
                <div key={taskIndex} className="m-10">
                    <CellsTitle>Task {taskIndex + 1}</CellsTitle>

                    <Form>
                        <FormCell>
                            <CellHeader style={headerStyle}>
                                <Label>Task</Label>
                            </CellHeader>
                            <CellBody style={bodyStyle}>
                                <Input
                                    type="text"
                                    placeholder="Task"
                                    value={taskCron.task}
                                    onChange={e => handleChange(taskIndex, 'task', e.target.value)}
                                />
                            </CellBody>
                            {/*<CellFooter>*/}
                            {/*    <Icon value='success'/>*/}
                            {/*</CellFooter>*/}
                            <div style={{
                                width: '150px',
                            }}>
                                <Button
                                    onClick={() => handleAddCommand(taskIndex)}
                                >
                                    添加命令
                                </Button>
                            </div>
                            <div style={{
                                width: '10px',
                            }}>
                            </div>
                            <div style={{
                                width: '150px',
                            }}>
                                <Button
                                    onClick={() => handleDeleteCron(taskIndex)}
                                    className="weui-btn weui-btn_warn px-2 py-2 text-lg font-bold"
                                >
                                    删除Task{taskIndex + 1}
                                </Button>
                            </div>
                        </FormCell>
                    </Form>

                    <Form>
                        <FormCell switch>
                            <CellHeader>
                                enabled
                            </CellHeader>
                            <CellBody></CellBody>
                            <Switch
                                checked={taskCron.enabled || false}
                                onChange={e => handleChange(taskIndex, 'enabled', e.target.checked)}
                            />
                        </FormCell>
                    </Form>

                    <CellsTitle>Cron Fields</CellsTitle>

                    <Form>
                        <FormCell>
                            <CellHeader style={headerStyle}>
                                <Label>Cron</Label>
                            </CellHeader>
                            <Picker
                                Pickerdata={TaskCron_cronData}
                                Pickerconfig={cronconfig(taskIndex, taskCron.cron)}
                            />
                        </FormCell>
                        <FormCell>
                            <CellHeader style={headerStyle}>
                                <Label>Year</Label>
                            </CellHeader>
                            <CellBody style={bodyStyle}>
                                <Input
                                    type="text"
                                    placeholder="Year"
                                    value={taskCron.cron.year}
                                    onChange={e => handleChange(taskIndex, 'cron', {
                                        ...taskCron.cron,
                                        year: e.target.value
                                    })}
                                />
                            </CellBody>
                        </FormCell>
                        <FormCell>
                            <CellHeader style={headerStyle}>
                                <Label>Month</Label>
                            </CellHeader>
                            <CellBody style={bodyStyle}>
                                <Input
                                    type="text"
                                    placeholder="Month"
                                    value={taskCron.cron.month}
                                    onChange={e => handleChange(taskIndex, 'cron', {
                                        ...taskCron.cron,
                                        month: e.target.value
                                    })}
                                />
                            </CellBody>
                        </FormCell>
                        <FormCell>
                            <CellHeader style={headerStyle}>
                                <Label>Day</Label>
                            </CellHeader>
                            <CellBody style={bodyStyle}>
                                <Input
                                    type="text"
                                    placeholder="Day"
                                    value={taskCron.cron.day}
                                    onChange={e => handleChange(taskIndex, 'cron', {
                                        ...taskCron.cron,
                                        day: e.target.value
                                    })}
                                />
                            </CellBody>
                        </FormCell>


                        <FormCell>
                            <CellHeader style={headerStyle}>
                                <Label>Hour</Label>
                            </CellHeader>
                            <CellBody style={bodyStyle}>
                                <Input
                                    type="text"
                                    placeholder="Hour"
                                    value={taskCron.cron.hour}
                                    onChange={e => handleChange(taskIndex, 'cron', {
                                        ...taskCron.cron,
                                        hour: e.target.value
                                    })}
                                />
                            </CellBody>
                        </FormCell>
                        <FormCell>
                            <CellHeader style={headerStyle}>
                                <Label>Minute</Label>
                            </CellHeader>
                            <CellBody style={bodyStyle}>
                                <Input
                                    type="text"
                                    placeholder="Minute"
                                    value={taskCron.cron.minute}
                                    onChange={e => handleChange(taskIndex, 'cron', {
                                        ...taskCron.cron,
                                        minute: e.target.value
                                    })}
                                />
                            </CellBody>
                        </FormCell>
                        <FormCell>
                            <CellHeader style={headerStyle}>
                                <Label>Second</Label>
                            </CellHeader>
                            <CellBody style={bodyStyle}>
                                <Input
                                    type="text"
                                    placeholder="Second"
                                    value={taskCron.cron.second}
                                    onChange={e => handleChange(taskIndex, 'cron', {
                                        ...taskCron.cron,
                                        second: e.target.value
                                    })}
                                />
                            </CellBody>
                        </FormCell>
                        <FormCell>
                            <CellHeader style={headerStyle}>
                                <Label>Timezone</Label>
                            </CellHeader>
                            <CellBody style={bodyStyle}>
                                <Input
                                    type="text"
                                    placeholder="Timezone"
                                    value={taskCron.cron.timezone}
                                    onChange={e => handleChange(taskIndex, 'cron', {
                                        ...taskCron.cron,
                                        timezone: e.target.value
                                    })}
                                />
                            </CellBody>
                        </FormCell>
                    </Form>

                    {taskCron.commands.map((command, commandIndex) => (
                        <div key={commandIndex}>
                            <CellsTitle>Command {commandIndex + 1}</CellsTitle>

                            <Form>
                                <FormCell>
                                    <CellHeader style={headerStyle}>
                                        <Label>Command</Label>
                                    </CellHeader>
                                    <CellBody style={bodyStyle}>
                                        {/*<Input*/}
                                        {/*    type="text"*/}
                                        {/*    placeholder="Command"*/}
                                        {/*    value={command.cmd}*/}
                                        {/*    onChange={e => handleCommandChange(taskIndex, commandIndex, 'cmd', e.target.value)}*/}
                                        {/*/>*/}

                                        <div style={{
                                            height: '100%',
                                            display: 'flex',
                                        }}>
                                            <Picker
                                                Pickerdata={TaskCron_pickerData}
                                                Pickerconfig={Pickerconfig(taskIndex, commandIndex, command)}
                                            />
                                        </div>

                                    </CellBody>

                                    <div style={{
                                        width: '150px',
                                    }}>
                                        <Button
                                            onClick={() => handleDeleteCommand(taskIndex, commandIndex)}
                                            className="weui-btn weui-btn_warn px-2 py-2 text-lg font-bold"
                                        >
                                            删除命令键
                                        </Button>
                                    </div>
                                </FormCell>
                                {isargsexist(command.cmd) ?// 如果Pickerdata中的命令键存在子命令键，则显示args输入框
                                    <FormCell>
                                        <CellHeader style={headerStyle}>
                                            <Label>Args</Label>
                                        </CellHeader>
                                        <CellBody style={bodyStyle}>
                                            <Input
                                                type="text"
                                                placeholder="Args"
                                                value={(command.args || []).join(', ')}
                                                onChange={e => handleCommandChange(taskIndex, commandIndex, 'args', e.target.value.split(', '))}
                                            />
                                        </CellBody>
                                    </FormCell>
                                    : null
                                }
                                <FormCell>
                                    <CellHeader style={headerStyle}>
                                        <Label>To Person List</Label>
                                    </CellHeader>
                                    <CellBody style={bodyStyle}>
                                        <Input
                                            type="text"
                                            placeholder="To Person List"
                                            value={(command.to_person_list || []).join(', ')}
                                            onChange={e => handleCommandChange(taskIndex, commandIndex, 'to_person_list', e.target.value.split(', '))}
                                        />
                                    </CellBody>
                                </FormCell>
                                <FormCell>
                                    <CellHeader style={headerStyle}>
                                        <Label>To Group List</Label>
                                    </CellHeader>
                                    <CellBody style={bodyStyle}>
                                        <Input
                                            type="text"
                                            placeholder="To Group List"
                                            value={(command.to_group_list || []).join(', ')}
                                            onChange={e => handleCommandChange(taskIndex, commandIndex, 'to_group_list', e.target.value.split(', '))}
                                        />
                                    </CellBody>
                                </FormCell>
                            </Form>
                        </div>
                    ))}
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

export default TaskCron;
