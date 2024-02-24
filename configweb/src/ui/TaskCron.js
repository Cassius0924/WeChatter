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

    return (
        <div className="border-4 border-dashed border-gray-200 rounded-lg mb-6">
            <div className="flex flex-col items-center justify-center h-full">
                <div className="text-center">
                    <h3 className="mb-4 text-lg leading-6 font-medium text-gray-900">
                        任务计划列表
                    </h3>
                    {taskCronList.map((taskCron, taskIndex) => (
                        <div key={taskIndex}>
                            <h4 className="mb-2 text-md leading-6 font-medium text-gray-900">
                                {taskCron.task}
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
    );
}


export default TaskCron;




// import React, {useEffect, useState} from 'react';
// import useFetchData from '../hooks/useFetchData';
// import useSaveConfig from '../hooks/useSaveConfig';
//
// function TaskCron() {
//     const [config, setConfig] = useFetchData('task-cron');
//     const handleSave = useSaveConfig('task-cron', config);
//     useEffect(() => {
//         console.log('config changed');
//         console.log(config);
//         console.log(setConfig);
//     }, [config]);
//     const [taskCronList, setTaskCronList] = useState(config.task_cron_list || []);
//
//     const handleAddTask = () => {
//         setTaskCronList([...taskCronList, {
//             task: "",
//             enabled: false,
//             cron: {
//                 hour: "",
//                 minute: "",
//                 second: "",
//                 timezone: ""
//             },
//             commands: [{
//                 cmd: "",
//                 args: [],
//                 to_person_list: []
//             }]
//         }]);
//     };
//
//     const handleRemoveTask = (index) => {
//         setTaskCronList(taskCronList.filter((_, i) => i !== index));
//     };
//
//     const handleAddCommand = (taskIndex) => {
//         const newTaskCronList = [...taskCronList];
//         newTaskCronList[taskIndex].commands.push({
//             cmd: "",
//             args: [],
//             to_person_list: []
//         });
//         setTaskCronList(newTaskCronList);
//     };
//
//     const handleRemoveCommand = (taskIndex, commandIndex) => {
//         const newTaskCronList = [...taskCronList];
//         newTaskCronList[taskIndex].commands = newTaskCronList[taskIndex].commands.filter((_, i) => i !== commandIndex);
//         setTaskCronList(newTaskCronList);
//     };
//
//     const handleAddArg = (taskIndex, commandIndex) => {
//         const newTaskCronList = [...taskCronList];
//         newTaskCronList[taskIndex].commands[commandIndex].args.push("");//解释：这里的args是一个数组，所以要push一个空字符串
//         setTaskCronList(newTaskCronList);
//     };
//
//     const handleRemoveArg = (taskIndex, commandIndex, argIndex) => {
//         const newTaskCronList = [...taskCronList];
//         newTaskCronList[taskIndex].commands[commandIndex].args = newTaskCronList[taskIndex].commands[commandIndex].args.filter((_, i) => i !== argIndex);
//         setTaskCronList(newTaskCronList);
//     };
//
//     const handleAddPerson = (taskIndex, commandIndex) => {
//         const newTaskCronList = [...taskCronList];
//         newTaskCronList[taskIndex].commands[commandIndex].to_person_list.push("");
//         setTaskCronList(newTaskCronList);
//     };
//
//     const handleRemovePerson = (taskIndex, commandIndex, personIndex) => {
//         const newTaskCronList = [...taskCronList];
//         newTaskCronList[taskIndex].commands[commandIndex].to_person_list = newTaskCronList[taskIndex].commands[commandIndex].to_person_list.filter((_, i) => i !== personIndex);
//         setTaskCronList(newTaskCronList);
//     };
//
//     useEffect(() => {//解释：这里的useEffect是为了监听taskCronList的变化，一旦taskCronList变化，就会触发这个useEffect
//         setConfig({...config, task_cron_list: taskCronList});
//     }, [taskCronList]);
//
//     return (
//         <div className="border-4 border-dashed border-gray-200 rounded-lg mb-6">
//             <div className="flex flex-col items-center justify-center h-full">
//                 <div className="text-center">
//                     <h3 className="mb-4 text-lg leading-6 font-medium text-gray-900">
//                         all_task_cron_enabled
//                     </h3>
//                     <p className="mb-4 text-sm leading-5 text-gray-500">
//                         是否开启所有定时任务（True/False）
//                     </p>
//                     <input type="text"
//                            className="form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm"
//                            placeholder="False"
//                            value={config.all_task_cron_enabled || ''}
//                            onChange={e => setConfig({...config, all_task_cron_enabled: e.target.value})}/>
//                     <h3 className="mb-4 text-lg leading-6 font-medium text-gray-900">
//                         task_cron_list
//                     </h3>
//                     {taskCronList.map((task, taskIndex) => (
//                         <div key={taskIndex}>
//                             <h4>Task {taskIndex + 1}</h4>
//                             <input type="text" placeholder="Task name" value={task.task} onChange={e => {
//                                 const newTaskCronList = [...taskCronList];
//                                 newTaskCronList[taskIndex].task = e.target.value;
//                                 setTaskCronList(newTaskCronList);
//                             }}/>
//                             <input type="checkbox" checked={task.enabled} onChange={e => {
//                                 const newTaskCronList = [...taskCronList];
//                                 newTaskCronList[taskIndex].enabled = e.target.checked;
//                                 setTaskCronList(newTaskCronList);
//                             }}/>
//                             {/* Render cron fields here */}
//                             <div>
//                                 <h5>Cron Fields</h5>
//                                 <input type="text" placeholder="Hour" value={task.cron.hour} onChange={e => {
//                                     const newTaskCronList = [...taskCronList];
//                                     newTaskCronList[taskIndex].cron.hour = e.target.value;
//                                     setTaskCronList(newTaskCronList);
//                                 }}/>
//                                 <input type="text" placeholder="Minute" value={task.cron.minute} onChange={e => {
//                                     const newTaskCronList = [...taskCronList];
//                                     newTaskCronList[taskIndex].cron.minute = e.target.value;
//                                     setTaskCronList(newTaskCronList);
//                                 }}/>
//                                 <input type="text" placeholder="Second" value={task.cron.second} onChange={e => {
//                                     const newTaskCronList = [...taskCronList];
//                                     newTaskCronList[taskIndex].cron.second = e.target.value;
//                                     setTaskCronList(newTaskCronList);
//                                 }}/>
//                                 <input type="text" placeholder="Timezone" value={task.cron.timezone} onChange={e => {
//                                     const newTaskCronList = [...taskCronList];
//                                     newTaskCronList[taskIndex].cron.timezone = e.target.value;
//                                     setTaskCronList(newTaskCronList);
//                                 }}/>
//                             </div>
//                             {task.commands.map((command, commandIndex) => (
//                                 <div key={commandIndex}>
//                                     {/* Render command fields here */}
//                                     <h5>Command {commandIndex + 1}</h5>
//                                     <input type="text" placeholder="Command" value={command.cmd} onChange={e => {
//                                         const newTaskCronList = [...taskCronList];
//                                         newTaskCronList[taskIndex].commands[commandIndex].cmd = e.target.value;
//                                         setTaskCronList(newTaskCronList);
//                                     }}/>
//                                     {command.args.map((arg, argIndex) => (
//                                         <div key={argIndex}>
//                                             <input type="text" placeholder="Arg" value={arg} onChange={e => {
//                                                 const newTaskCronList = [...taskCronList];
//                                                 newTaskCronList[taskIndex].commands[commandIndex].args[argIndex] = e.target.value;
//                                                 setTaskCronList(newTaskCronList);
//                                             }}/>
//                                             <button onClick={() => handleRemoveArg(taskIndex, commandIndex, argIndex)}>Remove Arg</button>
//                                         </div>
//                                     ))}
//                                     {command.to_person_list.map((person, personIndex) => (
//                                         <div key={personIndex}>
//                                             <input type="text" placeholder="Person" value={person} onChange={e => {
//                                                 const newTaskCronList = [...taskCronList];
//                                                 newTaskCronList[taskIndex].commands[commandIndex].to_person_list[personIndex] = e.target.value;
//                                                 setTaskCronList(newTaskCronList);
//                                             }}/>
//                                             <button onClick={() => handleRemovePerson(taskIndex, commandIndex, personIndex)}>Remove Person</button>
//                                         </div>
//                                     ))}
//                                     <button onClick={() => handleAddArg(taskIndex, commandIndex)}>Add Arg</button>
//                                     <button onClick={() => handleAddPerson(taskIndex, commandIndex)}>Add Person</button>
//                                     <button onClick={() => handleRemoveCommand(taskIndex, commandIndex)}>Remove Command</button>
//                                 </div>
//                             ))}
//                             <button onClick={() => handleRemoveTask(taskIndex)}>Remove Task</button>
//                             <button onClick={() => handleAddCommand(taskIndex)}>Add Command</button>
//                         </div>
//                     ))}
//                     <button onClick={handleAddTask}>Add Task</button>
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
