import React from 'react';
import WeChatter from "./WeChatter";
import WxBotWebhook from "./WxBotWebhook";
import Admin from "./Admin";
import Bot from "./Bot";
import Chat from "./Chat";
import CopilotGPT4 from "./CopilotGPT4";
import GitHubWebhook from "./GitHubWebhook";
import MessageForwarding from "./MessageForwarding";
import WeatherCron from "./Weather-Cron";
import CustomCommandKey from "./Custom-Command-Key";
import GasolinePriceCron from "./Gasoline-Price-Cron";

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
            <WeatherCron/>
            <CustomCommandKey/>
            <GasolinePriceCron/>
        </main>
    );
}

export default ConfigWeb;
