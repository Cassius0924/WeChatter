import React from "react";
import {BrowserRouter as Router, Link, Routes, Route} from "react-router-dom";
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
                                <div className="ml-3 relative">
                                    <div>
                                        <svg t="1707717876986" className="icon" viewBox="0 0 1024 1024" version="1.1"
                                             xmlns="http://www.w3.org/2000/svg" p-id="8632" width="32" height="32">
                                            <path
                                                d="M512 0C229.376 0 0 229.376 0 512s229.376 512 512 512 512-229.376 512-512S794.624 0 512 0z m62.464 774.144c0 27.648-22.528 50.176-50.176 50.176h-25.088c-27.648 0-50.176-22.528-50.176-50.176V474.624c0-27.648 22.528-50.176 50.176-50.176h25.088c27.648 0 50.176 22.528 50.176 50.176v299.52zM512 349.696c-34.304 0-62.464-28.16-62.464-62.464 0-34.304 28.16-62.464 62.464-62.464s62.464 28.16 62.464 62.464c0 34.304-28.16 62.464-62.464 62.464z"
                                                fill="#040000" p-id="8633"></path>
                                        </svg>
                                    </div>
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
                    <Route path="*" element={window.location.pathname.startsWith('/api') ? null : <ConfigWeb />} />
                    <Route path="/ConfigWeb" element={<ConfigWeb />} />
                    <Route path="/wechatter" element={<WeChatter />} />
                    <Route path="/wx-bot-webhook" element={<WxBotWebhook />} />
                    <Route path="/admin" element={<Admin />} />
                    <Route path="/bot" element={<Bot />} />
                    <Route path="/chat" element={<Chat />} />
                    <Route path="/copilot-gpt4" element={<CopilotGPT4 />} />
                    <Route path="/github-webhook" element={<GitHubWebhook />} />
                    <Route path="/message-forwarding" element={<MessageForwarding />} />
                    <Route path="/weather-cron" element={<WeatherCron />} />
                    <Route path="/custom-command-key" element={<CustomCommandKey />} />
                    <Route path="/gasoline-price-cron" element={<GasolinePriceCron />} />
                </Routes>
                <main>

                </main>
            </div>
        </Router>
    );

}

export default App;
