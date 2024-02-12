import {useCallback} from 'react';
import axios from 'axios';

function useSaveConfig(configName, config) {
    return useCallback(() => {
        // axios.post(`http://127.0.0.1:8000/${configName}`, config)
        // axios.post(`http://47.92.99.199:30/api/${configName}`, config)
        axios.post(`http://47.92.99.199:8000/${configName}`, config)
            .then(res => {
                console.log(res.data);
                // 可以在这里添加一些处理，例如显示一个通知告诉用户配置已经保存成功
                //TODO:搞个优美的通知
                alert('配置已经保存成功')
            })
            .catch(err => {
                console.error(err);
                // 可以在这里添加一些错误处理，例如显示一个通知告诉用户保存失败
                alert('保存失败')
            });
    }, [configName, config]);
}

export default useSaveConfig;
