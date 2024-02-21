# ⚙️ 定时任务配置详细

本篇文档仅包含配置文件中定时任务配置的详细说明，更多配置请查看项目[自述文件](../README.md#配置文件)。

## 定时任务配置详细

> [!TIP]
> 带有`*`的字段为必填字段。

- `all_task_cron_enabled`*: 功能开关，是否开启定时天气推送。
- `task_cron_list`: 推送规则列表，每个规则包含两个字段：`cron` 和 `tasks`。
  - `task`*: 任务名称，可任意填写。
  - `enabled`*: 功能开关，是否开启该定时任务。
  - `cron`*: 定时任务的时间设置，包含以下字段：
    - `year`: 4位数年份，可以是任何值或者特定的年份。
    - `month`: 月份，可以是1-12的任何值，或者特定的月份（支持英文月份缩写 jan - dec）。
    - `day`: 月份中的日期，可以是1-31的任何值，或者特定的日期。
    - `week`: ISO周数，可以是1-53的任何值，或者特定的周数。
    - `day_of_week`: 一周中的某一天，可以是0-6（周一到周日）的任何值，或者特定的一天（支持工作日缩写 mon - sun）。
    - `hour`*: 小时，可以是0-23的任何值，或者特定的小时。
    - `minute`*: 分钟，可以是0-59的任何值，或者特定的分钟。
    - `second`*: 秒，可以是0-59的任何值，或者特定的秒。
    - `start_date`: 定时任务的开始日期。
    - `end_date`: 定时任务的结束日期。
    - `timezone`: 用于日期/时间计算的时区（默认为中国时区）。
  - `commands`*: 推送命令列表，每个命令包含三个字段：`cmd`, `args` 和 `to_person_list` 和 `to_group_list`。
    - `cmd`*: 命令名称，可选值详见[自定义命令关键词配置详细](custom_command_key_config_detail.md)。
    - `args`: 命令参数列表。
    - `to_person_list`: 推送目标用户列表，即消息接收用户。
    - `to_group_list`: 推送目标群列表，即消息接收群。

> [!TIP]
> 更多关于 `cron` 定时器请参阅[APScheduler文档](https://apscheduler.readthedocs.io/en/3.x/modules/triggers/cron.html)。

> [!IMPORTANT]
> 为了保护帐号的安全，WeChatter 不允许低于每5秒级的定时任务，最小时间间隔为5秒。

## 定时任务配置示例

<details>
<summary>
<b>[示例一]</b> 每天早上7点推送北京天气给张三、文件传输助手和家人群，推送知乎热搜给李四
</summary>

```yaml
task_cron_list:
  - task: "每天早上7点推送北京天气给张三、文件传输助手和家人群，推送知乎热搜给李四"
    enabled: True
    cron:
      hour: "7"
      minute: "0"
      second: "0"
    commands:
      - cmd: "weather"
        args: [ "北京" ]
        to_person_list: [ "张三", "文件传输助手", "家人群" ]
      - cmd: "zhihu-hot"
        to_person_list: [ "李四" ]
```

</details>

<details>
<summary>
<b>[示例二]</b> 每周一到周五早上8点30分推送深圳汽油价格给张三和李四，每周六到周日下午6点推送人民日报给张三
</summary>

```yaml
task_cron_list:
  - task: "每周一到周五早上8点30分推送汽油价格给张三和李四"
    enabled: True
    cron:
      day_of_week: "1-5"
      hour: "8"
      minute: "30"
      second: "0"
    commands:
      - cmd: "gasoline-price"
        args: [ "深圳" ]
        to_person_list: [ "张三", "李四" ]
  - task: "每周六到周日下午6点推送广州天气给张三"
    enabled: True
    cron:
      day_of_week: "6,0"
      hour: "18"
      minute: "0"
      second: "0"
    commands:
      - cmd: "people-daily"
        to_person_list: [ "张三" ]
```

</details>

<details>
<summary>
<b>[示例三]</b> 一月的每一天的每整点推送一次深圳天气给张三
</summary>

```yaml
task_cron_list:
  - task: "一月的每一天每整点推送一次深圳天气给张三"
    enabled: True
    cron:
      month: "1"
      minute: "0"
      second: "0"
    commands:
      - cmd: "weather"
        args: [ "深圳" ]
        to_person_list: [ "张三" ]
        to_group_list: [ ]
```

</details>

