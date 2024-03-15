import React from 'react';
import 'weui';
import weui from 'weui.js';


function Picker({options="picker", Pickerdata, Pickerconfig}) {
    // options: "picker" or "datepicker" 默认为"picker"
    // Pickerdata: picker的数据
    // Pickerconfig: picker的配置

    //Pickerconfig详情：https://github.com/Tencent/weui.js/blob/master/docs/component/picker.md#pickeritems-options

    const handleClick = () => {
        if (options === "picker") {
            weui.picker(Pickerdata, Pickerconfig);
        }
        if (options === "datepicker") {
            weui.datePicker(Pickerconfig);
        }
        else {
            console.log("options is not picker or datepicker");
        }
    };
    const buttonStyle = {
        backgroundColor: '#002FA7', // 按钮的背景颜色
        color: 'white', // 按钮的文本颜色
        padding: '10px 30px', // 按钮的内边距
        textAlign: 'center', // 文本的对齐方式
        textDecoration: 'none', // 文本的装饰（在这里我们移除了任何装饰）
        display: 'inline-block', // 让按钮作为内联块显示
        fontSize: '16px', // 文本的字体大小
        margin: '4px 2px', // 按钮的外边距
        cursor: 'pointer', // 鼠标悬停时的光标样式
        borderRadius: '5px', // 按钮的边框半径（用于创建圆角）
        border: 'none', // 移除按钮的边框
    };

    return (
        <button style={buttonStyle} onClick={handleClick}>{Pickerconfig.title}</button>
    );
}

export default Picker;
