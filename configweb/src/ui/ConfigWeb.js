import React from 'react';
import WeChatter from "./WeChatter";
import WxBotWebhook from "./WxBotWebhook";
import Admin from "./Admin";
import Bot from "./Bot";
import Chat from "./Chat";
import CopilotGPT4 from "./CopilotGPT4";
import GitHubWebhook from "./GitHubWebhook";
import MessageForwarding from "./MessageForwarding";
import TaskCron from "./TaskCron";
import CustomCommandKey from "./Custom-Command-Key";
import OfficialAccountReminder from "./OfficialAccountReminder";

function ConfigWeb() {
    return (
        <main>
            <WeChatter/>
            <WxBotWebhook/>
            <Admin/>
            <Bot/>
            <Chat/>
            <CopilotGPT4/>
            <GitHubWebhook/>
            <MessageForwarding/>
            <OfficialAccountReminder/>
            <TaskCron/>
            <CustomCommandKey/>
        </main>
    );
}

export default ConfigWeb;
