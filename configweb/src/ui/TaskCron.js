import React, {useEffect, useState} from 'react';
import useFetchData from '../hooks/useFetchData';
import useSaveConfig from '../hooks/useSaveConfig';

function TaskCron() {
    const [config, setConfig] = useFetchData('task-cron');
    const handleSave = useSaveConfig('task-cron', config);
    useEffect(() => {
        console.log('config changed');
        console.log(config);
    }, [config]);

    const [taskCronList, setTaskCronList] = useState(config.task_cron_list || []);

    const handleAddTask = () => {
        setTaskCronList([...taskCronList, {
            task: "",
            enabled: false,
            cron: {
                hour: "",
                minute: "",
                second: "",
                timezone: ""
            },
            commands: [{
                cmd: "",
                args: [],
                to_person_list: []
            }]
        }]);
    };

    const handleRemoveTask = (index) => {
        setTaskCronList(taskCronList.filter((_, i) => i !== index));
    };

    const handleAddCommand = (taskIndex) => {
        const newTaskCronList = [...taskCronList];
        newTaskCronList[taskIndex].commands.push({
            cmd: "",
            args: [],
            to_person_list: []
        });
        setTaskCronList(newTaskCronList);
    };

    const handleRemoveCommand = (taskIndex, commandIndex) => {
        const newTaskCronList = [...taskCronList];
        newTaskCronList[taskIndex].commands = newTaskCronList[taskIndex].commands.filter((_, i) => i !== commandIndex);
        setTaskCronList(newTaskCronList);
    };

    useEffect(() => {
        setConfig({...config, task_cron_list: taskCronList});
    }, [taskCronList]);

    return (
        <div className="border-4 border-dashed border-gray-200 rounded-lg mb-6">
            <div className="flex flex-col items-center justify-center h-full">
                <div className="text-center">
                    <h3 className="mb-4 text-lg leading-6 font-medium text-gray-900">
                        all_task_cron_enabled
                    </h3>
                    <p className="mb-4 text-sm leading-5 text-gray-500">
                        是否开启所有定时任务（True/False）
                    </p>
                    <input type="text"
                           className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
                           placeholder="False"
                           value={config.all_task_cron_enabled || ''}
                           onChange={e => setConfig({...config, all_task_cron_enabled: e.target.value})}/>
                    <h3 className="mb-4 text-lg leading-6 font-medium text-gray-900">
                        task_cron_list
                    </h3>
                    {taskCronList.map((task, taskIndex) => (
                        <div key={taskIndex}>
                            {/* Render task fields here */}
                            {/* Render commands here */}
                            <button onClick={() => handleRemoveTask(taskIndex)}>Remove Task</button>
                            <button onClick={() => handleAddCommand(taskIndex)}>Add Command</button>
                        </div>
                    ))}
                    <button onClick={handleAddTask}>Add Task</button>
                    <button
                        onClick={handleSave}
                        className="mt-4 px-4 py-2 bg-gray-800 text-white text-sm font-medium rounded-md">
                        保存
                    </button>
                </div>
            </div>
        </div>
    );
}

export default TaskCron;



// // TaskCron.js
// import React from 'react';
// import useFetchData from '../hooks/useFetchData';
// import useSaveConfig from '../hooks/useSaveConfig';
//
// function TaskCron() {
//     const [config, setConfig] = useFetchData('task-cron');
//     const handleSave = useSaveConfig('task-cron', config);
//
//     const ruleList = config.task_cron_list ? config.task_cron_list[0] : {};
//
//     return (
//         <div className="border-4 border-dashed border-gray-200 rounded-lg mb-6">
//             <div className="flex flex-col items-center justify-center h-full">
//                 <div className="text-center">
//                     <h3 className="mb-4 text-lg leading-6 font-medium text-gray-900">
//                         task_cron_enabled
//                     </h3>
//                     <p className="mb-4 text-sm leading-5 text-gray-500">
//                         是否开启自动推送定时任务（True/False）
//                     </p>
//                     <input type="text"
//                            className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
//                            placeholder="False"
//                            value={config.all_task_cron_enabled || ''}
//                            onChange={e => setConfig({...config, all_task_cron_enabled: e.target.value})}/>
//                     <h3 className="mb-4 text-lg leading-6 font-medium text-gray-900">
//                         weather_cron_rule_list
//                     </h3>
//                     <p className="mb-4 text-sm leading-5 text-gray-500">
//                         cron: 定时任务规则
//                     </p>
//                     <input type="text"
//                            className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
//                            placeholder=""
//                            value={ruleList.task || ''}
//                            onChange={e => setConfig({...config, task_cron_list: [{...ruleList, task: e.target.value}]})} />
//                     {/*........*/}
//                     <button
//                         onClick={handleSave}
//                         className="mt-4 px-4 py-2 bg-gray-800 text-white text-sm font-medium rounded-md">
//                         保存
//                     </button>
//                 </div>
//             </div>
//         </div>
//     );
// }
//
// export default TaskCron;
