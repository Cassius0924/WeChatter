import React, {useState} from "react";
import {BrowserRouter as Router, Link, Route, Routes} from "react-router-dom";
import {Button, Cell, CellBody, Cells, Dialog} from 'react-weui';
import WxBotWebhook from "./ui/WxBotWebhook";
import WeChatter from "./ui/WeChatter";
import Admin from "./ui/Admin";
import Bot from "./ui/Bot";
import Chat from "./ui/Chat";
import CopilotGPT4 from "./ui/CopilotGPT4";
import GitHubWebhook from "./ui/GitHubWebhook";
import MessageForwarding from "./ui/MessageForwarding";
import OfficialAccountReminder from "./ui/OfficialAccountReminder";
import TaskCron from "./ui/TaskCron";
import CustomCommandKey from "./ui/Custom-Command-Key";
import ConfigWeb from "./ui/ConfigWeb";
import {BACKEND_IP, BACKEND_PORT} from './config';
import 'weui';
import './App.css';
import axios from "axios";
import SuccessFooter from "./ui/SuccessFooter";
import weui from 'weui.js';


//微信强迫症崩溃小点点
// export const ComponentCountContext = React.createContext();
// function getComponentCount(componentName) {
//     // 创建一个对象，每个键是一个组件名称，每个值是该组件的Form和CustomFormCell的数量
//     const componentCounts = {
//         'WeChatter': 1,
//         'WxBotWebhook': 3,
//         'Admin': 2,
//         'Bot': 1,
//         'Chat': 2,
//         'CopilotGPT4': 2,
//         'GitHubWebhook': 4,
//         'MessageForwarding': 5,
//         'OfficialAccountReminder': 4,
//         'TaskCron': 1,
//         'CustomCommandKey': 3
//         // ... other components ...
//     };
//     // 返回对应的数量，如果没有找到对应的组件，返回0
//     return componentCounts[componentName] || 0;
// }
// function App() {
//
//     // 创建一个状态来存储每个组件的Form和CustomFormCell的数量
//     const [componentCounts, setComponentCounts] = useState({});
//
//     // 在组件挂载后，计算所有组件的Form和CustomFormCell的数量
//     useEffect(() => {
//         const componentNames = ['WeChatter', 'WxBotWebhook', 'Admin', 'Bot', 'Chat', 'CopilotGPT4', 'GitHubWebhook', 'MessageForwarding', 'OfficialAccountReminder', 'TaskCron', 'CustomCommandKey'];
//         componentNames.forEach(componentName => {
//             // 假设你有一个函数可以获取每个组件的数量
//             const count = getComponentCount(componentName);
//             setComponentCounts(prevCounts => ({
//                 ...prevCounts,
//                 [componentName]: count,
//             }));
//         });
//     }, []);
function App() {


    const [dialog, setDialog] = useState({title: '', message: '', show: false});

    const showDialog = (title, message) => {
        setDialog({title, message, show: true});
    };

    const hideDialog = () => {
        setDialog(prevState => ({...prevState, show: false}));
    };

    const handleStart = () => {
        axios.get(`http://${BACKEND_IP}:${BACKEND_PORT}/run-main`)
            .then(res => {
                if (res.data.message === 'wechatter is running') {
                    showDialog('提示', '❇️WeChatter已经在运行啦，请勿重复点击❇️');
                } else {
                    axios.post(`http://${BACKEND_IP}:${BACKEND_PORT}/run-main`)
                        .then(res => {
                            showDialog('提示', '✅WeChatter运行成功✅');
                        })
                        .catch(error => {
                            showDialog('错误', 'Failed to run wechatter');
                        });
                }
            })
            .catch(error => {
                showDialog('错误', 'Failed to check wechatter status');
            });
    };

    const handleStop = () => {
        axios.get(`http://${BACKEND_IP}:${BACKEND_PORT}/run-main`)
            .then(res => {
                if (res.data.message === 'wechatter is running') {
                    axios.post(`http://${BACKEND_IP}:${BACKEND_PORT}/stop-main`)
                        .then(res => {
                            showDialog('提示', '❗成功停止WeChatter❗');
                        })
                        .catch(error => {
                            showDialog('错误', 'Failed to stop wechatter');
                        });
                } else {
                    showDialog('提示', '❇️WeChatter没有运行，请勿重复点击❇️');
                }
            })
            .catch(error => {
                showDialog('错误', 'Failed to check wechatter status');
            });
    };
    return (
        <Router>
            <div className="min-h-screen bg-gray-100">
                <nav className="bg-white shadow navbar">  {/* Add the CSS class here */}
                    <div className="max-w-7xl mx-auto px-2 sm:px-4 lg:px-8">
                        <header className="text-center py-2">
                            <Link to="/ConfigWeb" className="text-2xl font-bold text-blue-500 hover:text-blue-700">
                                ConfigWeb
                            </Link>
                        </header>
                        <Cells>
                            <Cell access>
                                <CellBody>
                                    <Link to="/WeChatter">WeChatter</Link>
                                </CellBody>
                            </Cell>
                            <Cell access>
                                <CellBody>
                                    <Link to="/Wx-Bot-Webhook">WxBotWebhook</Link>
                                </CellBody>
                            </Cell>
                            <Cell access>
                                <CellBody>
                                    <Link to="/Admin">Admin</Link>
                                </CellBody>
                            </Cell>
                            <Cell access>
                                <CellBody>
                                    <Link to="/Bot">Bot</Link>
                                </CellBody>
                            </Cell>
                            <Cell access>
                                <CellBody>
                                    <Link to="/Chat">Chat</Link>
                                </CellBody>
                            </Cell>
                            <Cell access>
                                <CellBody>
                                    <Link to="/Copilot-GPT4">CopilotGPT4</Link>
                                </CellBody>
                            </Cell>
                            <Cell access>
                                <CellBody>
                                    <Link to="/GitHub-Webhook">GitHubWebhook</Link>
                                </CellBody>
                            </Cell>
                            <Cell access>
                                <CellBody>
                                    <Link to="/Message-Forwarding">MessageForwarding</Link>
                                </CellBody>
                            </Cell>
                            <Cell access>
                                <CellBody>
                                    <Link to="/Official-Account-Reminder">OfficialAccountReminder</Link>
                                </CellBody>
                            </Cell>
                            <Cell access>
                                <CellBody>
                                    <Link to="/Task-Cron">TaskCron</Link>
                                </CellBody>
                            </Cell>
                            <Cell access>
                                <CellBody>
                                    <Link to="/Custom-Command-Key">CustomCommandKey</Link>
                                </CellBody>
                            </Cell>
                        </Cells>
                    </div>
                </nav>

                {/* Add the CSS class to your content area */}
                <div className="App">
                    <div className="content">
                        <header className="bg-white shadow">
                            <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
                                <div className="flex justify-between items-center">
                                    <h1 className="text-3xl font-bold leading-tight text-gray-900">
                                        WeChatter 配置
                                    </h1>

                                    <div className="flex">
                                        <div className="mr-4">
                                            <Button onClick={handleStart}
                                                    className="weui-btn weui-btn_primary px-5 py-2 text-lg font-bold">
                                                启动
                                            </Button>
                                        </div>
                                        <div>
                                            <Button onClick={handleStop}
                                                    className="weui-btn weui-btn_warn px-5 py-2 text-lg font-bold">
                                                停止
                                            </Button>
                                        </div>
                                        <Dialog type="ios" title={dialog.title} buttons={[{
                                            type: 'default',
                                            label: '确定',
                                            onClick: hideDialog
                                        }]} show={dialog.show}>
                                            {dialog.message}
                                        </Dialog>
                                    </div>

                                </div>
                            </div>
                        </header>


                        <Routes>
                            <Route path="*"
                                   element={window.location.pathname.startsWith('/api') ? null : <ConfigWeb/>}/>
                            <Route path="/ConfigWeb" element={<ConfigWeb/>}/>
                            <Route path="/wechatter" element={<WeChatter/>}/>
                            <Route path="/wx-bot-webhook" element={<WxBotWebhook/>}/>
                            <Route path="/admin" element={<Admin/>}/>
                            <Route path="/bot" element={<Bot/>}/>
                            <Route path="/chat" element={<Chat/>}/>
                            <Route path="/copilot-gpt4" element={<CopilotGPT4/>}/>
                            <Route path="/github-webhook" element={<GitHubWebhook/>}/>
                            <Route path="/message-forwarding" element={<MessageForwarding/>}/>
                            <Route path="/official-account-reminder" element={<OfficialAccountReminder/>}/>
                            <Route path="/task-cron" element={<TaskCron/>}/>
                            <Route path="/custom-command-key" element={<CustomCommandKey/>}/>
                        </Routes>

                        <main>

                        </main>

                    </div>
                    <SuccessFooter
                        className="footer"
                        links={[
                            {href: "https://github.com/Cassius0924/WeChatter", text: "WeChatter"},
                            {href: "https://github.com/Cassius0924", text: "Cassius0924"},
                            {href: "https://github.com/Ashesttt", text: "Ashesttt"},
                            {href: "http://47.92.99.199/", text: "blog"},
                        ]}
                        copyright="Copyright © 2024 WeChatter"
                    />
                </div>
            </div>
        </Router>
    );
}


export default App;
