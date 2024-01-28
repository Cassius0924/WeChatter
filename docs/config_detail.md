# ⚙️ 配置说明

本篇文档仅包含配置文件中部分复杂配置的详细说明，更多配置请查看项目[自述文件](../README.md)

## Weather Cron 配置详细

- `weather_cron_enabled`: 功能开关，是否开启定时天气推送
- `weather_cron_rules`: 推送规则列表，每个规则包含两个字段：`cron` 和 `tasks`
  - `cron`: 定时任务的时间设置，包含以下字段：
    - `year`: 4位数年份，可以是任何值或者特定的年份
    - `month`: 月份，可以是1-12的任何值，或者特定的月份
    - `day`: 月份中的日期，可以是1-31的任何值，或者特定的日期
    - `week`: ISO周数，可以是1-53的任何值，或者特定的周数
    - `day_of_week`: 一周中的某一天，可以是0-6的任何值，或者特定的一天（0代表周一，6代表周日）
    - `hour`: 小时，可以是0-23的任何值，或者特定的小时
    - `minute`: 分钟，可以是0-59的任何值，或者特定的分钟
    - `second`: 秒，可以是0-59的任何值，或者特定的秒
    - `start_date`: 定时任务的开始日期
    - `end_date`: 定时任务的结束日期
    - `timezone`: 用于日期/时间计算的时区（默认为调度器时区）
  - `tasks`: 推送任务列表，每个任务包含三个字段：`city`, `to_persons` 和 `to_groups`
    - `city`: 推送天气的城市名
    - `to_persons`: 推送目标用户列表，即消息接收用户
    - `to_groups`: 推送目标群列表，即消息接收群

以下表格列出了从除`timezone`外所有字段中可以使用的表达式。一个字段中可以用逗号分隔多个表达式。

| 表达式 | 字段 | 描述 |
| --- | --- | --- |
| `*` | 任何字段 | 在每个值上触发 |
| `*/a` | 任何字段 | 从最小值开始，每隔a个值触发 |
| `a-b` | 任何字段 | 在a-b范围内的任何值上触发（a必须小于b） |
| `a-b/c` | 任何字段 | 在a-b范围内，每隔c个值触发 |
| `xth y` | `day`字段 | 在月份中第x次出现的工作日y上触发 |
| `last x` | `day`字段 | 在月份中最后一次出现的工作日x上触发 |
| `last` | `day`字段 | 在月份的最后一天触发 |
| `x,y,z` | 任何字段 | 在任何匹配的表达式上触发；可以组合上述表达式中的任何数量 |

> [!NOTE]
> `month` 和 `day_of_week` 字段接受英文月份和工作日的缩写（jan – dec 和 mon – sun）。

### 配置示例

<details>
<summary>
<b>[示例一]</b> 每天早上7点推送北京天气给张三、文件传输助手和家人群，推送广州天气给李四
</summary>

```ini
weather_cron_rules = [ {
    "cron": {
      "year": "*",
      "month": "*",
      "day": "*",
      "week": "*",
      "day_of_week": "*",
      "hour": "7",
      "minute": "0",
      "second": "0",
      "start_date": null,
      "end_date": null,
      "timezone": "Asia/Shanghai"
    },
    "tasks": [ {
      "city": "北京",
      "to_persons": ["张三", "文件传输助手"],
      "to_groups": ["家人群"]
    }, {
      "city": "广州",
      "to_persons": ["李四"],
      "to_groups": []
    } ]
  } ]
```

</details>

<details>
<summary>
<b>[示例二]</b> 每周一到周五早上8点30分推送广州天气给张三和李四，每周六到周日下午6点推送广州天气给张三
</summary>

```ini
weather_cron_rules = [ {
    "cron": {
      "year": "*",
      "month": "*",
      "day": "*",
      "week": "*",
      "day_of_week": "1-5",
      "hour": "8",
      "minute": "30",
      "second": "0",
      "start_date": null,
      "end_date": null,
      "timezone": "Asia/Shanghai"
    },
    "tasks": [ {
      "city": "广州",
      "to_persons": ["张三", "李四"],
      "to_groups": []
    } ]
  }, {
    "cron": {
      "year": "*",
      "month": "*",
      "day": "*",
      "week": "*",
      "day_of_week": "6,0",
      "hour": "18",
      "minute": "0",
      "second": "0",
      "start_date": null,
      "end_date": null,
      "timezone": "Asia/Shanghai"
    },
    "tasks": [ {
      "city": "广州",
      "to_persons": ["张三"],
      "to_groups": []
    } ]
  } ]
```

</details>

<details>
<summary>
<b>[示例三]</b> 一月的每一天每整点推送一次深圳天气给张三
</summary>

```ini
weather_cron_rules = [ {
    "cron": {
      "year": "*",
      "month": "1",
      "day": "*",
      "week": "*",
      "day_of_week": "*",
      "hour": "*",
      "minute": "0",
      "second": "0",
      "start_date": null,
      "end_date": null,
      "timezone": "Asia/Shanghai"
    },
    "tasks": [ {
      "city": "深圳",
      "to_persons": ["张三"],
      "to_groups": []
    } ]
  } ]
```

</details>

> [!TIP]
> 更多关于`cron`定时器查看[APScheduler文档](https://apscheduler.readthedocs.io/en/3.x/modules/triggers/cron.html)
