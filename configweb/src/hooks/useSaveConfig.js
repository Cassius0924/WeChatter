import {useCallback} from 'react';
import axios from 'axios';
import { BASE_URL, PORT } from '../../config';


function useSaveConfig(configName, config) {
    return useCallback(() => {
        axios.post(`http://${BASE_URL}:${PORT}/${configName}`, config)
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
