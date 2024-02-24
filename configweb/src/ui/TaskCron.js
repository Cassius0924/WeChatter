// TaskCron.js
import React, {useEffect} from 'react';
import useFetchData from '../hooks/useFetchData';
import useSaveConfig from '../hooks/useSaveConfig';

function TaskCron() {
    const [config, setConfig] = useFetchData('task-cron');
    const handleSave = useSaveConfig('task-cron', config);
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
                hour: '*',
                minute: '*',
                second: '*/8',
                timezone: 'Asia/Shanghai',
            },
            commands: [],
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


    return (
        <div className="border-4 border-dashed border-gray-200 rounded-lg mb-6">
            <div className="flex flex-col items-center justify-center h-full">
                <div className="text-center">
                    <h3 className="mb-4 text-lg leading-6 font-medium text-gray-900">
                        任务计划列表
                    </h3>
                    <div className="flex justify-center flex-wrap">
                        {taskCronList.map((taskCron, taskIndex) => (
                            <div key={taskIndex} className="m-4">
                                <button
                                    onClick={handleAddCron}
                                    className="mt-4 px-4 py-2 bg-green-500 text-white text-sm font-medium rounded-md">
                                    添加任务
                                </button>
                                <button
                                    onClick={() => handleDeleteCron(taskIndex)}
                                    className="mt-4 px-4 py-2 bg-red-500 text-white text-sm font-medium rounded-md">
                                    删除任务
                                </button>
                                <h4 className="mb-2 text-md leading-6 font-medium text-gray-900">
                                    Task {taskIndex + 1}
                                </h4>
                                <input
                                    type="text"
                                    className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                                    placeholder="Task"
                                    value={taskCron.task}
                                    onChange={e => handleChange(taskIndex, 'task', e.target.value)}
                                />
                                <input
                                    type="checkbox"
                                    className="form-checkbox mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                                    checked={taskCron.enabled}
                                    onChange={e => handleChange(taskIndex, 'enabled', e.target.checked)}
                                />
                                <div>
                                    <h5 className="mb-2 text-sm leading-6 font-medium text-gray-900">
                                        Cron Fields
                                    </h5>
                                    <input
                                        type="text"
                                        className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                                        placeholder="Hour"
                                        value={taskCron.cron.hour}
                                        onChange={e => handleChange(taskIndex, 'cron', {
                                            ...taskCron.cron,
                                            hour: e.target.value
                                        })}
                                    />
                                    <input
                                        type="text"
                                        className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                                        placeholder="Minute"
                                        value={taskCron.cron.minute}
                                        onChange={e => handleChange(taskIndex, 'cron', {
                                            ...taskCron.cron,
                                            minute: e.target.value
                                        })}
                                    />
                                    <input
                                        type="text"
                                        className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                                        placeholder="Second"
                                        value={taskCron.cron.second}
                                        onChange={e => handleChange(taskIndex, 'cron', {
                                            ...taskCron.cron,
                                            second: e.target.value
                                        })}
                                    />
                                    <input
                                        type="text"
                                        className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                                        placeholder="Timezone"
                                        value={taskCron.cron.timezone}
                                        onChange={e => handleChange(taskIndex, 'cron', {
                                            ...taskCron.cron,
                                            timezone: e.target.value
                                        })}
                                    />
                                </div>

                                {taskCron.commands.map((command, commandIndex) => (
                                    <div key={commandIndex}>
                                        <h5 className="mb-2 text-sm leading-6 font-medium text-gray-900">
                                            Command {commandIndex + 1}
                                        </h5>
                                        {/*cmd*/}
                                        <input
                                            type="text"
                                            className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                                            placeholder="Command"
                                            value={command.cmd}
                                            onChange={e => handleCommandChange(taskIndex, commandIndex, 'cmd', e.target.value)}
                                        />
                                        {/*args*/}
                                        <input
                                            type="text"
                                            className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                                            placeholder="Args"
                                            value={(command.args || []).join(', ')}
                                            onChange={e => handleCommandChange(taskIndex, commandIndex, 'args', e.target.value.split(', '))}
                                        />
                                        {/*to_person_list*/}
                                        <input
                                            type="text"
                                            className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                                            placeholder="To Person List"
                                            value={(command.to_person_list || []).join(', ')}
                                            onChange={e => handleCommandChange(taskIndex, commandIndex, 'to_person_list', e.target.value.split(', '))}
                                        />
                                        {/*to_group_list*/}
                                        <input
                                            type="text"
                                            className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                                            placeholder="To Group List"
                                            value={(command.to_group_list || []).join(', ')}
                                            onChange={e => handleCommandChange(taskIndex, commandIndex, 'to_group_list', e.target.value.split(', '))}
                                        />
                                        <button
                                            onClick={() => handleAddCommand(taskIndex)}
                                            className="mt-4 px-4 py-2 bg-blue-500 text-white text-sm font-medium rounded-md">
                                            添加命令
                                        </button>
                                        <button
                                            onClick={() => handleDeleteCommand(taskIndex, commandIndex)}
                                            className="mt-4 px-4 py-2 bg-red-500 text-white text-sm font-medium rounded-md">
                                            删除命令
                                        </button>
                                    </div>
                                ))}
                            </div>
                        ))}
                        <button
                            onClick={handleSave}
                            className="mt-4 px-4 py-2 bg-gray-800 text-white text-sm font-medium rounded-md">
                            保存
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}


export default TaskCron;
