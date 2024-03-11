import { useCallback, useState } from 'react';
import axios from 'axios';
import { BACKEND_IP, BACKEND_PORT } from '../config';

function useSaveConfig(configName, config) {
    const [dialog, setDialog] = useState({ show: false, type: 'success', title: '', message: '' });

    const hideDialog = () => {
        setDialog({ show: false, type: 'success', title: '', message: '' });
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

    const saveConfig = useCallback(() => {
        axios.post(`http://${BACKEND_IP}:${BACKEND_PORT}/${configName}`, config)
            .then(res => {
                console.log(res.data);
                setDialog({ show: true, type: 'success', title: '保存成功', message: '配置已经保存成功' });
            })
            .catch(err => {
                console.error(err);
                setDialog({ show: true, type: 'error', title: '保存失败', message: '保存失败' });
            });
    }, [configName, config]);

    return [saveConfig, dialog, hideDialog];
}

export default useSaveConfig;

// import {useCallback} from 'react';
// import axios from 'axios';
// import { BACKEND_IP, BACKEND_PORT } from '../config';
//
//
// function useSaveConfig(configName, config) {
//     return useCallback(() => {
//         axios.post(`http://${BACKEND_IP}:${BACKEND_PORT}/${configName}`, config)//具体的post请求：
//             .then(res => {
//                 console.log(res.data);
//                 // 可以在这里添加一些处理，例如显示一个通知告诉用户配置已经保存成功
//                 //TODO:搞个优美的通知
//                 alert('配置已经保存成功')
//             })
//             .catch(err => {
//                 console.error(err);
//                 // 可以在这里添加一些错误处理，例如显示一个通知告诉用户保存失败
//                 alert('保存失败')
//             });
//     }, [configName, config]);
// }
//
// export default useSaveConfig;
