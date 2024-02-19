import React from "react";
import {BrowserRouter as Router, Link, Route, Routes} from "react-router-dom";
import WxBotWebhook from "./ui/WxBotWebhook";
import WeChatter from "./ui/WeChatter";
import Admin from "./ui/Admin";
import Bot from "./ui/Bot";
import Chat from "./ui/Chat";
import CopilotGPT4 from "./ui/CopilotGPT4";
import GitHubWebhook from "./ui/GitHubWebhook";
import MessageForwarding from "./ui/MessageForwarding";
import WeatherCron from "./ui/Weather-Cron";
import CustomCommandKey from "./ui/Custom-Command-Key";
import GasolinePriceCron from "./ui/Gasoline-Price-Cron";
import ConfigWeb from "./ui/ConfigWeb";
import axios from "axios";
import { BASE_URL, PORT } from './config';


function App() {

    return (
        <Router>
            <div className="min-h-screen bg-gray-100">
                <nav className="bg-white shadow">
                    <div className="max-w-7xl mx-auto px-2 sm:px-4 lg:px-8">
                        <div className="flex justify-between h-16">
                            <div className="flex">
                                <div className="-ml-2 mr-2 flex items-center md:hidden">
                                    <button
                                        className="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:bg-gray-100 focus:text-gray-500 transition">
                                        <svg className="h-6 w-6" stroke="currentColor" fill="none" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"
                                                  d="M4 6h16M4 12h16m-7 6h7"/>
                                        </svg>
                                    </button>
                                </div>
                                <div className="flex-shrink-0 flex items-center">
                                    <Link to="/ConfigWeb">
                                        <svg t="1707717753098" className="icon" viewBox="0 0 1024 1024" version="1.1"
                                             xmlns="http://www.w3.org/2000/svg" p-id="7550" width="32" height="32">
                                            <path
                                                d="M806.826667 329.472a21.333333 21.333333 0 0 1 10.666666 18.474667v328.106666a21.333333 21.333333 0 0 1-10.666666 18.474667l-284.16 164.096a21.333333 21.333333 0 0 1-21.333334 0l-284.16-164.096a21.333333 21.333333 0 0 1-10.666666-18.474667v-328.106666a21.333333 21.333333 0 0 1 10.666666-18.474667l284.16-164.096a21.333333 21.333333 0 0 1 21.333334 0l284.16 164.096zM554.666667 109.952a85.333333 85.333333 0 0 0-85.333334 0L185.173333 274.048a85.333333 85.333333 0 0 0-42.666666 73.898667v328.106666a85.333333 85.333333 0 0 0 42.666666 73.898667L469.333333 914.048a85.333333 85.333333 0 0 0 85.333334 0l284.16-164.096a85.333333 85.333333 0 0 0 42.666666-73.898667v-328.106666a85.333333 85.333333 0 0 0-42.666666-73.898667L554.666667 109.952z"
                                                fill="#333333" p-id="7551"></path>
                                            <path
                                                d="M512 618.666667a106.666667 106.666667 0 1 1 0-213.333334 106.666667 106.666667 0 0 1 0 213.333334z m0 64a170.666667 170.666667 0 1 0 0-341.333334 170.666667 170.666667 0 0 0 0 341.333334z"
                                                fill="#333333" p-id="7552"></path>
                                        </svg>
                                    </Link>
                                </div>
                                <div className="hidden md:ml-6 md:flex md:space-x-8">
                                    <Link to="WeChatter"
                                          className="border-b-2 border-indigo-500 text-gray-900 inline-flex items-center px-1 pt-1 text-sm font-medium leading-5 focus:outline-none focus:border-indigo-700 transition">
                                        WeChatter
                                    </Link>
                                    <Link to="Wx-Bot-Webhook"
                                          className="text-gray-500 hover:text-gray-700 inline-flex items-center px-1 pt-1 text-sm font-medium leading-5 focus:outline-none focus:text-gray-700 focus:border-gray-300 transition">
                                        Wx-Bot-Webhook
                                    </Link>
                                    <Link to="Admin"
                                          className="text-gray-500 hover:text-gray-700 inline-flex items-center px-1 pt-1 text-sm font-medium leading-5 focus:outline-none focus:text-gray-700 focus:border-gray-300 transition">
                                        Admin
                                    </Link>
                                    <Link to="Bot"
                                          className="text-gray-500 hover:text-gray-700 inline-flex items-center px-1 pt-1 text-sm font-medium leading-5 focus:outline-none focus:text-gray-700 focus:border-gray-300 transition">
                                        Bot
                                    </Link>
                                    <Link to="Chat"
                                          className="text-gray-500 hover:text-gray-700 inline-flex items-center px-1 pt-1 text-sm font-medium leading-5 focus:outline-none focus:text-gray-700 focus:border-gray-300 transition">
                                        Chat
                                    </Link>
                                    <Link to="Copilot-GPT4"
                                          className="text-gray-500 hover:text-gray-700 inline-flex items-center px-1 pt-1 text-sm font-medium leading-5 focus:outline-none focus:text-gray-700 focus:border-gray-300 transition">
                                        Copilot-GPT4
                                    </Link>
                                    <Link to="GitHub-Webhook"
                                          className="text-gray-500 hover:text-gray-700 inline-flex items-center px-1 pt-1 text-sm font-medium leading-5 focus:outline-none focus:text-gray-700 focus:border-gray-300 transition">
                                        GitHub-Webhook
                                    </Link>
                                    <Link to="Message-Forwarding"
                                          className="text-gray-500 hover:text-gray-700 inline-flex items-center px-1 pt-1 text-sm font-medium leading-5 focus:outline-none focus:text-gray-700 focus:border-gray-300 transition">
                                        Message-Forwarding
                                    </Link>
                                    <Link to="Weather-Cron"
                                          className="text-gray-500 hover:text-gray-700 inline-flex items-center px-1 pt-1 text-sm font-medium leading-5 focus:outline-none focus:text-gray-700 focus:border-gray-300 transition">
                                        Weather-Cron
                                    </Link>
                                    <Link to="Custom-Command-Key"
                                          className="text-gray-500 hover:text-gray-700 inline-flex items-center px-1 pt-1 text-sm font-medium leading-5 focus:outline-none focus:text-gray-700 focus:border-gray-300 transition">
                                        Custom-Command-Key
                                    </Link>
                                    <Link to="Gasoline-Price-Cron"
                                          className="text-gray-500 hover:text-gray-700 inline-flex items-center px-1 pt-1 text-sm font-medium leading-5 focus:outline-none focus:text-gray-700 focus:border-gray-300 transition">
                                        Gasoline-Price-Cron
                                    </Link>
                                </div>
                            </div>
                            <div className="flex items-center">
                                <div className="flex-shrink-0">
                                    <button
                                        className="relative inline-flex items-center px-4 py-2 border border-transparent text-sm leading-5 font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-500 focus:outline-none focus:shadow-outline-indigo focus:border-indigo-700 active:bg-indigo-700 transition">
                                        <span>Search</span>
                                    </button>
                                </div>
                                {/*启动main.py*/}
                                <div className="hidden md:ml-4 md:flex-shrink-0 md:flex md:items-center">
                                    <button
                                        className="p-1 border-2 border-transparent text-gray-400 rounded-full hover:text-gray-500 focus:outline-none focus:text-gray-500 focus:bg-gray-100 transition"
                                        onClick={async () => {
                                            try {
                                                await axios.post(`http://${BASE_URL}:${PORT}/run-main`).then(response => {log(response.data.message)});
                                                alert(log(response.data.message));
                                            } catch (error) {
                                                console.error(error);
                                                alert('Failed to run main.py');
                                            }
                                        }}
                                    >
                                        <span className="sr-only">View notifications</span>
                                        <svg t="1707823319943" className="icon" viewBox="0 0 1024 1024" version="1.1"
                                             xmlns="http://www.w3.org/2000/svg" p-id="2482" width="32" height="32">
                                            <path
                                                d="M0 512C0 229.218462 229.179077 0 512 0c282.781538 0 512 229.179077 512 512 0 282.781538-229.179077 512-512 512-282.781538 0-512-229.179077-512-512z m707.032615-34.264615c-36.903385-27.569231-87.906462-60.258462-142.020923-91.057231-54.626462-31.113846-108.307692-57.895385-150.055384-74.830769-20.125538-8.152615-36.864-13.784615-48.955077-16.46277-16.147692 54.075077-14.729846 373.76 0.472615 433.23077a382.582154 382.582154 0 0 0 46.08-16.187077c41.905231-17.171692 95.940923-44.110769 150.685539-74.870154 54.862769-30.877538 106.259692-63.330462 143.36-90.663385 18.156308-13.390769 32.374154-25.127385 41.708307-34.461538a381.243077 381.243077 0 0 0-41.275077-34.658462z"
                                                fill="#1afa29" p-id="2483"></path>
                                        </svg>
                                    </button>
                                </div>

                                {/*//停止main.py*/}
                                <div className="hidden md:ml-4 md:flex-shrink-0 md:flex md:items-center">
                                    <button
                                        className="p-1 border-2 border-transparent text-gray-400 rounded-full hover:text-gray-500 focus:outline-none focus:text-gray-500 focus:bg-gray-100 transition"
                                        onClick={async () => {
                                            try {
                                                await axios.post(`http://${BASE_URL}:${PORT}/stop-main`);
                                                alert('stop main.py successfully');
                                            } catch (error) {
                                                console.error(error);
                                                alert('Failed to stop main.py');
                                            }
                                        }}
                                    >
                                        <span className="sr-only">View notifications</span>
                                        <svg t="1707823376802" className="icon" viewBox="0 0 1024 1024" version="1.1"
                                             xmlns="http://www.w3.org/2000/svg" p-id="6126" width="32" height="32">
                                            <path
                                                d="M501.940706 0c277.082353 0 502.000941 224.858353 502.000941 501.940706s-224.918588 502.000941-502.000941 502.000941A502.121412 502.121412 0 0 1 0 501.940706C0 224.858353 224.858353 0 501.940706 0zM298.224941 451.764706a47.224471 47.224471 0 0 0-47.22447 47.22447v5.963295c0 26.081882 21.082353 47.224471 47.22447 47.22447h407.491765a47.224471 47.224471 0 0 0 47.22447-47.22447v-5.963295a47.224471 47.224471 0 0 0-47.22447-47.22447H298.224941z"
                                                fill="#E6394E" p-id="6127"></path>
                                        </svg>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </nav>

                <header className="bg-white shadow">
                    <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
                        <h1 className="text-3xl font-bold leading-tight text-gray-900">
                            WeChat Robot 配置
                        </h1>
                    </div>

                </header>
                <Routes>
                    <Route path="*" element={window.location.pathname.startsWith('/api') ? null : <ConfigWeb/>}/>
                    <Route path="/ConfigWeb" element={<ConfigWeb/>}/>
                    <Route path="/wechatter" element={<WeChatter/>}/>
                    <Route path="/wx-bot-webhook" element={<WxBotWebhook/>}/>
                    <Route path="/admin" element={<Admin/>}/>
                    <Route path="/bot" element={<Bot/>}/>
                    <Route path="/chat" element={<Chat/>}/>
                    <Route path="/copilot-gpt4" element={<CopilotGPT4/>}/>
                    <Route path="/github-webhook" element={<GitHubWebhook/>}/>
                    <Route path="/message-forwarding" element={<MessageForwarding/>}/>
                    <Route path="/weather-cron" element={<WeatherCron/>}/>
                    <Route path="/custom-command-key" element={<CustomCommandKey/>}/>
                    <Route path="/gasoline-price-cron" element={<GasolinePriceCron/>}/>
                </Routes>
                <main>

                </main>
            </div>
        </Router>
    );

}

export default App;
