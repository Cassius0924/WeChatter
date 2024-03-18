export const TaskCron_cronData = [
    {
        label: 'Year',
        value: 'year',
        children: [{label: 'Every', value: '*' }, ...Array.from({length: 100}, (_, i) => 2024 + i).map(year => ({ label: String(year), value: String(year) }))],
    },
    {
        label: 'Month',
        value: 'month',
        children: [{label: 'Every', value: '*' }, ...Array.from({length: 12}, (_, i) => i + 1).map(month => ({ label: String(month), value: String(month) }))],
    },
    {
        label: 'Day',
        value: 'day',
        children: [{label: 'Every', value: '*' }, ...Array.from({length: 31}, (_, i) => i + 1).map(day => ({ label: String(day), value: String(day) }))],
    },
    {
        label: 'Hour',
        value: 'hour',
        children: [{label: 'Every', value: '*' }, ...Array.from({length: 24}, (_, i) => i).map(hour => ({ label: String(hour), value: String(hour) }))],
    },
    {
        label: 'Minute',
        value: 'minute',
        children: [{label: 'Every', value: '*' }, ...Array.from({length: 60}, (_, i) => i).map(minute => ({ label: String(minute), value: String(minute) }))],
    },
    {
        label: 'Second',
        value: 'second',
        children: [{label: 'Every', value: '*' }, ...Array.from({length: 60}, (_, i) => i).map(second => ({ label: String(second), value: String(second) }))],
    },
    {
        label: 'Timezone',
        value: 'timezone',
        children: [
            { label: 'Every', value: '*' },
            { label: 'China Standard Time (CST)', value: 'Asia/Shanghai' },
            // 添加其他时区
        ],
    },
];
